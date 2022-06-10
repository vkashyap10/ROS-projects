#!/usr/bin/env python
# developed by: Vishal Kashyap
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
# import messages to be used
from std_msgs.msg import Float64
import time

def callback(data):
	
	# get square size to execute
	square_size = data.data
	print("========================= received square of size: ", square_size)

	#First initialize moveit_commander
	moveit_commander.roscpp_initialize(sys.argv)
	#Instantiate a RobotCommander object. Provides information such as the robots kinematic model and the robots current joint states.
	robot = moveit_commander.RobotCommander()
	# Instantiate a PlanningSceneInterface object. This provides a remote interface for getting, setting, and updating the robots internal understanding of the surrounding world
	scene = moveit_commander.PlanningSceneInterface()
	#Instantiate a MoveGroupCommander object. This object is an interface to a planning group (group of joints).
	group_name = "panda_arm"
	move_group = moveit_commander.MoveGroupCommander(group_name)

	#Create a DisplayTrajectory ROS publisher which is used to display trajectories in Rviz:
	display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)
	
	print("========================= moving to starting config")
	print()
	# 2.a) move the panda robot to starting config
	# We can get the joint values from the group and adjust some of the values:
	joint_goal = move_group.get_current_joint_values()
	joint_goal[0] = 0
	joint_goal[1] = -pi/4
	joint_goal[2] = 0
	joint_goal[3] = -pi/2
	joint_goal[4] = 0
	joint_goal[5] = pi/3
	joint_goal[6] = 0
	
	# The go command can be called with joint values, poses, or without any parameters if you have already set the pose or joint target for the group
	move_group.go(joint_goal, wait=True)

	# Calling stop() ensures that there is no residual movement
	move_group.stop()
	
	print("========================= planning cartesian path for square")
	print()
	# 2.b) plan a cartesian path
	waypoints = []
	scale = 1.0
	# move in the x direction
	wpose = move_group.get_current_pose().pose
	wpose.position.x += scale * square_size
	waypoints.append(copy.deepcopy(wpose))
	
	# move in the y direction
	wpose.position.y += scale * square_size
	waypoints.append(copy.deepcopy(wpose))
	
	# move back in the x direction
	wpose.position.x -= scale * square_size
	waypoints.append(copy.deepcopy(wpose))
	
	# move back in the y direction
	wpose.position.y -= scale * square_size
	waypoints.append(copy.deepcopy(wpose))

	# We want the Cartesian path to be interpolated at a resolution of 1 cm
	# which is why we will specify 0.01 as the eef_step in Cartesian
	# translation.  We will disable the jump threshold by setting it to 0.0,

	(plan, fraction) = move_group.compute_cartesian_path(
		                           waypoints,   # waypoints to follow
		                           0.01,        # eef_step
		                           0.0)         # jump_threshold

	# Note: We are just planning, not asking move_group to actually move the robot yet:
	time.sleep(5)
	
	# 2.c) show the planned trajectory
	print("========================= displaying planned trajectory again")
	print()
	display_trajectory = moveit_msgs.msg.DisplayTrajectory()
	display_trajectory.trajectory_start = robot.get_current_state()
	display_trajectory.trajectory.append(plan)
	# Publish
	display_trajectory_publisher.publish(display_trajectory)

	time.sleep(5)

	print("========================= executing planned trajectory")
	print()
	
	#2.d) execute the planned trajectory
	#Use execute if you would like the robot to follow the plan that has already been computed:
	move_group.execute(plan, wait=True)

	print("========================= waiting for new square length")


if __name__ == "__main__":

    # initialise node and subscribe to square size topic
    rospy.init_node('move_group_square', anonymous=True)

    # subscribe
    rospy.Subscriber('square_size', Float64, callback)

    rospy.spin()



