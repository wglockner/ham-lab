# Hybrid Testbed for Image Segmentation Control

This repository contains a hybrid testbed project for image segmentation control, utilizing various tools and techniques for open loop control and ROS implementation.

## Project Structure

- **Hybrid-Testbed**
  - **Open Loop Control**
    - Contains scripts and resources for open loop control implementation.
  - **ROS Implementation**
    - Contains scripts and resources for ROS (Robot Operating System) implementation.

## Features

- **Live Video Feed**: Start and stop live video feed from a Basler camera.
- **Display Options**: Choose between different image segmentation techniques including lines, blobs, color, edges, contours, shapes, or both lines and blobs.
- **Graphical Display**: Real-time plots of line and blob detection counts.
- **Save Data**: Save the processed image data (timestamp, line count, blob count) to a CSV file.

## Requirements

- Python 3.x
- `tkinter`
- `pypylon`
- `opencv-python`
- `numpy`
- `matplotlib`
- `Pillow`
- ROS (for ROS implementation)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/hybrid-testbed.git
    cd hybrid-testbed
    ```

2. **Install dependencies:**
    ```bash
    pip install tkinter pypylon opencv-python numpy matplotlib Pillow
    ```

3. **ROS Installation:**
    Follow the official ROS installation guide for your operating system. [ROS Installation Guide](http://wiki.ros.org/ROS/Installation)

## Usage

### Open Loop Control

1. **Navigate to the Open Loop Control directory:**
    ```bash
    cd Hybrid-Testbed/Open Loop Control
    ```

2. **Run the application:**
    ```bash
    python open_loop_control.py
    ```

3. **Control the application through the GUI:**
    - Click "Start Video Feed" to begin the live video feed.
    - Select the desired image segmentation technique from the display options.
    - Click "Stop Video Feed" to stop the live video feed.
    - Click "Save Data" to open a file dialog and choose where to save the CSV file with the processed image data.

### ROS Implementation

1. **Navigate to the ROS Implementation directory:**
    ```bash
    cd Hybrid-Testbed/ROS Implementation
    ```

2. **Follow the instructions in the README within the ROS Implementation directory to set up and run the ROS nodes.**

## GUI Elements

- **Video Feed Label**: Displays the live video feed from the camera.
- **Start/Stop Video Buttons**: Control the live video feed.
- **Display Options**: Radio buttons to choose the type of image segmentation.
- **Save Data Button**: Opens a file dialog to save the CSV file.
- **Real-time Plots**: Displays plots of line and blob detection counts.

## Code Overview

- **initialize_gui()**: Sets up the GUI elements.
- **setup_camera()**: Configures the Basler camera.
- **start_video_feed() / stop_video_feed()**: Starts and stops the live video feed.
- **update_camera_feed()**: Continuously retrieves images from the camera.
- **process_image()**: Processes each frame from the camera according to the selected display option.
- **save_data()**: Saves the collected image data to a CSV file.
- **detect_lines() / detect_blobs() / color_segmentation() / edge_detection() / contour_detection() / shape_detection()**: Image segmentation methods.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [pypylon](https://github.com/basler/pypylon) - Python bindings for the pylon Camera Software Suite.
- [OpenCV](https://opencv.org/) - Open Source Computer Vision Library.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python's de-facto standard GUI package.
- [matplotlib](https://matplotlib.org/) - Comprehensive library for creating static, animated, and interactive visualizations in Python.
- [Pillow](https://python-pillow.org/) - Python Imaging Library (PIL) fork.
- [ROS](http://www.ros.org/) - Robot Operating System.
