cmake_minimum_required(VERSION 3.0.2)
project(khi_cx_description)

find_package(catkin REQUIRED COMPONENTS)

catkin_package()

#if (CATKIN_ENABLE_TESTING)
#  find_package(roslaunch REQUIRED)
#  roslaunch_add_file_check(tests/roslaunch_test_cx.xml)
#endif()

install(DIRECTORY config meshes urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
