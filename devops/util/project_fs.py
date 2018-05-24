#!/usr/bin/python
import json
import os

# ============================================================================ #
# Filsystem-related helper functions (relative to project root)
# ============================================================================ #
def get_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def upsert_file(filename, contents):
    fhandle = open(__path(filename), 'w')
    fhandle.write(contents)

def read_file(filename):
    with open(__path(filename), 'r') as fhandle:
        return fhandle.read()

def read_file_safe(filename, fallback):
    try:
        _return = read_file(filename)
    except IOError:
        _return = fallback
    
    return _return

def read_json(filename):
    return json.loads(read_file_safe(filename, ''))

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def __path(filename):
    return "%s/%s" % (get_root(), filename.lstrip('/'))
