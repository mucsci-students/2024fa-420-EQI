from abc import ABC, abstractmethod
import os
import sys

# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from UML_INTERFACE.uml_controller_interface import UMLInterface as Interface
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView as CLIView

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddClassCommand(Command):
    def __init__(self, uml_interface, class_name):
        self.uml_interface = uml_interface
        self.class_name = class_name

    def execute(self):
        return self.uml_interface.add_class(self.class_name)

    def undo(self):
        self.uml_interface.delete_class(self.class_name)

class DeleteClassCommand(Command):
    def __init__(self, uml_interface, class_name, field_name):
        self.uml_interface = uml_interface
        self.class_name = class_name

    def execute(self):
        return self.uml_interface.delete_class(self.class_name)

    def undo(self):
        self.uml_interface.add_class(self.class_name)
        
class RenameClassCommand(Command):
    def __init__(self, uml_interface, class_name, new_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.new_name = new_name

    def execute(self):
        return self.uml_interface.rename_class(self.class_name, self.new_name)

    def undo(self):
        return self.uml_interface.rename_class(self.new_name, self.class_name)
        
class AddFieldCommand(Command):
    def __init__(self, uml_interface, class_name, type, field_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.type = type
        self.field_name = field_name

    def execute(self):
        return self.uml_interface.add_field(self.class_name, self.type, self.field_name)

    def undo(self):
        return self.uml_interface.delete_field(self.class_name, self.field_name)

class DeleteFieldCommand(Command):
    def __init__(self, uml_interface, class_name, field_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.field_name = field_name
        self.field_type = None  # To store the type of the field when it's deleted

    def execute(self):
        # Capture the field type before deleting the field
        chosen_field = self.uml_interface.get_chosen_field_or_method(self.class_name, self.field_name, is_field = True)
        if chosen_field is not None:
            self.field_type = chosen_field._get_type()
        return self.uml_interface.delete_field(self.class_name, self.field_name)

    def undo(self):
        return self.uml_interface.add_field(self.class_name, self.field_type, self.field_name)
    
class RenameFieldCommand(Command):
    def __init__(self, uml_interface, class_name, old_field_name, new_field_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.old_name = old_field_name
        self.new_name = new_field_name

    def execute(self):
        return self.uml_interface.rename_field(self.class_name, self.old_name, self.new_name)

    def undo(self):
        return self.uml_interface.rename_field(self.class_name, self.new_name, self.old_name)

class AddMethodCommand(Command):
    def __init__(self, uml_interface, class_name, type, method_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.type = type
        self.method_name = method_name

    def execute(self):
        return self.uml_interface.add_method(self.class_name, self.type, self.method_name)

    def undo(self):
        return self.uml_interface.delete_method(self.class_name, str(self.uml_interface.Model._current_number_of_method))
    
class DeleteMethodCommand(Command):
    def __init__(self, uml_interface, class_name, method_num):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.method_name = None
        self.type = None

    def execute(self):
        # Capture the field type before deleting the method
        chosen_method = self.uml_interface.get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.type = chosen_method._get_type()
        self.method_name = chosen_method._get_name()
        return self.uml_interface.delete_method(self.class_name, self.method_num)
        
    def undo(self):
        if self.type and self.method_name:
            return self.uml_interface.add_method(self.class_name, self.type, self.method_name)
        return False
    
class RenameMethodCommand(Command):
    def __init__(self, uml_interface, class_name, method_num, new_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.old_name = None
        self.new_name = new_name

    def execute(self):
        chosen_method = self.uml_interface.get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.old_name = chosen_method._get_name()
        return self.uml_interface.rename_method(self.class_name, self.method_num, self.new_name)

    def undo(self):
        if self.old_name:
            return self.uml_interface.rename_method(self.class_name, self.method_num, self.old_name)
    
class AddParameterCommand(Command):
    def __init__(self, uml_interface, class_name: str = None, method_num: int = None, param_type: str = None, param_name: str = None):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.param_type = param_type
        self.param_name = param_name

    def execute(self):
        return self.uml_interface.add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name)

    def undo(self):
        return self.uml_interface.delete_parameter(self.class_name, str(self.method_num), self.param_name)
    
class DeleteParameterCommand(Command):
    def __init__(self, uml_interface, class_name, method_num, param_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.param_name = param_name
        self.param_type = None

    def execute(self):
        chosen_param = self.uml_interface.get_param_based_on_index(self.class_name, self.method_num, self.param_name)
        if chosen_param is None:
            return False
        self.param_type = chosen_param._get_type()
        return self.uml_interface.delete_parameter(self.class_name, str(self.method_num), self.param_name)
        
    def undo(self):
        if self.param_type:
            return self.uml_interface.add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name)
        
class RenameParameterCommand(Command):
    def __init__(self, uml_interface, class_name, method_num, old_param_name, new_param_name):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_name = old_param_name
        self.new_param_name = new_param_name

    def execute(self):
        return self.uml_interface.rename_parameter(self.class_name, self.method_num, self.old_param_name, self.new_param_name)

    def undo(self):
        return self.uml_interface.rename_parameter(self.class_name, self.method_num, self.new_param_name, self.old_param_name)
    
class ReplaceParameterListCommand(Command):
    def __init__(self, uml_interface, class_name, method_num):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
    
    def execute(self):
        return self.uml_interface.replace_param_list(self.class_name, self.method_num)

    def undo(self):
        return self.uml_interface.replace_param_list(self.class_name, self.method_num)
        
class ChangeTypeCommand(Command):
    def __init__(self, uml_interface, class_name: str=None, method_num:int = None, input_name: str=None, new_type: str=None, 
                 is_field: bool=False, is_method: bool=False, is_param: bool=False):
        self.uml_interface = uml_interface
        self.class_name = class_name
        self.method_num = method_num
        self.input_name = input_name
        self.new_type = new_type
        self.is_field = is_field
        self.is_method = is_method
        self.is_param = is_param
        self.original_type = None  # To store the original type

    def execute(self):
        # Determine if it's a field or method and capture the original type
        if self.is_field:
            chosen_field = self.uml_interface.get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                self.original_type = chosen_field._get_type()
                return self.uml_interface.change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.new_type, is_field=True)

        elif self.is_method:
            chosen_method = self.uml_interface.get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is None:
                return False
            self.original_type = chosen_method._get_type()
            return self.uml_interface.change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.new_type, is_method=True)

    def undo(self):
        # Restore the original type
        if self.is_field and self.original_type:
            return self.uml_interface.change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.original_type, is_field=True)
        elif self.is_method and self.original_type:
            return self.uml_interface.change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.original_type, is_method=True)
        return False

class InputHandler:
    def __init__(self):
        self.command_list = []
        self.pointer = -1  # Start before the first command

    def execute_command(self, command):
        # Clear all commands after the current pointer position (redoing new commands)
        del self.command_list[self.pointer + 1:]
        # Execute the new command and add it to the list
        is_command_valid = command.execute()
        if not is_command_valid:
            return
        self.command_list.append(command)
        self.pointer += 1

    def undo(self):
        if self.pointer >= 0:
            command = self.command_list[self.pointer]
            command.undo()
            self.pointer -= 1

    def redo(self):
        if self.pointer < len(self.command_list) - 1:
            self.pointer += 1
            command = self.command_list[self.pointer]
            command.execute()

def main():
    cli_view = CLIView()
    interface = Interface(cli_view)
    interface.attach_observer(cli_view)
    command_manager = InputHandler()

    # Add a class
    add_class_command_1 = AddClassCommand(interface, "Human")
    command_manager.execute_command(add_class_command_1)
    
    add_method_command_1 = AddMethodCommand(interface, "Human", "void", "attack")
    command_manager.execute_command(add_method_command_1)
    add_method_command_1 = AddMethodCommand(interface, "Human", "void", "run")
    command_manager.execute_command(add_method_command_1)
    add_method_command_1 = AddMethodCommand(interface, "Human", "void", "walk")
    command_manager.execute_command(add_method_command_1)
    
    # cli_view._display_uml_data(interface.get_main_data())
    
    # change_method_name_command = RenameMethodCommand(interface, class_name="Human", method_num="1", new_name="sprint")
    # command_manager.execute_command(change_method_name_command)
    
    # change_method_name_command = RenameMethodCommand(interface, class_name="Human", method_num="2", new_name="swim")
    # command_manager.execute_command(change_method_name_command)
    
    add_param_command = AddParameterCommand(interface, class_name="Human", method_num="1", param_type="int", param_name="dmg")
    command_manager.execute_command(add_param_command)
    add_param_command = AddParameterCommand(interface, class_name="Human", method_num="1", param_type="string", param_name="stats")
    command_manager.execute_command(add_param_command)
    add_param_command = AddParameterCommand(interface, class_name="Human", method_num="2", param_type="int", param_name="stamina")
    command_manager.execute_command(add_param_command)
    
    rename_param_command = RenameParameterCommand(interface, class_name="Human", method_num="1", old_param_name="dmg", new_param_name="critical")
    command_manager.execute_command(rename_param_command)
    
    rename_param_command = RenameParameterCommand(interface, class_name="Human", method_num="1", old_param_name="stats", new_param_name="human_name")
    command_manager.execute_command(rename_param_command)
    
    rename_param_command = RenameParameterCommand(interface, class_name="Human", method_num="2", old_param_name="stamina", new_param_name="attack_rate")
    command_manager.execute_command(rename_param_command)
    
    # cli_view._display_uml_data(interface.get_main_data())
    
    # delete_param_command = DeleteParameterCommand(interface, class_name="Human", method_num="1", param_name="dmg")
    # command_manager.execute_command(delete_param_command)
    
    # delete_param_command = DeleteParameterCommand(interface, class_name="Human", method_num="1", param_name="stats")
    # command_manager.execute_command(delete_param_command)
    
    cli_view._display_uml_data(interface.get_main_data())
    
    command_manager.undo()
    
    command_manager.undo()
    
    command_manager.undo()
    
    cli_view._display_uml_data(interface.get_main_data())
    
    command_manager.redo()
    
    command_manager.redo()
    
    command_manager.redo()
    
    cli_view._display_uml_data(interface.get_main_data())
    
if __name__ == "__main__":
    main()
