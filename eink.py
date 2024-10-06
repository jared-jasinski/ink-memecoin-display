#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def show_on_display(image):
    try:
        logging.info("epd4in2 Demo")
        
        epd = epd4in2_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        
        logging.info("E-paper refresh")
        epd.init()
        
        logging.info("1.read output file")

        epd.display(epd.getbuffer(image))
        
        epd.sleep()
       
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd4in2_V2.epdconfig.module_exit(cleanup=True)
        exit()
