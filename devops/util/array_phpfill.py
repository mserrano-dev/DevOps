#!/usr/bin/python

# ============================================================================ #
# List-related helper functions (PHP inspired)
# ============================================================================ #
def array_column(input, column_key):
    """
    Given a multi-dimensional array, returns an array of values 
     representing a single column from the input array
    """
    return [obj.get(column_key) for obj in input]

def array_unique(array):
    """
    Removes duplicate values from an array
    """
    return list(set(array))

def array_intersect(array1, array2):
    """
    Returns a list of all values of array1 that are present in array2
    """
    return filter(lambda obj: in_array(obj, array2) == True, array1)

def array_diff(array1, array2):
    """
    Returns a list of all values of array1 that are NOT present in array2
    """
    return filter(lambda obj: in_array(obj, array2) == False, array1)

def in_array(needle, haystack):
    """
    Checks if a value exists in an array
    """
    return (needle in haystack)
