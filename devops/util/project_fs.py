#!/usr/bin/python
import os

# ============================================================================ #
# Filsystem-related helper functions (relative to project root)
# ============================================================================ #
def get_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
def upsert_file(filename, contents):
    path = "%s/%s" % (get_root(), filename.lstrip('/'))
    fhandle = open(path, 'w')
    fhandle.write(contents)