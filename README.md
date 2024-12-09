# Mobile Manipulator Vision-Based Surgery Assistant
Link to keras model: https://drive.google.com/file/d/1i00Yo24tktoG5qcwhM39OOEOX_g36iXb/view?usp=drive_link 

## Team Members and Roles
Tanay Patel - Implemented manipulator arm, compiled and debugged simulation. Wrote introduction, approach, and conclusion of GitHub page

Mark Shetyn - Implemented robot vision and neural network. Wrote approach and results section of GitHub page

Charles Kahn - Implemented mobile robot path planning and differential drive. Wrote approach and results section of GitHub page


## Introduction
Our goal was to create a surgery assistant robot that could pick up requested objects from a table for a surgeon who is operating on a patient or has their hands full. We struggled to find a good database with images and models of medical equipment so we decided to put different fruits on cubes for the sake of concept. In this project, we will be exploring many concepts from ECSE 275, such as mobile robotics path generation, off-center kinematics, inverse kinematics, trajectory generation, robot vision, and neural networks. In the end, we expect our robot to be able to navigate to a table, find a user-inputted object, pick up the object, transport the object to another table, and drop the object off on the table. The robot should be able to do this as many times as the user requests or until it runs out of objects to pick up. Furthermore, the position of the objects on the tables will randomized each time the robot goes to pick up a new one, as it is likely that things shift around in the real world.


## Approach
The system consisted of three main parts, the mobile PioneerP3DX robot, the manipulator Franka robot, and a vision sensor for robot vision. 

### PioneerP3DX
The PioneerP3DX mobile robot model was implemented initially using the CoppeliaSim template for it. Its routine was then built using CoppeliaSim's path generation library for direction and a Jacobian-based differential-drive control system.

The system's "state" was controlled by a series of variables which would then be polled by routines whenever needed. This was because the system performed various tasks at specific points, while it would be commanded to perform tasks in certain ways at any time. To accomplish this, we added a series of functions that Python scripts could access, which would alter the value of certain state variables, and then the actuation and sensing routines would respond to the altered value once those routines were called.

On initialization, the system would generate two target points to act as endpoints for the robot's path if the robot was commanded to go to table 1 or table 2 respectively. This allowed the robot to move to the correct points no matter where the tables were placed. Unfortunately, time constrainsts meant that we couldn't have the path avoid intrinsic obstacles, so the tables had to be placed in a way that a linear path between them would not go through the tables.

After the target points had been generated, the robot would then go into its sensing phase, in which it generated a path if no path existed that met the current criteria (such as on init), with its starting point at the robot's current position and its endpoint at the current target table's respective target point. To ensure that the robot would be oriented towards the table, the function also generated an intermediate point located a certain amount away from the target point on the table's x axis. This was to ensure that as soon as the robot reached a table, the camera could view all objects on it for the duration of the processing time, and then the objects would still be in roughly the same position as they were when processing started.

The effect of this is that a Python script could call changeTable() whenever it needed the robot to move to a new table, and then it would generate a new path from the current table to the new one, with a third point it would always hit in the middle that allowed the robot to reorient itself toward the new table's x axis. In case the robot could not reach some object, another function also existed to make the robot move toward a point offset along the table's y axis, but we did not end up using this function for the presentation.

### Franka
The Franka manipulator model was implemented using the CoppeliaSim template for it. It was controlled with an inverse kinematics environment using a CoppeliaSim add-on. Inverse kinematics were used to move the robot to a specified point with respect to the PioneerP3DX robot base. The first big question in the design of this section was whether to use a constant velocity trajectory or a minimum jerk trajectory. A constant velocity trajectory would lead to more predictable movement for the robot from an outside view, as it moves linearly to its target. A minimum jerk trajectory, however, was better for our applications. Our robot was expected to pick up an object from the table and a minimum jerk trajectory led to a much smoother interaction with the object on the table. To pick up and drop objects, we used the setObjectParent() function in CoppeliaSim to fake the actual picking up of a cube. This was because of the difficulty of picking up the objects with an actual gripper. 

### Robot Vision
The robot's vision system was done with the combination of OpenCV for object detection and a trained Convolutional Neural Network for fruit classification. The table is captured by the robot's vision sensor, where single fruit blobs were detected as the first step in this process. The blobs were identified by OpenCV's contour detection, which computed the centroids. These centroids are important in calculating the spatial location of the objects.

Once the centroids were computed, mapping and extraction of the region of interest around each blob were made. The images of the blobs were resized to 28 x 28 pixels to match the input size expected by the CNN. This CNN, trained on a dataset of thousands of fruit images, then classified each ROI image.

If the model's prediction matched the fruit specified by the user, the system calculated the centroid in the robot's frame of reference rather than the vision sensor's frame. This transformation ensured the manipulator could reach the target fruit with complete accuracy. The centroid data, along with the classification result, was then sent to the robot controller for precise picking and placement of the object. This integration allowed the vision system to effectively guide the robot's manipulator for the requested task.

### Compilation
A Python script was created to run all of the individual parts together. The script first asked the user to pick a fruit. Then it started the simulation and allowed the PioneerP3DX to make its way to the object table. It checked whether the robot was at its desired location by calling a getter function in the PioneerP3DX code. Once it reached the table, the Python code took a look at the vision sensor data and ran it through the model to table each cube. The centroids of each cube were found. The centroid of the requested object was sent to a function in the Frank code that moved the tip of the robot to a specified pose. Once it got there, another function was called to attach the object to the robot. Once the Franka moved back to its ideal position, a PioneerP3DX function was called that told the robot to move to the other table. Once there, the Franka dropped the object at a specified drop-point that was put on the table. The code closed by moving the drop-point over a bit and removing the dropped-off fruit from the list of fruits the user could select. The code asks if the user would like to continue and prompts them to pick another fruit as the PioneerP3DX makes its way back to the object table.

![Note Dec 9, 2024](https://github.com/user-attachments/assets/a89ee093-c962-4c1a-8191-3bac2c86f92c)


## Results
The robot ended up performing all the basic tasks we set out for it to complete: it would sense the locations of all the objects present on the "input" table, determine the nature of said objects, pick up the object of the requested nature, and move the object to the "output" table.

Video Demonstration:
[![Robot Demo](https://img.youtube.com/vi/TGcFJrstmKc/0.jpg)](https://www.youtube.com/watch?v=TGcFJrstmKc)

As for the computer vision section, we found that the model could predict the name of a fruit with an average accuracy of around 99.4%. 


## Conclusion
Using the robot models from CoppleiaSim and a neural network model, we created a robot that could pick up a specified fruit block and drop it on another table. We had a Python script that would prompt the user for an object, start the simulation, and have our robot perform the task with the object. The simulation worked very well and achieved our goals. It was not perfect, however. One problem we faced was that when our tables were placed in a certain orientation, the robot's path would cause the robot to go through the table. We would be able to address this by updating our path-planning algorithm to account for the table's dimensions. The biggest problem we encountered was the inaccuracy of the neural network model in simulation. Our model failed the accurately label fruit when it saw them through the vision sensor attached to the robot. We never got it to match the actual accuracy of our model in testing. This is definitely an aspect of our project that would need to be improved. We would also want to implement a gripper attached to the Franka to match how to robot would have to function in real life.
