import re

"""
Author : Israel Gonzalez
Created: September 12, 2024
Version: 1.0

Description: 
This function, check_format, validates whether a given string follows a specific format. 
The checks include:
1. The input must be a string.
2. The input length must be between 2 and 50 characters.
3. The input can only contain alphabetic characters (no spaces or special characters).
"""


VALID_NAME_PATTERN = re.compile(r"^[a-zA-Z]+$")

def check_format(name):

    # Check if the input is a string and matches the pattern
    if not isinstance(name, str):
        return "Input must be a string."
    
    # Check if minimum length 2, maximum length 50
    if not (2 <= len(name) <= 50):  
        return "Invalid length. Must be between 2 and 50 characters."
    
    # Check if the input matches the regex pattern (no spaces or special characters).
    if not VALID_NAME_PATTERN.match(name):
        return "Invalid format. Only alphabet characters are allowed."
    
    return "Valid input"