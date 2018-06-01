#!/usr/bin/python
from util import project_fs
from util.array_phpfill import *

# ============================================================================ #
# Amazon Simple Storage Service (S3) Bucket
# ============================================================================ #
def get_mserrano_config():
    return project_fs.read_json('.aws/mserrano.config', rel_to_user_home=True)
