;; Auto-generated. Do not edit!


(when (boundp 'khi_robot_msgs::KhiRobotCmd)
  (if (not (find-package "KHI_ROBOT_MSGS"))
    (make-package "KHI_ROBOT_MSGS"))
  (shadow 'KhiRobotCmd (find-package "KHI_ROBOT_MSGS")))
(unless (find-package "KHI_ROBOT_MSGS::KHIROBOTCMD")
  (make-package "KHI_ROBOT_MSGS::KHIROBOTCMD"))
(unless (find-package "KHI_ROBOT_MSGS::KHIROBOTCMDREQUEST")
  (make-package "KHI_ROBOT_MSGS::KHIROBOTCMDREQUEST"))
(unless (find-package "KHI_ROBOT_MSGS::KHIROBOTCMDRESPONSE")
  (make-package "KHI_ROBOT_MSGS::KHIROBOTCMDRESPONSE"))

(in-package "ROS")





(defclass khi_robot_msgs::KhiRobotCmdRequest
  :super ros::object
  :slots (_type _cmd ))

(defmethod khi_robot_msgs::KhiRobotCmdRequest
  (:init
   (&key
    ((:type __type) "")
    ((:cmd __cmd) "")
    )
   (send-super :init)
   (setq _type (string __type))
   (setq _cmd (string __cmd))
   self)
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:serialization-length
   ()
   (+
    ;; string _type
    4 (length _type)
    ;; string _cmd
    4 (length _cmd)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _type
       (write-long (length _type) s) (princ _type s)
     ;; string _cmd
       (write-long (length _cmd) s) (princ _cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _cmd
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _cmd (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass khi_robot_msgs::KhiRobotCmdResponse
  :super ros::object
  :slots (_driver_ret _as_ret _cmd_ret ))

(defmethod khi_robot_msgs::KhiRobotCmdResponse
  (:init
   (&key
    ((:driver_ret __driver_ret) 0)
    ((:as_ret __as_ret) 0)
    ((:cmd_ret __cmd_ret) "")
    )
   (send-super :init)
   (setq _driver_ret (round __driver_ret))
   (setq _as_ret (round __as_ret))
   (setq _cmd_ret (string __cmd_ret))
   self)
  (:driver_ret
   (&optional __driver_ret)
   (if __driver_ret (setq _driver_ret __driver_ret)) _driver_ret)
  (:as_ret
   (&optional __as_ret)
   (if __as_ret (setq _as_ret __as_ret)) _as_ret)
  (:cmd_ret
   (&optional __cmd_ret)
   (if __cmd_ret (setq _cmd_ret __cmd_ret)) _cmd_ret)
  (:serialization-length
   ()
   (+
    ;; int32 _driver_ret
    4
    ;; int32 _as_ret
    4
    ;; string _cmd_ret
    4 (length _cmd_ret)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _driver_ret
       (write-long _driver_ret s)
     ;; int32 _as_ret
       (write-long _as_ret s)
     ;; string _cmd_ret
       (write-long (length _cmd_ret) s) (princ _cmd_ret s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _driver_ret
     (setq _driver_ret (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _as_ret
     (setq _as_ret (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _cmd_ret
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _cmd_ret (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass khi_robot_msgs::KhiRobotCmd
  :super ros::object
  :slots ())

(setf (get khi_robot_msgs::KhiRobotCmd :md5sum-) "f15db04cfafadd1969de9fd7a8329ca4")
(setf (get khi_robot_msgs::KhiRobotCmd :datatype-) "khi_robot_msgs/KhiRobotCmd")
(setf (get khi_robot_msgs::KhiRobotCmd :request) khi_robot_msgs::KhiRobotCmdRequest)
(setf (get khi_robot_msgs::KhiRobotCmd :response) khi_robot_msgs::KhiRobotCmdResponse)

(defmethod khi_robot_msgs::KhiRobotCmdRequest
  (:response () (instance khi_robot_msgs::KhiRobotCmdResponse :init)))

(setf (get khi_robot_msgs::KhiRobotCmdRequest :md5sum-) "f15db04cfafadd1969de9fd7a8329ca4")
(setf (get khi_robot_msgs::KhiRobotCmdRequest :datatype-) "khi_robot_msgs/KhiRobotCmdRequest")
(setf (get khi_robot_msgs::KhiRobotCmdRequest :definition-)
      "string type
string cmd
---
int32 driver_ret
int32 as_ret
string cmd_ret
")

(setf (get khi_robot_msgs::KhiRobotCmdResponse :md5sum-) "f15db04cfafadd1969de9fd7a8329ca4")
(setf (get khi_robot_msgs::KhiRobotCmdResponse :datatype-) "khi_robot_msgs/KhiRobotCmdResponse")
(setf (get khi_robot_msgs::KhiRobotCmdResponse :definition-)
      "string type
string cmd
---
int32 driver_ret
int32 as_ret
string cmd_ret
")



(provide :khi_robot_msgs/KhiRobotCmd "f15db04cfafadd1969de9fd7a8329ca4")


