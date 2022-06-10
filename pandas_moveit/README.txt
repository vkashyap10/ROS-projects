Code developed by Vishal Kashyap
Student ID: 210684838

This package uses the moveit library to make a square in the cartesian plane using panda robot.

To run the package:

Note: Make sure you have installed the moveit_tutorials and panda_moveit_config 
In the src fodler of your catkin workspace:
git clone -b ROS_Distro-devel https://github.com/ros-planning/panda_moveit_config.git (replace ROS_Distro by the distribution of ROS you are running)
rosdep update
rosdep install --from-paths . --ignore-src -r -y
cd ..
catkin_make

1) unzip ar_week10_test.zip in your catking workspace
2) Go to your catkin workspace directory (this contains build, devel and src folders)
3) build the package using command: catkin_make
4) source the catkin workspace (from your catkin workspace directory)  using command: source devel/setup.bash
5) Use the following command to launch rvi with moveit :  roslaunch panda_moveit_config demo.launch
6) Run the node to generate length of square every 20 seconds: rosrun ar_week10_test square_size_generator.py
7) Run the node to plan and execute trajectory: rosrun ar_week10_test move_panda_square.py
8) Use rqt plot to visualise joint angles: rosrun rqt_plot rqt_plot


