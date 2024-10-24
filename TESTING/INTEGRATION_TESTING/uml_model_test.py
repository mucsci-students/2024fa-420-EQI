import sys
import os
import pytest
from rich.console import Console

# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Import the UMLModel class and UMLObserver
from UML_MVC.UML_MODEL.uml_model import UMLModel
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView
from UML_MVC.uml_observer import UMLObserver

# Import other dependencies such as UMLClass, UMLField, UMLMethod, UMLParameter, UMLRelationship
from UML_CORE.UML_CLASS.uml_class import UMLClass
from UML_CORE.UML_FIELD.uml_field import UMLField
from UML_CORE.UML_METHOD.uml_method import UMLMethod
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship

###############################################################################

@pytest.fixture
def uml_model():
    view = UMLView()
    console = Console()
    return UMLModel(view=view, console=console)

@pytest.fixture
def sample_class():
    return UMLClass(class_name="TestClass")

@pytest.fixture
def sample_field():
    return UMLField(type="int", field_name="sampleField")

@pytest.fixture
def sample_observer():
    class TestObserver(UMLObserver):
        def __init__(self):
            self.events = []

        def _update(self, event_type=None, data=None, is_loading=None):
            self.events.append({
                "event_type": event_type,
                "data": data,
                "is_loading": is_loading
            })

    return TestObserver()

###############################################################################
# Observer Pattern Tests
###############################################################################

def test_attach_observer(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._notify_observers(event_type="test_event", data={"key": "value"})
    
    assert len(sample_observer.events) == 1
    assert sample_observer.events[0]["event_type"] == "test_event"
    assert sample_observer.events[0]["data"] == {"key": "value"}

def test_detach_observer(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._detach_observer(sample_observer)
    
    uml_model._notify_observers(event_type="test_event", data={"key": "value"})
    assert len(sample_observer.events) == 0

###############################################################################
# Getter Methods Tests
###############################################################################

def test_get_class_list(uml_model):
    class_list = uml_model._get_class_list()
    assert isinstance(class_list, dict)
    assert len(class_list) == 0

def test_get_relationship_list(uml_model):
    relationship_list = uml_model._get_relationship_list()
    assert isinstance(relationship_list, list)
    assert len(relationship_list) == 0

def test_get_storage_manager(uml_model):
    storage_manager = uml_model._get_storage_manager()
    assert storage_manager is not None

###############################################################################
# Static Methods Tests
###############################################################################

def test_create_class(uml_model):
    created_class = UMLModel.create_class("TestClass")
    assert isinstance(created_class, UMLClass)
    assert created_class._get_class_name() == "TestClass"

def test_create_field(uml_model):
    created_field = UMLModel.create_field("int", "TestField")
    assert isinstance(created_field, UMLField)
    assert created_field._get_type() == "int"
    assert created_field._get_name() == "TestField"

def test_create_method(uml_model):
    created_method = UMLModel.create_method("void", "TestMethod")
    assert isinstance(created_method, UMLMethod)
    assert created_method._get_type() == "void"
    assert created_method._get_name() == "TestMethod"

def test_create_parameter(uml_model):
    created_parameter = UMLModel.create_parameter("int", "TestParam")
    assert isinstance(created_parameter, UMLParameter)
    assert created_parameter._get_type() == "int"
    assert created_parameter._get_parameter_name() == "TestParam"

def test_create_relationship(uml_model):
    created_relationship = UMLModel.create_relationship("ClassA", "ClassB", "inheritance")
    assert isinstance(created_relationship, UMLRelationship)
    assert created_relationship._get_source_class() == "ClassA"
    assert created_relationship._get_destination_class() == "ClassB"
    assert created_relationship._get_type() == "inheritance"

###############################################################################
# Class Management Tests
###############################################################################

def test_add_class(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    result = uml_model._add_class(class_name="NewClass", is_loading=False)
    assert result is True
    assert "NewClass" in uml_model._get_class_list()
    assert len(sample_observer.events) == 1
    assert sample_observer.events[0]["event_type"] == "add_class"

def test_delete_class(uml_model, sample_class, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    result = uml_model._delete_class(class_name="TestClass")
    assert result is True
    assert "TestClass" not in uml_model._get_class_list()
    assert len(sample_observer.events) == 2
    assert sample_observer.events[0]["event_type"] == "add_class"
    assert sample_observer.events[1]["event_type"] == "delete_class"


def test_rename_class(uml_model, sample_class, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    result = uml_model._rename_class(current_name="TestClass", new_name="RenamedClass")
    assert result is True
    assert "RenamedClass" in uml_model._get_class_list()
    assert "TestClass" not in uml_model._get_class_list()
    assert len(sample_observer.events) == 2
    assert sample_observer.events[0]["event_type"] == "add_class"
    assert sample_observer.events[1]["event_type"] == "rename_class"

###############################################################################
# Field Management Tests
###############################################################################

def test_add_field(uml_model, sample_class, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    result = uml_model._add_field(class_name="TestClass", type="string", field_name="newField", is_loading=False)
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 1
    assert fields[0]._get_name() == "newField"
    assert fields[0]._get_type() == "string"
    assert len(sample_observer.events) == 2
    assert sample_observer.events[1]["event_type"] == "add_field"

###############################################################################
# File Handling Tests (Mocking save/load)
###############################################################################

def test_save_and_load_diagram(uml_model, tmp_path):
    save_path = tmp_path / "test_diagram.json"
    
    # Save and load functionality would be implemented as needed
    # You can test the file handling with real save/load methods here