from setuptools import setup

package_name = 'atp221_assignment'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vladislav',
    maintainer_email='balanaraus@gmail.com',
    description='ATP-221 assignment package for Vladislav Mikhaylyuck',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_node = atp221_assignment.publisher_node:main',
            'subscriber_node = atp221_assignment.subscriber_node:main',
        ],
    },
)
