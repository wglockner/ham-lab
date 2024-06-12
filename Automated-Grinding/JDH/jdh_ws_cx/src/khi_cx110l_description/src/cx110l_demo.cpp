#include <ros/ros.h>
#include <trajectory_msgs/JointTrajectory.h>

// Inspiried by this demo script on Stack Overflow from William Fradin
// https://stackoverflow.com/questions/44626435/publishing-between-gazebo-and-controller-using-trajectory-msgs

double convert(double degree)
{
    double pi = 3.14159265359;
    return (degree * (pi / 180));
}

int main(int argc, char** argv) {
 ros::init(argc, argv, "state_publisher");
 ros::NodeHandle n;

 ros::Publisher arm_pub = n.advertise<trajectory_msgs::JointTrajectory>("/cx110l_arm_controller/command",1);
 trajectory_msgs::JointTrajectory traj;

 traj.header.stamp = ros::Time::now();
 traj.header.frame_id = "base_link";
 traj.joint_names.resize(6);
 traj.points.resize(6);

 traj.joint_names[0] ="joint1";
 traj.joint_names[1] ="joint2";
 traj.joint_names[2] ="joint3";
 traj.joint_names[3] ="joint4";
 traj.joint_names[4] ="joint5";
 traj.joint_names[5] ="joint6";

 double dt(0.5);

 while (ros::ok()) {

   for(int i=0;i<4;i++){

    double x1 = 2.23;
    double x2 = 0.09;
    double x3 = 1.46;
    double x4 = -3.35;
    double x5 = 1.63;
    double x6 = 4.98;

    trajectory_msgs::JointTrajectoryPoint points_n;
    points_n.positions.push_back(x1);
    points_n.positions.push_back(x2);
    points_n.positions.push_back(x3);
    points_n.positions.push_back(x4);
    points_n.positions.push_back(x5);
    points_n.positions.push_back(x6);
    traj.points.push_back(points_n);

     traj.points[i].time_from_start = ros::Duration(dt*i);

   }

   arm_pub.publish(traj);
   ros::spinOnce();
 }

 return 0;
}
