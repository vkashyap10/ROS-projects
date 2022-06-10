#!/usr/bin/env python

# This is the service node which constructs the bbn based on cpt values.

import rospy
import imp; imp.find_module('bayesian_belief_networks')
from bayesian_belief_networks.ros_utils import *

# probabilites for object and human expression ,action are equally distributed
def f_O(O):
    return 1.0/2

def f_HE(HE):
    return 1.0/3

def f_HA(HA):
    return 1.0/3

# probabilities for robot expression is calculated using cpt table.
def f_RE(O,HE,HA,RE):
    # here list of size 3 is for happy, sad and neutral expression of robot for given combination of observed information
    h_table = {}
    h_table['111'] = [0.8,0.2,0.0]
    h_table['112'] = [1.0,0.0,0.0]
    h_table['121'] = [0.8,0.2,0.0]
    h_table['122'] = [1.0,0.0,0.0]
    h_table['131'] = [0.6,0.2,0.2]
    h_table['132'] = [0.8,0.2,0.0]
    h_table['211'] = [0.0,0.0,1.0]
    h_table['212'] = [0.0,0.0,1.0]
    h_table['221'] = [0.0,0.1,0.9]
    h_table['222'] = [0.1,0.1,0.8]
    h_table['231'] = [0.0,0.2,0.8]
    h_table['232'] = [0.2,0.2,0.6]
    h_table['311'] = [0.7,0.3,0.0]
    h_table['312'] = [0.8,0.2,0.0]
    h_table['321'] = [0.8,0.2,0.0]
    h_table['322'] = [0.9,0.1,0.0]
    h_table['331'] = [0.6,0.2,0.2]
    h_table['332'] = [0.7,0.2,0.1]

    if(int(HE)>0 and int(HA)>0 and int(O)>0):
        return h_table[str(HE)+str(HA)+str(O)][int(RE)-1]

# initialise node
rospy.init_node('predict_robot_expression')

# initialise bbn
g = ros_build_bbn(
    f_O,
    f_HE,
    f_HA,
    f_RE,
    domains=dict(
        O=['1', '2'],
        HE=['1', '2', '3'],
        HA=['1', '2', '3'],
        RE=['1', '2', '3']))
    

rospy.spin()

