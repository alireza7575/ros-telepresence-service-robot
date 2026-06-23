#!/usr/bin/env python2.7

import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import socket
import numpy as np
import cv2 as cv



addr = ("10.207.16.155", 6000)
buf = 512
width = 640
height = 480
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')

class image_converter:

  def __init__(self):
    #self.image_pub = rospy.Publisher("image_topic_2",Image)
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      
      #cv.imshow('send', cv_image)
      
      self.s.sendto(code, addr)
      data = cv_image.tostring()
      for i in range(0, len(data), buf):
          self.s.sendto(data[i:i+buf], addr)
             
       
      #cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError as e:
      print(e)
    cv.imshow("Image window", cv_image)
    cv.waitKey(3)


    
  


def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
