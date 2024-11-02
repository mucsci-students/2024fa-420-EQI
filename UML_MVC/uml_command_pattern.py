from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, is_undo_or_redo=False):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddClassCommand(Command):
    def __init__(self, uml_model, class_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box

    def execute(self, is_undo_or_redo=False):
        is_class_added = self.uml_model._add_class(self.class_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_added:
            self.view.scene().addItem(self.class_box)
        return is_class_added

    def undo(self):
        self.view.scene().removeItem(self.class_box)
        self.uml_model._delete_class(self.class_name, is_undo_or_redo=True)

class DeleteClassCommand(Command):
    def __init__(self, uml_model, class_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box

    def execute(self, is_undo_or_redo=False):
        self.view.scene().removeItem(self.class_box)
        return self.uml_model._delete_class(self.class_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        self.view.scene().addItem(self.class_box)
        self.uml_model._add_class(self.class_name , is_undo_or_redo=True)
        
class RenameClassCommand(Command):
    def __init__(self, uml_model, class_name, new_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.new_name = new_name
        self.view = view
        self.class_box = class_box

    def execute(self, is_undo_or_redo=False):
        is_class_renamed = self.uml_model._rename_class(self.class_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_renamed:
            self.class_box.class_name_text.setPlainText(self.new_name)
            self.class_box.update_box()
        return is_class_renamed

    def undo(self):
        self.class_box.class_name_text.setPlainText(self.class_name)
        return self.uml_model._rename_class(self.new_name, self.class_name, is_undo_or_redo=True)
        
class AddFieldCommand(Command):
    def __init__(self, uml_model, class_name, type, field_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_type = type
        self.field_name = field_name
        self.view = view
        self.class_box = class_box

    def execute(self, is_undo_or_redo=False):
        is_field_added = self.uml_model._add_field(self.class_name, self.field_type, self.field_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_added:
            # Create a text item for the field and add it to the list
                field_text = self.class_box.create_text_item(self.field_type + " " + self.field_name, is_field=True, selectable=False, color=self.class_box.text_color)
                field_key = (self.field_type, self.field_name)
                self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                self.class_box.field_key_list.append(field_key)  # Track the field name in the name list
                self.class_box.update_box()
        return is_field_added

    def undo(self):
        for field_key in self.class_box.field_key_list:
            if field_key[1] == self.field_name:
                self.class_box.field_key_list.remove(field_key)  # Remove from the name list
                self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))  # Remove the text item from the scene
        self.class_box.update_box()
        return self.uml_model._delete_field(self.class_name, self.field_name, is_undo_or_redo=True)

class DeleteFieldCommand(Command):
    def __init__(self, uml_model, class_name, field_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_name = field_name
        self.field_type = None  # To store the type of the field when it's deleted
        self.view = view
        self.class_box = class_box
        self.position = None  # To store the position of the field when deleted

    def execute(self, is_undo_or_redo=False):
        # Capture the field type before deleting the field
        chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.field_name, is_field = True)
        if chosen_field is not None:
            self.field_type = chosen_field._get_type()
        for index, field_key in enumerate(self.class_box.field_key_list):
            if field_key[1] == self.field_name:
                self.position = index
                self.class_box.field_key_list.remove(field_key)  # Remove from the name list
                self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))  # Remove the text item from the scene
        self.class_box.update_box()
        return self.uml_model._delete_field(self.class_name, self.field_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        is_field_added = self.uml_model._add_field(self.class_name, self.field_type, self.field_name, is_undo_or_redo=True)
        if is_field_added:
            # Create a text item for the field and add it to the list
                field_text = self.class_box.create_text_item(self.field_type + " " + self.field_name, is_field=True, selectable=False, color=self.class_box.text_color)
                field_key = (self.field_type, self.field_name)
                self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                self.class_box.field_key_list.insert(self.position, field_key)
                self.class_box.update_box()
        return is_field_added
    
class RenameFieldCommand(Command):
    def __init__(self, uml_model, class_name, old_field_name, new_field_name, view, class_box):
        self.uml_model = uml_model
        self.class_name = class_name
        self.old_name = old_field_name
        self.new_name = new_field_name
        self.view = view
        self.class_box = class_box

    def execute(self, is_undo_or_redo=False):
        is_field_renamed = self.uml_model._rename_field(self.class_name, self.old_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_renamed:
            # Update the field name in the list and refresh the display
            for field_key in self.class_box.field_list:
                if field_key[1] == self.old_name:
                    new_key = (field_key[0], self.new_name)
                    self.class_box.field_list[new_key] = self.class_box.field_list.pop(field_key)
                    self.class_box.field_list[new_key].setPlainText(field_key[0] + " " + self.new_name)
                    # Update field_key_list
                    index = self.class_box.field_key_list.index(field_key)
                    self.class_box.field_key_list[index] = new_key
                    break  # Exit the loop after finding the matching field
            self.class_box.update_box()  # Refresh the box display 
        return is_field_renamed

    def undo(self):
        is_field_renamed = self.uml_model._rename_field(self.class_name, self.new_name, self.old_name, is_undo_or_redo=True)
        if is_field_renamed:
            # Update the field name in the list and refresh the display
            for field_key in self.class_box.field_list:
                if field_key[1] == self.new_name:
                    new_key = (field_key[0], self.old_name)
                    self.class_box.field_list[new_key] = self.class_box.field_list.pop(field_key)
                    self.class_box.field_list[new_key].setPlainText(field_key[0] + " " + self.old_name)
                    # Update field_key_list
                    index = self.class_box.field_key_list.index(field_key)
                    self.class_box.field_key_list[index] = new_key
                    break  # Exit the loop after finding the matching field
            self.class_box.update_box()  # Refresh the box display 
        return is_field_renamed

class AddMethodCommand(Command):
    def __init__(self, uml_model, class_name, type, method_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.type = type
        self.method_name = method_name

    def execute(self, is_undo_or_redo=False):
        return self.uml_model._add_method(self.class_name, self.type, self.method_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        return self.uml_model._delete_method(self.class_name, str(self.uml_model._current_number_of_method), is_undo_or_redo=True)
    
class DeleteMethodCommand(Command):
    def __init__(self, uml_model, class_name, method_num):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.method_name = None
        self.type = None

    def execute(self, is_undo_or_redo=False):
        # Capture the field type before deleting the method
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.type = chosen_method._get_type()
        self.method_name = chosen_method._get_name()
        return self.uml_model._delete_method(self.class_name, self.method_num, is_undo_or_redo=is_undo_or_redo)
        
    def undo(self):
        if self.type and self.method_name:
            return self.uml_model._add_method(self.class_name, self.type, self.method_name, is_undo_or_redo=True)
        return False
    
class RenameMethodCommand(Command):
    def __init__(self, uml_model, class_name, method_num, new_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_name = None
        self.new_name = new_name

    def execute(self, is_undo_or_redo=False):
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.old_name = chosen_method._get_name()
        return self.uml_model._rename_method(self.class_name, self.method_num, self.new_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        if self.old_name:
            return self.uml_model._rename_method(self.class_name, self.method_num, self.old_name, is_undo_or_redo=True)
    
class AddParameterCommand(Command):
    def __init__(self, uml_model, class_name: str = None, method_num: str = None, param_type: str = None, param_name: str = None):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_type = param_type
        self.param_name = param_name

    def execute(self, is_undo_or_redo=False):
        return self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=True)
    
class DeleteParameterCommand(Command):
    def __init__(self, uml_model, class_name, method_num, param_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_name = param_name
        self.param_type = None

    def execute(self, is_undo_or_redo=False):
        chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.param_name)
        if chosen_param is None:
            return False
        self.param_type = chosen_param._get_type()
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=is_undo_or_redo)
        
    def undo(self):
        if self.param_type:
            return self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=True)
        
class RenameParameterCommand(Command):
    def __init__(self, uml_model, class_name, method_num, old_param_name, new_param_name):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_name = old_param_name
        self.new_param_name = new_param_name

    def execute(self, is_undo_or_redo=False):
        return self.uml_model._rename_parameter(self.class_name, self.method_num, self.old_param_name, self.new_param_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        return self.uml_model._rename_parameter(self.class_name, self.method_num, self.new_param_name, self.old_param_name, is_undo_or_redo=True)
    
class ReplaceParameterListCommand(Command):
    def __init__(self, uml_model, class_name, method_num, new_param_list):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_list = None
        self.new_param_list = new_param_list
    
    def execute(self, is_undo_or_redo=False):
        self.old_param_list = self.uml_model._get_param_list(self.class_name, self.method_num)
        return self.uml_model._replace_param_list(self.class_name, self.method_num, self.new_param_list, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        if self.old_param_list:
            return self.uml_model._replace_param_list(self.class_name, self.method_num, self.old_param_list, is_undo_or_redo=True)

class AddRelationshipCommand(Command):
    def __init__(self, uml_model, source_class, dest_class, rel_type):
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = rel_type
    
    def execute(self, is_undo_or_redo=False):
        return self.uml_model._add_relationship(self.source_class, self.dest_class, self.rel_type, is_gui=False, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        return self.uml_model._delete_relationship(self.source_class, self.dest_class, is_undo_or_redo=True)
    
class DeleteRelationshipCommand(Command):
    def __init__(self, uml_model, source_class, dest_class):
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = None
    
    def execute(self, is_undo_or_redo=False):
        self.rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
        return self.uml_model._delete_relationship(self.source_class, self.dest_class, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        if self.rel_type:
            return self.uml_model._add_relationship(self.source_class, self.dest_class, self.rel_type, is_gui=False, is_undo_or_redo=True)

class ChangeTypeCommand(Command):
    def __init__(self, uml_model, 
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

    def execute(self, is_undo_or_redo=False):
        # Determine if it's a field or method and capture the original type
        if self.is_field:
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                self.original_type = chosen_field._get_type()
                return self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.new_type, is_field=True, is_undo_or_redo=is_undo_or_redo)

        elif self.is_method:
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is None:
                return False
            self.original_type = chosen_method._get_type()
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.new_type, is_method=True, is_undo_or_redo=is_undo_or_redo)
        
        elif self.is_param:
            chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.input_name)
            if chosen_param is None:
                return False
            self.original_type = chosen_param._get_type()
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, new_type=self.new_type, is_param=True, is_undo_or_redo=is_undo_or_redo)
        
        elif self.is_rel:
            self.original_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
            return self.uml_model._change_data_type(source_class=self.source_class, dest_class=self.dest_class, new_type=self.new_type, is_rel=True, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        # Restore the original type
        if self.is_field and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, new_type=self.original_type, is_field=True, is_undo_or_redo=True)
        elif self.is_method and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, new_type=self.original_type, is_method=True, is_undo_or_redo=True)
        elif self.is_param and self.original_type:
            return self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, new_type=self.original_type, is_param=True, is_undo_or_redo=True)
        elif self.is_rel and self.original_type:
             return self.uml_model._change_data_type(source_class=self.source_class, dest_class=self.dest_class, new_type=self.original_type, is_rel=True, is_undo_or_redo=True)
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
            return False
        self.command_list.append(command)
        self.pointer += 1
        return True

    def undo(self):
        if self.pointer >= 0:
            command = self.command_list[self.pointer]
            command.undo()
            self.pointer -= 1

    def redo(self):
        if self.pointer < len(self.command_list) - 1:
            self.pointer += 1
            command = self.command_list[self.pointer]
            command.execute(is_undo_or_redo=True)