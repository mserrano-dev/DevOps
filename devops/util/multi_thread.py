#!/usr/bin/python
from threading import Thread

# ============================================================================ #
# Class to facilitate Multi-Threading
# ============================================================================ #
class Runner():
    # =-=-=--=---=-----=--------=-------------=
    # Functions
    # ----------------------------------------=
    def __init__(self):
        self.__list_thread = []
    
    def add_task(self, name, target, args):
        """
        Add thread to queue
        """
        self.__list_thread.append(Thread(name=name, target=target, args=args))
    
    def invoke_all_and_wait(self):
        """
        Will resume execution after each thread has terminated
        """
        list_promise = []
        for thread in self.__list_thread:
            thread.start()
            list_promise.append(thread)
        for process in list_promise: process.join()