#!/usr/bin/env python3
"""
Author: Walter W Glockner
Date: 06/07/24

Real-time Point Cloud Visualization GUI

This script creates a PyQt-based GUI that subscribes to a PointCloud2 topic
from a ROS node and visualizes the point cloud data in real-time using Open3D.

Usage:
rosrun wwg_scan pointcloud_gui.py _pointcloud_topic:=/camera/pointcloud
"""

import sys
import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import numpy as np
import yaml
import open3d as o3d
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QApplication

class PointCloudVisualizer(QWidget):
    def __init__(self):
        super(PointCloudVisualizer, self).__init__()
        
        self.setWindowTitle('Real-time Point Cloud Visualization')
        self.setGeometry(50, 50, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.start_button = QPushButton('Start Visualization')
        self.start_button.clicked.connect(self.start_visualization)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Visualization')
        self.stop_button.clicked.connect(self.stop_visualization)
        self.layout.addWidget(self.stop_button)

        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(window_name='Open3D Point Cloud Viewer', width=800, height=600)
        
        self.pcd = o3d.geometry.PointCloud()
        self.is_running = False

    def start_visualization(self):
        self.is_running = True
        rospy.init_node('pointcloud_visualizer', anonymous=True)
        rospy.Subscriber('/camera/pointcloud', PointCloud2, self.callback)
        rospy.loginfo("Point cloud visualization started")
        self.vis.run()

    def stop_visualization(self):
        self.is_running = False
        rospy.loginfo("Point cloud visualization stopped")
        self.vis.destroy_window()

    def callback(self, msg):
        if not self.is_running:
            return
        
        rospy.loginfo("Received point cloud data")
        points_list = []

        for point in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
            points_list.append([point[0], point[1], point[2]])

        if points_list:
            points_array = np.array(points_list, dtype=np.float32)
            self.pcd.points = o3d.utility.Vector3dVector(points_array)
            self.vis.add_geometry(self.pcd)
            self.vis.update_geometry(self.pcd)
            self.vis.poll_events()
            self.vis.update_renderer()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = PointCloudVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
