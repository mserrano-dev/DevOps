#!/usr/bin/python

# ============================================================================ #
# Bash Arg related helpers
# ============================================================================ #
class SingleLineFile():
    def __init__(self):
        self.__list_line = []
    
    def add_line(self, line):
        """
        Enqueue a string
        """
        self.__list_line.append(line)
    
    def append_file(self, file):
        """
        Enqueue each line in a file
        """
        for line in file.split("\n"):
            escaped_line = line.replace('%', '%%')
            self.add_line(escaped_line)
    
    def get_file(self):
        """
        Return the composed file as a single line
        """
        return "\\n".join(self.__list_line)

def wait_until_complete(cond):
    """
    Wait until condition is satisfied
    """
    return "while %s; do sleep 0.2; done" % cond
