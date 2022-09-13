# Author: Ethan Villalovoz

# Imports
import os # Be able to clear screen
import math # Grabs math trig functions and pi
from math import * # Grabs certain math functions .ceil
import csv # Create a csv file
import numpy as np # Create a list modified by number inputs

#generate random float values
from random import seed
from random import random

#generte random integer values
from random import randint

#seed random number generator
seed(1)
class geometry:
    def __init__(self):
        self.goals = []

    # Linear Rotational Matrix around a point
    def rotate_around_point(self,x,y, ox,oy, degrees):

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
        radians = (degrees*math.pi)/180


        qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
        qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

        return qx, qy

    # Retrieves user inputs - reference_X, reference_Y, length of side/radius, number of robots, orientation
    def userInformation(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # # Array which stores the required info
        # storedInfo = []
        #
        # # Reference goal
        # print("What is the X coordinate you would want the reference goal to be?")
        # print("What is the Y coordinate you would want the reference goal to be?")
        #
        # # User choose the shape to be a square
        # if shape == "square":
        #     # Dimensions of the shape
        #     print("What is the side length of the square you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 4 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print("How would you like the orientation of the shape? (Up - 0 degrees, Down - 180 Degrees, Custom - X Degrees")
        #
        # # User choose the shape to be a triangle
        # elif shape == "triangle":
        #     # Dimensions of the shape
        #     print("What is the side length of the triangle you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 3 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print("How would you like the orientation of the shape? (Down - 0 degrees, Up - 180 Degrees, Custom - X Degrees")
        #
        # # User choose the shape to be a semi-circle
        # elif shape == "semi-circle":
        #     # Dimensions of the shape
        #     print("What is the radius of the semi-circle you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 3 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print("How would you like the orientation of the shape? (Up - 0 degrees, Down - 180 Degrees, Custom - X Degrees")
        #
        # # User choose the shape to be a clump
        # elif shape == "clump":
        #     # Dimensions of the shape
        #     print("What is the side length of the clump you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 3 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print(
        #         "How would you like the orientation of the shape? (Up - 0 degrees, Down - 180 Degrees, Custom - X Degress")
        #
        # # User choose the shape to be a circle
        # elif shape == "circle":
        #     # Dimensions of the shape
        #     print("What is the radius of the circle you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 3 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print(
        #         "How would you like the orientation of the shape? (Up - 0 degrees, Down - 180 Degrees, Custom - X Degrees")
        #
        # # User choose the shape to be a line
        # else:
        #     # Dimensions of the shape
        #     print("What is the side length of the line you would like?")
        #
        #     # Number of robots for configuration
        #     print("How many robots would you want for the shape? (Must be at least 2 and no greater than 10)")
        #
        #     # Orientation of shape
        #     print(
        #         "How would you like the orientation of the shape? (Up - 0 degrees, Horizontal - 90 Degrees, "
        #         "Custom - X Degrees")
        #
        # print("Respond as the format: X,Y,Length/Radius,# of robots,Orientation")
        # print("Example: 3,3,5,2,90")
        # info = input("Enter: ") # Grabs info from user
        #
        # # Splits the info of the string info and stores them in indexes of array used for the other functions
        # storedInfo = [int(x) for x in info.split(',') if x.strip()]

        storedInfo = [x_ref,y_ref,side_length,num_rob,orientation]
        ## In the stored array the info is in this order, all numbers and the array contains 5 elements
        # Index 0 - reference X goal
        # Index 1 - reference Y goal
        # Index 2 - Side/radius length of the shape
        # Index 3 - Number of robots in the configurations
        # Index 4-  Orientation of shape in degrees

        ## Checks if the number of robot configuration is valid

        valid = False

        while valid == False:

            # Square check
            if shape == "square" and (storedInfo[3] < 4 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 4 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 4 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 4 and storedInfo[3] <= 10:

                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Triangle check
            elif shape == "triangle" and (storedInfo[3] < 3 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 3 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 3 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 3 and storedInfo[3] <= 10:
                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Semi-Circle check
            elif shape == "semi-circle" and (storedInfo[3] < 3 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 3 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 3 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 3 and storedInfo[3] <= 10:
                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Clump check
            elif shape == "clump" and (storedInfo[3] < 3 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 3 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 3 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 3 and storedInfo[3] <= 10:
                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Circle check
            elif shape == "circle" and (storedInfo[3] < 3 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 3 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 3 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 3 and storedInfo[3] <= 10:
                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Line check
            elif shape == "line" and (storedInfo[3] < 2 or storedInfo[3] > 10):
                print("Number of robots you entered is less than 2 or greater than 10.")
                storedInfo[3] = int(input("Please enter a number of 2 or greater and of 10 or less: "))

                # Safe guard is valid
                if storedInfo[3] >= 2 and storedInfo[3] <= 10:
                    return storedInfo

                # Not valid must run again
                else:
                    continue

            # Passed all checks
            else:
                return storedInfo

    # User chooses to create a square with the robots
    def square(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        squareInfo = self.userInformation(shape,x_ref,y_ref,side_length,num_rob,orientation)

        # 4 robot configuration
        if squareInfo[3] == 4:
            # Square geometry calculations

            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y]

        # 5 robot configuration
        elif squareInfo[3] == 5:
            # Square geometry calculations

            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle of Square
            R5_X = float(squareInfo[0])
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y]

        # 6 robot configuration
        elif squareInfo[3] == 6:
            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle of Square
            R5_X = float(squareInfo[0])
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 6 - Bottom Middle of Square
            R6_X = float(squareInfo[0])
            R6_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y, R6_X, R6_Y]

        # 7 robot configuration
        elif squareInfo[3] == 7:
            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle of Square
            R5_X = float(squareInfo[0])
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 6 - Bottom Middle of Square
            R6_X = float(squareInfo[0])
            R6_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 7 - Middle Left of Square
            R7_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R7_Y = float(squareInfo[1])

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y, R6_X, R6_Y,
                          R7_X, R7_Y]

        # 8 robot configuration
        elif squareInfo[3] == 8:
            # Square geometry calculations
            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle of Square
            R5_X = float(squareInfo[0])
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 6 - Bottom Middle of Square
            R6_X = float(squareInfo[0])
            R6_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 7 - Middle Left of Square
            R7_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R7_Y = float(squareInfo[1])

            # Robot 8 - Middle Right of Square
            R8_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R8_Y = float(squareInfo[1])

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y, R6_X, R6_Y,
                          R7_X, R7_Y, R8_X, R8_Y]

        # 9 robot configuration
        elif squareInfo[3] == 9:
            # Square geometry calculations
            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle of Square
            R5_X = float(squareInfo[0])
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 6 - Bottom Middle of Square
            R6_X = float(squareInfo[0])
            R6_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 7 - Middle Left of Square
            R7_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R7_Y = float(squareInfo[1])

            # Robot 8 - Middle Right of Square
            R8_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R8_Y = float(squareInfo[1])

            # Robot 9 - Middle of Square
            R9_X = float(squareInfo[0])
            R9_Y = float(squareInfo[1])

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y, R6_X, R6_Y,
                          R7_X, R7_Y,
                          R8_X, R8_Y, R9_X, R9_Y]

        # 10 Robot Configuration
        else:
            # Square geometry calculations
            # Robot 1 - Top Left Corner
            R1_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R1_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)
            # Robot 2 - Top Right Corner
            R2_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R2_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 3 - Bottom Left Corner
            R3_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R3_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 4 - Bottom Right Corner
            R4_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R4_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 5 - Top Middle Left of Square
            R5_X = float(squareInfo[0]) - (float(squareInfo[2]) / 3)
            R5_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            # Robot 6 - Bottom Middle of Square
            R6_X = float(squareInfo[0])
            R6_Y = float(squareInfo[1]) - (float(squareInfo[2]) / 2)

            # Robot 7 - Middle Left of Square
            R7_X = float(squareInfo[0]) - (float(squareInfo[2]) / 2)
            R7_Y = float(squareInfo[1])

            # Robot 8 - Middle Right of Square
            R8_X = float(squareInfo[0]) + (float(squareInfo[2]) / 2)
            R8_Y = float(squareInfo[1])

            # Robot 9 - Middle of Square
            R9_X = float(squareInfo[0])
            R9_Y = float(squareInfo[1])

            # Robot 10 - Top Middle Right of Square
            R10_X = float(squareInfo[0]) + (float(squareInfo[2]) / 3)
            R10_Y = float(squareInfo[1]) + (float(squareInfo[2]) / 2)

            squareGoal = [R1_X, R1_Y, R2_X, R2_Y, R3_X, R3_Y, R4_X, R4_Y, R5_X, R5_Y, R6_X, R6_Y,
                          R7_X, R7_Y,
                          R8_X, R8_Y, R9_X, R9_Y, R10_X, R10_Y]

        numPoints = len(squareGoal)
        for j in range(0, numPoints, 2):
            x = squareGoal[j]
            y = squareGoal[j + 1]
            ox = squareInfo[0]
            oy = squareInfo[1]

            qx, qy =self.rotate_around_point(x, y, ox, oy, squareInfo[4])

            squareGoal[j] = qx
            squareGoal[j + 1] = qy

        return squareGoal

    # User chooses to create a triangle with the robots
    def triangle(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        triangleInfo = self.userInformation(shape, x_ref,y_ref,side_length,num_rob,orientation)

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

    # User chooses to create a semi-circle with the robots
    def semiCircle(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        semiCirlceInfo = self.userInformation(shape, x_ref,y_ref,side_length,num_rob,orientation)

        semiCircleGoal = np.zeros(int(semiCirlceInfo[3]) * 2)

        if semiCirlceInfo[4] == 0:
            # Semi-circle geometry calculations

            i = 0
            j = 0
            while (i < len(semiCircleGoal)):
                semiCircleGoal[i] = float(semiCirlceInfo[0]) + (
                    (float(semiCirlceInfo[2]) * math.cos((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                semiCircleGoal[i] = float(semiCirlceInfo[1]) + (
                    (float(semiCirlceInfo[2]) * math.sin((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in Y spot
                i += 1  # moves back to x spot
                j += 1

            return semiCircleGoal

        elif semiCirlceInfo[4] == 180:  # down oriented semi-circle
            # Semi-circle geometry calculations

            i = 0
            j = 0
            while (i < len(semiCircleGoal)):
                semiCircleGoal[i] = float(semiCirlceInfo[0]) + (
                    (float(semiCirlceInfo[2]) * math.cos((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                semiCircleGoal[i] = float(semiCirlceInfo[1]) - (
                    (float(semiCirlceInfo[2]) * math.sin((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in Y spot
                i += 1  # moves back to x spot
                j += 1

            return semiCircleGoal

        else:
            # Custom orientation
            i = 0
            j = 0
            while (i < len(semiCircleGoal)):
                semiCircleGoal[i] = float(semiCirlceInfo[0]) + (
                    (float(semiCirlceInfo[2]) * math.cos((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                semiCircleGoal[i] = float(semiCirlceInfo[1]) + (
                    (float(semiCirlceInfo[2]) * math.sin((math.pi * j) / (semiCirlceInfo[3] - 1))))  # Plugs in Y spot
                i += 1  # moves back to x spot
                j += 1

            numPoints = len(semiCircleGoal)
            for j in range(0, numPoints, 2):
                x = semiCircleGoal[j]
                y = semiCircleGoal[j + 1]
                ox = semiCirlceInfo[0]
                oy = semiCirlceInfo[1]

                qx, qy = self.rotate_around_point(x, y, ox, oy, semiCirlceInfo[4])

                semiCircleGoal[j] = qx
                semiCircleGoal[j + 1] = qy

            return semiCircleGoal

    # User chooses to create a clump with the robots
    def clump(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        clumpInfo = self.userInformation(shape, x_ref,y_ref,side_length,num_rob,orientation)

        clumpGoal = np.zeros(int(clumpInfo[3]) * 2)

        feature = input("How would you like the orientation of the clump: ").lower()

        if feature == "angular":
            # Random geometry calculations
            i = 0

            while (i < len(clumpGoal)):

                option = randint(0, 3)

                if option == 0:
                    # random number
                    num = random() + randint(1, 2)
                    num2 = random() + randint(1, 2)

                elif option == 1:
                    # random number
                    num = -(random() + randint(1, 2))
                    num2 = random() + randint(1, 2)

                elif option == 2:
                    # random number
                    num = random() + randint(1, 2)
                    num2 = -(random() + randint(1, 2))

                else:
                    # random number
                    num = -(random() + randint(1, 2))
                    num2 = -(random() + randint(1, 2))

                clumpGoal[i] = (float(clumpInfo[0]) + float(clumpInfo[2]) * num) / num2  # Plugs in x spot
                i += 1  # Moved to y spot

                option = randint(0, 3)

                if option == 0:
                    # random number
                    num = random() + randint(1, 2)
                    num2 = random() + randint(1, 2)

                elif option == 1:
                    # random number
                    num = -(random() + randint(1, 2))
                    num2 = random() + randint(1, 2)

                elif option == 2:
                    # random number
                    num = random() + randint(1, 2)
                    num2 = -(random() + randint(1, 2))

                else:
                    # random number
                    num = -(random() + randint(1, 2))
                    num2 = -(random() + randint(1, 2))

                # Calculates new y spot
                clumpGoal[i] = (float(clumpInfo[1]) + float(clumpInfo[2]) * num) / num2  # Plugs in Y spot
                i += 1  # moves back to x spot

        # More Rounded Feature
        else:
            # Random Geometry Calculations
            i = 0
            j = 1

            # random number
            num = random() + randint(1, 2)
            num2 = random() + randint(1, 2)

            while (i < len(clumpGoal)):
                clumpGoal[i] = float(clumpInfo[0]) + (((float(clumpInfo[2]) * math.cos(((2 * math.pi) * j) / clumpInfo[3]))) / num) + num2  # Plugs in x spot
                i += 1  # Moved to y spot

                # Calculates new y spot
                clumpGoal[i] = float(clumpInfo[1]) + (((float(clumpInfo[2]) * math.sin(((2 * math.pi) * j) / clumpInfo[3]))) / num) + num2  # Plugs in Y spot
                i += 1  # moves back to x spot
                j += 1

        numPoints = len(clumpGoal)
        for j in range(0, numPoints, 2):
            x = clumpGoal[j]
            y = clumpGoal[j + 1]
            ox = clumpInfo[0]
            oy = clumpInfo[1]

            qx, qy = self.rotate_around_point(x, y, ox, oy, clumpInfo[4])

            clumpGoal[j] = qx
            clumpGoal[j + 1] = qy

        return clumpGoal

    # User chooses to create a circle with the robots
    def circle(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        circleInfo = self.userInformation(shape, x_ref,y_ref,side_length,num_rob,orientation)

        circleGoal = np.zeros(int(circleInfo[3]) * 2)

        i = 0
        j = 1
        while (i < len(circleGoal)):
            circleGoal[i] = float(circleInfo[0]) + (
                (float(circleInfo[2]) * math.cos(((2 * math.pi) * j) / circleInfo[3])))  # Plugs in x spot
            i += 1  # Moved to y spot

            # Calculates new y spot
            circleGoal[i] = float(circleInfo[1]) + (
                (float(circleInfo[2]) * math.sin(((2 * math.pi) * j) / circleInfo[3])))  # Plugs in Y spot
            i += 1  # moves back to x spot
            j += 1

        numPoints = len(circleGoal)
        for j in range(0, numPoints, 2):
            x = circleGoal[j]
            y = circleGoal[j + 1]
            ox = circleInfo[0]
            oy = circleInfo[1]

            qx, qy = self.rotate_around_point(x, y, ox, oy, circleInfo[4])

            circleGoal[j] = qx
            circleGoal[j + 1] = qy

        return circleGoal

    # User chooses to create a line with the robots
    def line(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # Retrieves the info required to compute
        lineInfo = self.userInformation(shape, x_ref,y_ref,side_length,num_rob,orientation)

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

    def main(self,shape, x_ref,y_ref,side_length,num_rob,orientation):

        # # # Asks the user what shape they would like tp illustrate from the robots
        # print("1. Square \n2. Triangle \n3. Semi-Circle \n4. Clump \n5. Circle \n6. Line")
        # shape = input("What shape would you like to select: ").lower()


        # Performs the shape which the user asks
        if shape == "square":
            goal = self.square(shape, x_ref,y_ref,side_length,num_rob,orientation)

        elif shape == "triangle":
            goal = self.triangle(shape, x_ref,y_ref,side_length,num_rob,orientation)

        elif shape == "semi-circle":
            goal = self.semiCircle(shape, x_ref,y_ref,side_length,num_rob,orientation)

        elif shape == "clump":
            goal = self.clump(shape, x_ref,y_ref,side_length,num_rob,orientation)

        elif shape == "circle":
            goal = self.circle(shape, x_ref,y_ref,side_length,num_rob,orientation)

        else:
            goal = self.line(shape, x_ref,y_ref,side_length,num_rob,orientation)

        self.goals = goal
        return self.goals

        # # Prints all of the points which the robots should be in
        # print("Here are the final positions of the robots geometry: ")
        # rob = 1 # Robot Number
        # for i in range(0,len(goal),2):
        #     print("Robot X" + str(rob) + ": " + str(goal[i]) + " Robot Y" + str(rob) + ": " + str(goal[i+1]))
        #     rob += 1 # Changes robot number

        # with open('output.csv', 'w', newline='') as csvfile:
        #     outputWriter = csv.writer(csvfile, delimiter = ',')
        #     outputWriter.writerow(["R1x","R1y"])
        #     outputWriter.writerow(goal[0])
        #     outputWriter.writerow(["R2x", "R2y"])
        #     outputWriter.writerow(goal[1])
        #     outputWriter.writerow(["R3x", "R3y"])
        #     outputWriter.writerow(goal[2])
        #     outputWriter.writerow(["R4x", "R4y"])
        #     outputWriter.writerow(goal[3])
        #     outputWriter.writerow(["R5x", "R5y"])
        #     outputWriter.writerow(goal[4])
        #     outputWriter.writerow(["endx", "endy"])

if __name__ == "__main__":
    geom = geometry()
    geom.main()