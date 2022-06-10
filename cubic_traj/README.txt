Code developed by Vishal Kashyap
Student ID: 210684838

This package calculates the cubic trajectory for random initial conditions every 20 seconds and visualises them using rqt_plot.

To run the package:

1) unzip ar_week5_test.zip in your catking workspace
2) Go to your catkin workspace directory (this contains build, devel and src folders)
3) build the package using command: catkin_make
4) source the catkin workspace (from your catkin workspace directory)  using command: source devel/setup.bash
5) Use the following command to launch the package using launch file : roslaunch ar_week5_test cubic_traj_gen.launch
6) This will launch a GUI showing position, velocity and acceleration as a function of time. 
7) To visualise the topic, open a new tab in terminal and source as done in step 4.Command: rqt_graph
