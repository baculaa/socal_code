import numpy as np
import matplotlib.pyplot as plt
import math
class GoalTest:
    def __init__(self):
        self.x_offset1 = 0
        self.y_offset1 = 0.5
        self.x_offset2 = 0
        self.y_offset2 = 0
        self.x_offset3 = 0
        self.y_offset3 = -0.5
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
        y1_1 = self.y_offset1
        x2_1 = np.sqrt(side_length ** 2 - self.y_offset1 ** 2)
        y2_1 = 0
        x3_1 = 0
        y3_1 = self.y_offset3

        x1_2 = np.sqrt(side_length ** 2 - self.y_offset1 ** 2)
        y1_2 = self.y_offset1
        x2_2 = 0
        y2_2 = 0
        x3_2 = np.sqrt(side_length ** 2 - self.y_offset1 ** 2)
        y3_2 = self.y_offset3

        triangleGoal_base = [x1_1, y1_1, x2_1, y2_1, x3_1, y3_1]
        triangleGoal_base2 = [x1_2, y1_2, x2_2, y2_2, x3_2, y3_2]
        if shape == 2:
            goal_rot1 = self.rotate_around_point(triangleGoal_base[0], triangleGoal_base[1], 0, 0, orientation)
            goal_rot2 = self.rotate_around_point(triangleGoal_base[2], triangleGoal_base[3], 0, 0, orientation)
            goal_rot3 = self.rotate_around_point(triangleGoal_base[4], triangleGoal_base[5], 0, 0, orientation)
        elif shape == 1:
            goal_rot1 = self.rotate_around_point(triangleGoal_base2[0], triangleGoal_base2[1], 0, 0, orientation)
            goal_rot2 = self.rotate_around_point(triangleGoal_base2[2], triangleGoal_base2[3], 0, 0, orientation)
            goal_rot3 = self.rotate_around_point(triangleGoal_base2[4], triangleGoal_base2[5], 0, 0, orientation)

        triangleGoal = [goal_rot1[0], goal_rot1[1], goal_rot2[0], goal_rot2[1], goal_rot3[0], goal_rot3[1]]


        return triangleGoal


    def line(self, shape, x_ref, y_ref, side_length, num_rob, orientation):
        y1 = side_length / 3
        x1 = 0
        x2 = 0
        y2 = 0
        y3 = -side_length / 3
        x3 = 0

        lineGoal_base = [x1, y1, x2, y2, x3, y3]

        if shape == 4:
            goal_rot1 = self.rotate_around_point(lineGoal_base[0], lineGoal_base[1], 0, 0, orientation)
            goal_rot2 = self.rotate_around_point(lineGoal_base[2], lineGoal_base[3], 0, 0, orientation)
            goal_rot3 = self.rotate_around_point(lineGoal_base[4], lineGoal_base[5], 0, 0, orientation)

        elif shape == 3:
            goal_rot1 = self.rotate_around_point(lineGoal_base[0], lineGoal_base[1], 0, 0, 90 + orientation)
            goal_rot2 = self.rotate_around_point(lineGoal_base[2], lineGoal_base[3], 0, 0, 90 + orientation)
            goal_rot3 = self.rotate_around_point(lineGoal_base[4], lineGoal_base[5], 0, 0, 90 + orientation)

        lineGoal = [goal_rot1[0], goal_rot1[1], goal_rot2[0], goal_rot2[1], goal_rot3[0], goal_rot3[1]]

        return lineGoal

if __name__ == '__main__':
    tester = GoalTest()
    x_ref = 2
    y_ref = 2
    orientation = math.degrees(math.atan2(y_ref, x_ref))
    print(orientation)
    goals = tester.line(4, x_ref,y_ref,3,3,orientation)

    # Initialize the figure
    fig, ax = plt.subplots(figsize=(5, 5))
    # Set the axis limits
    ax.set(xlim=(-5, 5), ylim=(-5, 5))
    print(goals)
    x = [goals[0],goals[2],goals[4]]
    y = [goals[1], goals[3], goals[5]]
    plt.plot(x,y,'o')
    plt.plot(x_ref, y_ref, 'v')
    plt.show()

