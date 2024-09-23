"""
Author : Quang Bui
Created: September 12, 2024

Description:
    This shell has UML class features

List of date modified:
- September 18, 2024 (By Quang)

"""

import os
import sys
import unittest
from unittest.mock import patch

# Add the root directory of the project to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

import UML_CORE.UML_CLASS.uml_class as UMLClass

######################################################################
# TEST CASES FOR CLASS FUNCTIONS #
######################################################################


class TestUMLClassAdd(unittest.TestCase):
    def setUp(self):
        """
        This method runs before each test. It automatically sets up some default classes
        and clears the relationship list.
        """
        # Mock the relationship_list and class_and_attr_list
        UMLClass.class_list = ["house", "person"]
        UMLClass.class_and_attr_list = [
            {"class_name": "house", 
             "attr_list": [
                 {"attr_name": "roof"},
                 {"attr_name": "garage"}]},
            {"class_name": "person",
             "attr_list": []}
        ]
    ######################################################################
    # TEST ADDING CLASS #
    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_add_valid_class(self, mock_user_choice):
        """Test Case 1: Add a valid class"""
        # Expected: Added class 'chicken' successfully!
        UMLClass.add_class("chicken")
        self.assertIn("chicken", UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=False)
    def test_add_class_cancel(self, mock_user_choice):
        """Test Case 2: Cancel add class"""
        class_name = "universe"
        # Expected: Action is cancelled due to user_choice returning False
        UMLClass.add_class(class_name)
        # The class should not be added
        self.assertNotIn(class_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_add_invalid_class_01(self, mock_user_choice):
        """Test Case 3: Add an ivalid class with numeric characters"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "111house222"
        UMLClass.add_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_add_invalid_class_02(self, mock_user_choice):
        """Test Case 4: Add an ivalid class with special characters"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "!house@$#"
        UMLClass.add_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_add_invalid_class_03(self, mock_user_choice):
        """Test Case 5: Add an ivalid class with special and numeric characters"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "123house#$@"
        UMLClass.add_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_add_invalid_class_04(self, mock_user_choice):
        """Test Case 5: Add a class that has already existed"""
        # Expected: Class 'house' has already existed!
        class_name = "house"
        UMLClass.add_class(class_name)
        self.assertIn(class_name, UMLClass.class_list)

    ######################################################################
    # TEST DELETE CLASS #
    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_delete_class_that_exists(self, mock_user_choice):
        """Test Case 1: Delete a valid class"""
        # Expected: Successfully removed class 'house'!
        class_name = "house"
        UMLClass.delete_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)
        
    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_delete_class_invalid_format(self, mock_user_choice):
        """Test Case 2: Delete a class with invalid name"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "123house#$@"
        UMLClass.delete_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    def test_delete_class_that_does_not_exist(self):
        """Test Case 3: Delete a non-exist class"""
        # Expected: Class 'animal' not found!
        class_name = "animal"
        UMLClass.delete_class(class_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    ######################################################################
    # TEST RENAME CLASS #
    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_rename_class_that_exists(self, mock_user_choice):
        """Test Case 1: Add a valid class"""
        # Expected: Successfully changes name from "water" to "shape"
        class_name = "water"
        new_name = "shape"
        UMLClass.add_class(class_name)  # Setup
        UMLClass.rename_class(class_name, new_name)
        self.assertIn(new_name, UMLClass.class_list)
        self.assertNotIn(class_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_rename_class_to_existing_name(self, mock_user_choice):
        """Test Case 2: Rename a class to a name that already exists"""
        # Expected: Class 'water' has already existed!
        class_name = "water"
        new_name = "water"
        UMLClass.add_class(class_name)  # Setup
        UMLClass.rename_class(class_name, new_name)
        self.assertIn(new_name, UMLClass.class_list)

    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    def test_rename_class_invalid_format(self, mock_user_choice):
        """Test Case 3: Rename a class to an invalid name format"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "water"
        new_name = "oil123!@#"
        UMLClass.add_class(class_name)  # Setup
        UMLClass.rename_class(class_name, new_name)
        self.assertIn(class_name, UMLClass.class_list)
        self.assertNotIn(new_name, UMLClass.class_list)

    def test_rename_class_that_does_not_exist(self):
        """Test Case 4: Rename a class that does not exist to a valid new name"""
        # Expected: Class 'player' not found!
        class_name = "player"
        new_name = "human"
        UMLClass.rename_class(class_name, new_name)
        self.assertNotIn(new_name, UMLClass.class_list)

    ######################################################################


if __name__ == "__main__":
    unittest.main()
