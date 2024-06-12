# Install script for directory: /home/rosindustrial/jdh_ws_cx/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/rosindustrial/jdh_ws_cx/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE PROGRAM FILES "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE PROGRAM FILES "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/setup.bash;/home/rosindustrial/jdh_ws_cx/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE FILE FILES
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/setup.bash"
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/setup.sh;/home/rosindustrial/jdh_ws_cx/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE FILE FILES
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/setup.sh"
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/setup.zsh;/home/rosindustrial/jdh_ws_cx/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE FILE FILES
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/setup.zsh"
    "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/rosindustrial/jdh_ws_cx/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/rosindustrial/jdh_ws_cx/install" TYPE FILE FILES "/home/rosindustrial/jdh_ws_cx/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/rosindustrial/jdh_ws_cx/build/gtest/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_cx110l_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_cx_description/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_cx165l_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_robot/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_robot_msgs/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_duaro_description/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_duaro_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_robot_bringup/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs_description/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs007l_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs007n_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs013n_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs020n_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs025n_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs080n_moveit_config/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_cx_gazebo/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_duaro_gazebo/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_robot_control/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs_gazebo/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_cx110l_description/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_duaro_ikfast_plugin/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_rs_ikfast_plugin/cmake_install.cmake")
  include("/home/rosindustrial/jdh_ws_cx/build/khi_robot_test/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/rosindustrial/jdh_ws_cx/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
