#!/usr/bin/python
import date
import datetime
import time

# ============================================================================ #
# Time-related helper functions
# ============================================================================ #
def sleep(duration):
    """
    Pause execution for specified duration
    """
    time.sleep(duration)

def today_w_time():
    """
    Returns today in format 'Y-m-d H:i:s'
    """
    today = datetime.datetime.now()
    today = today.replace(microsecond=0)
    return today.isoformat(' ')

def today():
    """
    Returns today in format 'Y-m-d'
    """
    return date.today()

def time_string(delta, hours, minutes, seconds, delim, always_show=True):
    """
    Convert seconds into the format specified
    """
    t_hours, remainder = divmod(delta, 3600)
    t_minutes, t_seconds = divmod(remainder, 60)
    
    output = []
    if always_show or t_hours > 0: output.append(hours % t_hours)
    if always_show or t_minutes > 0: output.append(minutes % t_minutes)
    if always_show or t_seconds > 0: output.append(seconds % t_seconds)
    
    return delim.join(output)

class Stopwatch():
    """
    Class to facilitate tracking execution time
    """
    def __init__(self):
        self.__start_time = time.time()
    
    def output_report(self):
        self.__end_time = time.time()
        
        formatted_string = time_string(delta=int(self.__end_time - self.__start_time),
                                       hours="%dh",
                                       minutes="%dm",
                                       seconds="%ds",
                                       delim=" ",
                                       always_show=False)
        print 'Execution Time: %s' % formatted_string
