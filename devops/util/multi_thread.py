#!/usr/bin/python
import remote_host
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
    
    def add_recipe_on_each(self, cloud, list_instance, recipe):
        """
        Enqueue an ssh call to each instance
        """
        for obj in list_instance:
            target_args = (obj['IP'], cloud.id_file, cloud.recipe(recipe), )
            self.add_task(name=obj['KEY'], target=remote_host.ssh, args=target_args)
    
    def invoke_all_and_wait(self):
        """
        Will resume execution after each thread has terminated
        """
        list_promise = []
        for thread in self.__list_thread:
            thread.start()
            list_promise.append(thread)
        for process in list_promise: process.join()
