import io
import sys
import os
import unittest

# Import the module you're testing
import UML_CORE.UML_RELATIONSHIP.uml_relationship as UMLRelationship

################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

################################################################
class TestUMLRelationship(unittest.TestCase):

    def setUp(self):
        # Reset the relationships list to ensure a clean state for each test
        UMLRelationship.relationships = []

        # Setup sample data to simulate class existence
        self.sample_data = [
            {"class_name": "person"},
            {"class_name": "cat"},
            {"class_name": "dog"},
            {"class_name": "animal"},
            {"class_name": "fish"}
        ]

        # Manually setting the data for classes
        UMLRelationship.SAVE_LOAD.load_data_from_json = lambda _: (self.sample_data, UMLRelationship.relationships)


    def test_check_format_invalid(self):
        # Capture printed output
        with io.StringIO() as fake_out:
            sys.stdout = fake_out

            # Test invalid class names
            invalid_names = ["Name", "Person123", "Cat!", "Dog_", "Animal@"]
            for name in invalid_names:
                result = UMLRelationship.check_format(name)
                self.assertEqual(result, "Invalid format. Only lowercase alphabet characters are allowed.")
        
            # Restore sys.stdout
            sys.stdout = sys.__stdout__

    def test_check_format_valid(self):
        # Test valid class names
        valid_names = ["person", "cat", "dog", "animal", "fish"]
        for name in valid_names:
            result = UMLRelationship.check_format(name)
            self.assertEqual(result, "Valid input")

    def test_add_relationship_valid(self):
        # Calling the add_relationship function from your module
        UMLRelationship.add_relationship("person", "cat", "owns")

        # Check if the relationship was added correctly
        self.assertIn({"source": "person", "dest": "cat", "relation": "owns"}, UMLRelationship.relationships)

    def test_add_relationship_existing(self):
        # Adding an initial relationship
        UMLRelationship.relationships.append({"source": "person", "dest": "cat", "relation": "owns"})

        # Try to add the same relationship again
        UMLRelationship.add_relationship("person", "cat", "owns")

        # Ensure no duplicates were added
        self.assertEqual(len(UMLRelationship.relationships), 1)

    def test_remove_relationship_valid(self):
        # Add a relationship first
        UMLRelationship.relationships.append({"source": "person", "dest": "cat", "relation": "owns"})

        # Remove the relationship
        UMLRelationship.remove_relationship("person", "cat")

        # Ensure it was removed
        self.assertNotIn({"source": "person", "dest": "cat", "relation": "owns"}, UMLRelationship.relationships)


    def test_remove_relationship_nonexistent(self):
        # Try to remove a relationship that doesn't exist
        UMLRelationship.remove_relationship("person", "cat")

        # Ensure the list remains empty
        self.assertEqual(len(UMLRelationship.relationships), 0)


    def test_add_relationship_non_existent_classes(self):
        # Capture printed output
        with io.StringIO() as fake_out:
            sys.stdout = fake_out

            # Attempt to add a relationship with non-existent classes
            UMLRelationship.add_relationship("nonexistent_class_1", "nonexistent_class_2", "friend")

            # Check printed output
            output = fake_out.getvalue()
            self.assertIn("One or both classes do not exist. Relationship not added.", output)
        
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def test_remove_relationship_non_existent_classes(self):
        # Capture printed output
        with io.StringIO() as fake_out:
            sys.stdout = fake_out

            # Attempt to remove a relationship with non-existent classes
            UMLRelationship.remove_relationship("nonexistent_class_1", "nonexistent_class_2")

            # Check printed output
            output = fake_out.getvalue()
            self.assertIn("One or both classes do not exist. Relationship not removed.", output)
        
        # Restore sys.stdout
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
