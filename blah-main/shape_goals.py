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

    def get_into_formation(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        if shape == 'triangle':
            goals = self.triangle(shape, x_ref,y_ref,side_length,num_rob,orientation)
        elif shape == 'line':
            goals = self.line(shape, x_ref, y_ref, side_length, num_rob, orientation)


        goal = Point()



    def move_to_ref_point(self):


        goal = Point()

        response = raw_input("Are you ready for act 2? ")

        self.mover.move_to_goal_point(goal)
        self.mover.correct_orientation(goal)

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

        initiator = Initiator(mover
        ########################################
        #
        #       SOCKET CONNECTION FOR BUTTON
        #
        ########################################




        # test_data=pd.read_csv('test.csv')
        # test_df=pd.DataFrame(data=test_data)
        #row, column= input('Row, Column #s:').split()


        scenario = input('What shape would you like?').lower()

        # THE REFERENCE POINT IS RELATIVE TO ROBOT 0, ROBOT 0 IS CONSIDERED 0,0
        ref_point_input = input('Where would you like the shape to go? Ex. 3,3')
        ref_point = [int(x) for x in ref_point_input.split(',') if x.strip()]
        x_ref_final = ref_point[0]
        y_ref_final = ref_point[1]

        # Orientation is relative to the reference point so that the
        #### formation is created pointing to the ref point then the robots
        #### all just have to move forward until robot 0 is at the ref point
        orientation = atan2(y_ref,x_ref)

        ready=raw_input('Are you ready? (yes/no)').lower()

        while ready == 'no':
            time.sleep(5)
            ready=input('Are you ready?')




        if scenario == 'triangle':

            initiator.entrance("clump")
            time.sleep(1)
            initiator.set_clump_shape_goals(direction='towards',grouping='disperse')

        elif scenario == 2:
            # Initiator == both
            # toWhom == Person A/B
            initiator.entrance("clump")
            time.sleep(1)
            initiator.set_clump_shape_goals(direction='towards',grouping='clump')

        elif scenario == 3:
            # Initiator == person
            # toWhom == Person A/B
            initiator.entrance("clump")
            time.sleep(1)
            initiator.set_clump_shape_goals(direction='away',grouping='disperse')

        elif scenario == 4:
            initiator.entrance("clump")
            time.sleep(1)
            initiator.set_clump_shape_goals(direction='away',grouping='clump')

        
        elif scenario == 5:
            # Initiator == robot
            # toWhom == Person A/B
            initiator.entrance("disperse")
            time.sleep(1) # may need to adjust to be greater for robots 1 and 8
            initiator.set_disperse_shape_goals(direction='towards',grouping='disperse')

        elif scenario == 6:
            # Initiator == both
            # toWhom == Person A/B
            initiator.entrance("disperse")
            time.sleep(1) # may need to adjust to be greater for robots 1 and 8
            initiator.set_disperse_shape_goals(direction='towards',grouping='clump')

        elif scenario == 7:
            # Initiator == person
            # toWhom == Person A/B
            initiator.entrance("disperse")
            time.sleep(1) # may need to adjust to be greater for robots 1 and 8
            initiator.set_disperse_shape_goals(direction='away',grouping='disperse')

        elif scenario == 8:
            initiator.entrance("disperse")
            time.sleep(1)
            initiator.set_disperse_shape_goals(direction='away',grouping='clump')



        # mover.return_to_starting_pos()

    except rospy.ROSInterruptException:
        rospy.loginfo("Didn't work, so cry")