#!/usr/bin/python
import json
import os

# ============================================================================ #
# Filsystem-related helper functions (relative to project root)
# ============================================================================ #
def get_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def upsert_file(filename, contents, rel_to_user_home=False):
    fhandle = open(__path(filename, rel_to_user_home), 'w')
    fhandle.write(contents)

def read_file(filename, rel_to_user_home=False):
    with open(__path(filename, rel_to_user_home), 'r') as fhandle:
        return fhandle.read()

def read_file_safe(filename, fallback, rel_to_user_home=False):
    try:
        _return = read_file(filename, rel_to_user_home)
    except IOError:
        _return = fallback
    return _return

def read_json(filename, rel_to_user_home=False):
    return json.loads(read_file_safe(filename, '', rel_to_user_home))

# =-=-=--=---=-----=--------=-------------=
# Helpers
# ----------------------------------------=
def __path(filename, rel_to_user_home):
    if rel_to_user_home:
        _return = "%s/%s" % (os.path.expanduser("~"), filename.lstrip('/'))
    else:
        _return = "%s/%s" % (get_root(), filename.lstrip('/'))
    return _return
