#!/usr/bin/python

# ============================================================================ #
# List-related helper functions (PHP inspired)
# ============================================================================ #
def array_column(input, column_key):
    return [obj.get(column_key) for obj in input]