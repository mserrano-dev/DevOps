#!/usr/bin/python

# ============================================================================ #
# Bash Arg related helpers
# ============================================================================ #
class SingleLineFile():
    __list_line = []

    def add_line(self, line):
        """
        Enqueue a string
        """
        self.__list_line.append(line)
        
    def append_yaml_file(self, file):
        """
        Enqueue each line in a yaml file
        """
        for line in file.split("\n"):
            self.add_line(line)
            
    def get_file(self):
        """
        Return the composed file as a single line
        """
        return "\\n".join(self.__list_line)