#!/usr/bin/python
import sys
from termcolor import colored
import time

# ============================================================================ #
# Polling Mechanism
# ============================================================================ #
class Polling(object):
    __tail = "                         \r"
    __do_initial_animation = True
    __polling_count = 0
    __polling_interval = 10 #seconds
    
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.__output_start_banner(True)
    
    def wait(self, args):
        self.__polling_count += 1
        resp = self.polling_mechanism(** args)
        self.__output_status_report(resp)
        if self.resp_parser(resp) == False:
            time.sleep(self.__polling_interval * 0.6)
            self.wait(args)
        else:
            self.__output_end_banner()
            
        if self.__do_initial_animation == True:
            sys.stdout.write("\n ")
            sys.stdout.flush()
        
    def register_polling_fn(self, fn):
        self.polling_mechanism = fn
        
    def register_resp_parser_fn(self, fn):
        self.resp_parser = fn
        
    def register_resp_status_fn(self, fn):
        self.resp_status = fn
    
    # =-=-=--=---=-----=--------=-------------=
    # Helpers
    # ----------------------------------------=
    def __output_start_banner(self, val):
        self.__do_initial_animation = val
        
        list_attrs = ['blink'] if val else []
        cond_tail = self.__tail if val else '\n'
        end_bar = colored('|', 'cyan', attrs=list_attrs) if val else ' '
        sys.stdout.write('  Spinning up new servers...' + end_bar + cond_tail)
        sys.stdout.flush()
        
    def __output_end_banner(self):
        sys.stdout.write(colored('\n  > ', 'cyan') + '...' + colored('DONE', 'cyan') + '\n')
        sys.stdout.flush()
        
    def __output_status_report(self, resp):
        result = self.resp_status(resp)
        if len(result) != 0:
            if self.__do_initial_animation == True:
                self.__output_start_banner(False)
            info = result + ' (Polling: %s)' % self.__polling_count + self.__tail

            # blink for 4 sec, then solid
            sys.stdout.write(colored('  > ', 'cyan', attrs=['blink']) + info)
            sys.stdout.flush()
            arrow = '    '
            if self.resp_parser(resp) == False:
                time.sleep(max(2, self.__polling_interval * 0.4))
                arrow = '  > '
            sys.stdout.write(colored(arrow, 'cyan') + info)
            sys.stdout.flush()