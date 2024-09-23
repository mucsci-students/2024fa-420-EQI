import io
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

"""
Author : Israel Gonzalez
Created: September 13, 2024
Version: 1.4

Description: 
This test suite is designed to verify the functionality of the `uml_relationship.py` module,
which manages relationships between UML classes.
"""

################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
import UML_CORE.UML_RELATIONSHIP.uml_relationship as UMLRelationship
import UML_CORE.UML_CLASS.uml_class as UMLClass
################################################################

class TestUMLRelationship(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test. It automatically sets up some default classes
        and clears the relationship list.
        """
        # Mock the relationship_list and class_and_attr_list
        UMLRelationship.relationship_list = []
        UMLRelationship.class_and_attr_list = [
            {"class_name": "person"},
            {"class_name": "cat"},
            {"class_name": "bank"}
        ]

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_empty_class_name(self, mock_user_choice):
        """Test case for empty class name"""
        source = ""
        dest = "cat"
        relation = "friend"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid length. Must be between 2 and 50 characters.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_valid_relationship(self, mock_user_choice):
        """
        Test adding a valid relationship between classes.
        """
        source = "person"
        dest = "cat"
        relation = "pet"
        
        # Add a valid relationship
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the relationship has been added
        self.assertIn({'source': 'person', 'dest': 'cat', 'relation': 'pet'}, UMLRelationship.relationship_list)
        self.assertEqual(printed_output, f"Added relationship from '{source}' to '{dest}' of type '{relation}'.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_existing_relationship(self, mock_user_choice):
        """
        Test adding an existing relationship should print a message.
        """
        source = "person"
        dest = "cat"
        relation = "pet"
        
        # Add the relationship once
        UMLRelationship.add_relationship(source, dest, relation)
        
        # Attempt to add the same relationship again
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the printed message indicates the relationship already exists
        self.assertEqual(printed_output, f"Relationship between '{source}' and '{dest}' already exists!")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_invalid_format(self, mock_user_choice):
        """
        Test adding a relationship with invalid format.
        """
        source = "person"
        dest = "cat"
        relation = "InvalidFormat123"
        
        # Attempt to add a relationship with invalid format
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the format error message is printed
        self.assertEqual(printed_output, "Invalid format. Only lowercase alphabet characters are allowed.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_same_source_dest(self, mock_user_choice):
        """
        Test adding a relationship where the source and destination are the same.
        """
        source = "person"
        dest = "person"
        relation = "self"
        
        # Attempt to add a relationship with the same source and destination
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, "Source and destination classes cannot be the same.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_non_existent_source(self, mock_user_choice):
        """
        Test adding a relationship where the source class does not exist.
        """
        source = "nonexistent"
        dest = "cat"
        relation = "unknown"
        
        # Attempt to add a relationship with a non-existent source class
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, "Class 'nonexistent' not found!")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_non_existent_dest(self, mock_user_choice):
        """
        Test adding a relationship where the destination class does not exist.
        """
        source = "person"
        dest = "nonexistentdest"
        relation = "unknown"
        
        # Attempt to add a relationship with a non-existent destination class
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(source, dest, relation)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, "Class 'nonexistentdest' not found!")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_too_short(self, mock_user_choice):
        """Test adding relationships with names that are too short."""
        UMLRelationship.add_relationship("p", "c", "f")
        # Check that the correct message is printed for invalid length
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship("p", "c", "f")
            printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Invalid length. Must be between 2 and 50 characters.", printed_output)

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_add_relationship_too_long(self, mock_user_choice):
        """Test adding relationships with names that are too long."""
        long_name = "a" * 51  # Assuming the maximum length is 50 characters
        UMLRelationship.add_relationship(long_name, "cat", "test")
        # Check that the correct message is printed for invalid length
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.add_relationship(long_name, "cat", "test")
            printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Invalid length. Must be between 2 and 50 characters.", printed_output)

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_existing_relationship(self, mock_user_choice):
        """
        Test removing an existing relationship successfully.
        """
        source = "person"
        dest = "cat"
        relation = "pet"
        
        # Add the relationship first
        UMLRelationship.add_relationship(source, dest, relation)
        
        # Remove the relationship
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship(source, dest)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the relationship has been removed
        self.assertNotIn({'source': source, 'dest': dest, 'relation': relation}, UMLRelationship.relationship_list)
        self.assertEqual(printed_output, f"Removed relationship from '{source}' to '{dest}'.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_non_existent_relationship(self, mock_user_choice):
        """
        Test attempting to remove a non-existent relationship.
        """
        source = "person"
        dest = "cat"
        
        # Attempt to remove a relationship that doesn't exist
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship(source, dest)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, f"No relationship exists between '{source}' and '{dest}'.")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_relationship_non_existent_source(self, mock_user_choice):
        """
        Test attempting to remove a relationship where the source class does not exist.
        """
        source = "nonexistent"
        dest = "cat"
        
        # Attempt to remove a relationship with a non-existent source class
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship(source, dest)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, f"Class '{source}' not found!")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_relationship_non_existent_dest(self, mock_user_choice):
        """
        Test attempting to remove a relationship where the destination class does not exist.
        """
        source = "person"
        dest = "nonexistentdest"
        
        # Attempt to remove a relationship with a non-existent destination class
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship(source, dest)
            printed_output = mock_stdout.getvalue().strip()

        # Check that the correct message is printed
        self.assertEqual(printed_output, f"Class '{dest}' not found!")

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_relationship_too_short(self, mock_user_choice):
        """Test removing relationships with names that are too short."""
        UMLRelationship.remove_relationship("p", "c")
        # Check that the correct message is printed for invalid length
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship("p", "c")
            printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Invalid length. Must be between 2 and 50 characters.", printed_output)

    @patch("UML_CORE.UML_RELATIONSHIP.uml_relationship.user_choice", return_value=True)
    def test_remove_relationship_too_long(self, mock_user_choice):
        """Test removing relationships with names that are too long."""
        long_name = "a" * 51  # Assuming the maximum length is 50 characters
        UMLRelationship.remove_relationship(long_name, "cat")
        # Check that the correct message is printed for invalid length
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLRelationship.remove_relationship(long_name, "cat")
            printed_output = mock_stdout.getvalue().strip()
        self.assertIn("Invalid length. Must be between 2 and 50 characters.", printed_output)



if __name__ == "__main__":
    unittest.main()
