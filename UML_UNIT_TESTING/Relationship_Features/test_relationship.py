import io
import sys
import os
import unittest
from unittest.mock import patch


"""
Author : Israel Gonzalez
Created: September 13, 2024
Version: 1.2

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
        # Reset the data_list and relationship_list to ensure a clean state for each test
        UMLClass.data_list = [[], []]  # Initialize as empty lists
        
        # Define sample data
        self.sample_data = [
            {"class_name": "person"},
            {"class_name": "cat"},
            {"class_name": "dog"},
            {"class_name": "animal"},
            {"class_name": "fish"}
        ]

        # Set up class_and_attr_list and relationship_list
        UMLClass.data_list[0] = self.sample_data  # Set class and attribute list
        UMLClass.data_list[1] = []  # Set relationship list
        
        # Mock load_data_from_json to return sample data
        self.patcher_load = patch('UML_UTILITY.SAVE_LOAD.save_load.load_data_from_json', return_value=(self.sample_data, UMLClass.data_list[1]))
        self.mock_load_data = self.patcher_load.start()

        # Initialize the global variables
        UMLRelationship.relationship_list = UMLClass.data_list[1]

    def tearDown(self):
        self.patcher_load.stop()

    def test_check_format_invalid(self):
        with io.StringIO() as fake_out:
            old_stdout = sys.stdout  # Backup sys.stdout
            sys.stdout = fake_out
            try:
                # Test invalid class names
                invalid_names = ["Name", "Person123", "Cat!", "Dog_", "Animal@"]
                for name in invalid_names:
                    result = UMLRelationship.check_format(name)
                    self.assertEqual(result, "Invalid format. Only lowercase alphabet characters are allowed.")
            finally:
                sys.stdout = old_stdout  # Restore sys.stdout

    def test_check_format_valid(self):
        # Test valid class names
        valid_names = ["person", "cat", "dog", "animal", "fish"]
        for name in valid_names:
            result = UMLRelationship.check_format(name)
            self.assertEqual(result, "Valid input")

    def test_add_relationship_valid(self):
        # Initial state
        self.assertEqual(len(UMLRelationship.relationship_list), 0)

        # Simulate user input to add a relationship
        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.add_relationship("person", "cat", "owns")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Added relationship from 'person' to 'cat' of type 'owns'.", output)
        
        # Check if the relationship was added correctly
        self.assertIn({"source": "person", "dest": "cat", "relation": "owns"}, UMLRelationship.relationship_list)
        self.assertEqual(len(UMLRelationship.relationship_list), 1)

    def test_add_relationship_existing(self):
        UMLRelationship.relationship_list.append({"source": "person", "dest": "cat", "relation": "owns"})

        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.add_relationship("person", "cat", "owns")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Relationship between 'person' and 'cat' already exists!", output)

        self.assertEqual(len(UMLRelationship.relationship_list), 1)

    def test_add_relationship_invalid_source_class(self):
        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.add_relationship("invalidsource", "cat", "owns")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Class 'invalidsource' not found!", output)
                self.assertNotIn({"source": "invalidsource", "dest": "cat", "relation": "owns"}, UMLRelationship.relationship_list)

    def test_add_relationship_invalid_dest_class(self):
        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.add_relationship("person", "invaliddest", "owns")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Class 'invaliddest' not found!", output)
                self.assertNotIn({"source": "person", "dest": "invaliddest", "relation": "owns"}, UMLRelationship.relationship_list)

    def test_add_relationship_invalid_relation(self):
        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.add_relationship("person", "cat", "InvalidRelation123")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Invalid format. Only lowercase alphabet characters are allowed.", output)
                self.assertNotIn({"source": "person", "dest": "cat", "relation": "InvalidRelation123"}, UMLRelationship.relationship_list)

    def test_remove_relationship_existing(self):
        UMLRelationship.relationship_list.append({"source": "person", "dest": "cat", "relation": "owns"})

        with patch('builtins.input', side_effect=['Yes']):
            UMLRelationship.remove_relationship("person", "cat")
            self.assertNotIn({"source": "person", "dest": "cat", "relation": "owns"}, UMLRelationship.relationship_list)

    def test_remove_relationship_non_existent(self):
        with patch('builtins.input', side_effect=['Yes']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.remove_relationship("person", "cat")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("No relationship exists between 'person' and 'cat'.", output)

    def test_cancel_remove_relationship(self):
        with patch('builtins.input', side_effect=['No']):
            with io.StringIO() as fake_out:
                old_stdout = sys.stdout
                sys.stdout = fake_out

                try:
                    UMLRelationship.remove_relationship("person", "cat")
                finally:
                    sys.stdout = old_stdout

                output = fake_out.getvalue()
                self.assertIn("Action cancelled.", output)

    def test_remove_relationship_non_existent_classes(self):
        with io.StringIO() as fake_out:
            old_stdout = sys.stdout
            sys.stdout = fake_out

            try:
                UMLRelationship.remove_relationship("nonexistentclass", "nonexistent")
            finally:
                sys.stdout = old_stdout

            output = fake_out.getvalue()
            self.assertIn("Class 'nonexistentclass' not found!", output)

    def test_add_relationship_empty_class_name(self):
        with io.StringIO() as fake_out:
            old_stdout = sys.stdout
            sys.stdout = fake_out

            try:
                UMLRelationship.add_relationship("", "cat", "owns")
            finally:
                sys.stdout = old_stdout

            output = fake_out.getvalue()
            self.assertIn("Invalid length. Must be between 2 and 50 characters.", output)

    def test_add_relationship_same_source_dest(self):
        with io.StringIO() as fake_out:
            old_stdout = sys.stdout
            sys.stdout = fake_out

            try:
                UMLRelationship.add_relationship("person", "person", "owns")
            finally:
                sys.stdout = old_stdout

            output = fake_out.getvalue()
            self.assertIn("Source and destination classes cannot be the same.", output)

    def test_check_class_name_not_in_list(self):
        with io.StringIO() as fake_out:
            old_stdout = sys.stdout
            sys.stdout = fake_out

            try:
                result = UMLRelationship.check_class_name("nonexistentclass", should_exist=True)
            finally:
                sys.stdout = old_stdout

            output = fake_out.getvalue()
            self.assertIn("Class 'nonexistentclass' not found!", output)
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
