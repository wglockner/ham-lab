// Auto-generated. Do not edit!

// (in-package khi_robot_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class KhiRobotCmdRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.type = null;
      this.cmd = null;
    }
    else {
      if (initObj.hasOwnProperty('type')) {
        this.type = initObj.type
      }
      else {
        this.type = '';
      }
      if (initObj.hasOwnProperty('cmd')) {
        this.cmd = initObj.cmd
      }
      else {
        this.cmd = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type KhiRobotCmdRequest
    // Serialize message field [type]
    bufferOffset = _serializer.string(obj.type, buffer, bufferOffset);
    // Serialize message field [cmd]
    bufferOffset = _serializer.string(obj.cmd, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type KhiRobotCmdRequest
    let len;
    let data = new KhiRobotCmdRequest(null);
    // Deserialize message field [type]
    data.type = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [cmd]
    data.cmd = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.type);
    length += _getByteLength(object.cmd);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'khi_robot_msgs/KhiRobotCmdRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '5d68f1ab31d25490e0af3d08f063b65d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string type
    string cmd
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new KhiRobotCmdRequest(null);
    if (msg.type !== undefined) {
      resolved.type = msg.type;
    }
    else {
      resolved.type = ''
    }

    if (msg.cmd !== undefined) {
      resolved.cmd = msg.cmd;
    }
    else {
      resolved.cmd = ''
    }

    return resolved;
    }
};

class KhiRobotCmdResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.driver_ret = null;
      this.as_ret = null;
      this.cmd_ret = null;
    }
    else {
      if (initObj.hasOwnProperty('driver_ret')) {
        this.driver_ret = initObj.driver_ret
      }
      else {
        this.driver_ret = 0;
      }
      if (initObj.hasOwnProperty('as_ret')) {
        this.as_ret = initObj.as_ret
      }
      else {
        this.as_ret = 0;
      }
      if (initObj.hasOwnProperty('cmd_ret')) {
        this.cmd_ret = initObj.cmd_ret
      }
      else {
        this.cmd_ret = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type KhiRobotCmdResponse
    // Serialize message field [driver_ret]
    bufferOffset = _serializer.int32(obj.driver_ret, buffer, bufferOffset);
    // Serialize message field [as_ret]
    bufferOffset = _serializer.int32(obj.as_ret, buffer, bufferOffset);
    // Serialize message field [cmd_ret]
    bufferOffset = _serializer.string(obj.cmd_ret, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type KhiRobotCmdResponse
    let len;
    let data = new KhiRobotCmdResponse(null);
    // Deserialize message field [driver_ret]
    data.driver_ret = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [as_ret]
    data.as_ret = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [cmd_ret]
    data.cmd_ret = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.cmd_ret);
    return length + 12;
  }

  static datatype() {
    // Returns string type for a service object
    return 'khi_robot_msgs/KhiRobotCmdResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'baff9913c1b46a5cd1d4da599ea7743d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 driver_ret
    int32 as_ret
    string cmd_ret
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new KhiRobotCmdResponse(null);
    if (msg.driver_ret !== undefined) {
      resolved.driver_ret = msg.driver_ret;
    }
    else {
      resolved.driver_ret = 0
    }

    if (msg.as_ret !== undefined) {
      resolved.as_ret = msg.as_ret;
    }
    else {
      resolved.as_ret = 0
    }

    if (msg.cmd_ret !== undefined) {
      resolved.cmd_ret = msg.cmd_ret;
    }
    else {
      resolved.cmd_ret = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: KhiRobotCmdRequest,
  Response: KhiRobotCmdResponse,
  md5sum() { return 'f15db04cfafadd1969de9fd7a8329ca4'; },
  datatype() { return 'khi_robot_msgs/KhiRobotCmd'; }
};
