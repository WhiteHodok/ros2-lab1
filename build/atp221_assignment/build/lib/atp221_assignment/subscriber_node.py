#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('vladislav_subscriber')
        
        # Создаем подписчика на топик 'atp221_topic'
        self.subscription = self.create_subscription(
            String,
            'atp221_topic',
            self.listener_callback,
            10)
        
        self.get_logger().info('👂 Подписчик Vladislav запущен и ожидает сообщения...')
        self.get_logger().info('📡 Подписка на топик: /atp221_topic')

    def listener_callback(self, msg):
        # Выводим полученное сообщение
        self.get_logger().info(f'📥 ПОЛУЧЕНО: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    
    node = SubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('🛑 Подписчик остановлен по команде пользователя')
    except Exception as e:
        node.get_logger().error(f'❌ Ошибка в подписчике: {e}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
