#!/usr/bin/env python3
"""
Узел для рисования прямоугольника и треугольника с помощью черепахи turtlesim.
Управление по времени (открытый контур).
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class ShapePublisher(Node):
    """Узел, управляющий черепахой для рисования фигур по таймеру."""

    # Константы
    LINEAR_SPEED = 1.0  # м/с
    ANGULAR_SPEED_90 = math.pi / 2  # рад/с (90 градусов/сек)
    ANGULAR_SPEED_120 = 2.0 * math.pi / 3.0  # рад/с (120 градусов/сек)

    def __init__(self):
        super().__init__('shape_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer_period = 0.1  # 100 ms
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Параметры фигуры (можно менять через параметры ROS)
        self.declare_parameter('shape', 'rectangle')  # 'rectangle' или 'triangle'
        self.declare_parameter('side_length', 2.0)  # Длина стороны
        self.declare_parameter('auto_restart', True)  # Автоматический перезапуск

        # Переменные состояния
        self.reset_state()

        self.get_logger().info('ShapePublisher node started')
        self.get_logger().info('Available shapes: rectangle, triangle')
        self.get_logger().info('Usage: ros2 run lab_turtlesim shape_publisher --ros-args -p shape:=triangle -p side_length:=3.0')

    def reset_state(self):
        """Сброс состояния узла."""
        self.state = 'forward'
        self.step_count = 0
        self.state_start_time = self.get_clock().now()
        self.figure_completed = False

    def timer_callback(self):
        """Коллбэк таймера: публикует команды скорости."""
        try:
            if self.publisher_.get_subscription_count() == 0:
                self.get_logger().warn('No subscribers on /turtle1/cmd_vel - is turtlesim running?')
                return

            shape = self.get_parameter('shape').value
            side_length = self.get_parameter('side_length').value
            auto_restart = self.get_parameter('auto_restart').value

            # Автоматический перезапуск после завершения фигуры
            if self.figure_completed and auto_restart:
                self.get_logger().info('Auto-restarting figure drawing...')
                self.reset_state()

            msg = Twist()
            current_time = self.get_clock().now()
            state_elapsed_time = (current_time - self.state_start_time).nanoseconds / 1e9

            if shape == 'rectangle':
                self.handle_rectangle(msg, state_elapsed_time, side_length)
            elif shape == 'triangle':
                self.handle_triangle(msg, state_elapsed_time, side_length)
            else:
                self.get_logger().error(f'Unknown shape: {shape}')
                return

            self.publisher_.publish(msg)

        except Exception as e:
            self.get_logger().error(f'Error in timer_callback: {str(e)}')

    def handle_rectangle(self, msg, elapsed_time, side_length):
        """Логика рисования прямоугольника."""
        forward_time = side_length / self.LINEAR_SPEED
        turn_time = 1.0  # Поворот на 90°

        if self.figure_completed:
            return

        if self.state == 'forward':
            msg.linear.x = self.LINEAR_SPEED
            msg.angular.z = 0.0
            if elapsed_time >= forward_time:
                self.state = 'turn'
                self.state_start_time = self.get_clock().now()
                self.step_count += 1
                self.get_logger().info(f'Rectangle: turning at corner {self.step_count}/4')

        elif self.state == 'turn':
            msg.linear.x = 0.0
            msg.angular.z = self.ANGULAR_SPEED_90
            if elapsed_time >= turn_time:
                self.state = 'forward'
                self.state_start_time = self.get_clock().now()
                if self.step_count >= 4:  # Прямоугольник завершён (4 стороны)
                    self.get_logger().info('Rectangle completed!')
                    self.figure_completed = True

    def handle_triangle(self, msg, elapsed_time, side_length):
        """Логика рисования равностороннего треугольника."""
        forward_time = side_length / self.LINEAR_SPEED
        turn_time = 1.0  # Поворот на 120°

        if self.figure_completed:
            return

        if self.state == 'forward':
            msg.linear.x = self.LINEAR_SPEED
            msg.angular.z = 0.0
            if elapsed_time >= forward_time:
                self.state = 'turn'
                self.state_start_time = self.get_clock().now()
                self.step_count += 1
                self.get_logger().info(f'Triangle: turning at corner {self.step_count}/3')

        elif self.state == 'turn':
            msg.linear.x = 0.0
            msg.angular.z = self.ANGULAR_SPEED_120
            if elapsed_time >= turn_time:
                self.state = 'forward'
                self.state_start_time = self.get_clock().now()
                if self.step_count >= 3:  # Треугольник завершён (3 стороны)
                    self.get_logger().info('Triangle completed!')
                    self.figure_completed = True

def main(args=None):
    rclpy.init(args=args)
    shape_publisher = ShapePublisher()
    try:
        rclpy.spin(shape_publisher)
    except KeyboardInterrupt:
        shape_publisher.get_logger().info('Node stopped by user')
    finally:
        shape_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()