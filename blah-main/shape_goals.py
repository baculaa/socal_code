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




# def write_script(row, column):
#     #print(trial_number, test_df.iloc[row, column])
#     condition= random.choice(conditions)
#     relationship=random.choice(relationships)
#     print('Scenario:', test_df.iloc[row, column], condition, ',',relationship)
#     return 'Scenario:', test_df.iloc[row, column], condition, ',',relationship



#######################################
# CLASS NAME: Initiator
# DESCRIPTION: Represents the initiator variable in our cocktailbot study
#
# INPUT: a Movement() object for directing
#
#######################################
class Initiator:
    def __init__(self, mover):
        self.mover = mover
        ## CHANGE LATER?
        self.ref_point = (4, 0)
        self.offset = (0, 0) # -0.5,

    def set_clump_shape_goals(self, direction, grouping):

        # # wait X amount of seconds before moving
        # time.sleep(random.choice([10,15,20]))

        # STARTING OFFSET POSITIONS OF ROBOTS
        # 1: (2, 0.5)
        # 2: (2, 0.5)
        # 8: (2, -0.5)
        # 10: (2, -0.5)

        # STARTING ROBOT POSITION ACCORDING TO RVIZ
        # 1: (2, 0)
        # 2: (2, 0)
        # 8: (2, 0)
        # 10: (2, 0)


        goal = Point()

        if direction == 'towards' and grouping == "disperse": # in test_df.iloc[row][column]:
            # FOR ROBOT 2
            goal.x = self.ref_point[0] # 
            goal.y = self.offset[1] + 0.5
           
            # # FOR ROBOTS 1 and 8
            # goal.x = self.ref_point[0] - 0.5 # already farther in front than robots 2 and 10 by 0.5
            # goal.y = self.offset[1]

            # FOR ROBOT 10
            # goal.x = self.ref_point[0] # - self.offset[0]
            # goal.y = self.offset[1] - 0.5

        elif direction == 'towards' and grouping == "clump": # in test_df.iloc[row][column]:
            # # FORWARD ROBOTS 1 and 8
            # goal.x = self.ref_point[0] # already farther in front than robots 2 and 10 by 0.5
            # goal.y = self.offset[1] # robot 8 -0.25

            # ROBOT 2
            goal.x = self.ref_point[0] - 0.25
            goal.y = self.offset[1] - 0.25 #robot 10 -0.6

            # ROBOT 10
            # goal.x = self.ref_point[0] - 0.25
            # goal.y = self.offset[1] + 0.25 #robot 10 -0.6

        elif direction == 'away' and grouping == "disperse": # in test_df.iloc[row][column]:
            # FOR ROBOTS 2 and 10
            goal.x = self.offset[0] - 0.25
            goal.y = self.offset[1]

            # # FOR ROBOT 1
            # goal.x = self.offset[0] - 0.25
            # goal.y = self.offset[1] + 0.5

            # FOR ROBOT 8
            # goal.x = self.offset[0] - 0.25
            # goal.y = self.offset[1] - 0.5

        elif direction == 'away' and grouping == "clump":
            # FOR ALL ROBOTS
            goal.x = self.offset[0] - 0.25
            goal.y = 0

        # else:
        #     goal.x = 1
        #     goal.y = 0

        response = raw_input("Are you ready for act 2? ")
        self.mover.move_to_goal_point(goal)
        self.mover.correct_orientation(goal)




    def set_disperse_shape_goals(self, direction, grouping):

        # # wait X amount of seconds before moving
        # time.sleep(random.choice([10,15,20]))

        # STARTING OFFSET POSITIONS OF ROBOTS
        # 1: (2, -0.5)
        # 2: (2, 1)
        # 8: (2, -1)
        # 10: (2, 0.5)

        # STARTING ROBOT POSITIONS BASED ON RVIS:
        # 1: (1.5, -1)
        # 2: (2, 1)
        # 8: (1.5, -1)
        # 10: (2, 1)


        goal = Point()

        if direction == 'towards' and grouping == "disperse": # in test_df.iloc[row][column]:
            # START POSITIONS
            # OFFSET COORDINATE OF ROBOTS vs CURRENT POSITIONS IN RVIZ --> OFFSET EQUATION:
            # 1: (2, -0.5) vs. (1.5, -1) -->  OFFSET = (goalB.x + 0.5, goalB.y + 0.5)
            # 2: (2, 1) vs. (2, 1) --> OFFSET = (goalB.x, goalB.y)
            # 8: (2, -1) vs. (1.5, -1) --> OFFSET = (goalB.x + 0.5, goalB.y)
            # 10: (2, 0.5) vs. (2, 1) --> OFFSET = (goalB.x, goalB.y - 0.5)



            # FINAL POSITIONS
            # 1: (4, -0.5) vs. (3.5, -1) 
            # 2: (4, 1) vs. (4, 1) 
            # 8: (4, -1) vs. (3.5, -1) 
            # 10: (4, 0.5) vs. (4, 1) 

            # # FOR ROBOTS 1 and 8
            # goal.x = self.ref_point[0] - 0.5 # get to (3.5, -1) in RVIZ
            # goal.y = -1 # 1: (offset[1] - 0.5), 8: (offset[1])

            # FOR ROBOTS 2 and 10
            goal.x = self.ref_point[0]
            goal.y = 1 # 2: offset[1], 10: (offset[1] + 0.5)



        elif direction == 'towards' and grouping == "clump": # in test_df.iloc[row][column]:

            # OFFSET COORDINATE OF ROBOTS vs CURRENT POSITIONS IN RVIZ --> OFFSET EQUATION:
            # 1: (2, -0.5) vs. (1.5, -1) 
            # 2: (2, 1) vs. (2, 1) 
            # 8: (2, -1) vs. (1.5, -1) 
            # 10: (2, 0.5) vs. (2, 1) 

            # FINAL POSITIONS
            # 1: (3.5, -0.25) vs. (3, -0.75) 
            # 2: (4, 0.5) vs. (4, 0.5) 
            # 8: (4, -0.5) vs. (3.5, -0.5) 
            # 10: (3.5, 0.25) vs. (3, 0.75) 

            # # FOR ROBOT 1
            # goal.x = self.ref_point[0] - 1 
            # goal.y = self.offset[1] - 0.25 # -0.5 - 0.25

            # # FOR ROBOT 8 
            # goal.x = self.ref_point[0] - 0.5 # - self.offset[0]
            # goal.y = self.offset[1] + 0.5 # 

            # # ROBOT 10
            # goal.x = self.ref_point[0] - 0.5 # 4 - 0.5 = 3.5
            # goal.y = self.offset[1] + 0.25 # 0.5 + 0.25 = 0.75

            # ROBOT 2
            goal.x = self.ref_point[0] # 4
            goal.y = self.offset[1] - 0.5 # 1 - 0.5 = 0.5


        elif direction == 'away' and grouping == "disperse": # in test_df.iloc[row][column]:


            # OFFSET COORDINATE OF ROBOTS vs CURRENT POSITIONS IN RVIZ --> OFFSET EQUATION:
            # 1: (2, -0.5) vs. (1.5, -1) 
            # 2: (2, 1) vs. (2, 1) 
            # 8: (2, -1) vs. (1.5, -1) 
            # 10: (2, 0.5) vs. (2, 1) 

            # FINAL POSITIONS
            # 1: (1.75, -0.5) vs. (1.25, -1) 
            # 2: (1.75, 1) vs. (1.75, 1) 
            # 8: (1.75, -1) vs. (1.25, -1) 
            # 10: (1.75, 0.5) vs. (1.75, 1)
            
            # FOR ROBOT 2
            goal.x = self.offset[0] - 0.25 # 
            goal.y = self.offset[1] # want to equal 1

            # # FOR ROBOT 1
            # goal.x = self.offset[0] - 0.25
            # goal.y = self.offset[1] - 0.5

            # # FOR ROBOT 8
            # goal.x = self.offset[0] - 0.25
            # goal.y = self.offset[1] 

            # # FOR ROBOT 10
            # goal.x = self.offset[0] - 0.25
            # goal.y = self.offset[1] + 0.5 # want to equal -1



        elif direction == 'away' and grouping == "clump":


            # OFFSET COORDINATE OF ROBOTS vs CURRENT POSITIONS IN RVIZ --> OFFSET EQUATION:
            # 1: (2, -0.5) vs. (1.5, -1) 
            # 2: (2, 1) vs. (2, 1) 
            # 8: (2, -1) vs. (1.5, -1) 
            # 10: (2, 0.5) vs. (2, 1) 

            # FINAL POSITIONS
            # 1: (1.9, -0.5) vs. (1.4, -1) 
            # 2: (1.5, 0.5) vs. (1.5, 0.5) 
            # 8: (1.5, -0.5) vs. (1, -0.5) 
            # 10: (1.9, 0.5) vs. (1.9, 1)


            # FOR ROBOT 1
            # goal.x = self.offset[0] - 0.6 # 2 - 0.6 = 1.4
            # goal.y = self.offset[1] - 0.5 # want to equal 0.5


            # FOR ROBOTS 2
            goal.x = self.offset[0] - 0.5 
            goal.y = self.offset[1] - 0.5


            # FOR ROBOTS 8
            # goal.x = self.offset[0] - 0.5
            # goal.y = self.offset[1] + 0.5

            # # FOR ROBOT 10
            # goal.x = self.offset[0] - 0.1
            # goal.y = self.offset[1] + 0.5 # want to equal -0.5

        # else:
        #     goal.x = 1
        #     goal.y = 0

        response = raw_input("Are you ready for act 2? ")

        self.mover.move_to_goal_point(goal)
        self.mover.correct_orientation(goal)




    def entrance(self, grouping):
        goalA = Point()
        goalB = Point()
        goalC = Point()

        # Move to the side
        if grouping == "clump":
            goalA.x = 0
            goalA.y = 1

            # move to the front
            goalB.x = 2
            goalB.y = 1

            # move back to the side
            goalC.x = 2
            goalC.y = 0

            goals = [goalA, goalB, goalC]


            # Loop through all the goals and move to the positions
            for goal in goals:
                self.mover.move_to_goal_point(goal)

            # correct the orientation with respect to the last goal point
            self.mover.correct_orientation(goalC)
            # set offset to the last goal point
            # Added offset number for x and y will vary for different robots
            # OFFSET = (goalB.x, goalB.y - 0.5) for robot 8 and 10
            # OFFSET = (goalB.x, goalB.y + 0.5) for robots 1 and 2
            self.offset = (goalC.x, goalC.y + 0.5)

        else:
            # ROBOTS 2 and 10
            goalA.x = 0
            goalA.y = 1

            # move to the front
            goalB.x = 2
            goalB.y = 1

            # ROBOTS 1 and 8
            # goalA.y = -1
            # goalB.x = 1.5 and goalB.y = -1

            goals = [goalA, goalB]

            # Loop through all the goals and move to the positions
            for goal in goals:
                self.mover.move_to_goal_point(goal)

            # correct the orientation with respect to the last goal point
            self.mover.correct_orientation(goalB)

            # OFFSET COORDINATE OF ROBOTS vs CURRENT POSITIONS IN RVIZ --> OFFSET EQUATION:
            # 1: (2, -0.5) vs. (1.5, -1) -->  OFFSET = (goalB.x + 0.5, goalB.y + 0.5)
            # 2: (2, 1) vs. (2, 1) --> OFFSET = (goalB.x, goalB.y)
            # 8: (2, -1) vs. (1.5, -1) --> OFFSET = (goalB.x + 0.5, goalB.y)
            # 10: (2, 0.5) vs. (2, 1) --> OFFSET = (goalB.x, goalB.y - 0.5)
            
            self.offset = (goalB.x, goalB.y) # TO FIX MATH EVENTUALLY

        # ROBOT 1 OFFSET
        # goalC.x + 0.5, goalC.y + 0.5

        # ROBOT 8 OFFSET:
        # goalC.x + 0.5, goalC.y - 0.5








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


        scenario = int(input('What scenario # are you running?'))

        ready=raw_input('Are you ready? (yes/no)').lower()

        while ready == 'no':
            time.sleep(5)
            ready=input('Are you ready?')




        if scenario == 1:
            # Initiator == robot
            # toWhom == Person A/B
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