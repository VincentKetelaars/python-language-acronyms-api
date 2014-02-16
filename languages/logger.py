'''
Created on Feb 16, 2014

@author: Vincent Ketelaars
'''
import logging
import sys
logging.basicConfig(stream = sys.stderr, level=logging.DEBUG)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger
    