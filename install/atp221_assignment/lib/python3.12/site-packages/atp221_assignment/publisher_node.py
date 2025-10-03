#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class PublisherNode(Node):
    def __init__(self):
        super().__init__('vladislav_publisher')
        
        # Создаем издателя для топика 'atp221_topic'
        self.publisher_ = self.create_publisher(String, 'atp221_topic', 10)
        
        # Таймер для отправки сообщений каждые 2 секунды
        self.timer = self.create_timer(2.0, self.timer_callback)
        
        # Счетчик сообщений
        self.counter = 0
        
        self.get_logger().info('🚀 Издатель Vladislav запущен и готов отправлять сообщения!')
        self.get_logger().info('📡 Публикация в топик: /atp221_topic')
        self.get_logger().info('⏰ Период отправки: 2 секунды')

    def timer_callback(self):
        # Создаем сообщение
        msg = String()
        msg.data = f"Vladislav Mikhaylyuck ATP-221: Сообщение #{self.counter} - Время: {time.strftime('%H:%M:%S')}"
        
        # Публикуем сообщение
        self.publisher_.publish(msg)
        
        # Логируем отправку
        self.get_logger().info(f'📤 ОТПРАВЛЕНО: "{msg.data}"')
        
        # Увеличиваем счетчик
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    
    node = PublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('🛑 Издатель остановлен по команде пользователя')
    except Exception as e:
        node.get_logger().error(f'❌ Ошибка в издателе: {e}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
