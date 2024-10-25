import sys
import os
import pytest

###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Import the UMLRelationship class
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship

###############################################################################

@pytest.fixture
def uml_relationship():
    # Fixture to set up an instance of UMLRelationship for testing
    return UMLRelationship(
        source_class="ClassA", 
        destination_class="ClassB", 
        rel_type="inheritance"
    )

def test_get_source_class(uml_relationship):
    # Test getting the source class
    assert uml_relationship._get_source_class() == "ClassA"

def test_get_destination_class(uml_relationship):
    # Test getting the destination class
    assert uml_relationship._get_destination_class() == "ClassB"

def test_get_type(uml_relationship):
    # Test getting the relationship type
    assert uml_relationship._get_type() == "inheritance"

def test_set_source_class(uml_relationship):
    # Test setting a new source class
    uml_relationship._set_source_class("NewSourceClass")
    assert uml_relationship._get_source_class() == "NewSourceClass"

def test_set_destination_class(uml_relationship):
    # Test setting a new destination class
    uml_relationship._set_destination_class("NewDestinationClass")
    assert uml_relationship._get_destination_class() == "NewDestinationClass"

def test_set_type(uml_relationship):
    # Test setting a new relationship type
    uml_relationship._set_type("aggregation")
    assert uml_relationship._get_type() == "aggregation"

def test_str(uml_relationship):
    # Test string representation of the relationship
    expected_str = (
        "Source: ClassA\nDestination: ClassB\nType: inheritance"
    )
    assert str(uml_relationship) == expected_str

def test_convert_to_json_relationship(uml_relationship):
    # Test conversion of UMLRelationship to JSON format
    json_data = uml_relationship._convert_to_json_relationship()
    
    expected_json = {
        "source": "ClassA",
        "destination": "ClassB",
        "type": "inheritance"
    }
    
    assert json_data == expected_json