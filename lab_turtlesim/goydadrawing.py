#!/usr/bin/env python3
"""
Задание 2: Узел для рисования квадрата с помощью черепахи turtlesim.
Управление по времени (открытый контур).
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class GoydaDrawing(Node):
    """Узел для задания 2 - рисование квадрата."""

    def __init__(self):
        super().__init__('goyda_drawing')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Параметры движения для квадрата
        self.linear_speed = 1.0  # м/с
        self.angular_speed = math.pi / 2  # рад/с (90 градусов/сек)
        self.side_duration = 2.0  # время движения вперед (сек)
        self.turn_duration = 1.0  # время поворота на 90° (сек)
        
        # Состояния управления
        self.state = 'forward'
        self.state_start_time = self.get_clock().now()
        self.sides_completed = 0

        self.get_logger().info('GoydaDrawing node started - рисование квадрата')
        self.get_logger().info('Состояния: forward -> turn -> forward -> ...')

    def timer_callback(self):
        """Коллбэк таймера: публикует команды скорости."""
        try:
            # Проверяем, есть ли подписчики (запущен ли turtlesim)
            if self.publisher_.get_subscription_count() == 0:
                self.get_logger().warn('Нет подписчиков на /turtle1/cmd_vel - запустите turtlesim_node')
                return

            msg = Twist()
            current_time = self.get_clock().now()
            elapsed_time = (current_time - self.state_start_time).nanoseconds / 1e9

            if self.state == 'forward':
                # Движение вперед по стороне квадрата
                msg.linear.x = self.linear_speed
                msg.angular.z = 0.0
                
                if elapsed_time >= self.side_duration:
                    self.state = 'turn'
                    self.state_start_time = self.get_clock().now()
                    self.get_logger().info(f'Поворот на 90 градусов... Сторона {self.sides_completed + 1} завершена')

            elif self.state == 'turn':
                # Поворот на 90 градусов
                msg.linear.x = 0.0
                msg.angular.z = self.angular_speed
                
                if elapsed_time >= self.turn_duration:
                    self.state = 'forward'
                    self.state_start_time = self.get_clock().now()
                    self.sides_completed += 1
                    
                    if self.sides_completed >= 4:
                        self.get_logger().info('🎉 Квадрат завершен! Перезапуск...')
                        self.sides_completed = 0
                    else:
                        self.get_logger().info(f'Движение вперед по стороне {self.sides_completed + 1}')

            self.publisher_.publish(msg)
            
        except Exception as e:
            self.get_logger().error(f'Ошибка в timer_callback: {str(e)}')

def main(args=None):
    """Основная функция для запуска узла."""
    rclpy.init(args=args)
    node = GoydaDrawing()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Узел остановлен пользователем')
    except Exception as e:
        node.get_logger().error(f'Неожиданная ошибка: {str(e)}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
