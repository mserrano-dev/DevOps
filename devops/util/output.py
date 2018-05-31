#!/usr/bin/python
import sys
from termcolor import colored
from util import timer

# ============================================================================ #
# Terminal output related helpers
# ============================================================================ #
def start_banner_animation(msg):
    start_banner(msg, True)
    timer.sleep(1)
    start_banner(msg, False)

def start_banner(msg, do_blink):
    """
    Will present msg with a blinking I bar
    """
    list_attrs = []
    cond_tail = '\n'
    end_bar = ' '
    if do_blink == True:
        list_attrs = ['blink']
        cond_tail = tail()
        end_bar = colored('|', primary_color(), attrs=list_attrs)
    
    sys.stdout.write('  ' + msg + end_bar + cond_tail)
    sys.stdout.flush()

def end_banner(msg):
    """
    Will blink arrow for a little bit, then solid. All colored
    """
    blinking = colored('  > ', primary_color(), attrs=['blink'])
    static = colored('  > ', primary_color())
    colored_msg = colored('...DONE (%s)' % msg, primary_color())
    
    sys.stdout.write(blinking + colored_msg + tail())
    sys.stdout.flush()
    timer.sleep(2)
    sys.stdout.write(static + colored_msg + '\n')
    sys.stdout.flush()

def status_report(info_string, duration):
    """
    Will blink arrow. Note info_string is not colored
    """
    blinking = colored('  > ', primary_color(), attrs=['blink'])
    static = colored('    ', primary_color())
    colored_msg = colored(info_string, None)
    
    sys.stdout.write(blinking + colored_msg + tail())
    sys.stdout.flush()
    timer.sleep(duration)
    sys.stdout.write(static + colored_msg + tail())
    sys.stdout.flush()

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def new_line():
    sys.stdout.write('\n')
    sys.stdout.flush()

def primary_color():
    return 'cyan'

def tail():
    """
    Returns a string that will cover up bleeding output when printing in place
    """
    return "                            \r"
