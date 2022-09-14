#!/usr/bin/env python
#8/2/22

# import pandas as pd
import random
import time
import socket
import sys


import rospy
import math
import actionlib
import local_plan # imports the Movement class from the movement.py file



# Just here for imports in case the Movement class variables need to see it in this file
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion

from math import atan2





#######################################
# CLASS NAME: Initiator

#
#######################################
class Initiator:
    def __init__(self):

        self.ref_point = (4, 0)
        self.rob_id = 0 # all robots will be 0, 1, or 2

    def get_into_formation(self,shape, x_ref,y_ref,side_length):
        # Orientation is relative to the reference point so that the
        #### formation is created pointing to the ref point then the robots
        #### all just have to move forward until robot 0 is at the ref point
        orientation = atan2(y_ref, x_ref)

        num_rob = 3

        #### ROBOTS WILL BE LINED UP 0 1 2
        if self.rob_id == 0:
            x_offset = 0
            y_offset = -0.5
            x_ref = 0 - x_offset
            y_ref = 0 - y_offset

        elif self.rob_id == 1:
            x_offset = 0
            y_offset = 0
            x_ref = 0 - x_offset
            y_ref = 0 - y_offset
        else:
            x_offset = 0
            y_offset = 0.5
            x_ref = 0 - x_offset
            y_ref = 0 - y_offset

        if shape == 'up triangle':
            goals = self.triangle(shape, x_ref,y_ref,side_length,num_rob,orientation)
        elif shape == 'down triangle':
            goals = self.triangle(shape, x_ref, y_ref, side_length, num_rob, orientation = orientation + 180)
        elif shape == 'vertical line':
            goals = self.line(shape, x_ref, y_ref, side_length, num_rob, orientation)
        elif shape == 'horizontal line':
            goals = self.line(shape, x_ref, y_ref, side_length, num_rob, oreintation = orientation + 90)
        else:
            print("Not a currently supported shape")

        if self.rob_id == 0:
            x_goal = goals[0]
            y_goal = goals[1]
        elif self.rob_id == 1:
            x_goal = goals[2]
            y_goal = goals[3]
        elif self.rob_id == 2:
            x_goal = goals[4]
            y_goal = goals[5]
        else:
            print("There are only three robots right now")


        goal = Point()
        goal.X = x_goal
        goal.Y = y_goal

        self.mover.move_to_goal_point(goal)
        self.mover.final_formation_orientation(orientation)


    def reset_to_home(self):
        goal = Point()
        goal.X = 0
        goal.Y = 0
        self.mover.move_to_goal_point(goal)
        self.mover.final_formation_orientation(0)


    def move_to_ref_point(self,x_ref,y_ref):
        ref_point = np.array((x_ref,y_ref))
        fwd_dist = np.linalg.norm(ref_point)

        goal = Point()
        goal.X = fwd_dist
        goal.Y = 0

        self.mover.move_to_goal_point(goal)



    def triangle(self, shape, x_ref, y_ref, side_length, num_rob, orientation):

        # Retrieves the info required to compute
        triangleInfo = [shape, x_ref, y_ref, side_length, num_rob, orientation]

        if triangleInfo[3] % 2 == 0:
            # We have an even number of robots

            robotNum = math.ceil(float(triangleInfo[3]) / 2)

            triangleGoal = np.zeros(int(robotNum) * 2)

            # starting from the left side
            triangleGoal[0] = float(triangleInfo[0])
            bottomEndPoint = float(triangleInfo[1])
            triangleGoal[1] = bottomEndPoint

            i = 2
            while (i < len(triangleGoal)):
                triangleGoal[i] = float(triangleInfo[0])  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                bottomEndPoint += (float(triangleInfo[2]) / (float(robotNum) - 1))  # Adding length using Thales theorem
                triangleGoal[i] = bottomEndPoint
                i += 1  # moves back to x spot

            line2 = triangleGoal

            # For the other side of the triangle line

            numPoints = len(line2)
            for j in range(0, numPoints, 2):
                x = line2[j]
                y = line2[j + 1]
                ox = triangleInfo[0]
                oy = triangleInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, -45)

                line2[j] = qx
                line2[j + 1] = qy

            # For the original side of the triangle line

            numPoints = len(triangleGoal)
            for j in range(0, numPoints, 2):
                x = triangleGoal[j]
                y = triangleGoal[j + 1]
                ox = triangleInfo[0]
                oy = triangleInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, 45)

                triangleGoal[j] = qx
                triangleGoal[j + 1] = qy

            line2_trim = line2[2:]
            triangleGoal = triangleGoal[2:]

            np.append(triangleGoal, line2_trim)

        else:
            # We have an odd number of robots

            robotNum = math.ceil(float(triangleInfo[3]) / 2)

            triangleGoal = np.zeros(int(robotNum) * 2)

            # starting from the left side
            triangleGoal[0] = float(triangleInfo[0])
            bottomEndPoint = float(triangleInfo[1])
            triangleGoal[1] = bottomEndPoint

            i = 2
            while (i < len(triangleGoal)):
                triangleGoal[i] = float(triangleInfo[0])  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                bottomEndPoint += (float(triangleInfo[2]) / (float(robotNum) - 1))  # Adding length using Thales theorem
                triangleGoal[i] = bottomEndPoint
                i += 1  # moves back to x spot

            line2 = triangleGoal

            # For the other side of the triangle line

            numPoints = len(line2)
            for j in range(0, numPoints, 2):
                x = line2[j]
                y = line2[j + 1]
                ox = triangleInfo[0]
                oy = triangleInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, -45)

                line2[j] = qx
                line2[j + 1] = qy

            # For the original side of the triangle line

            numPoints = len(triangleGoal)
            for j in range(0, numPoints, 2):
                x = triangleGoal[j]
                y = triangleGoal[j + 1]
                ox = triangleInfo[0]
                oy = triangleInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, 45)

                triangleGoal[j] = qx
                triangleGoal[j + 1] = qy

            line2_trim = line2[2:]

            np.append(triangleGoal, line2_trim)

        # Rotates the shape based on user input - No rotation down orientation default
        numPoints = len(triangleGoal)
        for j in range(0, numPoints, 2):
            x = triangleGoal[j]
            y = triangleGoal[j + 1]
            ox = triangleInfo[0]
            oy = triangleInfo[1]

            qx, qy = self.rotate_around_point(x, y, ox, oy, triangleInfo[4])

            triangleGoal[j] = qx
            triangleGoal[j + 1] = qy

        return triangleGoal

    def line(self, shape, x_ref, y_ref, side_length, num_rob, orientation):

        # Retrieves the info required to compute
        lineInfo = [shape, x_ref, y_ref, side_length, num_rob, orientation]

        lineGoal = np.zeros(int(lineInfo[3]) * 2)

        # Vertical Config
        if lineInfo[4] == 0:
            # starting from the left side
            lineGoal[0] = float(lineInfo[0])
            bottomEndPoint = float(lineInfo[1]) - (float(lineInfo[2]) / 2)
            lineGoal[1] = bottomEndPoint

            i = 2
            while (i < len(lineGoal)):
                lineGoal[i] = float(lineInfo[1])  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                bottomEndPoint += (float(lineInfo[2]) / (float(lineInfo[3]) - 1))  # Adding length using Thales theorem
                lineGoal[i] = bottomEndPoint
                i += 1  # moves back to x spot

            return lineGoal

        # Horizontal Orientation
        elif lineInfo[4] == 90:
            # starting from the left side
            leftEndPoint = float(lineInfo[0]) - (float(lineInfo[2]) / 2)
            lineGoal[0] = leftEndPoint
            lineGoal[1] = float(lineInfo[1])

            i = 2
            while (i < len(lineGoal)):
                leftEndPoint += (float(lineInfo[2]) / (float(lineInfo[3]) - 1))  # Adding length using Thales theorem
                lineGoal[i] = leftEndPoint
                i += 1  # Moved to y spot

                # Calculates new y spot
                lineGoal[i] = float(lineInfo[1])  # Plugs in x spot
                i += 1  # moves back to x spot

            return lineGoal

        # Custom Orientation
        else:
            # starting from the left side
            lineGoal[0] = float(lineInfo[0])
            bottomEndPoint = float(lineInfo[1]) - (float(lineInfo[2]) / 2)
            lineGoal[1] = bottomEndPoint

            i = 2
            while (i < len(lineGoal)):
                lineGoal[i] = float(lineInfo[0])  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                bottomEndPoint += (float(lineInfo[2]) / (float(lineInfo[3]) - 1))  # Adding length using Thales theorem
                lineGoal[i] = bottomEndPoint
                i += 1  # moves back to x spot

            numPoints = len(lineGoal)
            for j in range(0, numPoints, 2):
                x = lineGoal[j]
                y = lineGoal[j + 1]
                ox = lineInfo[0]
                oy = lineInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, lineInfo[4])

                lineGoal[j] = qx
                lineGoal[j + 1] = qy

            return lineGoal



if __name__ == '__main__':
    try:
        rospy.init_node('please_work',anonymous=True)
        mover = local_plan.Movement()

        initiator = Initiator(mover)
        ########################################
        #
        #       SOCKET CONNECTION FOR BUTTON
        #
        ########################################




        # test_data=pd.read_csv('test.csv')
        # test_df=pd.DataFrame(data=test_data)
        #row, column= input('Row, Column #s:').split()


        shape = input('What shape would you like? /n Options: up triangle, down triangle, vertical line, horizontal line').lower()

        # THE REFERENCE POINT IS RELATIVE TO ROBOT 0, ROBOT 0 IS CONSIDERED 0,0
        ref_point_input = input('Where would you like the shape to go? Ex. 3,3')
        ref_point = [int(x) for x in ref_point_input.split(',') if x.strip()]
        x_ref = ref_point[0]
        y_ref = ref_point[1]

        # How big do you want the shape?
        side_length = int(input('What would you like the side length of the shape? Ex. 2'))




        ready=raw_input('Are you ready? (yes/no)').lower()

        while ready == 'no':
            time.sleep(5)
            ready=input('Are you ready?')



        initiator.get_into_formation(shape,x_ref,y_ref,side_length)
        next_move = input("Hit enter when all robots are in the formation")
        initiator.move_to_ref_point(x_ref,y_ref)


    except rospy.ROSInterruptException:
        rospy.loginfo("Didn't work, so cry")