# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 15:30:43 2018

@author: Ocean Insight Inc.
"""

import json

class od_logger:
    def __init__(self):
        pass

    def debug(self, message):
        mtype = type(message)
        if mtype is str:
            print("DEBUG:  %s" % message)
        elif mtype is json:
            print("DEBUG:  %s" % json.dumps(message))
        else:
            str_msg = str(message)
            print("DEBUG:  %s" % json.dumps(str_msg))


    def info(self, message):
        mtype = type(message)
        if mtype is str:
            print("INFO:  %s" % message)
        elif mtype is json:
            print("INFO:  %s" % json.dumps(message))
        else:
            str_msg = str(message)
            print("INFO:  %s" % json.dumps(str_msg))

            
    def warning(self, message):
        mtype = type(message)
        if mtype is str:
            print("WARN:  %s" % message)
        elif mtype is json:
            print("WARN:  %s" % json.dumps(message))
        else:
            str_msg = str(message)
            print("WARN:  %s" % json.dumps(str_msg))

            
    def error(self, message):
        mtype = type(message)
        if mtype is str:
            print("ERROR:  %s" % message)
        elif mtype is json:
            print("ERROR:  %s" % json.dumps(message))
        else:
            str_msg = str(message)
            print("ERROR:  %s" % json.dumps(str_msg))

