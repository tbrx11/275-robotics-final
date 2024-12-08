# Mobile Manipulator Vision-Based Surgery Assistant
Name of your project

## Team Members and Roles
Tanay Patel - Implemented manipulator arm, compiled and debugged simulation

Mark Shetyn - Implemented robot vision and neural network

Charles Khan - Implemented mobile robot path planning and differential drive

Describe the roles and responsibilities of each member of your team. For example: Did they help with the
implementation of a certain component of the project? Did they analyze or run experiments on the
implementation to gather results or data? Did they help plot the data and write up the project description?


## Introduction
Our goal was to create a surgery assistant robot that could pick up requested objects from a table for a surgeon who is operating on a patient or has their hands full. We struggled to find a good database with images and models of medical equipment so we decided to put different fruits on cubes for the sake of concept. In this project, we will be exploring many concepts from ECSE 275, such as mobile robotics path generation, off-center kinematics, inverse kinematics, trajectory generation, robot vision, and neural networks. In the end, we expect our robot to be able to navigate to a table, find a user-inputted object, pick up the object, transport the object to another table, and drop the object off on the table. The robot should be able to do this as many times as the user requests or until it runs out of objects to pick up. Furthermore, the position of the objects on the tables will randomized each time the robot goes to pick up a new one, as it is likely that things shift around in the real world.


## Approach
The system consisted of three main parts, the mobile PioneerP3DX robot, the manipulator Franka robot, and a vision sensor for robot vision. 

### PioneerP3DX

### Franka
The Franka manipulator model was implemented using the CoppeliaSim template for it. It was controlled with an inverse kinematics environment using a CoppeliaSim add-on. Inverse kinematics were used to move the robot to a specified point with respect to the PioneerP3DX robot base. The first big question in the design of this section was whether to use a constant velocity trajectory or a minimum jerk trajectory. A constant velocity trajectory would lead to more predictable movement for the robot from an outside view, as it moves linearly to its target. A minimum jerk trajectory, however, was better for our applications. Our robot was expected to pick up an object from the table and a minimum jerk trajectory led to a much smoother interaction with the object on the table. (INSERT GIFF??)

### Robot Vision



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
Using premade models from CoppleiaSim, we created a robot that could pick up a specified fruit block and drop it on another table. 

Summarize what you did, and the result that you achieved. Discuss how the work can be further developed
or improved in the future.
