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
from UML_MVC import uml_command_pattern as Command

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
        self.__input_handler = Command.InputHandler()
        self.__model = model  # Reference to the UML model
        self.__user_view = view  # Reference to the view for displaying data
        self.__console = console  # Console for printing messages
        self.__storage_manager: Storage = self.__model._get_storage_manager()  # Storage manager to handle save/load functionality
        
    
    def _get_model_obj(self):
        return self.__model
    
    def _get_input_handler(self):
        return self.__input_handler
    
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
        param_list_str = ' '.join(parameters[2:]) if len(parameters) > 2 else None
        fourth_param = parameters[3] if len(parameters) > 3 else None
        
        #######################################################
        
        # Handle class-related commands

        # Add class
        if command == InterfaceOptions.ADD_CLASS.value and first_param:
            add_class_command = Command.AddClassCommand(self.__model, class_name=first_param)
            self.__input_handler.execute_command(add_class_command)
        
        # Delete class
        elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
            delete_class_command = Command.DeleteClassCommand(self.__model, class_name=first_param)
            self.__input_handler.execute_command(delete_class_command)
        
        # Rename class
        elif (
            command == InterfaceOptions.RENAME_CLASS.value
            and first_param
            and second_param
        ):
            rename_class_command = Command.RenameClassCommand(self.__model, class_name=first_param, new_name=second_param)
            self.__input_handler.execute_command(rename_class_command)

        #######################################################
        
        # Handle field-related commands

        # Add field to class
        elif (
            command == InterfaceOptions.ADD_FIELD.value
            and first_param
            and second_param
            and third_param
        ):
            add_field_command = Command.AddFieldCommand(self.__model, class_name=first_param, type=second_param, field_name=third_param)
            self.__input_handler.execute_command(add_field_command)
        
        # Delete field from class
        elif (
            command == InterfaceOptions.DELETE_FIELD.value
            and first_param
            and second_param
        ):
            delete_field_command = Command.DeleteFieldCommand(self.__model, class_name=first_param, field_name=second_param)
            self.__input_handler.execute_command(delete_field_command)
        
        # Rename field in class
        elif (
            command == InterfaceOptions.RENAME_FIELD.value
            and first_param
            and second_param
            and third_param
        ):
            rename_field_command = Command.RenameFieldCommand(self.__model, class_name=first_param, old_field_name=second_param, new_field_name=third_param)
            self.__input_handler.execute_command(rename_field_command)
        
        # Change field type in class
        elif (
            command == InterfaceOptions.EDIT_FIELD_TYPE.value
            and first_param
            and second_param
            and third_param
        ):
            edit_field_type_command = Command.ChangeTypeCommand(self.__model, class_name=first_param, input_name=second_param, new_type=third_param, is_field=True)
            self.__input_handler.execute_command(edit_field_type_command)

        #######################################################
        
        # Handle method-related commands

        # Add method to class
        elif (
            command == InterfaceOptions.ADD_METHOD.value
            and first_param
            and second_param
            and third_param
        ):
            add_method_command = Command.AddMethodCommand(self.__model, class_name=first_param, type=second_param, method_name=third_param)
            self.__input_handler.execute_command(add_method_command)
        
        # Delete method from class
        elif (
            command == InterfaceOptions.DELETE_METHOD.value
            and first_param
            and second_param
        ):
            delete_method_command = Command.DeleteMethodCommand(self.__model, class_name=first_param, method_num=second_param)
            self.__input_handler.execute_command(delete_method_command)
        
        # Rename method in class
        elif (
            command == InterfaceOptions.RENAME_METHOD.value
            and first_param
            and second_param
            and third_param
        ):
            rename_method_command = Command.RenameMethodCommand(self.__model, class_name=first_param, method_num=second_param, new_name=third_param)
            self.__input_handler.execute_command(rename_method_command)
        
        # Change method type in class
        elif (
            command == InterfaceOptions.EDIT_METHOD_TYPE.value
            and first_param
            and second_param
            and third_param
        ):
            edit_method_type_command = Command.ChangeTypeCommand(self.__model, class_name=first_param, method_num=second_param, new_type=third_param, is_method=True)
            self.__input_handler.execute_command(edit_method_type_command)

        #######################################################
        
        # Handle parameter-related commands
        elif (
            command == InterfaceOptions.ADD_PARAM.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            add_param_command = Command.AddParameterCommand(self.__model, class_name=first_param, method_num=second_param, param_type=third_param, param_name=fourth_param)
            self.__input_handler.execute_command(add_param_command)
        # Delete parameter from method
        elif (
            command == InterfaceOptions.DELETE_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            delete_param_command = Command.DeleteParameterCommand(self.__model, class_name=first_param, method_num=second_param, param_name=third_param)
            self.__input_handler.execute_command(delete_param_command)

        elif(
            command == InterfaceOptions.EDIT_PARAM_TYPE.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            edit_param_type_command = Command.ChangeTypeCommand(self.__model, class_name=first_param, method_num=second_param, input_name=third_param, new_type=fourth_param, is_param=True)
            self.__input_handler.execute_command(edit_param_type_command)
        
        # Rename parameter in method
        elif (
            command == InterfaceOptions.RENAME_PARAM.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            rename_param_command = Command.RenameParameterCommand(self.__model, class_name=first_param, method_num=second_param, old_param_name=third_param, new_param_name=fourth_param)
            self.__input_handler.execute_command(rename_param_command)
        
        # Replace parameter list in method
        elif (
            command == InterfaceOptions.REPLACE_PARAM.value 
            and first_param 
            and second_param
        ):
            # Collect all remaining parameters into one string
            param_list_str = ' '.join(parameters[2:]) if len(parameters) > 2 else None
            if param_list_str:
                # Split param_list_str by commas to get individual parameters
                new_param_list = [item.strip() for item in param_list_str.split(",")]
                rename_param_command = Command.ReplaceParameterListCommand(self.__model, class_name=first_param, method_num=second_param, new_param_list=new_param_list)
                self.__input_handler.execute_command(rename_param_command)
            else:
                self.__console.print("\n[bold red]Error: Parameter list is missing.[/bold red]")

        #######################################################
        
        # Handle relationship-related commands

        # Add relationship between classes
        elif (
            command == InterfaceOptions.ADD_REL.value
            and first_param
            and second_param
            and third_param
        ):
            add_rel_command = Command.AddRelationshipCommand(self.__model, source_class=first_param, dest_class=second_param, 
                                           rel_type=third_param)
            self.__input_handler.execute_command(add_rel_command)
        
        # Delete relationship between classes
        elif (
            command == InterfaceOptions.DELETE_REL.value
            and first_param
            and second_param
        ):
            delete_rel_command = Command.DeleteRelationshipCommand(self.__model, source_class=first_param, dest_class=second_param)
            self.__input_handler.execute_command(delete_rel_command)
        
        # Change relationship type between classes
        elif (
            command == InterfaceOptions.EDIT_REL_TYPE.value 
            and first_param
            and second_param
            and third_param
        ):
            edit_rel_type_command = Command.ChangeTypeCommand(self.__model, source_class=first_param, dest_class=second_param, new_type=third_param, is_rel=True)
            self.__input_handler.execute_command(edit_rel_type_command)
            
        #######################################################
        
        # Undo #
        elif command == InterfaceOptions.UNDO.value:
            self.__input_handler.undo()
        
        # Redo #
        elif command == InterfaceOptions.REDO.value:
            self.__input_handler.redo()
        
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
        elif command == InterfaceOptions.NEW.value:
            self.__model._new_file()
        
        # Sort the list of classes alphabetically
        # elif command == InterfaceOptions.SORT.value:
        #     self.__model._sort_class_list()
        
        # Handle unknown command
        else:
            self.__console.print("\n[bold red]Unknown command. Type [bold white]'help'[/bold white] for a list of commands.[/bold red]")

###################################################################################################