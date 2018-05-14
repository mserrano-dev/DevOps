#!/usr/bin/python
import datetime

# ============================================================================ #
# Date-related helper functions (iso format)
# ============================================================================ #
def today():
    return datetime.date.today().isoformat()