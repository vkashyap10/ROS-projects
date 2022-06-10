#!/usr/bin/env python
# developed by: Vishal Kashyap
import sys
import copy
import rospy
import time

# import messages to be used
from std_msgs.msg import Float64
from cr_final.msg import htc_hand_sensor
from std_msgs.msg import String

import random


# import Q agent class
from Q_agent import QLearningAgent

from message_filters import ApproximateTimeSynchronizer, Subscriber

def callback(data):

	if(data.data == "Agent 2"):

		print("Agent 2 will speak now for next 20 seconds")
		
		# generate fluency tag

		t_start = time.time()
		total_interaction_time = 9
		while(time.time()-t_start < total_interaction_time):
        
			# within an episode communication can be fluent or not for a random amount of time
			mis_comm = random.uniform(0, 1)
			mis_comm = mis_comm > 0.8
			mis_comm_time = random.uniform(2, 5)
		
			t_start_comm = time.time()
		
			while( (time.time()-t_start < total_interaction_time) and (time.time()-t_start_comm < mis_comm_time) ):
				# publish fluency tag to topic fluency_agent_1
			    	fluency_var = String()
				# initialise cubic_traj coeffs msg
				if mis_comm == 1:
					fluency_var.data = "fluent"
				else:
					fluency_var.data = "not fluent"
	    
				# publish to topic
				rospy.loginfo(fluency_var)
				pub1.publish(fluency_var)

				time.sleep(1)
	return


def gotinfo(hand_sub, head_sub):
	
	reward_pos = 5.0
	reward_neg = -1.0
	reward_neut = 0.1
	reward_neg_small = -0.1

	print("Agent 2 will now listen to Agent 1")

	# get data from sensors of agent 1
	state = [hand_sub.hand_height, hand_sub.gesture_rate, head_sub.data]

	# get best action (Q_max)
	# find best action based on state (action ==1 implies mis comm detected)
        action = Q_agent.max_Q_value(state)

	# call service to receive reward
	print("service called to collect reward from agent 1")
	
	mis_comm = 0
	if(hand_sub.fluency == 'fluent'):
		mis_comm = 1
	# execute action and obtained reward and new state
	# interrupt agent
	if(action == 1):
		if(mis_comm == 1):
			# righly caught miscomm
			Q_agent.update_percept(reward_pos)
			Q_agent.update_qf()

                
		if(mis_comm == 0):
			# wrongly caught miscomm
			Q_agent.update_percept(reward_neg)
			Q_agent.update_qf()
	
	# agent decides there is no miscomm       
	if(action == -1):
		# did not detect miscomm
		if(mis_comm == 1):
			Q_agent.total_mis_comm = Q_agent.total_mis_comm + 0.01
			Q_agent.update_percept(reward_neg_small)
			Q_agent.update_qf()

                
		if(mis_comm == 0):
			# wrongly caught miscomm
			Q_agent.update_percept(reward_neut)
			Q_agent.update_qf()

	print("updated params")
	print(Q_agent.qf_params)

	print("cumulative rewards")
	print(Q_agent.cumulative_reward)

	reward_var = Float64()

	reward_var.data = Q_agent.cumulative_reward
	# publish to topic
	rospy.loginfo(reward_var)
	pub2_reward.publish(reward_var)

	mis_var = Float64()

	mis_var.data = Q_agent.total_mis_comm
	# publish to topic
	rospy.loginfo(mis_var)
	pub3_mis.publish(mis_var)

	return
		
		


if __name__ == "__main__":



	# initialise node and subscribe to speaker topic
	rospy.init_node('agent_2', anonymous=False)

	# initialise q learning agent
	Q_agent = QLearningAgent()	

	pub1 = rospy.Publisher('fluency_agent_2', String, queue_size=10)

	pub2_reward = rospy.Publisher('cumulative_reward_agent_2', Float64, queue_size=10)

	pub3_mis = rospy.Publisher('mis_comm_time_agent_1', Float64, queue_size=10)

	# subscribe to speaker topic
	rospy.Subscriber('speaker', String, callback)

	# subscribe to topics
    	hand_sub = Subscriber("HTC_tracker_agent_2", htc_hand_sensor)
    	head_sub = Subscriber("head_nod_agent_2", Float64)
    
	# ApproximateTimeSynchronizers synchronizes incoming channels by the timestamps, and outputs them in the form of a single callback that takes the same number of channels
	ats = ApproximateTimeSynchronizer([hand_sub, head_sub], queue_size=10, slop=1,allow_headerless=True)
	ats.registerCallback(gotinfo)

	rospy.spin()



