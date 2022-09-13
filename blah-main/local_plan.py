#!/usr/bin/env python

import rospy
import math
import actionlib
import socket


from std_msgs.msg import String
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion

from math import atan2



#msg_pub = rospy.Publisher('msgTest', String, queue_size=10)
#move_pub = rospy.Publisher('moveTest', MoveBaseGoal, queue_size=10)

# rospy.init_node('move_bot', anonymous=True)
# vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
# rate = rospy.Rate(10)
# move = Twist()


class Movement:
    def __init__(self):
        # self.goal = Point()
        # self.goal.x = 0
        # self.goal_y = 0

        self.cur_x = 0.0
        self.cur_y = 0.0
        self.theta = 0.0

        self.delta = 0.1

        self.rot_speed = 0.3
        self.forward_speed = 0.6
        # rospy.init_node("speed_controller")

        # create publisher and subscriber
        self.sub = rospy.Subscriber("/odom", Odometry, self.newOdom) # our odometry node is called /odom and not /odometry/filtered
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

        # create a move variable
        self.move = Twist()

        # set the rate
        self.r = rospy.Rate(4)



    # def set_goal_point(self, goal_x, goal_y):
    #     self.goal.x = goal_x
    #     self.goal.y = goal_y



    def newOdom(self, msg):
        # get the current x and y position values for the robot
        self.cur_x = msg.pose.pose.position.x
        self.cur_y = msg.pose.pose.position.y

        rot_q = msg.pose.pose.orientation
        (roll, pitch, self.theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
        # rospy.loginfo("Current x-coordinate: " + str(self.cur_x))
        # rospy.loginfo("Current y-coordinate: " + str(self.cur_y))
        # rospy.loginfo("Current theta value: " + str(self.theta))


    # curGoal is of type Point()
    def move_to_goal_point(self, curGoal):
        reached = False
        x = curGoal.x
        y = curGoal.y
	    rospy.loginfo("Inside move_to_goal_point()")
        while not rospy.is_shutdown() and not reached:
            inc_x = x - self.cur_x
            inc_y = y - self.cur_y

            rospy.loginfo("Incrementation of x: " + str(inc_x))
            rospy.loginfo("Incrementation of y: " + str(inc_y))

            angle_to_goal = atan2(inc_y, inc_x)
            dist = math.sqrt(((x - self.cur_x)**2) + ((y - self.cur_y)**2))
            # rospy.loginfo("Current distance to goal: " + str(dist))

        # IS NOT UPDATING TO THE NEW ANGLE SEEN, SO IT IS STUCK AT 0.78
            if dist <= self.delta: #and abs(self.theta) <= self.delta * 0.5:
                rospy.loginfo("Theta: " + str(self.theta))
                rospy.loginfo("Robot is close enough to the participants. Stopping now!")
                self.move.linear.x = 0.0
                self.move.angular.z = 0.0
                reached = True

            # elif dist <= self.delta and abs(self.theta) > self.delta * 0.5:
            #     rospy.loginfo("Theta: " + str(self.theta))
            #     if y > 0:
            #          self.move.linear.x = 0.0
            #          self.move.angular.z = -0.15
            #          # do something
            #     else:
            #          self.move.linear.x = 0.0
            #          self.move.angular.z = 0.15



            elif abs(angle_to_goal - self.theta) > 0.1:
                if y > 0:
                     self.move.linear.x = 0.0
                     self.move.angular.z = self.rot_speed # 0.25
                     # do something
                else:
                     self.move.linear.x = 0.0
                     self.move.angular.z = -1 * self.rot_speed # -0.25

            else:
                self.move.linear.x = self.forward_speed # 0.5
                self.move.angular.z = 0.0

            self.pub.publish(self.move)
            self.r.sleep()


    def return_to_starting_pos(self):
        startGoal = Point()
        startGoal.x = 0
        startGoal.y = 0

        # prompt user if ready to return to table
        ready = raw_input("Should the robot return to the starting position (y/n)?")

        if ready.lower() == "y":
            self.move_to_goal_point(startGoal)
        else:
            rospy.loginfo("Study complete. People didn't summon robot")

    # PASS GOAL POINT TO MOVEMENT FUNCTION
    def stop(self):
        self.move.linear.x = 0.0
        self.move.angular.z = 0.0
        self.pub.publish(self.move)

    #
    # def mixed_circle(self):
    #     rospy.loginfo("Inside mixed_circle")
	#     #Start listening on socket
    #     self.move.linear.x= 0.6
    #     self.move.angular.z=-0.3
    #     self.pub.publish(self.move)

    def correct_orientation(self, curGoal):
        reached = False
        x = curGoal.x
        y = curGoal.y
	    rospy.loginfo("Inside move_to_goal_point()")
        while not rospy.is_shutdown() and not reached:
            inc_x = x - self.cur_x
            inc_y = y - self.cur_y

            angle_to_goal = atan2(inc_y, inc_x)
            dist = math.sqrt(((x - self.cur_x)**2) + ((y - self.cur_y)**2))

            if dist <= self.delta and abs(self.theta) > self.delta * 0.5:
                rospy.loginfo("Theta: " + str(self.theta))
                if y > 0:
                     self.move.linear.x = 0.0
                     self.move.angular.z = self.rot_speed * -0.5 #-0.15
                     # do something
                else:
                     self.move.linear.x = 0.0
                     self.move.angular.z = self.rot_speed * 0.5 # 0.15
            else:
                 self.move.linear.x = 0.0
                 self.move.angular.z = 0.0
                 reached = True
            self.pub.publish(self.move)

    def final_formation_orientation(self,orientation):
        while abs(self.theta - orientation) > self.delta*0.5:
            if self.theta < orientation:
                self.move.linear.x = 0.0
                self.move.angular.z = self.rot_speed  # 0.25
            else:
                self.move.linear.x = 0.0
                self.move.angular.z = -self.rot_speed

