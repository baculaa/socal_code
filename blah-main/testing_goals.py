import numpy as np

class GoalTest:
    def __init__(self):
        pass
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
    tester = GoalTest()
    goals = tester.triangle(1, 0,0,3,3,0)
    print(goals)
