###################################################################################################
"""
Module: UMLController
This module contains the UMLController class that serves as the controller in the MVC (Model-View-Controller) pattern.
It handles user input and updates the UML model and view accordingly. The controller interprets commands from the user 
and calls the appropriate methods in the model to perform actions like adding, deleting, or renaming UML classes, fields, 
methods, parameters, and relationships.
"""
###################################################################################################

# Import necessary libraries and modules for console interaction, typing, and model/view handling.
from rich.console import Console
from typing import List
from UML_MVC.UML_CONTROLLER.uml_storage_manager import UMLStorageManager as Storage
from UML_MVC.UML_MODEL.uml_model import UMLModel as Model
from UML_ENUM_CLASS.uml_enum import InterfaceOptions

###################################################################################################
   
class UMLController:
    """
    The UMLController class is responsible for processing user commands and interacting with the UML model
    and view. It handles various actions like adding, deleting, and renaming UML classes, fields, methods, 
    parameters, and relationships. It also manages the loading, saving, and clearing of UML data through 
    the storage manager.
    """

    def __init__(self, model: Model, view, console: Console):
        """
        Initializes the UMLController with a reference to the model, view, and console for interaction.

        Args:
            model (Model): The UML model that holds the data structure.
            view: The view class responsible for displaying output to the user.
            console (Console): A rich console instance used to print messages to the terminal.
        """
        self.__model = model  # Reference to the UML model
        self.__user_view = view  # Reference to the view for displaying data
        self.__console = console  # Console for printing messages
        self.__storage_manager: Storage = Storage()  # Storage manager to handle save/load functionality
    
    #################################################################
    
    ## HANDLE USER INPUT FOR INTERFACE ##
    
    # Processing main program commands based on user input
    def _process_command(self, command: str, parameters: List[str]):
        """
        Processes the user's command and executes the corresponding function in the model or view.
        It parses the command and calls the appropriate model method based on user input.

        Args:
            command (str): The command to execute (e.g., ADD_CLASS, DELETE_CLASS, etc.).
            parameters (List[str]): A list of parameters that accompany the command (e.g., class names, field names).

        This function supports multiple commands such as:
            - Adding, deleting, renaming classes, fields, methods, and parameters.
            - Managing relationships (adding, deleting, modifying types).
            - Loading, saving, and clearing data.
            - Displaying class details and relationships.
        """
        # Extract parameters for the command
        first_param = parameters[0] if len(parameters) > 0 else None
        second_param = parameters[1] if len(parameters) > 1 else None
        third_param = parameters[2] if len(parameters) > 2 else None
        fourth_param = parameters[3] if len(parameters) > 3 else None
        
        #######################################################
        
        # Handle class-related commands

        # Add class
        if command == InterfaceOptions.ADD_CLASS.value and first_param:
            self.__model._add_class(first_param, is_loading=False)
        
        # Delete class
        elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
            self.__model._delete_class(first_param)
        
        # Rename class
        elif (
            command == InterfaceOptions.RENAME_CLASS.value
            and first_param
            and second_param
        ):
            self.__model._rename_class(first_param, second_param)

        #######################################################
        
        # Handle field-related commands

        # Add field to class
        elif (
            command == InterfaceOptions.ADD_FIELD.value
            and first_param
            and second_param
        ):
            self.__model._add_field(first_param, second_param, is_loading=False)
        
        # Delete field from class
        elif (
            command == InterfaceOptions.DELETE_FIELD.value
            and first_param
            and second_param
        ):
            self.__model._delete_field(first_param, second_param)
        
        # Rename field in class
        elif (
            command == InterfaceOptions.RENAME_FIELD.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._rename_field(first_param, second_param, third_param)

        #######################################################
        
        # Handle method-related commands

        # Add method to class
        elif (
            command == InterfaceOptions.ADD_METHOD.value
            and first_param
            and second_param
        ):
            self.__model._add_method(first_param, second_param, is_loading=False)
        
        # Delete method from class
        elif (
            command == InterfaceOptions.DELETE_METHOD.value
            and first_param
            and second_param
        ):
            self.__model._delete_method(first_param, second_param)
        
        # Rename method in class
        elif (
            command == InterfaceOptions.RENAME_METHOD.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._rename_method(first_param, second_param, third_param)

        #######################################################
        
        # Handle parameter-related commands

        # Add parameter to method
        elif (
            command == InterfaceOptions.ADD_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._add_parameter(first_param, second_param, third_param, is_loading=False)
        
        # Delete parameter from method
        elif (
            command == InterfaceOptions.DELETE_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self.__model._delete_parameter(first_param, second_param, third_param)
        
        # Rename parameter in method
        elif (
            command == InterfaceOptions.RENAME_PARAM.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            self.__model._rename_parameter(first_param, second_param, third_param, fourth_param)
        
        # Replace parameter list in method
        elif command == InterfaceOptions.REPLACE_PARAM.value and first_param and second_param:
            self.__model._replace_param_list(first_param, second_param)

        #######################################################
        
        # Handle relationship-related commands

        # Add relationship between classes
        elif (
            command == InterfaceOptions.ADD_REL.value
        ):
            self.__model._add_relationship_wrapper(is_loading=False)
        
        # Delete relationship between classes
        elif (
            command == InterfaceOptions.DELETE_REL.value
            and first_param
            and second_param
        ):
            self.__model._delete_relationship(first_param, second_param)
        
        # Change relationship type between classes
        elif (
            command == InterfaceOptions.TYPE_MOD.value 
            and first_param
            and second_param
            and third_param
        ):
            self.__model._change_type(first_param, second_param, third_param)
        
        #######################################################
        
        # Handle display and data management commands

        # List all created class names or details
        elif command == InterfaceOptions.LIST_CLASS.value:
            self.__user_view._display_wrapper(self.__model._get_main_data())
        
        # Show the details of a specific class
        elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
            self.__user_view._display_single_class(first_param, self.__model._get_main_data())
        
        # Show the relationships between classes
        elif command == InterfaceOptions.CLASS_REL.value:
            self.__user_view._display_relationships(self.__model._get_main_data())
        
        # Show the list of saved files
        elif command == InterfaceOptions.SAVED_LIST.value:
            saved_list = self.__storage_manager._get_saved_list()
            self.__user_view._display_saved_list(saved_list)
        
        # Save current UML data
        elif command == InterfaceOptions.SAVE.value:
            self.__model._save()
        
        # Load saved UML data
        elif command == InterfaceOptions.LOAD.value:
            self.__model._load()
        
        # Delete a saved file
        elif command == InterfaceOptions.DELETE_SAVED.value:
            self.__model._delete_saved_file()
        
        # Clear current data from storage
        elif command == InterfaceOptions.CLEAR_DATA.value:
            self.__model._clear_current_active_data()
        
        # Reset to a blank program
        elif command == InterfaceOptions.DEFAULT.value:
            self.__model._end_session()
        
        # Sort the list of classes alphabetically
        elif command == InterfaceOptions.SORT.value:
            self.__model._sort_class_list()
        
        # Handle unknown command
        else:
            self.__console.print(f"\n[bold red]Unknown command [bold white]'{command}'[/bold white]. Type 'help' for a list of commands.[/bold red]")

###################################################################################################