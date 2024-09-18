"""
Author : Israel Gonzalez
Created: September 12, 2024
Version: 1.1

Description: 
Unit tests for the check_format function, which validates whether a given string follows a specific format.
"""

################################################################
# IMPORTED MODULES #

import unittest
import os
import sys
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

################################################################
# ADD ROOT PATH #

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

################################################################

class TestCheckFormat(unittest.TestCase):
    
    def test_valid_input(self):
        """Test for valid inputs."""
        self.assertEqual(check_format("example"), "Valid input")
        self.assertEqual(check_format("test"), "Valid input")
        self.assertEqual(check_format("validstring"), "Valid input")
    
    def test_invalid_type(self):
        """Test for non-string inputs."""
        self.assertEqual(check_format(123), "Input must be a string.")
        self.assertEqual(check_format(None), "Input must be a string.")
        self.assertEqual(check_format(["list"]), "Input must be a string.")
        self.assertEqual(check_format(1.2), "Input must be a string.")
        self.assertEqual(check_format(True), "Input must be a string.")
        self.assertEqual(check_format({"key": "value"}), "Input must be a string.")
        self.assertEqual(check_format(("tuple",)), "Input must be a string.")
        self.assertEqual(check_format({"set"}), "Input must be a string.")
    
    def test_invalid_characters(self):
        """Test for invalid characters."""
        self.assertEqual(check_format("example123"), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format("example!"), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format("hello world"), "Invalid format. Only lowercase alphabet characters are allowed.")
    
    def test_valid_edge_cases(self):
        """Test edge cases like minimum and maximum valid lengths."""
        self.assertEqual(check_format("ab"), "Valid input")  
        self.assertEqual(check_format("a" * 50), "Valid input")

    def test_length_boundary(self):
        """Test edge cases at length boundaries."""
        self.assertEqual(check_format("ab"), "Valid input")  
        self.assertEqual(check_format("a" * 50), "Valid input")  
        self.assertEqual(check_format("a" * 51), "Invalid length. Must be between 2 and 50 characters.") 
        self.assertEqual(check_format(""), "Invalid length. Must be between 2 and 50 characters.") 

    def test_lowercase_only(self):
        """Test for strings with only lowercase alphabetic characters."""
        self.assertEqual(check_format("abcdefghijklmnopqrstuvwxyz"), "Valid input")  
        self.assertEqual(check_format("a" * 50), "Valid input")  

    def test_mixed_content(self):
        """Test for strings with invalid characters."""
        self.assertEqual(check_format("abc123"), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format("validname123"), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format("Name"), "Invalid format. Only lowercase alphabet characters are allowed.")

    def test_leading_trailing_spaces(self):
        """Test for strings with leading or trailing spaces."""
        self.assertEqual(check_format(" example"), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format("example "), "Invalid format. Only lowercase alphabet characters are allowed.")
        self.assertEqual(check_format(" example "), "Invalid format. Only lowercase alphabet characters are allowed.")

if __name__ == '__main__':
    unittest.main()
