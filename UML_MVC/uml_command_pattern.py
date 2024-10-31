from abc import ABC, abstractmethod
from UML_MVC.UML_MODEL.uml_model import UMLModel as Model

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddClassCommand(Command):
    def __init__(self, uml_model: Model, class_name):
        self.uml_model = uml_model
        self.class_name = class_name

    def execute(self):
        return self.uml_model._add_class(self.class_name)

    def undo(self):
        self.uml_model._delete_class(self.class_name)

class DeleteClassCommand(Command):
    def __init__(self, uml_model: Model, class_name):
        self.uml_model = uml_model
        self.class_name = class_name

    def execute(self):
        return self.uml_model._delete_class(self.class_name)

    def undo(self):
        self.uml_model._add_class(self.class_name)
        
class RenameClassCommand(Command):
    def __init__(self, uml_model: Model, class_name, new_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.new_name = new_name

    def execute(self):
        return self.uml_model._rename_class(self.class_name, self.new_name)

    def undo(self):
        return self.uml_model._rename_class(self.new_name, self.class_name)
        
class AddFieldCommand(Command):
    def __init__(self, uml_model: Model, class_name, type, field_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.type = type
        self.field_name = field_name

    def execute(self):
        return self.uml_model._add_field(self.class_name, self.type, self.field_name)

    def undo(self):
        return self.uml_model._delete_field(self.class_name, self.field_name)

class DeleteFieldCommand(Command):
    def __init__(self, uml_model: Model, class_name, field_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_name = field_name
        self.field_type = None  # To store the type of the field when it's deleted

    def execute(self):
        # Capture the field type before deleting the field
        chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.field_name, is_field = True)
        if chosen_field is not None:
            self.field_type = chosen_field._get_type()
        return self.uml_model._delete_field(self.class_name, self.field_name)

    def undo(self):
        return self.uml_model._add_field(self.class_name, self.field_type, self.field_name)
    
class RenameFieldCommand(Command):
    def __init__(self, uml_model: Model, class_name, old_field_name, new_field_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.old_name = old_field_name
        self.new_name = new_field_name

    def execute(self):
        return self.uml_model._rename_field(self.class_name, self.old_name, self.new_name)

    def undo(self):
        return self.uml_model._rename_field(self.class_name, self.new_name, self.old_name)

class AddMethodCommand(Command):
    def __init__(self, uml_model: Model, class_name, type, method_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.type = type
        self.method_name = method_name

    def execute(self):
        return self.uml_model._add_method(self.class_name, self.type, self.method_name)

    def undo(self):
        return self.uml_model._delete_method(self.class_name, str(self.uml_model._Model._current_number_of_method))
    
class DeleteMethodCommand(Command):
    def __init__(self, uml_model: Model, class_name, method_num):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.method_name = None
        self.type = None

    def execute(self):
        # Capture the field type before deleting the method
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.type = chosen_method._get_type()
        self.method_name = chosen_method._get_name()
        return self.uml_model._delete_method(self.class_name, self.method_num)
        
    def undo(self):
        if self.type and self.method_name:
            return self.uml_model._add_method(self.class_name, self.type, self.method_name)
        return False
    
class RenameMethodCommand(Command):
    def __init__(self, uml_model: Model, class_name, method_num, new_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_name = None
        self.new_name = new_name

    def execute(self):
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.old_name = chosen_method._get_name()
        return self.uml_model._rename_method(self.class_name, self.method_num, self.new_name)

    def undo(self):
        if self.old_name:
            return self.uml_model._rename_method(self.class_name, self.method_num, self.old_name)
    
class AddParameterCommand(Command):
    def __init__(self, uml_model: Model, class_name: str = None, method_num: str = None, param_type: str = None, param_name: str = None):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_type = param_type
        self.param_name = param_name

    def execute(self):
        return self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name)

    def undo(self):
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name)
    
class DeleteParameterCommand(Command):
    def __init__(self, uml_model: Model, class_name, method_num, param_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_name = param_name
        self.param_type = None

    def execute(self):
        chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.param_name)
        if chosen_param is None:
            return False
        self.param_type = chosen_param._get_type()
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name)
        
    def undo(self):
        if self.param_type:
            return self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name)
        
class RenameParameterCommand(Command):
    def __init__(self, uml_model: Model, class_name, method_num, old_param_name, new_param_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_name = old_param_name
        self.new_param_name = new_param_name

    def execute(self):
        return self.uml_model._rename_parameter(self.class_name, self.method_num, self.old_param_name, self.new_param_name)

    def undo(self):
        return self.uml_model._rename_parameter(self.class_name, self.method_num, self.new_param_name, self.old_param_name)
    
class ReplaceParameterListCommand(Command):
    def __init__(self, uml_model: Model, class_name, method_num, new_param_list):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_list = None
        self.new_param_list = new_param_list
    
    def execute(self):
        self.old_param_list = self.uml_model._get_param_list(self.class_name, self.method_num)
        return self.uml_model._replace_param_list(self.class_name, self.method_num, self.new_param_list)

    def undo(self):
        if self.old_param_list:
            return self.uml_model._replace_param_list(self.class_name, self.method_num, self.old_param_list)

class AddRelationshipCommand(Command):
    def __init__(self, uml_model: Model, source_class, dest_class, rel_type):
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = rel_type
    
    def execute(self):
        return self.uml_model._add_relationship(self.source_class, self.dest_class, self.rel_type, is_gui=False)

    def undo(self):
        return self.uml_model._delete_relationship(self.source_class, self.dest_class)
    
class DeleteRelationshipCommand(Command):
    def __init__(self, uml_model: Model, source_class, dest_class):
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = None
    
    def execute(self):
        self.rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
        return self.uml_model._delete_relationship(self.source_class, self.dest_class)

    def undo(self):
        if self.rel_type:
            return self.uml_model._add_relationship(self.source_class, self.dest_class, self.rel_type, is_gui=False)

class ChangeTypeCommand(Command):
    def __init__(self, uml_model: Model, 
                 class_name: str=None, method_num:int = None, 
                 input_name: str=None, source_class: str=None,
                 dest_class: str=None, new_type: str=None, 
                 is_field: bool=None,is_method: bool=None, 
                 is_param: bool=None, is_rel: bool=None):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.input_name = input_name
        self.source_class = source_class
        self.dest_class = dest_class
        self.new_type = new_type
        self.is_field = is_field
        self.is_method = is_method
        self.is_param = is_param
        self.is_rel = is_rel
        self.original_type = None  # To store the original type

    def execute(self):
        # Determine if it's a field or method and capture the original type
        if self.is_field:
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                self.original_type = chosen_field._get_type()
                return self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.new_type, is_field=True)

        elif self.is_method:
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is None:
                return False
            self.original_type = chosen_method._get_type()
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.new_type, is_method=True)
        
        elif self.is_param:
            chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.input_name)
            if chosen_param is None:
                return False
            self.original_type = chosen_param._get_type()
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, new_type=self.new_type, is_param=True)
        
        elif self.is_rel:
            self.original_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
            return self.uml_model._change_data_type(source_class=self.source_class, dest_class=self.dest_class, new_type=self.new_type, is_rel=True)

    def undo(self):
        # Restore the original type
        if self.is_field and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.original_type, is_field=True)
        elif self.is_method and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.original_type, is_method=True)
        elif self.is_param and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, new_type=self.original_type, is_param=True)
        elif self.is_rel and self.original_type:
             return self.uml_model._change_data_type(source_class=self.source_class, dest_class=self.dest_class, new_type=self.original_type, is_rel=True)
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