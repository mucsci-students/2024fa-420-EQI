import sys
import os
import pytest

###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_FIELD.uml_field import UMLField  # noqa: E402

###############################################################################

@pytest.fixture
def uml_field():
    # Fixture to set up an instance of UMLField for testing
    return UMLField(type="int", field_name="test_field")

def test_get_name(uml_field):
    # Test that the field name is returned correctly
    assert uml_field._get_name() == "test_field"

def test_set_name(uml_field):
    # Test setting a new field name
    uml_field._set_name("new_field_name")
    assert uml_field._get_name() == "new_field_name"

def test_get_type(uml_field):
    # Test that the field type is returned correctly
    assert uml_field._get_type() == "int"

def test_set_type(uml_field):
    # Test setting a new field type
    uml_field._set_type("string")
    assert uml_field._get_type() == "string"

def test_str(uml_field):
    # Test the string representation of the field
    assert str(uml_field) == "int test_field"

def test_convert_to_json_field(uml_field):
    # Test conversion of UMLField to JSON format
    json_data = uml_field._convert_to_json_field()
    
    expected_json = {
        "name": "test_field",
        "type": "int"
    }
    
    assert json_data == expected_json

