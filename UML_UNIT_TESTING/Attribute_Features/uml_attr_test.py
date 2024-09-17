import os
import sys
import unittest
from unittest.mock import patch

# Add the root directory of the project to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

import UML_CORE.UML_CLASS.uml_class as UMLClass
import UML_CORE.UML_ATTRIBUTE.uml_attribute as UMLAttribute

######################################################################
# TEST CASES FOR CLASS FUNCTIONS #
######################################################################


class TestUMLAttributeAdd(unittest.TestCase):

    ######################################################################
    # TEST ADDING CLASS #
    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute(self, mock_user_choice):
        """Test Case 1: Add a valid attribute"""
        # Expected: Added attribute 'beak' successfully to class 'chicken!
        UMLAttribute.add_attr("chicken", "beak")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertIn({'attr_name': 'beak'}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute2(self, mock_user_choice):
        """Test Case 1: Add a valid attribute"""
        # Expected: Added attribute 'beak' successfully to class 'chicken!
        UMLAttribute.add_attr("chicken", "eyes")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertIn({'attr_name': 'eyes'}, attr_list)


    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=False)
    def test_add_attr_cancel(self, mock_user_choice, mock_user_choice2):
        UMLClass.add_class("chicken")
        """Test Case 1: Add a valid attribute"""
        # Expected: Added attribute 'beak' successfully to class 'chicken!
        UMLAttribute.add_attr("chicken", "beak")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': 'beak'}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute(self, mock_user_choice):
        """Test Case 1: Add a valid attribute"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        UMLAttribute.add_attr("chicken", "123beak")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': '123beak'}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute2(self, mock_user_choice):
        """Test Case 1: Add a valid attribute"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        UMLAttribute.add_attr("chicken", "!beak@$#")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': '!beak@$#'}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute3(self, mock_user_choice):
        
        """Test Case 1: Add a valid attribute"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        UMLAttribute.add_attr("chicken", "!@$beak125")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': '!@$beak125'}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute3(self, mock_user_choice, mock_user_choice2):
        UMLAttribute.add_attr("chicken", "feathers")
        """Test Case 1: Add a valid attribute"""
        # Expected: Attribute 'feathers' already existed in class 'chicken'.
        UMLAttribute.add_attr("chicken", "feathers")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertIn({'attr_name': 'feathers'}, attr_list)

    ######################################################################
    ######################################################################
    # TEST DELETE ATTRIBUTE #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_that_exists(self, mock_user_choice):
        """Test Case 1: Delete a valid class"""
        # Expected: Successfully removed class 'house'!
        UMLAttribute.delete_attr("chicken", "beak")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': 'beak'}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_invalid(self, mock_user_choice):
        """Test Case 1: Delete a valid class"""
        # Expected: Successfully removed class 'house'!
        UMLAttribute.delete_attr("chicken", "123beak")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': '123beak'}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_not_exist(self, mock_user_choice):
        """Test Case 1: Delete a valid class"""
        # Expected: Successfully removed class 'house'!
        UMLAttribute.delete_attr("chicken", "feather")
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertNotIn({'attr_name': 'feather'}, attr_list)

    ######################################################################
    # TEST RENAME CLASS #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_exists(self, mock_user_choice):
        """Test Case 1: Add a valid class"""
        # Expected: Successfully changes name from "water" to "shape"
        class_name = "chicken"
        attr_name = "feathers"
        new_name = "tail"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list("chicken")
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_not_exist(self, mock_user_choice):
        """Test Case 1: Add a valid class"""
        # Expected: Successfully changes name from "water" to "shape"
        class_name = "chicken"
        attr_name = "feathers"
        new_name = "heart"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_to_already_exist(self, mock_user_choice):
        """Test Case 1: Add a valid class"""
        # Expected: Successfully changes name from "water" to "shape"
        class_name = "chicken"
        attr_name = "eyes"
        new_name = "tail"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertIn({"attr_name": attr_name}, attr_list)


if __name__ == "__main__":
    unittest.main()
