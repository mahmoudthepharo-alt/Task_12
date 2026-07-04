#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32


class TrafficManager(Node):

    def __init__(self):
        super().__init__('traffic_manager')

        self.positions = {}
        self.priorities = {}
        self.safety_distance = 2.0

        robots = ['robot_1', 'robot_2']

        for robot in robots:

            self.create_subscription(
                Pose2D,
                f'/{robot}/pose',
                lambda msg, name=robot: self.pose_callback(msg, name),
                10
            )

            self.create_subscription(
                Int32,
                f'/{robot}/priority',
                lambda msg, name=robot: self.priority_callback(msg, name),
                10
            )

        self.get_logger().info("Traffic Manager Started")

    def pose_callback(self, msg, robot):

        self.positions[robot] = (msg.x, msg.y)
        self.check_traffic()

    def priority_callback(self, msg, robot):

        self.priorities[robot] = msg.data

    def check_traffic(self):

        if len(self.positions) < 2 or len(self.priorities) < 2:
            return

        x1, y1 = self.positions['robot_1']
        x2, y2 = self.positions['robot_2']

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        p1 = self.priorities['robot_1']
        p2 = self.priorities['robot_2']

        self.get_logger().info(f"Distance = {distance:.2f} m")

        if distance >= self.safety_distance:
            self.get_logger().info("[CLEAR] Safe Distance Maintained")
            return

        if p1 >= p2:
            self.get_logger().warn("[DANGER] Robot 2 must YIELD to Robot 1!")

        elif p2 > p1:
            self.get_logger().warn("[DANGER] Robot 1 must YIELD to Robot 2!")

        else:
            self.get_logger().info("[CLEAR] Both Robots Have Same Priority")


def main(args=None):
    rclpy.init(args=args)

    node = TrafficManager()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()