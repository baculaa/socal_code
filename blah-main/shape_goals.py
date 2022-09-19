#!/usr/bin/env python
#8/2/22

# import pandas as pd
import random
import time
import socket
import sys
import numpy as np

import rospy
import math
import actionlib
import local_plan # imports the Movement class from the movement.py file
import websocket_session



# Just here for imports in case the Movement class variables need to see it in this file
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion

from math import atan2
from socket import *


ROBOT_ID = 10 # TO CHANGE ON EACH COMPUTER
HOST = '127.0.0.1'
SERVER_PORT = 8000

ROBOT_PORT_1 = 8001
ROBOT_PORT_2 = 8002
ROBOT_PORT_6 = 8006
ROBOT_PORT_10 = 8010


#######################################
# CLASS NAME: Initiator

#
#######################################
class Initiator:
    def __init__(self,mover):
        self.mover = mover
        # self.ref_point = (4, 0)
        self.rob_id = 1 # all robots will be 0, 1, or 2

    def get_into_formation(self,shape, x_ref,y_ref,side_length):
        # Orientation is relative to the reference point so that the
        #### formation is created pointing to the ref point then the robots
        #### all just have to move forward until robot 0 is at the ref point
        orientation = atan2(y_ref, x_ref)

        num_rob = 3

        #### ROBOTS WILL BE LINED UP 0 1 2
        if self.rob_id == 0:
            self.x_offset = 0
            self.y_offset = -0.5
            x_ref = 0 - self.x_offset
            y_ref = 0 - self.y_offset

        elif self.rob_id == 1:
            self.x_offset = 0
            self.y_offset = 0
            x_ref = 0 - self.x_offset
            y_ref = 0 - self.y_offset
        else:
            self.x_offset = 0
            self.y_offset = 0.5
            x_ref = 0 - self.x_offset
            y_ref = 0 - self.y_offset

        if shape == 1:
            # up triangle
            goals = self.triangle(shape, x_ref,y_ref,side_length,num_rob,orientation)
        elif shape == 2:
            # down triangle
            goals = self.triangle(shape, x_ref, y_ref, side_length, num_rob, orientation)
        elif shape == 3:
            # vertical line
            goals = self.line(shape, x_ref, y_ref, side_length, num_rob, orientation)
        elif shape == 4:
            # horizontal line
            goals = self.line(shape, x_ref, y_ref, side_length, num_rob, orientation)
        else:
            print("Not a currently supported shape")

        if self.rob_id == 0:
            x_goal = goals[0] - self.x_offset
            y_goal = goals[1] - self.y_offset
            
        elif self.rob_id == 1:
            x_goal = goals[2] - self.x_offset
            y_goal = goals[3] - self.y_offset
        elif self.rob_id == 2:
            x_goal = goals[4] - self.x_offset
            y_goal = goals[5] - self.y_offset
        else:
            print("There are only three robots right now")


        goal = Point()
        goal.x = x_goal
        goal.y = y_goal
        rospy.loginfo("Going to formation: "+str(x_goal)+", "+str(y_goal))
        self.mover.move_to_goal_avoidance(goal)
        rospy.loginfo("Rotating to face ref goal: " + str(orientation))
        self.mover.final_formation_orientation(orientation)


    def reset_to_home(self):
        goal = Point()
        goal.x = 0
        goal.y = 0

        rospy.loginfo("Going home")
        self.mover.move_to_goal_avoidance(goal)
        self.mover.final_formation_orientation(0)


    def move_to_ref_point(self,x_ref,y_ref):
        ref_point = np.array((x_ref,y_ref))
        fwd_dist = np.linalg.norm(ref_point)

        goal = Point()
        goal.x = x_ref+mover.cur_x
        goal.y = y_ref+mover.cur_y

        rospy.loginfo("Moving to ref goal")
        self.mover.move_to_goal_avoidance(goal)

    def rotate_around_point(self, x, y, ox, oy, degrees):

        # INPUTS:
        ## # x, y = this is our point in the geometrical shape, the point we want to rotate
        ## # ox, oy =  this is our reference point
        ## # radians = this is how much we want to rotate by in radians
        x = float(x)
        y = float(y)
        ox = float(ox)
        oy = float(oy)
        degrees = float(degrees)
        # OUTPUTS:
        ## # qx, qy = this is our point rotated about our ox, oy reference point

        """Rotate a point around a given point.

        I call this the "low performance" version since it's recalculating
        the same values more than once [cos(radians), sin(radians), x-ox, y-oy).
        It's more readable than the next function, though.
        """
        radians = (degrees * math.pi) / 180

        qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
        qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

        return qx, qy

    def triangle(self, shape, x_ref, y_ref, side_length, num_rob, orientation):
        x1_1 = 0
        y1_1 = 0
        x2_1 = np.sqrt(side_length**2 - self.y_offset**2)
        y2_1 = 0
        x3_1 = 0
        y3_1 = 0

        x1_2 = np.sqrt(side_length**2 - self.y_offset**2)
        y1_2 = 0
        x2_2 = 0 
        y2_2 = 0
        x3_2 = np.sqrt(side_length**2 - self.y_offset**2)
        y3_2 = 0


        triangleGoal_base = [x1_1,y1_1,x2_1,y2_1,x3_1,y3_1]
        triangleGoal_base2 = [x1_2,y1_2,x2_2,y2_2,x3_2,y3_2]
        if shape == 2:
            goal_rot1 = self.rotate_around_point(triangleGoal_base[0],triangleGoal_base[1],0,0,orientation)
            goal_rot2 = self.rotate_around_point(triangleGoal_base[2],triangleGoal_base[3],0,0,orientation)
            goal_rot3 = self.rotate_around_point(triangleGoal_base[4],triangleGoal_base[5],0,0,orientation)
        elif shape == 1:
            goal_rot1 = self.rotate_around_point(triangleGoal_base2[0],triangleGoal_base2[1],0,0,orientation)
            goal_rot2 = self.rotate_around_point(triangleGoal_base2[2],triangleGoal_base2[3],0,0,orientation)
            goal_rot3 = self.rotate_around_point(triangleGoal_base2[4],triangleGoal_base2[5],0,0,orientation)

        triangleGoal = [goal_rot1[0],goal_rot1[1],goal_rot2[0],goal_rot2[1],goal_rot3[0],goal_rot3[1]]
	rospy.loginfo(str(triangleGoal))
        return triangleGoal

    def line(self, shape, x_ref, y_ref, side_length, num_rob, orientation):

        y1 = side_length/3
        x1 = 0
        x2 = 0
        y2 = 0
        y3 = -side_length/3
        x3 = 0

        lineGoal_base = [x1,y1,x2,y2,x3,y3]

        if shape == 4:
            goal_rot1 = self.rotate_around_point(lineGoal_base[0],lineGoal_base[1],0,0,orientation)
            goal_rot2 = self.rotate_around_point(lineGoal_base[2],lineGoal_base[3],0,0,orientation)
            goal_rot3 = self.rotate_around_point(lineGoal_base[4],lineGoal_base[5],0,0,orientation)

        elif shape == 3:
            goal_rot1 = self.rotate_around_point(lineGoal_base[0],lineGoal_base[1],0,0,90+orientation)
            goal_rot2 = self.rotate_around_point(lineGoal_base[2],lineGoal_base[3],0,0,90+orientation)
            goal_rot3 = self.rotate_around_point(lineGoal_base[4],lineGoal_base[5],0,0,90+orientation)
        
        lineGoal = [goal_rot1[0],goal_rot1[1],goal_rot2[0],goal_rot2[1],goal_rot3[0],goal_rot3[1]]

        return lineGoal

##################################
# 
#       METHODS FOR SOCKET
#           CONNECTIONS
#
##################################

def create_send_sessions():
    

    # ROBOT 1
    sendSocket1 = socket(AF_INET, SOCK_DGRAM)
    sendSocket1.bind(('', ROBOT_PORT_1))
    sendSocket1.connect((HOST, SERVER_PORT))

    # ROBOT 2
    sendSocket2 = socket(AF_INET, SOCK_DGRAM)
    sendSocket2.bind(('', ROBOT_PORT_2))
    sendSocket2.connect((HOST, SERVER_PORT))

    # ROBOT 6
    sendSocket6 = socket(AF_INET, SOCK_DGRAM)
    sendSocket6.bind(('', ROBOT_PORT_6))
    sendSocket6.connect((HOST, SERVER_PORT))

    # ROBOT 10
    sendSocket10 = socket(AF_INET, SOCK_DGRAM)
    sendSocket10.bind(('', ROBOT_PORT_10))
    sendSocket10.connect((HOST, SERVER_PORT))

    addr = (HOST, SERVER_PORT)


    # CREATE THE SESSIONS
    session1 = websocket_session.Session(sendSocket1, addr)
    session2 = websocket_session.Session(sendSocket2, addr)
    session6 = websocket_session.Session(sendSocket6, addr)
    session10 = websocket_session.Session(sendSocket10, addr)



    if ROBOT_ID == 1:
        return [session2, session6, session10]
        
    elif ROBOT_ID == 2:
        return [session1, session6, session10]

    elif ROBOT_ID == 6:
        return [session1, session2, sesson10]

    else:
        return [session1, session2, session6]


def create_listen_session():
    addr = (HOST, SERVER_PORT)

    if ROBOT_ID == 1:
        listenSocket1 = socket(AF_INET, SOCK_DGRAM)
        listenSocket1.bind(('', SERVER_PORT))

        return websocket_session.Session(listenSocket1, addr)

    elif ROBOT_ID == 2:
        listenSocket2 = socket(AF_INET, SOCK_DGRAM)
        listenSocket2.bind(('', SERVER_PORT))

        return websocket_session.Session(listenSocket2, addr)

    elif ROBOT_ID == 6:
        listenSocket6 = socket(AF_INET, SOCK_DGRAM)
        listenSocket6.bind(('', SERVER_PORT))

        return websocket_session.Session(listenSocket6, addr)

    else:
        listenSocket10 = socket(AF_INET, SOCK_DGRAM)
        listenSocket10.bind(('', SERVER_PORT))

        return websocket_session.Session(listenSocket10, addr)

def send_msg_to_sessions(sessions, msg, blocknum):
    msg_encode = msg.encode('utf-8')
    for session in sessions:
        to_send_msg = session.make_DATA(msg_encode, blocknum)
        session.send_message(to_send_msg)


def sessions_shutdown(sessions, listenSession):
    for session in sessions:
        session.shutdown()

    listenSession.shutdown()




def read_packets(packets):
    shape = 0
    x_ref = 0
    y_ref = 0
    size = 0
    for packet in packets:
        if packet["blocknum"] == 1:
            shape = int(packet["data"])
            rospy.loginfo("shape: " + str(packet["data"]))
        elif packet["blocknum"] == 2:
            x_ref = int(packet["data"])
            rospy.loginfo("x-ref: " +str(packet["data"]))
        elif packet["blocknum"] == 3:
            y_ref = int(packet["data"])
            rospy.loginfo("y-ref: " + str(packet["data"]))
        elif:
            size = int(packet["data"])
            rospy.loginfo("size: " + str(packet["data"]))

    return shape, x_ref, y_ref, size



if __name__ == '__main__':
    try:
        rospy.init_node('please_work',anonymous=True)

        # create initiator
        mover = local_plan.Movement()
        initiator = Initiator(mover)


        # CREATE THE SESSIONS FOR ROBOTS
        


        job = raw_input("Am I (s)ending or (r)eceiving?")
        
        # RETURN A LIST OF SESSIONS TO SEND THE MESSAGE TO
        sessions = create_send_sessions()
        listenSession = create_listen_session()

        # Sending out the commands
        if job == "s":

           

            # ASK ABOUT SPECIFIC COMMANDS
            shape = input('What shape would you like? Type the number Options: 1) up triangle, 2) down triangle, 3) vertical line, 4) horizontal line: ')
            send_msg_to_sessions(sessions, shape, 1)

            # THE REFERENCE POINT IS RELATIVE TO ROBOT 0, ROBOT 0 IS CONSIDERED 0,0
            ref_point_input = input('Where would you like the shape to go? Ex. 3,3: ')
            ref_point = ref_point_input
            x_ref = ref_point[0]
            y_ref = ref_point[1]
            send_msg_to_sessions(sessions, str(x_ref), 2)
            send_msg_to_sessions(sessions, str(y_ref), 3)

            # How big do you want the shape?
            side_length = input('What would you like the side length of the shape? Ex. 3: ')
            send_msg_to_sessions(sessions, str(side_length), 4)



            ready=raw_input('Are you ready? (yes/no)').lower()

            while ready == 'no':
                time.sleep(5)
                ready=raw_input('Are you ready?')
            
            send_msg_to_sessions(sessions, ready, 5)






        else:

            # RECEIVE THE DATA FROM PORT
            packet = listenSession.receive_message()
            packet2 = listenSession.receive_message()
            packet3 = listenSession.receive_message()
            packet4 = listenSession.receive_message()
            packet5 = listenSession.receive_message()
            packets = [packet, packet2, packet3, packet4, packet5]


            # WAITS TO READ UNTIL ALL 5 ARE RECEIVED
            shape, x_ref, y_ref, side_length = read_packets(packets)

            # initiator.get_into_formation(shape,x_ref,y_ref,side_length)
            # raw_input("Hit enter when all robots are in the formation")
            # initiator.move_to_ref_point(x_ref,y_ref)
            # raw_input("Hit enter to return home")
            # initiator.reset_to_home() # TO DO: FIGURE THIS ONE OUT

        sessions_shutdown()


    except rospy.ROSInterruptException:
        rospy.loginfo("Didn't work, so cry")


