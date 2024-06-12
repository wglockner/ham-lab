
(cl:in-package :asdf)

(defsystem "khi_robot_msgs-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "KhiRobotCmd" :depends-on ("_package_KhiRobotCmd"))
    (:file "_package_KhiRobotCmd" :depends-on ("_package"))
  ))