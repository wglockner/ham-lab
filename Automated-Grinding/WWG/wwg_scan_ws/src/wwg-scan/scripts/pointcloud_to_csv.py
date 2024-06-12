#!/usr/bin/env python3

"""
Author: Walter W Glockner
Date: 06/07/24

PointCloud to CSV Converter Node

This ROS node subscribes to a PointCloud2 topic from a Realsense camera,
converts the point cloud data to CSV format, and saves it to a specified directory.

Parameters:
- ~output_dir (string): The directory where the CSV files will be saved. Default is '/tmp/pointclouds'.

Usage:
rosrun wwg_scan pointcloud_to_csv.py _output_dir:=/path/to/save/csv
"""
import rospy
from sensor_msgs.msg import Image, PointCloud2, PointField
from sensor_msgs import point_cloud2
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import numpy as np

def image_to_pointcloud(cv_image):
    """
    Convert a depth image to a point cloud.
    """
    points = []
    fx = 1.0  # Focal length x (change as per your camera)
    fy = 1.0  # Focal length y (change as per your camera)
    cx = cv_image.shape[1] / 2.0
    cy = cv_image.shape[0] / 2.0

    for u in range(cv_image.shape[0]):
        for v in range(cv_image.shape[1]):
            depth = cv_image[u, v] / 1000.0  # Convert from mm to meters
            if depth > 0:
                x = (v - cx) * depth / fx
                y = (u - cy) * depth / fy
                z = depth
                points.append([x, y, z, 255])  # Assuming intensity is 255 for all points

    return points

def callback(msg, args):
    output_dir, pointcloud_pub = args
    # Callback function to process the received image data
    rospy.loginfo("Received image data")
    
    # Convert ROS Image message to OpenCV image
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "16UC1")  # Assuming depth image is 16-bit
    except CvBridgeError as e:
        rospy.logerr(f"Could not convert image: {e}")
        return
    
    # Get the current timestamp to use in the filename
    timestamp = rospy.Time.now().to_sec()
    filename = os.path.join(output_dir, f'image_{timestamp}.csv')
    
    # Open a CSV file to write the image data
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the pixel data
        for row in cv_image:
            csvwriter.writerow(row)
    
    rospy.loginfo(f"Image data saved to {filename}")
    
    # Convert image to point cloud
    points = image_to_pointcloud(cv_image)
    
    # Create PointCloud2 message
    fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
        PointField('intensity', 12, PointField.UINT8, 1)
    ]
    
    header = msg.header
    pointcloud_msg = point_cloud2.create_cloud(header, fields, points)
    
    # Publish the point cloud message
    pointcloud_pub.publish(pointcloud_msg)
    rospy.loginfo(f"Point cloud data published to {pointcloud_pub.name}")

def main():
    # Initialize the ROS node
    rospy.init_node('image_to_pointcloud', anonymous=True)
    
    # Get the output directory parameter, default is '/tmp/images'
    output_dir = rospy.get_param('~output_dir', '/tmp/images')
    pointcloud_topic = rospy.get_param('~pointcloud_topic', '/camera/pointcloud')
    
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a publisher for the point cloud data
    pointcloud_pub = rospy.Publisher(pointcloud_topic, PointCloud2, queue_size=10)
    
    # Subscribe to the depth image topic
    rospy.Subscriber('/camera/depth/image_raw', Image, callback, (output_dir, pointcloud_pub))
    
    rospy.loginfo("Node initialized, listening for image data and publishing point cloud data...")
    
    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass