"""
调试版launch文件：用于排查可视化问题
包含所有必要的诊断输出
"""
import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rviz_config_file = get_package_share_directory('ocs2_legged_robot_ros') + "/rviz/legged_robot.rviz"
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='rviz',
            default_value='true'
        ),
        launch.actions.DeclareLaunchArgument(
            name='description_name',
            default_value='legged_robot_description'
        ),
        launch.actions.DeclareLaunchArgument(
            name='multiplot',
            default_value='false'
        ),
        launch.actions.DeclareLaunchArgument(
            name='terminal_prefix',
            default_value=''
        ),
        launch.actions.DeclareLaunchArgument(
            name='taskFile',
            default_value=get_package_share_directory(
                'ocs2_legged_robot') + '/config/mpc/task.info'
        ),
        launch.actions.DeclareLaunchArgument(
            name='referenceFile',
            default_value=get_package_share_directory(
                'ocs2_legged_robot') + '/config/command/reference.info'
        ),
        launch.actions.DeclareLaunchArgument(
            name='urdfFile',
            default_value=get_package_share_directory(
                'ocs2_robotic_assets') + '/resources/anymal_c/urdf/anymal.urdf'
        ),
        launch.actions.DeclareLaunchArgument(
            name='gaitCommandFile',
            default_value=get_package_share_directory(
                'ocs2_legged_robot') + '/config/command/gait.info'
        ),
        # Robot state publisher - 发布joint_states和TF
        launch_ros.actions.Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            arguments=[launch.substitutions.LaunchConfiguration("urdfFile")],
            emulate_tty=True,
        ),
        # RViz visualization
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=["-d", rviz_config_file],
            condition=launch.conditions.IfCondition(
                launch.substitutions.LaunchConfiguration('rviz')),
            emulate_tty=True,
        ),
        # MPC 优化器
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_sqp_mpc',
            name='legged_robot_sqp_mpc',
            output='screen',
            prefix= "",
            emulate_tty=True,
            parameters=[
                {
                    'multiplot': launch.substitutions.LaunchConfiguration('multiplot')
                },
                {
                    'taskFile': launch.substitutions.LaunchConfiguration('taskFile')
                },
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                },
                {
                    'urdfFile': launch.substitutions.LaunchConfiguration('urdfFile')
                }
            ]
        ),
        # 跟踪并可视化仿真的机器人行走
        # 这个节点很关键，它发布visualization markers
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_dummy',
            name='legged_robot_dummy',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            emulate_tty=True,
            parameters=[
                {
                    'taskFile': launch.substitutions.LaunchConfiguration('taskFile')
                },
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                },
                {
                    'urdfFile': launch.substitutions.LaunchConfiguration('urdfFile')
                }
            ],
            # 增加日志级别用于调试
            env={'ROS_LOG_DIR': '/tmp/ros2_logs'}
        ),
        # 目标位置发布器
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_target',
            name='legged_robot_target',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            emulate_tty=True,
            parameters=[
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                }
            ]
        ),
        # 步态命令发布器
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_gait_command',
            name='legged_robot_gait_command',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            emulate_tty=True,
            parameters=[
                {
                    'gaitCommandFile': launch.substitutions.LaunchConfiguration('gaitCommandFile')
                }
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
