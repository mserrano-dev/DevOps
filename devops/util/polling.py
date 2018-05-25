#!/usr/bin/python
import sys
from termcolor import colored
import time
from util import output

# ============================================================================ #
# Polling Mechanism
# ============================================================================ #
class Polling():
    __do_initial_animation = True
    __polling_count = 0
    __polling_interval = 10 #seconds
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self, ** kwargs):
        self.__polling_interval = kwargs['polling_interval']
        self.__polling_function = kwargs['polling_function']
        self.__start_msg = kwargs['start_msg']
        self.__end_msg = kwargs['end_msg']
        self.__start_banner(True)
    
    def wait(self, args):
        self.__polling_count += 1
        resp = self.__polling_function( ** args)
        self.__status_report(resp)
        if self.resp_parser(resp, ** self.resp_parser_args) == False:
            time.sleep(self.__polling_interval * 0.6)
            self.wait(args)
        else:
            self.__end_banner()
        
        if self.__do_initial_animation == True:
            sys.stdout.write("\n ")
            sys.stdout.flush()
    
    def register_resp_parser_fn(self, fn, args):
        self.resp_parser = fn
        self.resp_parser_args = args
    
    def register_resp_status_fn(self, fn, args):
        self.resp_status = fn
        self.resp_status_args = args
    
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __start_banner(self, do_blink):
        self.__do_initial_animation = do_blink
        output.start_banner(self.__start_msg, do_blink)
    
    def __end_banner(self):
        output.new_line()
        output.end_banner(self.__end_msg)
    
    def __status_report(self, resp):
        result = self.resp_status(resp, ** self.resp_status_args)
        if self.__do_initial_animation == True:
            self.__start_banner(False)
        
        info_string = result + ' (Polling: %s)' % self.__polling_count
        duration = max(2, self.__polling_interval * 0.4)
        output.status_report(info_string, duration)
