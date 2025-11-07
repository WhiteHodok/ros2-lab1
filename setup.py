from setuptools import setup
import os
from glob import glob

package_name = 'lab_turtlesim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='whitehodok',
    maintainer_email='balanaraus@gmail.com',
    description='Turtlesim lab package for ROS 2 learning',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'square_publisher = lab_turtlesim.square_publisher:main',
            'shape_publisher = lab_turtlesim.shape_publisher:main',
        ],
    },
)