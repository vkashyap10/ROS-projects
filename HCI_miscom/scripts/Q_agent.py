# time spent in miscommunication will be negatively rewarded
import numpy as np
import random
import time
import copy


class QLearningAgent:
    
    def __init__(self):
        # transition tuple: prev_state --> new_state via action.
        self.prev_state = []
        self.action = 0
        # best Q value for transition (based on action)
        self.maxQ = 0
        # reward obtained for transition
        self.reward = []
        # learning rate
        self.alpha = 0.1
        self.gamma = 1
        # function mapping (state,action) to reward
        self.qf_params = np.array([0,0,0,0,0])
        self.num_updates = 0
        self.cumulative_reward = 0
        self.reward_list = []
	self.total_mis_comm = 0
        
    def Q_value(self,action):
        #var = self.prev_state.copy()
	var = copy.copy(self.prev_state)

        # append bias and action terms
        var.append(1)
        var.append(action)
        return np.matmul(self.qf_params,np.array(var))
    
    # call 2: execute action and observe new state and reward
    def update_percept(self, reward):
        # after action in previous step
        self.reward = reward

	self.cumulative_reward = self.cumulative_reward + reward
        self.reward_list.append(self.reward)
        return
    
    # call 1: given a state find optimal action.
    def max_Q_value(self,state):
        self.prev_state = state
        maxQ = 0
        action = 0
        if( self.Q_value(-1) >= self.Q_value(1) ):
            maxQ = self.Q_value(-1)
            action = -1
        else:
            maxQ = self.Q_value(1)
            action = 1
        self.action = action
        self.maxQ = maxQ
        return self.action
    
    # call 3: update after transitionsing from s to s' taking action a.
    def update_qf(self):
        
        # TD_error for transition
        self.num_updates = self.num_updates + 1
        step = self.alpha/(self.num_updates)
        TD_error = step*(self.reward + self.gamma*self.maxQ - self.Q_value(self.action))
        
        #grad = self.prev_state.copy()
	grad = copy.copy(self.prev_state)
        # append bias and action terms
        grad.append(1)
        grad.append(self.action)
        grad = np.array(grad)
                
        if(self.num_updates%10 == 0):
#             print("current parameters: ",self.qf_params )
#             print("updates: ", TD_error*grad)
            print("num updates done: ", self.num_updates)
            print("cumulative reward", self.cumulative_reward)
        self.qf_params = self.qf_params + TD_error*grad # TD_error*grad

        return

