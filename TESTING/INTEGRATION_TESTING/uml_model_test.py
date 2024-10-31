import sys
import os
import pytest
from rich.console import Console
from unittest.mock import patch

def test_delete_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", type="int", method_name="testMethod", is_loading=False)
    
    # Use patch to simulate user input for method selection
    with patch("builtins.input", return_value="1"):  # Simulates selecting the first method
        # Delete the method from the class
        result = uml_model._delete_method(class_name="TestClass")
    
    # Check if method was successfully deleted
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    methods = class_data._get_method_and_parameters_list()
    assert len(methods) == 0  # Ensure method list is now empty
    
    # Check that observers were notified
    assert len(sample_observer.events) == 3  # Expecting add_class, add_method, delete_method events
    assert sample_observer.events[2]["event_type"] == "delete_method"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod"
    }


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
from UML_MVC.UML_CONTROLLER.uml_storage_manager import UMLStorageManager  # Corrected import

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

        def _update(self, event_type=None, data=None, is_loading=None, is_undo_or_redo=None):
            self.events.append({
                "event_type": event_type,
                "data": data,
                "is_loading": is_loading,
                "is_undo_or_redo": is_undo_or_redo
            })

    return TestObserver()


###############################################################################
# Initialization
###############################################################################
def test_uml_model_init():
    
    view = UMLView()  
    console = Console()  # Using Rich's Console
    
    # Create UMLModel instance
    uml_model = UMLModel(view=view, console=console)
    
    # Verify attributes are correctly initialized
    assert uml_model._UMLModel__user_view == view
    assert uml_model._UMLModel__console == console
    assert isinstance(uml_model._UMLModel__class_list, dict)
    assert isinstance(uml_model._UMLModel__storage_manager, UMLStorageManager)  # Corrected to UMLStorageManager
    assert isinstance(uml_model._UMLModel__relationship_list, list)
    assert isinstance(uml_model._UMLModel__main_data, dict)
    assert isinstance(uml_model._observers, list)


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
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Add field to the class
    result = uml_model._add_field(class_name="TestClass", field_type="string", field_name="newField", is_loading=False)
    assert result is True
    
    # Verify the field was added
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 1
    assert fields[0]._get_name() == "newField"
    assert fields[0]._get_type() == "string"
    
    # Verify observer notification
    assert len(sample_observer.events) == 2  # add_class and add_field events
    assert sample_observer.events[1]["event_type"] == "add_field"
    assert sample_observer.events[1]["data"] == {
        "class_name": "TestClass",
        "type": "string",
        "field_name": "newField"
    }
    assert sample_observer.events[1]["is_undo_or_redo"] is False


def test_delete_field(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and field to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    
    # Delete the field
    result = uml_model._delete_field(class_name="TestClass", field_name="testField")
    assert result is True
    
    # Verify the field was deleted
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 0
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_field, delete_field events
    assert sample_observer.events[2]["event_type"] == "delete_field"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "field_name": "testField"
    }
    assert sample_observer.events[2]["is_undo_or_redo"] is False


def test_rename_field(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and field to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    
    # Rename the field
    result = uml_model._rename_field(class_name="TestClass", old_field_name="testField", new_field_name="renamedField")
    assert result is True
    
    # Verify the field was renamed
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 1
    assert fields[0]._get_name() == "renamedField"
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_field, rename_field events
    assert sample_observer.events[2]["event_type"] == "rename_field"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "old_field_name": "testField",
        "new_field_name": "renamedField"
    }
    assert sample_observer.events[2]["is_undo_or_redo"] is False
    
###############################################################################
# Method Management Tests
###############################################################################

from unittest.mock import patch

def test_add_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Add method to the class
    result = uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Check if method was successfully added
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    methods = class_data._get_method_and_parameters_list()
    assert len(methods) == 1
    assert list(methods[0].keys())[0]._get_name() == "testMethod"
    
    # Check that observers were notified
    assert len(sample_observer.events) == 2  # Expecting add_class and add_method events
    assert sample_observer.events[1]["event_type"] == "add_method"
    assert sample_observer.events[1]["data"] == {
        "class_name": "TestClass",
        "type": "int",
        "method_name": "testMethod"
    }

def test_check_method_param_list(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="existingMethod", is_loading=False)
    
    # Prepare a new method with the same name and parameter list to check for duplicates
    existing_methods = uml_model._get_class_list()["TestClass"]._get_method_and_parameters_list()
    duplicate_method = uml_model.create_method(method_type="void", method_name="existingMethod")
    
    # Attempt to add a duplicate method
    result = uml_model._check_method_param_list("TestClass", {duplicate_method: []})
    assert result is False  # Should return False due to duplicate
    
    # Verify observer notifications
    assert len(sample_observer.events) == 2  # add_class and add_method events
    assert sample_observer.events[1]["event_type"] == "add_method"
    assert sample_observer.events[1]["data"]["method_name"] == "existingMethod"

def test_delete_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Use patch to simulate user input for method selection
    with patch("builtins.input", return_value="1"):  # Simulates selecting the first method
        # Delete the method from the class
        result = uml_model._delete_method(class_name="TestClass", method_num="1")
    
    # Check if method was successfully deleted
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    methods = class_data._get_method_and_parameters_list()
    assert len(methods) == 0  # Ensure method list is now empty
    
    # Check that observers were notified
    assert len(sample_observer.events) == 3  # Expecting add_class, add_method, delete_method events
    assert sample_observer.events[2]["event_type"] == "delete_method"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod"
    }

def test_rename_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)
    
    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and verify the renaming
        result = uml_model._rename_method(class_name="TestClass", method_num="1", new_name="newMethod")
        
    # Check if renaming was successful
    assert result is True  # Should return True if renaming is successful
    
    # Check if the method name has been updated
    class_data = uml_model._get_class_list()["TestClass"]
    renamed_method = list(class_data._get_method_and_parameters_list()[0].keys())[0]
    assert renamed_method._get_name() == "newMethod"  # Should reflect the new name
    
    # Verify observer notifications
    assert len(sample_observer.events) == 3  # add_class, add_method, and rename_method events
    assert sample_observer.events[2]["event_type"] == "rename_method"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "old_method_name": "oldMethod",
        "new_method_name": "newMethod"
    }

###############################################################################
# Parameter
###############################################################################

from unittest.mock import patch

def test_add_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Add parameter with method_num
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Check if parameter was added successfully
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    method_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(method_params) == 1
    assert method_params[0]._get_parameter_name() == "param1"
    assert method_params[0]._get_type() == "int"
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_method, add_param
    assert sample_observer.events[2]["event_type"] == "add_param"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "param_name": "param1",
        "type": "int"
    }

def test_delete_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Delete the parameter
    result = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="param1")
    
    # Ensure parameter deletion succeeded
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    method_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(method_params) == 0  # parameter list should be empty after deletion
    
    # Verify observer notification
    assert len(sample_observer.events) == 4  # add_class, add_method, add_param, delete_param
    assert sample_observer.events[3]["event_type"] == "delete_param"
    assert sample_observer.events[3]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "param_name": "param1",
        "param_type": "int"
    }

def test_rename_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="TestClass", method_num="1", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was successful
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    renamed_param = list(class_data._get_method_and_parameters_list()[0].values())[0][0]
    assert renamed_param._get_parameter_name() == "newParam"
    
    # Verify observer notification
    assert len(sample_observer.events) == 4  # add_class, add_method, add_param, rename_param
    assert sample_observer.events[3]["event_type"] == "rename_param"
    assert sample_observer.events[3]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "old_param_name": "param1",
        "new_param_name": "newParam"
    }

def test_replace_param_list(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Replace the parameter list with new parameters
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=["int newParam1", "float newParam2"])
    
    # Ensure replacement was successful
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    new_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(new_params) == 2
    assert new_params[0]._get_parameter_name() == "newParam1"
    assert new_params[1]._get_parameter_name() == "newParam2"
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_method, replace_param
    assert sample_observer.events[2]["event_type"] == "replace_param"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "new_list": new_params
    }


###############################################################################
# RELATIONSHIP
###############################################################################

def test_add_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add two classes to create a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    
    
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Verify that the relationship was added
    relationships = uml_model._get_relationship_list()
    assert len(relationships) == 1
    assert relationships[0]._get_source_class() == "ClassA"
    assert relationships[0]._get_destination_class() == "ClassB"
    assert relationships[0]._get_type() == "Aggregation"
    
    # Verify observer notifications
    assert len(sample_observer.events) == 3  # add_class x2 and add_relationship
    assert sample_observer.events[2]["event_type"] == "add_rel"
    assert sample_observer.events[2]["data"] == {
        "source": "ClassA",
        "dest": "ClassB",
        "type": "Aggregation"
    }

def test_delete_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Delete the relationship
    result = uml_model._delete_relationship("ClassA", "ClassB")
    assert result is True  # Relationship deletion successful
    
    # Verify the relationship list is empty
    relationships = uml_model._get_relationship_list()
    assert len(relationships) == 0
    
    # Verify observer notifications
    assert len(sample_observer.events) == 4  # add_class x2, add_relationship, delete_relationship
    assert sample_observer.events[3]["event_type"] == "delete_rel"
    assert sample_observer.events[3]["data"] == {
        "source": "ClassA",
        "dest": "ClassB"
    }

def test_change_relationship_type(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA", "ClassB", "Composition")
    assert result is True  # Type change successful
    
    # Verify the relationship type was updated
    relationships = uml_model._get_relationship_list()
    assert relationships[0]._get_type() == "Composition"
    
    # Verify observer notifications
    assert len(sample_observer.events) == 4  # add_class x2, add_relationship, type_mod
    assert sample_observer.events[3]["event_type"] == "edit_rel_type"
    assert sample_observer.events[3]["data"] == {
        "source": "ClassA",
        "dest": "ClassB",
        "new_type": "Composition"
    }

###############################################################################
# CLASS HELPER FUNCTIONS
###############################################################################

def test_private_class_exists(uml_model):
    # Add a class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Directly test the private __class_exists method
    assert uml_model._UMLModel__class_exists("TestClass") == True
    assert uml_model._UMLModel__class_exists("NonExistentClass") == False

from unittest.mock import patch

def test_private_validate_class_existence(uml_model):
    # Add a class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Test for existing class
    with patch.object(uml_model._console, "print") as mock_console:
        assert uml_model._UMLModel__validate_class_existence("TestClass", should_exist=True) == True
        mock_console.assert_not_called()  # No error message
    
    # Test for non-existing class
    with patch.object(uml_model._console, "print") as mock_console:
        assert uml_model._UMLModel__validate_class_existence("NonExistentClass", should_exist=True) == False
        mock_console.assert_called_once_with("\n[bold red]Class [bold white]'NonExistentClass'[/bold white] does not exist![/bold red]")
