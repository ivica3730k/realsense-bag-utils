#!/usr/bin/env python
from __future__ import print_function

# -*- coding: utf-8 -*-
"""
:ABSTRACT:
This script is part of the of the Field Companion project.
:REQUIRES: 
:
:AUTHOR:  Jack Bonnell
:ORGANIZATION: Sundance Multiprocessor Technology
:CONTACT: jack.b@sundance.com
:SINCE: 02/05/2020
:VERSION: 1.0
2020 (c) All rights reserved, Sundance Multiprocessor Technology
project: Field Companion project
email:  jack.b@sundance.com
website: www.sundance.com
"""

# ===============================================================================
# PROGRAM METADATA
# ===============================================================================
__author__ = 'Jack Bonnell'
__contact__ = 'jack.b@sundance.com'
__copyright__ = '2020 (C) All rights reserved, Sundance Multiprocessor Technology'
__license__ = 'All rights reserved'
__date__ = '02/05/2020'
__version__ = '1.0'
__file_name__ = 'viewer.py'
__description__ = 'visualisation'
__compatibility__ = "Python 2"
__platforms__ = "x86_64, arm32 and arm64"
__diff__ = "first version"

# ===============================================================================
# IMPORT STATEMENTS
# ===============================================================================

import traceback
import numpy as np
import cv2
import rospy
from cv_bridge import CvBridge
import Configuration as Config
from sensor_msgs.msg import Image


# ===============================================================================
# GLOBAL VARIABLES DECLARATIONS
# ===============================================================================


# ===============================================================================
# METHODS
# ===============================================================================

def rgb_image_callback(image):
    """
    RGB Image callback

    Function obtains the rgb rgb_image from the depth publishing topic
    and displays it to the user

    :rgb_image: raw RGB rgb_image
    """
    try:
        image = np.asarray(br.imgmsg_to_cv2(image, "bgr8"))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow(side + " rgb", image)
        key = cv2.waitKey(3) & 0xFF
        if key == ord("q"):
            pass
    except:
        rospy.logerr(traceback.print_exc())


def depth_image_callback(image):
    """
    Depth Image callback

    Function obtains the depth rgb_image from the depth publishing topic
    and displays it to the user

    :rgb_image: raw DEPTH rgb_image
    """

    try:
        image = np.asarray(br.imgmsg_to_cv2(image, "mono16"))
        # rgb_image = np.asarray(br.imgmsg_to_cv2(rgb_image, "rgb8"))
        cv2.imshow(side + " depth", image)
        key = cv2.waitKey(3) & 0xFF
        if key == ord("q"):
            pass
    except:
        rospy.logerr(traceback.print_exc())


# ===============================================================================
#  TESTING AREA
# ===============================================================================

# ===============================================================================
# MAIN METHOD
# ===============================================================================
if __name__ == '__main__':
    ns = rospy.get_namespace()
    side = rospy.get_param(ns + 'configuration/side')
    rospy.init_node(side + '_viewer', anonymous=True)
    br = CvBridge()
    try:
        ###################################
        # Uncomment to see RGB rgb_image
        rospy.Subscriber(Config.AI_INFERENCE_TOPICS.get_rgb_image_inference_results_topic(side), Image,
                         rgb_image_callback,
                         queue_size=1)
        ###################################
        # Uncomment to see DEPTH rgb_image
        # rospy.Subscriber(Config.AI_INFERENCE_TOPICS.get_depth_image_inference_results_topic(side), Image,
        #                 depth_image_callback,
        #                 queue_size=1)
        # Uncomment to see NIR rgb_image

        print("Starting AI viewer on", side, "side")
        rospy.spin()
    # Spin until ctrl + c
    except:
        rospy.logerr(traceback.print_exc())
