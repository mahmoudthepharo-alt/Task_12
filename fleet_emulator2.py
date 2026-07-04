#!/usr/bin/env python3

import random
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32


class FleetEmulator(Node):

    def __init__(self):
        super().__init__('fleet_emulator')

        self.robots = {
            "robot_1": 1,
            "robot_2": 5
        }

        self.pose_publishers = {}
        self.priority_publishers = {}

        for robot_name in self.robots:
            self.pose_publishers[robot_name] = self.create_publisher(
                Pose2D,
                f'/{robot_name}/pose',
                10
            )
            
            self.priority_publishers[robot_name] = self.create_publisher(
                Int32,
                f'/{robot_name}/priority',
                10
            )

        self.timer = self.create_timer(0.1, self.publish_robot_data)

        self.get_logger().info("Fleet Emulator Started")

    def publish_robot_data(self):

        for robot_name, priority in self.robots.items():

            pose = Pose2D()
            pose.x = random.uniform(0.0, 10.0)
            pose.y = random.uniform(0.0, 10.0)
            pose.theta = 0.0

            priority_msg = Int32()
            priority_msg.data = priority

            self.pose_publishers[robot_name].publish(pose)
            self.priority_publishers[robot_name].publish(priority_msg)

            self.get_logger().info(
                f'{robot_name}: '
                f'x={pose.x:.2f}, '
                f'y={pose.y:.2f}, '
                f'priority={priority_msg.data}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = FleetEmulator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()