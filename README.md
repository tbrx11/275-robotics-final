# Mobile Manipulator Vision-Based Surgery Assistant

## Team Members and Roles
Tanay Patel - Implemented manipulator arm, compiled and debugged simulation. Wrote introduction, approach, and conclusion of GitHub page

Mark Shetyn - Implemented robot vision and neural network. Wrote approach and results section of GitHub page

Charles Kahn - Implemented mobile robot path planning and differential drive. Wrote approach and results section of GitHub page


## Introduction
Our goal was to create a surgery assistant robot that could pick up requested objects from a table for a surgeon who is operating on a patient or has their hands full. We struggled to find a good database with images and models of medical equipment so we decided to put different fruits on cubes for the sake of concept. In this project, we will be exploring many concepts from ECSE 275, such as mobile robotics path generation, off-center kinematics, inverse kinematics, trajectory generation, robot vision, and neural networks. In the end, we expect our robot to be able to navigate to a table, find a user-inputted object, pick up the object, transport the object to another table, and drop the object off on the table. The robot should be able to do this as many times as the user requests or until it runs out of objects to pick up. Furthermore, the position of the objects on the tables will randomized each time the robot goes to pick up a new one, as it is likely that things shift around in the real world.


## Approach
The system consisted of three main parts, the mobile PioneerP3DX robot, the manipulator Franka robot, and a vision sensor for robot vision. 

### PioneerP3DX
The PioneerP3DX mobile robot model was implemented using the CoppeliaSim template for it.

### Franka
The Franka manipulator model was implemented using the CoppeliaSim template for it. It was controlled with an inverse kinematics environment using a CoppeliaSim add-on. Inverse kinematics were used to move the robot to a specified point with respect to the PioneerP3DX robot base. The first big question in the design of this section was whether to use a constant velocity trajectory or a minimum jerk trajectory. A constant velocity trajectory would lead to more predictable movement for the robot from an outside view, as it moves linearly to its target. A minimum jerk trajectory, however, was better for our applications. Our robot was expected to pick up an object from the table and a minimum jerk trajectory led to a much smoother interaction with the object on the table. To pick up and drop objects, we used the setObjectParent() function in CoppeliaSim to fake the actual picking up of a cube. This was because of the difficulty of picking up the objects with an actual gripper. 

### Robot Vision


### Compilation
A Python script was created to run all of the individual parts together. The script first asked the user to pick a fruit. Then it started the simulation and allowed the PioneerP3DX to make its way to the object table. It checked whether the robot was at its desired location by calling a getter function in the PioneerP3DX code. Once it reached the table, the Python code took a look at the vision sensor data and ran it through the model to table each cube. The centroids of each cube were found. The centroid of the requested object was sent to a function in the Frank code that moved the tip of the robot to a specified pose. Once it got there, another function was called to attach the object to the robot. Once the Franka moved back to its ideal position, a PioneerP3DX function was called that told the robot to move to the other table. Once there, the Franka dropped the object at a specified drop-point that was put on the table. The code closed by moving the drop-point over a bit and removing the dropped-off fruit from the list of fruits the user could select. The code asks if the user would like to continue and prompts them to pick another fruit as the PioneerP3DX makes its way back to the object table.

What are the main “building blocks” of your system? How did you implement each of them? Why did you
choose to implement them this way? How did the ECSE 275 concepts you learned inform your approach to
each part? What experiments did you conduct and what data did you gather to measure the performance
of the system or define success? Include a summary flow chart of how different components in your
implementation interface with each other. What messages or data is passed between components?


## Results
The results section should contain images of your final implementation, GIFs of some part of your system
in action. You should embed mp4 videos of your working implementation into the page by first
uploading it to YouTube. It should go over any quantitative data you might have gathered which can be
presented as a table, or a graphical plot. Also, talk about the performance qualitatively. Then discuss if
the implementation met the team’s pre-determined metrics of success. If it did, why was it successful? If it
did not, then what could have been done instead (offer some suggestions).


## Conclusion
Using the robot models from CoppleiaSim and a neural network model, we created a robot that could pick up a specified fruit block and drop it on another table. We had a Python script that would prompt the user for an object, start the simulation, and have our robot perform the task with the object. The simulation worked very well and achieved our goals. It was not perfect, however. One problem we faced was that when our tables were placed in a certain orientation, the robot's path would cause the robot to go through the table. We would be able to address this by updating our path-planning algorithm to account for the table's dimensions. The biggest problem we encountered was the inaccuracy of the neural network model in simulation. Our model failed the accurately label fruit when it saw them through the vision sensor attached to the robot. We never got it to match the actual accuracy of our model in testing. This is definitely an aspect of our project that would need to be improved. We would also want to implement a gripper attached to the Franka to match how to robot would have to function in real life.
