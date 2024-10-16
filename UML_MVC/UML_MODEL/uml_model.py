###################################################################################################
"""
Module: UMLModel
This module defines the UMLModel class, which manages the core data for a UML diagram, including classes,
fields, methods, parameters, and relationships. It also implements the Observer design pattern to notify
observers (such as views) about changes in the UML data. This model interacts with the storage manager 
to handle save/load functionality and provides static methods for creating UML components.
"""
###################################################################################################

import re
import os
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_MVC.UML_CONTROLLER.uml_storage_manager import UMLStorageManager as Storage
from UML_ENUM_CLASS.uml_enum import InterfaceOptions, RelationshipType
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_grid import GridGraphicsView as GUIView
# Get the root directory where the main.py file exists
root_directory = os.path.dirname(os.path.abspath(__file__))  # This gets the current script's directory
root_directory = os.path.abspath(os.path.join(root_directory, "..", ".."))  # Move to the root directory (where main.py is)

###################################################################################################

class UMLModel:
    
    """
    UMLModel class serves as the data manager for UML diagrams. It manages the UML components such as 
    classes, fields, methods, parameters, and relationships. The model also implements the Observer 
    pattern to update any attached observers (e.g., views) when changes occur.
    """
    
    #################################################################
    
    # UML Class Manager Constructor #
    
    def __init__(self, view, console):    
        """
        Initializes the UMLModel with the provided view and console. Sets up internal structures
        for managing UML classes, relationships, and observers. Also initializes the storage manager 
        for saving/loading UML diagrams.

        Args:
            view: The view instance that presents data to the user.
            console: The console instance for displaying output via Rich.
        """
        self.__user_view = view
        self.__console = console   
        self.__class_list: Dict[str, Class] = {}
        self.__storage_manager: Storage = Storage()
        self.__relationship_list: List[Relationship] = []
        self.__main_data: Dict = {"classes":[], "relationships":[]}
        self._observers = [] # For observer design pattern
                    
    #################################################################
      
    # Observer management methods
    def _attach_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def _detach_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers (self, event_type=None, data=None, is_loading=None):
        for observer in self._observers:
            observer._update(event_type, data, is_loading)
    
    #################################################################
        
    # Getters #
        
    def _get_class_list(self) -> Dict[str, Class]:
        return self.__class_list
    
    def _get_storage_manager(self) -> Storage:
        return self.__storage_manager
    
    def _get_relationship_list(self) -> List[Relationship]:
        return self.__relationship_list
    
    def _get_main_data(self) -> Dict:
        return self.__main_data
    
    def _get_user_view(self):
        return self.__user_view
        
    #################################################################
    ### STATIC FUNCTIONS ###

    # Class creation method #
    @staticmethod
    def create_class(class_name: str) -> Class:
        return Class(class_name)
    
    # Field creation method #
    @staticmethod
    def create_field(field_name: str) -> Field:
        return Field(field_name)
    
    # Method creation method #
    @staticmethod
    def create_method(method_name: str) -> Method:
        return Method(method_name)
    
    # Parameter creation method #
    @staticmethod
    def create_parameter(parameter_name: str) -> Parameter:
        return Parameter(parameter_name)
    
    # Relationship creation method #
    @staticmethod
    def create_relationship(source_class: str, destination_class: str, rel_type: str) -> Relationship:
        return Relationship(source_class, destination_class, rel_type)
    
    #################################################################
    """
    Module: UMLModel (Member Functions)
    This module defines the detailed member functions for the UMLModel class, which handles the management 
    of UML classes, fields, methods, parameters, and relationships. It uses the observer pattern to notify 
    the attached views about changes to the UML model and provides various functions for adding, deleting, 
    and modifying UML components.
    """
    #################################################################
    
    ### MEMBER FUNCTIONS ###

    ## CLASS RELATED ##
    
    # Add class #
    def _add_class(self, class_name: str, is_loading: bool) -> bool:
        """
        Adds a new UML class to the class list. If the class already exists, no action is taken.
        Notifies observers of the addition event.

        Args:
            class_name (str): The name of the class to be added.
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class already exists
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=False)
        # If the class already exists, exit the function
        if not is_class_exist:
            return False
        # Create a new class and add it to the class list
        new_class = self.create_class(class_name)
        self.__class_list[class_name] = new_class
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.ADD_CLASS.value, data={"class_name": class_name}, is_loading=is_loading)
        return True
    
    # Delete class #
    def _delete_class(self, class_name: str):
        """
        Deletes a UML class from the class list. Also removes any relationships involving the class.
        Notifies observers of the deletion event.

        Args:
            class_name (str): The name of the class to be deleted.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class exists
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=True)
        # If the class does not exist, exit the function
        if not is_class_exist:
            return False
        # Remove the class from the class list
        self.__class_list.pop(class_name)
        # Clean up any relationships involving the class
        self.__clean_up_relationship(class_name)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.DELETE_CLASS.value, data={"class_name": class_name})
        return True
        
    # Rename class #
    def _rename_class(self, current_name: str, new_name: str):
        """
        Renames an existing UML class. Updates any associated relationships and notifies observers
        of the renaming event.

        Args:
            current_name (str): The current name of the class.
            new_name (str): The new name for the class.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(current_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Current class name [bold white]'{current_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(new_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]New class name [bold white]'{new_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if renaming is possible (class name validation)
        is_able_to_rename = self.__check_class_rename(current_name, new_name)
        if not is_able_to_rename:
            return False
        # Rename the class and update the class list
        class_object = self.__class_list[current_name]
        class_object._set_class_name(new_name)
        self.__class_list[new_name] = self.__class_list.pop(current_name)
        # Update the class name in the relationships
        self.__update_name_in_relationship(current_name, new_name)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.RENAME_CLASS.value, data={"old_name": current_name, "new_name": new_name})
        return True
        
    ## FIELD RELATED ##
    
    # Add field #
    def _add_field(self, class_name: str, field_name: str, is_loading: bool):
        """
        Adds a new field to a UML class. Notifies observers of the field addition event.

        Args:
            class_name (str): The name of the class to which the field will be added.
            field_name (str): The name of the field to be added.
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(field_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Field name [bold white]'{field_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if both the class and the field do not already exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=False)
        if not is_class_and_field_exist:
            return False
        # Retrieve the class and add the new field to its field list
        class_object = self.__class_list[class_name]
        field_list = class_object._get_class_field_list()
        new_field = self.create_field(field_name)
        field_list.append(new_field)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.ADD_FIELD.value, data={"class_name": class_name, "field_name": field_name}, is_loading=is_loading)
        return True
        
    # Delete field #
    def _delete_field(self, class_name: str, field_name: str):
        """
        Deletes an existing field from a UML class. Notifies observers of the field deletion event.

        Args:
            class_name (str): The name of the class from which the field will be deleted.
            field_name (str): The name of the field to be deleted.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if both the class and the field exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=True)
        if not is_class_and_field_exist:
            return False
        # Remove the field from the class's field list
        class_object = self.__class_list[class_name]
        field_list = class_object._get_class_field_list()
        chosen_field = self.__get_chosen_field_or_method(class_name, field_name, is_field=True)
        field_list.remove(chosen_field)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.DELETE_FIELD.value, data={"class_name": class_name, "field_name": field_name})
        return True
        
    # Rename field #
    def _rename_field(self, class_name: str, current_field_name: str, new_field_name: str):
        """
        Renames an existing field in a UML class. Notifies observers of the field renaming event.

        Args:
            class_name (str): The name of the class containing the field.
            current_field_name (str): The current name of the field.
            new_field_name (str): The new name for the field.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(current_field_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Current Field name [bold white]'{current_field_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(new_field_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]New field name [bold white]'{new_field_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if renaming is possible (field name validation)
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_field_name, new_field_name, is_field=True)
        if not is_able_to_rename:
            return False
        # Rename the field in the class
        chosen_field = self.__get_chosen_field_or_method(class_name, current_field_name, is_field=True)
        chosen_field._set_name(new_field_name)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.RENAME_FIELD.value, data={"class_name": class_name, "old_field_name": current_field_name, "new_field_name": new_field_name})
        return True
        
    ## METHOD RELATED ##
    
    # Add method #
    def _add_method(self, class_name: str, method_name: str, is_loading: bool):
        """
        Adds a new method to a UML class. Notifies observers of the method addition event.

        Args:
            class_name (str): The name of the class to which the method will be added.
            method_name (str): The name of the method to be added.
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class exists and the method does not already exist
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=False)
        if not is_class_and_method_exist:
            return False
        # Add the new method to the class's method list
        class_object = self.__class_list[class_name]
        method_list = class_object._get_class_method_list()
        new_method = self.create_method(method_name)
        method_list.append(new_method)
        # Initialize an empty parameter list for the new method
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        method_and_parameter_list[method_name] = []
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.ADD_METHOD.value, data={"class_name": class_name, "method_name": method_name}, is_loading=is_loading)
        return True
        
    # Delete method #
    def _delete_method(self, class_name: str, method_name: str):
        """
        Deletes an existing method from a UML class. Notifies observers of the method deletion event.

        Args:
            class_name (str): The name of the class from which the method will be deleted.
            method_name (str): The name of the method to be deleted.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if both the class and the method exist
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return False
        # Remove the method from the class's method list
        class_object = self.__class_list[class_name]
        method_list = class_object._get_class_method_list()
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list.pop(method_name)
        chosen_method = self.__get_chosen_field_or_method(class_name, method_name, is_field=False)
        method_list.remove(chosen_method)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.DELETE_METHOD.value, data={"class_name": class_name, "method_name": method_name})
        return True
        
    # Rename method #
    def _rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        """
        Renames an existing method in a UML class. Notifies observers of the method renaming event.

        Args:
            class_name (str): The name of the class containing the method.
            current_method_name (str): The current name of the method.
            new_method_name (str): The new name for the method.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(current_method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Current method name [bold white]'{current_method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(new_method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]New method name [bold white]'{new_method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if renaming is possible (method name validation)
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_method_name, new_method_name, is_field=False)
        if not is_able_to_rename:
            return False
        # Rename the method in the class and update the method list
        class_object = self.__class_list[class_name]
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list[new_method_name] = method_and_parameter_list.pop(current_method_name)
        chosen_method = self.__get_chosen_field_or_method(class_name, current_method_name, is_field=False)
        chosen_method._set_name(new_method_name)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.RENAME_METHOD.value, data={"class_name": class_name, "old_method_name": current_method_name, "new_method_name": new_method_name})
        return True

    ## PARAMETER RELATED ##
    
    # Add parameter #
    def _add_parameter(self, class_name: str, method_name: str, parameter_name: str, is_loading: bool):
        """
        Adds a new parameter to a method in a UML class. Notifies observers of the parameter addition event.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method to which the parameter will be added.
            parameter_name (str): The name of the parameter to be added.
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(parameter_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Parameter name [bold white]'{parameter_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class, method, and parameter do not already exist
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name, parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False)
        if not is_class_and_method_and_parameter_exist:
            return False
        # Add the new parameter to the method's parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        new_parameter = self.create_parameter(parameter_name)
        method_and_parameter_list[method_name].append(new_parameter)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.ADD_PARAM.value, data={"class_name": class_name, "method_name": method_name, "param_name": parameter_name}, is_loading=is_loading)
        return True
        
    # Delete parameter #
    def _delete_parameter(self, class_name: str, method_name: str, parameter_name: str):
        """
        Deletes an existing parameter from a method in a UML class. Notifies observers of the parameter deletion event.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method from which the parameter will be deleted.
            parameter_name (str): The name of the parameter to be deleted.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(parameter_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Parameter name [bold white]'{parameter_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class, method, and parameter exist
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name, parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True)
        if not is_class_and_method_and_parameter_exist:
            return False
        # Remove the parameter from the method's parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, parameter_name)
        method_and_parameter_list[method_name].remove(chosen_parameter)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.DELETE_PARAM.value, data={"class_name": class_name, "method_name": method_name, "param_name": parameter_name})
        return True

    # Rename parameter #
    def _rename_parameter(self, class_name: str, method_name: str, current_parameter_name: str, new_parameter_name: str):
        """
        Renames an existing parameter in a method of a UML class. Notifies observers of the parameter renaming event.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method containing the parameter.
            current_parameter_name (str): The current name of the parameter.
            new_parameter_name (str): The new name for the parameter.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(current_parameter_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Current parameter name [bold white]'{new_parameter_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(new_parameter_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]New parameter name [bold white]'{new_parameter_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        
        # Validate that the class, method, and current parameter exist, and that the new parameter does not already exist
        is_class_and_method_and_current_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name, parameter_name=current_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True)
        is_new_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name, parameter_name=new_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False)
        if not is_class_and_method_and_current_parameter_exist or not is_new_parameter_exist:
            return False
        # Rename the parameter
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, current_parameter_name)
        chosen_parameter._set_parameter_name(new_parameter_name)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.RENAME_PARAM.value, data={"class_name": class_name, "method_name": method_name, "old_param_name": current_parameter_name, "new_param_name": new_parameter_name})
        return True
        
    # Replace parameter list #
    def _replace_param_list(self, class_name: str, method_name: str):
        """
        Replaces the parameter list for a method in a UML class. The user is prompted to enter the new parameter names.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method whose parameter list will be replaced.
        """
        # Check valid input #
        is_input_valid = self._is_valid_input(class_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Class name [bold white]'{class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(method_name)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Method name [bold white]'{method_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check if the class and method exist
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return 
        # Prompt the user to input new parameter names
        self.__console.print("\n[bold yellow]Enter the names for the new parameter list, each name must be separated by spaces:[/bold yellow]\n\n[bold white]==>[/bold white] ")
        user_input = input()
        new_param_name_list = user_input.split()
        # Check for duplicate parameter names
        unique_param_names = list(set(new_param_name_list))
        for param in unique_param_names:
            # Check valid input #
            is_input_valid = self._is_valid_input(param)
            if not is_input_valid:
                self.__console.print(f"\n[bold red]Parameter name [bold white]'{param}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
                return
        if len(unique_param_names) != len(new_param_name_list):
            self.__console.print("\n[bold red]Duplicate parameters detected:[/bold red]")
            duplicates = [param for param in new_param_name_list if new_param_name_list.count(param) > 1]
            self.__console.print(f"\n[bold red]Duplicates: [bold white]{set(duplicates)}[/bold white][/bold red]")
            self.__console.print("\n[bold red]Please modify the parameter list manually to ensure uniqueness.[/bold red]")
            return 
        # Create parameter objects for the new list and replace the old list
        new_param_list: List[Parameter] = []
        for param_name in new_param_name_list:
            new_param = self.create_parameter(param_name)
            new_param_list.append(new_param)
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        method_and_parameter_list[method_name] = new_param_list
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.REPLACE_PARAM.value, data={"class_name": class_name, "method_name": method_name, "new_list": new_param_list})
        return 
    
    def _replace_param_list_gui(self, class_name: str, method_name: str, new_param_name_list: List):
        # Check if the class and method exist
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return False
        new_param_list: List[Parameter] = []
        for param_name in new_param_name_list:
            new_param = self.create_parameter(param_name)
            new_param_list.append(new_param)
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        method_and_parameter_list[method_name] = new_param_list
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.REPLACE_PARAM.value, data={"class_name": class_name, "method_name": method_name, "new_list": new_param_list})
        return True
        

    ## RELATIONSHIP RELATED ##
    
    # Add relationship wrapper #
    def _add_relationship_wrapper(self, is_loading: bool):
        """
        Wrapper method for adding a new relationship between UML classes. Prompts the user to input 
        the source class, destination class, and relationship type.

        Args:
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        if len(self.__class_list) == 0:
            self.__console.print("\n[bold red]No class exists![/bold red]")
            return
        # Prompt the user for input
        self.__console.print("\n[bold yellow]Type [bold white]'<source_class> <destination_class> <type>'[/bold white] or type [bold white]'quit'[/bold white] to return to main menu[/bold yellow]")
        self.__user_view._display_type_enum()
        self.__user_view._display_class_names(self.__main_data)
        self.__user_view._display_relationships(self.__main_data)
        self.__console.print("\n[bold yellow]==>[/bold yellow] ", end="")
        user_input: str = input()
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled adding relationship[/bold green]")
            return
        # Parse user input and validate the relationship
        user_input_component = user_input.split()
        source_class_name = user_input_component[0]
        destination_class_name = user_input_component[1] if len(user_input_component) > 1 else None
        type = user_input_component[2] if len(user_input_component) > 2 else None
        # Check valid input #
        is_source_valid = self._is_valid_input(source_class_name)
        if not is_source_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{source_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_dest_valid = self._is_valid_input(destination_class_name)
        if not is_dest_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{destination_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_dest_valid = self._is_valid_input(type)
        if not is_dest_valid:
            self.__console.print(f"\n[bold red]Type name [bold white]'{type}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        if source_class_name and destination_class_name and type:
            # Validate class and relationship existence
            is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
            is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
            if not is_source_class_exist or not is_destination_class_exist:
                return
            # Check if the relationship already exists
            is_relationship_exist = self._relationship_exist(source_class_name, destination_class_name)
            if is_relationship_exist:
                self.__console.print(f"\n[bold red]Relationship between class [bold white]'{source_class_name}'[/bold white] and class [bold white]'{destination_class_name}'[/bold white] already exists![/bold red]")
                return
            # Validate relationship type
            is_type_exist = self.__validate_type_existence(type, should_exist=True)
            if not is_type_exist:
                return
            # Add the new relationship
            self._add_relationship(source_class_name, destination_class_name, type, is_loading)
        else:
            self.__console.print("\n[bold red]Wrong format! Please try again![/bold red]")
            
    # Add relationship #
    def _add_relationship(self, source_class_name: str, destination_class_name: str, rel_type: str, is_loading: bool, is_gui: bool=None):
        """
        Adds a new relationship between two UML classes. Notifies observers of the relationship addition event.

        Args:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
            rel_type (str): The type of the relationship (e.g., aggregation, composition).
            is_loading (bool): Flag indicating whether the operation is part of loading saved data.
        """
        if is_gui:
            # Validate class and relationship existence
            is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
            is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
            if not is_source_class_exist or not is_destination_class_exist:
                return False
            # Check if the relationship already exists
            is_relationship_exist = self._relationship_exist(source_class_name, destination_class_name)
            if is_relationship_exist:
                return False
            # Validate relationship type
            is_type_exist = self.__validate_type_existence(rel_type, should_exist=True)
            if not is_type_exist:
                return False
        # Create a new relationship and add it to the relationship list
        new_relationship = self.create_relationship(source_class_name, destination_class_name, rel_type)
        self.__relationship_list.append(new_relationship)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.ADD_REL.value, data={"source": source_class_name, "dest": destination_class_name, "type": rel_type}, is_loading=is_loading)
        return True
        
    # Delete relationship #
    def _delete_relationship(self, source_class_name: str, destination_class_name: str) -> bool | str:
        """
        Deletes an existing relationship between two UML classes. Notifies observers of the relationship deletion event.

        Args:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
        """
        # Check valid input #
        is_source_valid = self._is_valid_input(source_class_name)
        if not is_source_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{source_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_dest_valid = self._is_valid_input(destination_class_name)
        if not is_dest_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{destination_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Validate class existence and relationship
        is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        if not is_source_class_exist:
            return False
        if not is_destination_class_exist:
            return False
        is_relationship_exist = self._relationship_exist(source_class_name, destination_class_name)
        if not is_relationship_exist:
            self.__console.print(f"\n[bold red]Relationship between class [bold white]'{source_class_name}'[/bold white] and class [bold white]'{destination_class_name}'[/bold white] does not exist![bold red]")
            return False
        # Delete the relationship
        current_relationship = self._get_chosen_relationship(source_class_name, destination_class_name)
        self.__relationship_list.remove(current_relationship)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.DELETE_REL.value, data={"source": source_class_name, "dest": destination_class_name})
        return True
        
    # Change type #
    def _change_type(self, source_class_name: str, destination_class_name: str, new_type: str):
        """
        Changes the type of an existing relationship between two UML classes. Notifies observers of the type modification event.

        Args:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
            new_type (str): The new type for the relationship (e.g., change from aggregation to composition).
        """
        # Check valid input #
        is_source_valid = self._is_valid_input(source_class_name)
        if not is_source_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{source_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_dest_valid = self._is_valid_input(destination_class_name)
        if not is_dest_valid:
            self.__console.print(f"\n[bold red]Source class name [bold white]'{destination_class_name}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        # Check valid input #
        is_input_valid = self._is_valid_input(new_type)
        if not is_input_valid:
            self.__console.print(f"\n[bold red]Type name [bold white]'{new_type}'[/bold white] is invalid! Only allow a-zA-Z, number, and underscore![/bold red]")
            return
        is_source_class_name_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        is_destination_class_name_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        if not is_source_class_name_exist or not is_destination_class_name_exist:
            return False
        # Check if the new type is the same as the current type
        current_type = self._get_chosen_relationship_type(source_class_name, destination_class_name)
        if current_type == new_type:
            self.__console.print(f"\n[bold red]New type [bold white]'{new_type}'[/bold white] is identical to the existing type of the current relationship![/bold red]")
            return False
        # Validate new type existence
        is_type_exist = self.__validate_type_existence(new_type, should_exist=True)
        if not is_type_exist:
            return False
        # Update the relationship type
        current_relationship = self._get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is None:
            return False
        current_relationship._set_type(new_type)
        # Update main data and notify observers
        self._update_main_data_for_every_action()
        self._notify_observers(event_type=InterfaceOptions.TYPE_MOD.value, data={"source": source_class_name, "dest": destination_class_name, "new_type": new_type})
        return True
         
    #################################################################    
    ### HELPER FUNCTIONS ###  

    ## CLASS RELATED ## 

    # Validate if the class name exists in the class list #
    def __class_exists(self, class_name: str) -> bool:
        """
        Checks if the specified class name exists in the class list.

        Args:
            class_name (str): The name of the class to check.

        Returns:
            bool: True if the class exists, False otherwise.
        """
        return class_name in self.__class_list
    
    # Validate class name based on whether it should exist or not #
    def __validate_class_existence(self, class_name: str, should_exist: bool) -> bool:
        """
        Validates the existence of a class name based on the expected existence (should_exist).
        If the class should exist but does not, or if it should not exist but does, the method prints an error message.

        Args:
            class_name (str): The name of the class to validate.
            should_exist (bool): True if the class is expected to exist, False if it should not exist.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        # When class name should exist but it does not
        is_class_name_exist = self.__class_exists(class_name)
        if should_exist and not is_class_name_exist:
            self.__console.print(f"\n[bold red]Class [bold white]'{class_name}'[/bold white] does not exist![/bold red]")
            return False
        # When class name should not exist but it does
        elif not should_exist and is_class_name_exist:
            self.__console.print(f"\n[bold red]Class [bold white]'{class_name}'[/bold white] has already existed![/bold red]")
            return False
        # Return True in any other cases
        return True

    # Check if we are able to rename class #
    def __check_class_rename(self, current_class_name: str, new_class_name: str) -> bool:
        """
        Checks whether the class can be renamed by validating the existence of both the current class name and
        the new class name. Ensures that the current class exists and the new class name does not exist.

        Args:
            current_class_name (str): The current name of the class.
            new_class_name (str): The proposed new name for the class.

        Returns:
            bool: True if renaming is possible, False otherwise.
        """
        # Check if current class name exists or not
        is_current_class_name_exist = self.__validate_class_existence(current_class_name, should_exist=True)
        if not is_current_class_name_exist:
            return False
        # Check if new class name exists or not
        is_new_class_name_exist = self.__validate_class_existence(new_class_name, should_exist=False)
        if not is_new_class_name_exist:
            return False
        return True
    
    # Clean Up Relationship #
    def __clean_up_relationship(self, class_name: str):
        """
        Cleans up relationships by removing any relationships where the specified class is either the source or 
        destination. This is useful when deleting a class.

        Args:
            class_name (str): The name of the class to clean relationships for.
        """
        # Create a new list that excludes relationships with dest or source equal to class_name
        relationship_list = self.__relationship_list
        relationship_list[:] = [
            relationship
            for relationship in relationship_list
            if relationship._get_source_class() != class_name and relationship._get_destination_class() != class_name
        ]
    
    # Update source/destination class name when we rename a class name #
    def __update_name_in_relationship(self, current_name: str, new_name: str):
        """
        Updates the source or destination class name in existing relationships when a class is renamed.

        Args:
            current_name (str): The current class name.
            new_name (str): The new class name to update in relationships.
        """
        # Get relationship list
        relationship_list = self.__relationship_list
        # Loop through the relationship list
        for each_relationship in relationship_list:
            source_name = each_relationship._get_source_class()
            destination_name = each_relationship._get_destination_class()
            if source_name == current_name:
                each_relationship._set_source_class(new_name)
            if destination_name == current_name:
                each_relationship._set_destination_class(new_name)
                
    # Get method and parameter list of a chosen class #
    def _get_method_and_parameter_list(self, class_name: str) -> Dict[str, List[Parameter]] | None:
        """
        Retrieves the method and parameter list of a specified class.

        Args:
            class_name (str): The name of the class to retrieve the method and parameter list for.

        Returns:
            Dict[str, List[Parameter]] | None: The method and parameter list, or None if the class does not exist.
        """
        is_class_name_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_name_exist:
            return None
        return self.__class_list[class_name]._get_method_and_parameters_list()
    
    ## FIELD AND METHOD RELATED ##
    
    # Check field/method name exist or not #
    def __field_or_method_exist(self, class_name: str, input_name: str, is_field: bool) -> bool:
        """
        Checks if a field or method exists in the specified class.

        Args:
            class_name (str): The name of the class.
            input_name (str): The name of the field or method to check.
            is_field (bool): True if checking for a field, False if checking for a method.

        Returns:
            bool: True if the field or method exists, False otherwise.
        """
        # Check if class exists
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on whether it's a field or method
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        # Loop through the list to find the field or method
        for element in general_list:
            current_name = element._get_name()
            if current_name == input_name:
                return True
        return False
    
    # Validate field existence based on whether it should exist or not #
    def __validate_field_existence(self, class_name: str, field_name: str, should_exist: bool) -> bool:
        """
        Validates the existence of a field in a class based on whether it should or should not exist.

        Args:
            class_name (str): The name of the class containing the field.
            field_name (str): The name of the field to validate.
            should_exist (bool): True if the field should exist, False if it should not.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        is_field_name_exist = self.__field_or_method_exist(class_name, field_name, is_field=True)
        if should_exist and not is_field_name_exist:
            self.__console.print(f"\n[bold red]Field [bold white]'{field_name}'[/bold white] does not exist in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        elif not should_exist and is_field_name_exist:
            self.__console.print(f"\n[bold red]Field [bold white]'{field_name}'[/bold white] has already existed in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        return True
    
    # Validate method existence based on whether it should exist or not #
    def __validate_method_existence(self, class_name: str, method_name: str, should_exist: bool) -> bool:
        """
        Validates the existence of a method in a class based on whether it should or should not exist.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method to validate.
            should_exist (bool): True if the method should exist, False if it should not.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        is_method_name_exist = self.__field_or_method_exist(class_name, method_name, is_field=False)
        if should_exist and not is_method_name_exist:
            self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] does not exist in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        elif not should_exist and is_method_name_exist:
            self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] has already existed in class [bold white]'{class_name}'[/bold white]![/bold red]")
            return False
        return True
    
    # Check if we are able to rename field/method #
    def __check_field_or_method_rename(self, class_name: str, current_name: str, new_name: str, is_field: bool) -> bool:
        """
        Checks if a field or method can be renamed by validating the existence of the current and new names.

        Args:
            class_name (str): The name of the class containing the field or method.
            current_name (str): The current name of the field or method.
            new_name (str): The proposed new name for the field or method.
            is_field (bool): True if renaming a field, False if renaming a method.

        Returns:
            bool: True if renaming is possible, False otherwise.
        """
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return False
        # Rename check for field
        if is_field:
            is_current_field_name_exist = self.__validate_field_existence(class_name, current_name, should_exist=True)
            if not is_current_field_name_exist:
                return False
            is_new_name_exist = self.__validate_field_existence(class_name, new_name, should_exist=False)
            if not is_new_name_exist:
                return False
        # Rename check for method
        else:
            is_current_method_name_exist = self.__validate_method_existence(class_name, current_name, should_exist=True)
            if not is_current_method_name_exist:
                return False
            is_new_name_exist = self.__validate_method_existence(class_name, new_name, should_exist=False)
            if not is_new_name_exist:
                return False
        return True
    
    # Get the chosen field or method #
    def __get_chosen_field_or_method(self, class_name: str, input_name: str, is_field: bool) -> Field | Method | None:
        """
        Retrieves the specified field or method from a class.

        Args:
            class_name (str): The name of the class containing the field or method.
            input_name (str): The name of the field or method to retrieve.
            is_field (bool): True if retrieving a field, False if retrieving a method.

        Returns:
            Field | Method | None: The field or method object, or None if not found.
        """
        class_object = self.__class_list[class_name]
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        for element in general_list:
            if element._get_name() == input_name:
                return element
        return None
    
    ## PARAMETER RELATED ##
    
    # Check if parameter exists #
    def __parameter_exist(self, class_name: str, method_name: str, parameter_name: str) -> bool:
        """
        Checks if a parameter exists for a specified method in a class.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method.
            parameter_name (str): The name of the parameter to check.

        Returns:
            bool: True if the parameter exists, False otherwise.
        """
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        if method_name not in method_and_parameter_list:
            self.__console.print(f"\n[bold red]Method [bold white]'{method_name}'[/bold white] does not exist![/bold red]")
            return False
        parameter_list = method_and_parameter_list[method_name]
        for parameter in parameter_list:
            if parameter_name == parameter._get_parameter_name():
                return True
        return False
    
    # Validate parameter existence #
    def __validate_parameter_existence(self, class_name: str, method_name: str, parameter_name: str, should_exist: bool) -> bool:
        """
        Validates the existence of a parameter in a method based on whether it should or should not exist.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method containing the parameter.
            parameter_name (str): The name of the parameter to validate.
            should_exist (bool): True if the parameter should exist, False if it should not.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        is_parameter_exist = self.__parameter_exist(class_name, method_name, parameter_name)
        if should_exist and not is_parameter_exist:
            self.__console.print(f"\n[bold red]Parameter [bold white]'{parameter_name}'[/bold white] does not exist![/bold red]")
            return False
        elif not should_exist and is_parameter_exist:
            self.__console.print(f"\n[bold red]Parameter [bold white]'{parameter_name}'[/bold white] has already existed![/bold red]")
            return False
        return True
    
    # Get the chosen parameter #
    def __get_chosen_parameter(self, class_name: str, method_name: str, parameter_name: str) -> Parameter:
        """
        Retrieves a specified parameter from a method in a class.

        Args:
            class_name (str): The name of the class containing the method.
            method_name (str): The name of the method containing the parameter.
            parameter_name (str): The name of the parameter to retrieve.

        Returns:
            Parameter: The parameter object, or None if not found.
        """
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        parameter_list = method_and_parameter_list[method_name]
        for each_parameter in parameter_list:
            if each_parameter._get_parameter_name() == parameter_name:
                return each_parameter
        return None
    
    ## RELATIONSHIP RELATED ##
    
    # Check if relationship type exists #
    def __type_exist(self, type_name: str) -> bool:
        """
        Checks if a relationship type exists in the available relationship types.

        Args:
            type_name (str): The name of the relationship type to check.

        Returns:
            bool: True if the relationship type exists, False otherwise.
        """
        if type_name in RelationshipType._value2member_map_:
            return True
        return False
    
    # Validate relationship type based on whether it should exist or not #
    def __validate_type_existence(self, type_name: str, should_exist: bool) -> bool:
        """
        Validates the existence of a relationship type based on whether it should or should not exist.

        Args:
            type_name (str): The name of the relationship type to validate.
            should_exist (bool): True if the type should exist, False if it should not.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        is_type_exist = self.__type_exist(type_name)
        if should_exist and not is_type_exist:
            self.__console.print(f"\n[bold red]Type [bold white]'{type_name}'[/bold white] does not exist![/bold red]")
            return False
        return True

    # Check if relationship exists between source and destination class #
    def _relationship_exist(self, source_class_name: str, destination_class_name: str) -> bool:
        """
        Checks if a relationship exists between the source and destination classes.

        Args:
            source_class_name (str): The source class name.
            destination_class_name (str): The destination class name.

        Returns:
            bool: True if the relationship exists, False otherwise.
        """
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            if each_relationship._get_source_class() == source_class_name and each_relationship._get_destination_class() == destination_class_name:
                return True
        return False
    
    # Get the chosen relationship #
    def _get_chosen_relationship(self, source_class_name: str, destination_class_name: str) -> Relationship:
        """
        Retrieves the relationship between the specified source and destination classes.

        Args:
            source_class_name (str): The source class name.
            destination_class_name (str): The destination class name.

        Returns:
            Relationship: The relationship object, or None if not found.
        """
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            if each_relationship._get_source_class() == source_class_name and each_relationship._get_destination_class() == destination_class_name:
                return each_relationship
        return None
    
    # Get the relationship type between two classes #
    def _get_chosen_relationship_type(self, source_class_name: str, destination_class_name: str) -> str | None:
        """
        Retrieves the type of the relationship between two classes.

        Args:
            source_class_name (str): The source class name.
            destination_class_name (str): The destination class name.

        Returns:
            str | None: The relationship type, or None if no relationship exists.
        """
        current_relationship = self._get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is not None:
            return current_relationship._get_type()
        self.__console.print(f"\n[bold red]No relationship between class [bold white]'{source_class_name}'[/bold white] and class [bold white]'{destination_class_name}'[/bold white]![/bold red]")
        return None

    #################################################################
    ### JSON FORMAT ###
    
    # Get field format list #
    def _get_field_format_list(self, class_object: Class) -> List[Dict]:
        """
        Retrieves a list of fields from the given class object, converting each field to a JSON-compatible format.
        
        Args:
            class_object (Class): The UMLClass object from which fields are extracted.
        
        Returns:
            List[Dict]: A list of field dictionaries formatted for JSON storage.
        """
        # Get field list
        field_list = class_object._get_class_field_list()
        # Field format list to store fields in JSON format
        field_list_format: List[Dict] = []
        for each_field in field_list:
            attr_json_format = each_field._convert_to_json_field()
            field_list_format.append(attr_json_format)
        return field_list_format
    
    # Get method format list #
    def _get_method_format_list(self, class_object: Class) -> List[Dict]:
        """
        Retrieves a list of methods from the given class object, converting each method and its associated parameters 
        to a JSON-compatible format.
        
        Args:
            class_object (Class): The UMLClass object from which methods and parameters are extracted.
        
        Returns:
            List[Dict]: A list of method dictionaries formatted for JSON storage, including their parameters.
        """
        # Get method list
        method_list = class_object._get_class_method_list()
        # Method format list to store methods in JSON format
        method_list_format: List[Dict] = []
        # Get method and parameter list for the specified class
        method_and_parameter_list = self._get_method_and_parameter_list(class_object._get_class_name())
        
        for each_method in method_list:
            # Convert method to JSON format
            method_json_format = each_method._convert_to_json_method()
            # Get the parameters of the current method
            parameter_list = method_and_parameter_list[each_method._get_name()]
            # Convert each parameter to JSON format
            parameter_format_list: List[Dict] = []
            for each_parameter in parameter_list:
                parameter_format_list.append(each_parameter._convert_to_json_parameter())
            # Add method format to the method list format
            method_list_format.append(method_json_format)
            # Add the parameters to the method format
            for each_method_format in method_list_format:
                if each_method_format["name"] == each_method._get_name():
                    each_method_format["params"].extend(parameter_format_list)
        return method_list_format
    
    # Get relationship format list #
    def _get_relationship_format_list(self) -> List[Dict]:
        """
        Retrieves a list of relationships, converting each to a JSON-compatible format for storage.
        
        Returns:
            List[Dict]: A list of relationship dictionaries formatted for JSON storage.
        """
        # Get relationship list
        relationship_list = self.__relationship_list
        # Relationship format list to store relationships in JSON format
        relationship_list_format: List[Dict] = []
        for each_relationship in relationship_list:
            rel_json_format = each_relationship._convert_to_json_relationship()
            relationship_list_format.append(rel_json_format)
        return relationship_list_format
    
    # Combine class json format #
    def _class_json_format(self, class_name: str) -> Dict:
        """
        Generates a JSON-compatible dictionary representing the specified class, including its fields and methods.
        
        Args:
            class_name (str): The name of the class to format.
        
        Returns:
            Dict: A dictionary representing the class, fields, and methods in JSON format, or None if the class doesn't exist.
        """
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return None
        # Get class object
        class_object = self.__class_list[class_name]
        # Get the base class format
        class_format = class_object._convert_to_json_uml_class()
        # Set the class name
        class_format["name"] = class_object._get_class_name()
        # Get and assign field list in JSON format
        field_list_format: List[Dict] = self._get_field_format_list(class_object)
        class_format["fields"] = field_list_format
        # Get and assign method list in JSON format
        method_list_format: List[Dict] = self._get_method_format_list(class_object)
        class_format["methods"] = method_list_format
        return class_format
    
    ### SAVE/LOAD ###
    
    # Save data #
    def _save(self):
        """
        Saves the current UML data to a JSON file, prompting the user for a file name or allowing them to select from 
        existing saved files. Data is saved in JSON format with the class and relationship data.
        """
        # Prompt the user for a file name to save
        self.__console.print("\n[bold yellow]Please provide a name for the file you'd like to save or choose file from the list to override.[/bold yellow]")
        self.__console.print("[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[bold yellow]")
        # Display the list of saved files
        saved_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(saved_list)
        self.__console.print("[bold yellow]==>[/bold yellow] ", end="")
        user_input = input()
        # Prevent user from overriding NAME_LIST.json
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't save to [bold white]'{user_input}.json'[/bold white][bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled saving![/bold green]")
            return
        # Class and relationship data lists for storing in main data
        class_data_list = []
        relationship_data_list = []
        # Update main data with class and relationship information
        main_data = self.__update_main_data_from_loaded_file(user_input, class_data_list, relationship_data_list)
        current_active_file = self._get_active_file()
        if current_active_file == "No active file!":
            self._set_file_status(user_input, "on")
        self.__storage_manager._update_saved_list(saved_list)
        # Save data to JSON file
        self.__storage_manager._save_data_to_json(user_input, main_data)
        self.__console.print(f"\n[bold green]Successfully saved data to [bold white]'{user_input}.json'![/bold white][/bold green]")

    # Save for GUI #
    def _save_gui(self, file_name, full_path):
        """
        Saves UML data through the GUI, saving to the specified file name and path.
        
        Args:
            file_name (str): The name of the file to save.
            file_path (str): The file path for saving the data.
        """
        # Class and relationship data lists for storing in main data
        class_data_list = []
        relationship_data_list = []
        # Update main data with class and relationship information
        main_data = self.__update_main_data_from_loaded_file(file_name, class_data_list, relationship_data_list, file_path=full_path)
        current_active_file = self._get_active_file()
        if current_active_file == "No active file!":
            self._set_file_status(file_name, "on")
        current_active_file_gui = self._get_active_file_gui()
        if current_active_file_gui == "No active file!":
            self._set_file_status_gui(full_path, "on")
        saved_list = self.__storage_manager._get_saved_list()
        self.__storage_manager._update_saved_list(saved_list)
        saved_list_gui = self.__storage_manager._get_saved_list_gui()
        self.__storage_manager._update_saved_list_gui(saved_list_gui)
        # Save data to JSON via the GUI
        self.__storage_manager._save_data_to_json_gui(full_path, main_data)

    # Load data #
    def _load(self):
        """
        Loads UML data from a saved JSON file, prompting the user for a file name or displaying a list of saved files.
        The data is loaded and the program's state is updated.
        """
        # Prompt the user for a file name to load
        self.__console.print("\n[bold yellow]Please provide a name for the file you'd like to load.[/bold yellow]")
        self.__console.print("[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[/bold yellow]")
        # Display the list of saved files
        save_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(save_list)
        self.__console.print("[bold yellow]==>[/bold yellow] ", end="")
        user_input = input()
        # Prevent loading NAME_LIST.json
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't load from [bold white]'{user_input}.json'[/bold white][/bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled loading![/bold green]")
            return
        # Validate if the file exists
        is_loading = self._saved_file_name_check(user_input)
        if not is_loading:
            self.__console.print(f"\n[bold red]File [bold white]'{user_input}.json'[/bold white] does not exist[/bold red]")
            return
        # Load data from the file and update program state
        main_data = self.__main_data = self.__storage_manager._load_data_from_json(user_input)
        self.__update_data_members(main_data)
        self.__check_file_and_set_status(user_input)
        self.__console.print(f"\n[bold green]Successfully loaded data from [bold white]'{user_input}.json'[/bold white]![/bold green]")
        
    def _load_gui(self, file_name: str, file_path: str, graphical_view: GUIView):
        """
        Loads UML data from a saved JSON file, prompting the user for a file name or displaying a list of saved files.
        The data is loaded and the program's state is updated.
        """
        # Load data from the file and update program state
        main_data = self.__main_data = self.__storage_manager._load_data_from_json_gui(file_path)
        is_file_exist_gui = self._check_saved_file_exist_gui(file_name)
        if not is_file_exist_gui:
            self.__storage_manager._add_name_to_saved_file_gui(file_path)
        is_file_exist = self._check_saved_file_exist(file_name)
        if not is_file_exist:
            self.__storage_manager._add_name_to_saved_file(file_name)
        self.__update_data_members_gui(main_data, graphical_view)
        self.__check_file_and_set_status(file_name)
        self._check_file_and_set_status_gui(file_path)

    # Update main data to store data to JSON file #
    def __update_main_data_from_loaded_file(self, user_input: str, class_data_list: List, relationship_data_list: List, file_path=None) -> Dict:
        """
        Updates the main data to be saved into a JSON file by compiling class data and relationship data.

        Args:
            user_input (str): The name of the file to save or load.
            class_data_list (List): A list to store formatted class data.
            relationship_data_list (List): A list to store formatted relationship data.

        Returns:
            Dict: The updated main data dictionary containing class and relationship details.
        """
        # Format relationships for JSON storage
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Add the file name to the saved list if it is a new one
        self.__storage_manager._add_name_to_saved_file(user_input)
        if file_path is not None:
            self.__storage_manager._add_name_to_saved_file_gui(file_path)
        # Format classes for JSON storage
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        # Store formatted class and relationship data in main_data
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
        return main_data
    
    # Update UMLCoreManager data after loading a file #
    def __update_data_members(self, main_data: Dict):
        """
        Updates the internal data members (class and relationship) after loading from a JSON file.

        Args:
            main_data (Dict): The data dictionary loaded from a JSON file.
        """
        class_data = main_data["classes"]
        relationship_data = main_data["relationships"]
        # Reset the current storage before loading new data
        self._reset_storage()
        # Set the new main data
        self.__main_data = main_data
        # Extract and recreate class, fields, methods, and parameters from the loaded data
        extracted_class_data = self._extract_class_data(class_data)
        for each_pair in extracted_class_data:
            for class_name, data in each_pair.items():
                field_list = data['fields']
                method_param_list = data['methods_params']
                # Add classes, fields, methods, and parameters to the program state
                self._add_class(class_name, is_loading=True)
                for each_field in field_list:
                    self._add_field(class_name, each_field, is_loading=True)
                for method_name, param_list in method_param_list.items():
                    self._add_method(class_name, method_name, is_loading=True)
                    for param_name in param_list:
                        self._add_parameter(class_name, method_name, param_name, is_loading=True)
        # Recreate relationships from the loaded data
        for each_dictionary in relationship_data:
            self._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True, is_gui=False)
            
    def __update_data_members_gui(self, main_data: Dict, graphical_view: GUIView):
        """
        Updates the internal data members (class and relationship) after loading from a JSON file.

        Args:
            main_data (Dict): The data dictionary loaded from a JSON file.
        """
        class_data = main_data["classes"]
        relationship_data = main_data["relationships"]
        # Reset the current storage before loading new data
        self._reset_storage()
        # Set the new main data
        self.__main_data = main_data
        # Extract and recreate class, fields, methods, and parameters from the loaded data
        extracted_class_data = self._extract_class_data(class_data)
        for each_pair in extracted_class_data:
            for class_name, data in each_pair.items():
                field_list = data['fields']
                method_param_list = data['methods_params']
                # Add classes, fields, methods, and parameters to the program state
                graphical_view.add_class(class_name, is_loading=True)
                for each_field in field_list:
                    graphical_view.add_field(class_name, each_field, is_loading=True)
                for method_name, param_list in method_param_list.items():
                    graphical_view.add_method(class_name, method_name, is_loading=True)
                    for param_name in param_list:
                        graphical_view.add_param(class_name, method_name, param_name, is_loading=True)
        # Recreate relationships from the loaded data
        for each_dictionary in relationship_data:
            graphical_view.add_relationship(
                loaded_class_name=each_dictionary["source"],
                loaded_source_class=each_dictionary["source"],
                loaded_dest_class=each_dictionary["destination"],
                loaded_type=each_dictionary["type"],
                is_loading=True
            )
            
    # Extract class, field, method, and parameters from json file #
    def _extract_class_data(self, class_data: List[Dict]) -> List[Dict[str, Dict[str, List | Dict]]]:
        """
        Extracts class, field, method, and parameter information from the loaded JSON data and prepares it for further processing.

        Args:
            class_data (List[Dict]): A list of dictionaries representing class data loaded from JSON.

        Returns:
            List[Dict[str, Dict[str, List | Dict]]]: A list of dictionaries containing class names, fields, methods, and parameters.
        """
        class_info_list: List[Dict[str, Dict[str, List | Dict]]] = []
        # Loop through the class data to extract fields and methods
        for class_element in class_data:
            method_and_param_list = {}
            class_name = class_element["name"]
            fields = [field["name"] for field in class_element["fields"]]
            # Extract methods and their parameters
            for method_element in class_element["methods"]:
                temp_param_list: List[str] = []
                for param_element in method_element["params"]:
                    temp_param_list.append(param_element["name"])
                method_and_param_list[method_element["name"]] = temp_param_list
            class_info_list.append({class_name: {'fields': fields, 'methods_params': method_and_param_list}})
        return class_info_list
    
    # Delete saved file #
    def _delete_saved_file(self):
        """
        Allows the user to delete a saved file. Prompts the user for the file to delete and updates the saved file list.
        """
        self.__console.print("\n[bold yellow]Please choose a file you want to delete.[/bold yellow]")
        self.__console.print("\n[bold yellow]Type [bold white]'quit'[/bold white] to go back to main menu:[/bold yellow]")
        saved_list = self.__storage_manager._get_saved_list()
        is_saved_list_not_empty = self.__user_view._display_saved_list(saved_list)
        if not is_saved_list_not_empty:
            return
        user_input = input()
        if user_input == "NAME_LIST":
            self.__console.print(f"\n[bold red]You can't delete file [bold white]'{user_input}.json'[/bold white][/bold red]")
            return 
        if user_input == "quit":
            self.__console.print("\n[bold green]Canceled loading![/bold green]")
            return
        is_file_exist = self._check_saved_file_exist(user_input)
        if not is_file_exist:
            self.__console.print(f"[bold red]File [bold white]'{user_input}.json'[/bold white] does not exist![/bold red]")
            return
       # Remove the file from saved list and filesystem
        save_list = self.__storage_manager._get_saved_list()
        for dictionary in save_list.copy():
            if user_input in dictionary:
                save_list.remove(dictionary)

        # Remove file path in NAME_LIST_GUI.json
        save_list_gui = self.__storage_manager._get_saved_list_gui()
        for dictionary in save_list_gui.copy():
            for full_path in dictionary:
                file_name_with_ext = os.path.basename(full_path)
                file_name_without_ext, extension = os.path.splitext(file_name_with_ext)
                if file_name_without_ext == user_input:
                    save_list_gui.remove(dictionary)
                    
        self.__storage_manager._update_saved_list(save_list)
        self.__storage_manager._update_saved_list_gui(save_list_gui)
        file_path = os.path.join(root_directory, f"{user_input}.json")
        os.remove(file_path)
        self.__console.print(f"\n[bold green]Successfully removed file [bold white]'{user_input}.json'[/bold white][/bold green]")
    
    # Check if a saved file exists #
    def _check_saved_file_exist(self, file_name: str):
        """
        Checks if a saved file exists by looking for the file name in the saved list.

        Args:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        saved_list = self.__storage_manager._get_saved_list()
        for element in saved_list:
            for name in element:
                if file_name == name:
                    return True
        return False
    
    # Check if a saved file exists #
    def _check_saved_file_exist_gui(self, file_path: str):
        """
        Checks if a saved file exists by looking for the file name in the saved list.

        Args:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        saved_list = self.__storage_manager._get_saved_list_gui()
        for element in saved_list:
            for path in element:
                if file_path == path:
                    return True
        return False
    
    # End session and return to blank state #
    def _end_session(self):
        """
        Ends the current session and resets the program to its default blank state by resetting all data and turning off active files.
        """
        self.__set_all_file_off()
        self._set_all_file_off_gui()
        self._reset_storage()
        self.__console.print("\n[bold green]Successfully back to default program![/bold green]")
    
    # Get active file #
    def _get_active_file(self) -> str:
        """
        Retrieves the name of the currently active file if one exists.

        Returns:
            str: The name of the active file, or 'No active file!' if none is active.
        """
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key, val in each_dictionary.items():
                if val == "on":
                    return key
        return "No active file!"
    
    # Get active file #
    def _get_active_file_gui(self) -> str:
        """
        Retrieves the name of the currently active file if one exists.

        Returns:
            str: The name of the active file, or 'No active file!' if none is active.
        """
        saved_list = self.__storage_manager._get_saved_list_gui()
        for each_dictionary in saved_list:
            for key, val in each_dictionary.items():
                if val == "on":
                    return key
        return "No active file!"
    
    # Clear data in the current active file #
    def _clear_current_active_data(self):
        """
        Clears all data in the currently active file and resets it, effectively starting with a blank slate.
        """
        saved_list = self.__storage_manager._get_saved_list()
        if len(saved_list) == 0:
            self.__console.print("\n[bold red]No active file to clear data![bold red]")
            return
        current_active_file = self._get_active_file()
        if current_active_file == "No active file!":
            self.__console.print("\n[bold red]No active file![bold red]")
            return
        self._reset_storage()
        self.__storage_manager._save_data_to_json(current_active_file, self.__main_data)
        self.__console.print(f"\n[bold green]Successfully cleared data in file [bold white]'{current_active_file}.json'[/bold white][/bold green]")
    
    # Exit program #
    def _exit(self):
        """
        Exits the program, turning off any active file and cleaning up.
        """
        self.__set_all_file_off()
        self._set_all_file_off_gui()
        self.__console.print("\n[bold green]Exited Program[/bold green]")
    
    # Set all files' status to 'off' #
    def __set_all_file_off(self):
        """
        Resets the status of all files in the saved list, setting their status to 'off' (inactive).
        """
        # CLI
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                each_dictionary[key] = "off"
        self.__storage_manager._update_saved_list(saved_list)

    # Set a specific file's status #
    def _set_file_status(self, file_name: str, status: str):
        """
        Sets the status of a specific file in the saved list.

        Args:
            file_name (str): The name of the file.
            status (str): The new status to assign to the file ('on' or 'off').
        """
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if key == file_name:
                    each_dictionary[key] = status
    
    # Check and set file status #
    def __check_file_and_set_status(self, file_name: str) -> str:
        """
        Ensures only the selected file is marked as 'on', setting all others to 'off'.

        Args:
            file_name (str): The name of the file to activate.
        """
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if each_dictionary[key] == "on":
                    each_dictionary[key] = "off"
        self._set_file_status(file_name, status="on")
        self.__storage_manager._update_saved_list(saved_list)
    
    # Set all files' status to 'off' #
    def _set_all_file_off_gui(self):
        saved_list = self.__storage_manager._get_saved_list_gui()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                each_dictionary[key] = "off"
        self.__storage_manager._update_saved_list_gui(saved_list)
    
    # Set a specific file's status #
    def _set_file_status_gui(self, file_path: str, status: str):
        """
        Sets the status of a specific file in the saved list.

        Args:
            file_name (str): The name of the file.
            status (str): The new status to assign to the file ('on' or 'off').
        """
        
        saved_list = self.__storage_manager._get_saved_list_gui()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if key == file_path:
                    each_dictionary[key] = status
                    
    # Check and set file status #
    def _check_file_and_set_status_gui(self, file_path: str) -> str:
        """
        Ensures only the selected file is marked as 'on', setting all others to 'off'.

        Args:
            file_name (str): The name of the file to activate.
        """
        saved_list = self.__storage_manager._get_saved_list_gui()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if each_dictionary[key] == "on":
                    each_dictionary[key] = "off"
        self._set_file_status_gui(file_path, status="on")
        self.__storage_manager._update_saved_list_gui(saved_list)
    
    # Reset all storage (classes, relationships, and main data) #
    def _reset_storage(self):
        """
        Resets the entire storage by clearing all class data, relationships, and the main data dictionary.
        """
        self.__class_list: Dict[str, Class] = {}
        self.__relationship_list: List = []
        self.__main_data: Dict = {}
    
    #################################################################
    ### UTILITY FUNCTIONS ###
        
    # Check if a saved file exists by name #
    def _saved_file_name_check(self, save_file_name: str) -> bool:
        """
        Checks if a saved file name exists in the saved list.

        Args:
            save_file_name (str): The name of the file to check.

        Returns:
            bool: True if the file name exists, False if it does not.
        """
        saved_list = self.__storage_manager._get_saved_list()
        for each_pair in saved_list:
            for file_name in each_pair:
                if file_name == save_file_name:
                    return True
        return False
    
    # Update main data for every action #
    def _update_main_data_for_every_action(self):
        """
        Updates the main data by fetching and formatting all classes and relationships, ensuring the state is kept up to date after every change.
        """
        class_data_list = []
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Fetch and format class data
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
    
    # Validate entities (Class, Field, Method, Parameter) #
    def _validate_entities(
        self, 
        class_name: str = None, 
        field_name: str = None, 
        method_name: str = None, 
        parameter_name: str = None, 
        class_should_exist: bool = None, 
        field_should_exist: bool = None,
        method_should_exist: bool = None, 
        parameter_should_exist: bool = None
    ) -> bool:
        """
        General validation function for class, field, method, and parameter existence.

        Args:
            class_name (str, optional): Name of the class to check.
            field_name (str, optional): Name of the field to check.
            method_name (str, optional): Name of the method to check.
            parameter_name (str, optional): Name of the parameter to check.
            class_should_exist (bool, optional): Whether the class should exist or not.
            field_should_exist (bool, optional): Whether the field should exist or not.
            method_should_exist (bool, optional): Whether the method should exist or not.
            parameter_should_exist (bool, optional): Whether the parameter should exist or not.

        Returns:
            bool: True if all required entities exist or don't exist as expected, otherwise False.
        """
        # Validate class existence
        if class_name is not None and class_should_exist is not None:
            is_class_exist = self.__validate_class_existence(class_name, class_should_exist)
            if not is_class_exist:
                return False
        # Validate field existence
        if field_name is not None and field_should_exist is not None:
            is_field_exist = self.__validate_field_existence(class_name, field_name, field_should_exist)
            if not is_field_exist:
                return False
        # Validate method existence
        if method_name is not None and method_should_exist is not None:
            is_method_exist = self.__validate_method_existence(class_name, method_name, method_should_exist)
            if not is_method_exist:
                return False
        # Validate parameter existence
        if parameter_name is not None and parameter_should_exist is not None:
            is_parameter_exist = self.__validate_parameter_existence(class_name, method_name, parameter_name, parameter_should_exist)
            if not is_parameter_exist:
                return False
        return True
    
    # Sort class list alphabetically #
    def _sort_class_list(self):
        """
        Sorts the list of UML classes in alphabetical order and updates the main data to reflect this change.
        """
        class_list = self.__class_list
        if len(class_list) == 0:
            self.__console.print("\n[bold red]No class to sort![/bold red]")
            return
        # Sort classes alphabetically by their names
        self.__class_list = dict(sorted(self.__class_list.items()))
        self._update_main_data_for_every_action()
        # Display updated UML data
        self.__user_view._display_uml_data(self.__main_data)
        
    def _is_valid_input(self, user_input):
        """
        Check if the user input contains only letters, numbers, and underscores.

        Args:
        user_input (str): The input string to validate.

        Returns:
        bool: True if input is valid (contains only a-z, A-Z, 0-9, and _), False otherwise.
        """
        # Regular expression pattern to allow only a-z, A-Z, 0-9, and _
        pattern = r'^[a-zA-Z0-9_]+$'

        # Match the input string against the pattern
        if re.match(pattern, user_input):
            return True
        else:
            return False
                           
###################################################################################################