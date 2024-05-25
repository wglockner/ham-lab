; Auto-generated. Do not edit!


(cl:in-package khi_robot_msgs-srv)


;//! \htmlinclude KhiRobotCmd-request.msg.html

(cl:defclass <KhiRobotCmd-request> (roslisp-msg-protocol:ros-message)
  ((type
    :reader type
    :initarg :type
    :type cl:string
    :initform "")
   (cmd
    :reader cmd
    :initarg :cmd
    :type cl:string
    :initform ""))
)

(cl:defclass KhiRobotCmd-request (<KhiRobotCmd-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <KhiRobotCmd-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'KhiRobotCmd-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name khi_robot_msgs-srv:<KhiRobotCmd-request> is deprecated: use khi_robot_msgs-srv:KhiRobotCmd-request instead.")))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <KhiRobotCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader khi_robot_msgs-srv:type-val is deprecated.  Use khi_robot_msgs-srv:type instead.")
  (type m))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <KhiRobotCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader khi_robot_msgs-srv:cmd-val is deprecated.  Use khi_robot_msgs-srv:cmd instead.")
  (cmd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <KhiRobotCmd-request>) ostream)
  "Serializes a message object of type '<KhiRobotCmd-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'type))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'cmd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'cmd))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <KhiRobotCmd-request>) istream)
  "Deserializes a message object of type '<KhiRobotCmd-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'cmd) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<KhiRobotCmd-request>)))
  "Returns string type for a service object of type '<KhiRobotCmd-request>"
  "khi_robot_msgs/KhiRobotCmdRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'KhiRobotCmd-request)))
  "Returns string type for a service object of type 'KhiRobotCmd-request"
  "khi_robot_msgs/KhiRobotCmdRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<KhiRobotCmd-request>)))
  "Returns md5sum for a message object of type '<KhiRobotCmd-request>"
  "f15db04cfafadd1969de9fd7a8329ca4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'KhiRobotCmd-request)))
  "Returns md5sum for a message object of type 'KhiRobotCmd-request"
  "f15db04cfafadd1969de9fd7a8329ca4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<KhiRobotCmd-request>)))
  "Returns full string definition for message of type '<KhiRobotCmd-request>"
  (cl:format cl:nil "string type~%string cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'KhiRobotCmd-request)))
  "Returns full string definition for message of type 'KhiRobotCmd-request"
  (cl:format cl:nil "string type~%string cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <KhiRobotCmd-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'type))
     4 (cl:length (cl:slot-value msg 'cmd))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <KhiRobotCmd-request>))
  "Converts a ROS message object to a list"
  (cl:list 'KhiRobotCmd-request
    (cl:cons ':type (type msg))
    (cl:cons ':cmd (cmd msg))
))
;//! \htmlinclude KhiRobotCmd-response.msg.html

(cl:defclass <KhiRobotCmd-response> (roslisp-msg-protocol:ros-message)
  ((driver_ret
    :reader driver_ret
    :initarg :driver_ret
    :type cl:integer
    :initform 0)
   (as_ret
    :reader as_ret
    :initarg :as_ret
    :type cl:integer
    :initform 0)
   (cmd_ret
    :reader cmd_ret
    :initarg :cmd_ret
    :type cl:string
    :initform ""))
)

(cl:defclass KhiRobotCmd-response (<KhiRobotCmd-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <KhiRobotCmd-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'KhiRobotCmd-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name khi_robot_msgs-srv:<KhiRobotCmd-response> is deprecated: use khi_robot_msgs-srv:KhiRobotCmd-response instead.")))

(cl:ensure-generic-function 'driver_ret-val :lambda-list '(m))
(cl:defmethod driver_ret-val ((m <KhiRobotCmd-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader khi_robot_msgs-srv:driver_ret-val is deprecated.  Use khi_robot_msgs-srv:driver_ret instead.")
  (driver_ret m))

(cl:ensure-generic-function 'as_ret-val :lambda-list '(m))
(cl:defmethod as_ret-val ((m <KhiRobotCmd-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader khi_robot_msgs-srv:as_ret-val is deprecated.  Use khi_robot_msgs-srv:as_ret instead.")
  (as_ret m))

(cl:ensure-generic-function 'cmd_ret-val :lambda-list '(m))
(cl:defmethod cmd_ret-val ((m <KhiRobotCmd-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader khi_robot_msgs-srv:cmd_ret-val is deprecated.  Use khi_robot_msgs-srv:cmd_ret instead.")
  (cmd_ret m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <KhiRobotCmd-response>) ostream)
  "Serializes a message object of type '<KhiRobotCmd-response>"
  (cl:let* ((signed (cl:slot-value msg 'driver_ret)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'as_ret)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'cmd_ret))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'cmd_ret))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <KhiRobotCmd-response>) istream)
  "Deserializes a message object of type '<KhiRobotCmd-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'driver_ret) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'as_ret) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd_ret) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'cmd_ret) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<KhiRobotCmd-response>)))
  "Returns string type for a service object of type '<KhiRobotCmd-response>"
  "khi_robot_msgs/KhiRobotCmdResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'KhiRobotCmd-response)))
  "Returns string type for a service object of type 'KhiRobotCmd-response"
  "khi_robot_msgs/KhiRobotCmdResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<KhiRobotCmd-response>)))
  "Returns md5sum for a message object of type '<KhiRobotCmd-response>"
  "f15db04cfafadd1969de9fd7a8329ca4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'KhiRobotCmd-response)))
  "Returns md5sum for a message object of type 'KhiRobotCmd-response"
  "f15db04cfafadd1969de9fd7a8329ca4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<KhiRobotCmd-response>)))
  "Returns full string definition for message of type '<KhiRobotCmd-response>"
  (cl:format cl:nil "int32 driver_ret~%int32 as_ret~%string cmd_ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'KhiRobotCmd-response)))
  "Returns full string definition for message of type 'KhiRobotCmd-response"
  (cl:format cl:nil "int32 driver_ret~%int32 as_ret~%string cmd_ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <KhiRobotCmd-response>))
  (cl:+ 0
     4
     4
     4 (cl:length (cl:slot-value msg 'cmd_ret))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <KhiRobotCmd-response>))
  "Converts a ROS message object to a list"
  (cl:list 'KhiRobotCmd-response
    (cl:cons ':driver_ret (driver_ret msg))
    (cl:cons ':as_ret (as_ret msg))
    (cl:cons ':cmd_ret (cmd_ret msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'KhiRobotCmd)))
  'KhiRobotCmd-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'KhiRobotCmd)))
  'KhiRobotCmd-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'KhiRobotCmd)))
  "Returns string type for a service object of type '<KhiRobotCmd>"
  "khi_robot_msgs/KhiRobotCmd")