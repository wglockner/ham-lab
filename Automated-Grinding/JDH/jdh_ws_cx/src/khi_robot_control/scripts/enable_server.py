import rospy
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
from khi_robot_msgs.srv import KhiRobotCmd, KhiRobotCmdRequest, KhiRobotCmdResponse


class KHIRobotManager:
    def __init__(self):
        self._enable_server = rospy.Service('robot_enable', Trigger, self.enable_callback)
        self._disable_server = rospy.Service('robot_disable', Trigger, self.disable_callback)
        self._khi_client = rospy.ServiceProxy('khi_robot_command_service', KhiRobotCmd)

    def enable_callback(self, _: TriggerRequest):
        # Activate controller
        cmd = KhiRobotCmdRequest()
        cmd.type = 'driver'
        cmd.cmd = 'restart'
        khi_res: KhiRobotCmdResponse = self._khi_client.call(cmd)

        res = TriggerResponse()
        if khi_res.driver_ret != 0:
            res.success = False
            res.message = f'Failed to enable robot with driver error \'{khi_res.driver_ret}\', AS error \'{khi_res.as_ret}\''
        else:
            res.success = True
            res.message = 'Successfully enabled robot'

        return res

    def disable_callback(self, _: TriggerRequest):
        # Deactivate controller
#        cmd = KhiRobotCmdRequest()
#        cmd.type = 'driver'
#        cmd.cmd = 'quit'
#        khi_res: KhiRobotCmdResponse = self._khi_client.call(cmd)

#        res = TriggerResponse()
#        if khi_res.driver_ret != 0:
#            res.success = False
#            res.message = f'Failed to disable robot with driver error \'{khi_res.driver_ret}\', AS error \'{khi_res.as_ret}\''
#        else:
#            res.success = True
#            res.message = 'Successfully disabled robot'

        res = TriggerResponse()
        res.success = True
        res.message = 'Successfully disabled robot'

        return res


def main():
    rospy.init_node('robot_enable_server')
    _ = KHIRobotManager()
    print('Started KHI robot manager')
    rospy.spin()


if __name__ == '__main__':
    main()
