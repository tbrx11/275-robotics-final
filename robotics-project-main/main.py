import coppeliasim_zmqremoteapi_client as zmq
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
import utils.ecse275_vision_utils as util
import utils.my_functions_solution as func
import json
import time
import random


plt.close("all")

f = 0.020  # focal length in meters
pixels_per_inch = 560.0165995731867
z = 0.63  # vertical distance to the centerpoint of the blocks on the table

vision_mode = "RGB"  # or "RGB"

client = zmq.RemoteAPIClient()
sim = client.getObject('sim')
fruits = ['Cucumber Ripe', 'Pineapple', 'Watermelon', 'Banana', 'Kiwi', 'Tomato', 'Corn', 'Raspberry']
cubes = [sim.getObject('/cucumber'), sim.getObject('/pineapple'), sim.getObject('/watermelon'), sim.getObject('/banana'),
            sim.getObject('/kiwi'), sim.getObject('/tomato'), sim.getObject('/corn'),sim.getObject('/raspberry')]
    

while True:
    
    for i in range(len(fruits)):
        print(f"{i}: {fruits[i]}")

    while True:
        usr_inpt = input("Enter the index of the fruit you want to pick up: ")
        try:
            usr_inpt = int(usr_inpt)
            if usr_inpt < 0 or usr_inpt >= len(fruits):
                print("Invalid input. Please enter a valid index.")
            else: 
                break   
        except:
            print("Invalid input. Please enter a valid index.")

    cubes_x = [0] * len(cubes)
    cubes_y = [0] * len(cubes)

    # set table dimensions
    table_left = -.525
    table_right = .175
    table_bottom = .925
    table_top = 1.625
    table_height = 1.027

    # randomize cubes
    random.seed(0)
    for i in range(0, len(cubes)):
        cubes_x[i] = round(random.uniform(table_left, table_right),3)
        cubes_y[i] = round(random.uniform(table_bottom, table_top),3)
        sim.setObjectPosition(cubes[i], -1, [cubes_x[i], cubes_y[i], table_height])


    #start sim and let pioneer move to table 1
    sim.startSimulation()

    # what object should be picked up
    simBase = sim.getObject('/PioneerP3DX')
    fscript = sim.getObject("/PioneerP3DX/Franka/Script")
    pscript = sim.getObject("/robot_trackpt/Script")
    dropoff = sim.getObject('/droppoint')
    waypt = sim.getObject('/waypoint1')



    while not sim.callScriptFunction("isPathDone", pscript):
        print("moving")
    print("here")
    time.sleep(.5)



    #pickup object (1 to pickup / 2 to drop / 0 to do nothing))
    waypt_pos = sim.getObjectPose(waypt, simBase)
    while (sim.callScriptFunction("get_move_done", fscript) == 0):
        sim.callScriptFunction("franka_control", fscript, waypt_pos)
    time.sleep(.2)

    camera_handle = sim.getObject("/Vision_sensor")

    # Capture image from the vision sensor
    if vision_mode == "gray":
        image, resolution = sim.getVisionSensorImg(camera_handle, 1)
        image = np.array(bytearray(image), dtype='uint8').reshape(resolution[0], resolution[1])
    elif vision_mode == "RGB":
        image, resolution = sim.getVisionSensorImg(camera_handle, 0)
        image = np.array(bytearray(image), dtype='uint8').reshape(resolution[0], resolution[1], 3)
    else:
        print("Invalid vision mode!")

    image = np.flip(image, axis=1)

    if vision_mode == "gray":
        plt.imshow(image, cmap="binary")
    elif vision_mode == "RGB":
        plt.imshow(image)
        #plt.show()

    # Detect blobs
    masked_image = util.mask_image(image)
    keypoints = util.detect_blobs(masked_image, visualize=False)

    # Get centroids and ROI
    centroids, roi = util.blob_images(masked_image, keypoints)

    # Extract and resize fruits
    resized_fruits = util.extract_and_resize_fruits(image, centroids)

    # Load TensorFlow model
    model_path = "model.keras"  # Replace with your actual TensorFlow model file path
    model = tf.keras.models.load_model(model_path, compile=False)

    # Get model's input shape (exclude batch size)
    model_input_shape = model.input_shape[1:]  # e.g., (128, 128, 3)

    # Preprocess the fruits
    preprocessed_fruits = util.preprocess_fruit_images(resized_fruits, model_input_shape)

    # Ensure the preprocessed fruits have the correct shape for the model
    preprocessed_fruits = tf.reshape(preprocessed_fruits, (-1, *model_input_shape))

    class_indices = json.load(open("data/class_indices.json", "r"))
    centroid = None
    for i, fruit in enumerate(preprocessed_fruits):
        pred = model.predict(tf.expand_dims(fruit, axis=0))
        predicted_label = [key for key,value in class_indices.items() if value == np.argmax(pred, axis=1)[0]]
        
        plt.figure()
        plt.imshow(resized_fruits[i])  # Show the original image
        plt.title(f"Predicted Class: {predicted_label}")
        #plt.show()     
        print(predicted_label)
        
        if predicted_label == [fruits[usr_inpt]]:
            centroid = centroids[i]
    
    if centroid is None:
        centroid = centroids[0]
        usr_inpt = 0   
        
        
        
    T_cam_base = np.array(sim.getObjectMatrix(camera_handle,simBase)).reshape(3,4) 
    pos_cam = func.compute_pos_from_pix(centroid,resolution[0],f,pixels_per_inch,z)

    obj_pos = util.hand_eye_transform(pos_cam, T_cam_base)
    obj_pos = [obj_pos[0]+.015, obj_pos[1], obj_pos[2], 0, 0 , 0, 1]
    print(obj_pos)

    while (sim.callScriptFunction("get_move_done", fscript) == 0):
        sim.callScriptFunction("franka_control", fscript, obj_pos)
    time.sleep(.8)
    sim.callScriptFunction("pickup_obj", fscript, cubes[usr_inpt], 1)
    while (sim.callScriptFunction("get_move_done", fscript) == 0):
        sim.callScriptFunction("franka_control", fscript, waypt_pos)




    sim.callScriptFunction("changeTable", pscript, 0)

    time.sleep(1)
    while not sim.callScriptFunction("isPathDone", pscript):
        print("moving")
    print('here')

    dropoff_pos = sim.getObjectPose(dropoff, simBase)

    while (sim.callScriptFunction("get_move_done", fscript) == 0):
            sim.callScriptFunction("franka_control", fscript, dropoff_pos)
    time.sleep(.8)
    sim.callScriptFunction("pickup_obj", fscript, cubes[usr_inpt], 2)

    while (sim.callScriptFunction("get_move_done", fscript) == 0):
            sim.callScriptFunction("franka_control", fscript, waypt_pos)

    dropoff_pos = sim.getObjectPose(dropoff, -1)
    sim.setObjectPosition(dropoff, -1, [dropoff_pos[0] +.1, dropoff_pos[1], dropoff_pos[2]])

    cont_inpt = input("Do you want to continue? (y/n): ")

    if (cont_inpt == 'n'):
        break
    
    sim.callScriptFunction("changeTable", pscript, 0)
    cubes.remove(cubes[usr_inpt])
    fruits.remove(fruits[usr_inpt])
