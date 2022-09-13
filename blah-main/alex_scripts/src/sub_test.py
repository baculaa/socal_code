#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

pub = rospy.Publisher('test', MoveBaseGoal, queue_size=10)
pub2 = rospy.Publisher('plswork',String,queue_size=10)
# pu++b2 = rospy.Publisher('pioneer1/move_base/goal', MoveBaseGoal, queue_size=10)

def callback(data):

    pub2.publish('check pre goal')
    client = actionlib.SimpleActionClient('/move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = '/map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0
    goal.target_pose.pose.position.y = 0
    goal.target_pose.pose.position.z = 0

    goal.target_pose.pose.orientation.x = 0
    goal.target_pose.pose.orientation.y = 0
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1

    pub2.publish("check post goal pre if")

    if data.data=="to":
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 2.5
        goal.target_pose.pose.position.y = -0.5
        goal.target_pose.pose.position.z = 0

        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1

        pub2.publish('check in to')
        pub.publish(goal)

    elif data.data=="away":
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = -1.0
        goal.target_pose.pose.position.y = 0.6
        goal.target_pose.pose.position.z = 0

        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1

        pub2.publish('check in away')
        pub.publish(goal)
    else:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0

        goal.target_pose.pose.orientation.x = 0
        goal.target_pose.pose.orientation.y = 0
        goal.target_pose.pose.orientation.z = 0
        goal.target_pose.pose.orientation.w = 1

        pub2.publish('check in else')
        pub.publish(goal)

    pub.publish(goal)
    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.loginfo("Action sever not avail, cry")
    else:
        return client.get_result()

    pub2.publish('check passed goal')


#
# def movebase_client():
#     client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
#     client.wait_for_server()
#
#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = '/pioneer1/map'
#     goal.target_pose.header.stamp = rospy.Time.now()
#     goal.target_pose.pose.position.x = 0.4
#     goal.target_pose.pose.position.y = 0
#     goal.target_pose.pose.position.z = 0
#
#     goal.target_pose.pose.orientation.x = 0
#     goal.target_pose.pose.orientation.y = 0
#     goal.target_pose.pose.orientation.z = 0
#     goal.target_pose.pose.orientation.w = 1
#
#     client.send_goal(goal)
#     wait = client.wait_for_result()
#
#     if not wait:
#         rospy.loginfo("Action sever not avail, cry")
#     else:
#         return client.get_result()


def listener():
    rospy.init_node('sub_test', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()

# def talker2(self):
#
#     rate = rospy.Rate(10) # 10hz
#     #while not rospy.is_shutdown():
#     pub.publish("hello world")
#     pub.publish(self.published_data)

if __name__ == '__main__':

    listener()


    # rospy.spin()
