import math
from geometry_msgs.msg import TransformStamped
import numpy as np
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
import curses


def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q


class ManualTfTunner(Node):

    def __init__(self):
        super().__init__('manual_tf_tunner')

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)



        self.parent_frame = 'base_link'
        self.child_frame = 'camera_base_link'

        self.values = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'pitch': 0.0, 'roll': 0.0, 'yaw': 0.0}
        self.mode = 'x'
        self.step = 0.1

        self.key_timer = self.create_timer(0.1, self.timer_callback)


    def timer_callback(self):

        self.key_timer.cancel()
        curses.wrapper(self.curses_function)
        self.tf_callback()
        self.key_timer = self.create_timer(0.01, self.timer_callback)

    def curses_function(self, stdscr):

            string = 'Set ' + self.mode + ' value (step = ', str(self.step), '): ' + str(self.values[self.mode])
            for char in string:
                stdscr.addstr(char)
                stdscr.refresh()
            c = stdscr.getch()

            # switch case c
            if c == ord('+'):
                self.values[self.mode] += self.step
            elif c == ord('-'):
                self.values[self.mode] -= self.step
            elif c == ord('x'):
                self.mode = 'x'
            elif c == ord('y'):
                self.mode = 'y'
            elif c == ord('z'):
                self.mode = 'z'
            elif c == ord('r'):
                self.mode = 'roll'
            elif c == ord('p'):
                self.mode = 'pitch'
            elif c == ord('w'):
                self.mode = 'yaw'
            elif c == ord('*'):
                self.step *= 10
            elif c == ord('/'):
                self.step /= 10
            else:
                pass


            stdscr.clear()
            # stdscr.addstr(chr(c))
            # stdscr.refresh()
            


    def tf_callback(self):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self.parent_frame
        t.child_frame_id = self.child_frame

        # Turtle only exists in 2D, thus we get x and y translation
        # coordinates from the message and set the z coordinate to 0
        t.transform.translation.x = self.values['x']
        t.transform.translation.y = self.values['y']
        t.transform.translation.z = self.values['z']

        # For the same reason, turtle can only rotate around one axis
        # and this why we set rotation in x and y to 0 and obtain
        # rotation in z axis from the message
        q = quaternion_from_euler(self.values['roll'], self.values['pitch'], self.values['yaw'])
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = ManualTfTunner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
    rclpy.shutdown()