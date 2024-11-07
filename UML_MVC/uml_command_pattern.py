from abc import ABC, abstractmethod
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import UMLArrow as ArrowLine

class Command(ABC):
    @abstractmethod
    def execute(self, is_undo_or_redo=False):
        pass

    @abstractmethod
    def undo(self):
        pass
    
class MoveUnitCommand(Command):
    def __init__(self, class_box, old_x, old_y, new_x, new_y):
        self.class_box = class_box
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        
    def execute(self, is_undo_or_redo=False):
        if self.class_box:
            self.class_box.setPos(self.new_x, self.new_y)
            self.class_box.update_box()
            return True
        return False
        
    def undo(self):
        if self.class_box:
            self.class_box.setPos(self.old_x, self.old_y)
            self.class_box.update_box()
            return True
        return False




class AddClassCommand(Command):
    def __init__(self, uml_model, class_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_class_added = self.uml_model._add_class(self.class_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_added and self.is_gui:
            self.view.scene().addItem(self.class_box)
            self.view.class_name_list[self.class_name] = self.class_box
        return is_class_added

    def undo(self):
        if self.is_gui:       
            # Create a copy of the arrow_line_list to avoid modifying the list while iterating
            arrow_lines = list(self.class_box.arrow_line_list)
            for arrow_line in arrow_lines:
                # Remove the arrow from the scene
                if arrow_line.scene() == self.view.scene():  # Check if the arrow is in the current scene
                    self.view.scene().removeItem(arrow_line)
                # Remove the arrow from the source class's arrow_line_list if it's not the selected class
                if arrow_line.source_class != self.class_box:
                    if arrow_line in arrow_line.source_class.arrow_line_list:
                        arrow_line.source_class.arrow_line_list.remove(arrow_line)
                # Remove the arrow from the destination class's arrow_line_list if it's not the selected class
                if arrow_line.dest_class != self.class_box:
                    if arrow_line in arrow_line.dest_class.arrow_line_list:
                        arrow_line.dest_class.arrow_line_list.remove(arrow_line)
                # Remove the arrow from the selected class's arrow_line_list
                self.class_box.arrow_line_list.remove(arrow_line)
                
            # Clear all fields and methods in the class_box
            for field_item in self.class_box.field_list.values():
                if field_item.scene() == self.view.scene():
                    self.view.scene().removeItem(field_item)

            for method_entry in self.class_box.method_list:
                if method_entry["method_text"].scene() == self.view.scene():
                    self.view.scene().removeItem(method_entry["method_text"])
                method_entry["method_key"] = None
                method_entry["method_text"] = None
                method_entry["parameters"] = []
                
            # Clear lists to avoid any visual overlaps on restore
            self.class_box.field_list = {}
            self.class_box.field_key_list = []
            self.class_box.method_list = []
            self.class_box.param_num = 0 
            # self.view.model._current_number_of_method = 0  
            
            # Remove the class from the class_name_list and scene
            self.view.class_name_list.pop(self.class_name, None)  
            if self.class_box.scene() == self.view.scene():
                self.view.scene().removeItem(self.class_box)    
        return self.uml_model._delete_class(self.class_name, is_undo_or_redo=True)
    
class DeleteClassCommand(Command):
    def __init__(self, uml_model, class_name, view=None, class_box=None, is_gui=False):
        super().__init__()
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
        self.cli_class_list = None
        self.cli_main_data = None

        # Store the state of the class before deletion
        self.stored_fields = []          # List of tuples: (field_type, field_name)
        self.stored_methods = []         # List of tuples: (method_type, method_name)
        self.stored_parameters = {}      # Dict: {method_key: [(param_type, param_name), ...]}
        self.stored_relationships = {}   # List of arrow_line objects

    def execute(self, is_undo_or_redo=False):
        self.cli_main_data = self.uml_model._get_main_data()
        if self.is_gui:
            # 0. Store relationship
            self.stored_relationships = self.view.relationship_track_list
            
            # 1. Store all fields before deletion
            self.stored_fields = list(self.class_box.field_list.keys())

            # 2. Store all methods and their parameters before deletion
            for method_entry in self.class_box.method_list:
                method_key = method_entry["method_key"]
                self.stored_methods.append(method_key)
                self.stored_parameters[method_key] = list(method_entry["parameters"])

            # 3. Remove all associated arrow lines from the scene
            # Create a copy of the arrow_line_list to avoid modifying the list while iterating
            arrow_lines = list(self.class_box.arrow_line_list)
            for arrow_line in arrow_lines:
                # Remove the arrow from the scene
                if arrow_line.scene() == self.view.scene():  # Check if the arrow is in the current scene
                    self.view.scene().removeItem(arrow_line)
                # Remove the arrow from the source class's arrow_line_list if it's not the selected class
                if arrow_line.source_class != self.class_box:
                    if arrow_line in arrow_line.source_class.arrow_line_list:
                        arrow_line.source_class.arrow_line_list.remove(arrow_line)
                # Remove the arrow from the destination class's arrow_line_list if it's not the selected class
                if arrow_line.dest_class != self.class_box:
                    if arrow_line in arrow_line.dest_class.arrow_line_list:
                        arrow_line.dest_class.arrow_line_list.remove(arrow_line)
                # Remove the arrow from the selected class's arrow_line_list
                self.class_box.arrow_line_list.remove(arrow_line)

            # 4. Remove all fields from the scene
            for field_key in self.stored_fields:
                field_type, field_name = field_key
                field_text = self.class_box.field_list.get(field_key)
                if field_text and field_text.scene() == self.view.scene():
                    self.view.scene().removeItem(field_text)

            # 5. Remove all methods and their parameters from the scene
            for method_entry in self.class_box.method_list:
                method_text = method_entry["method_text"]
                if method_text and method_text.scene() == self.view.scene():
                    self.view.scene().removeItem(method_text)

            # 6. Update the class box and remove it from the scene
            self.class_box.update_box()
            if self.class_box.scene() == self.view.scene():
                self.view.scene().removeItem(self.class_box)

            # 7. Clear lists to avoid any visual overlaps on restore
            self.class_box.field_list = {}
            self.class_box.field_key_list = []
            self.class_box.method_list = []
            self.class_box.param_num = 0
            self.view.relationship_track_list = {}
            self.view.class_name_list.pop(self.class_name, None)

        # 8. Delete the class from the model
        result = self.uml_model._delete_class(self.class_name, is_undo_or_redo=is_undo_or_redo)
        return result

    def undo(self):
        if self.is_gui:
            if self.class_name in self.view.class_name_list:
                return False
            # 1. Re-execute the AddClassCommand to add the class back
            add_class_command = AddClassCommand(
                uml_model=self.uml_model,
                class_name=self.class_name,
                view=self.view,
                class_box=self.class_box,
                is_gui=True
            )
            add_class_command.execute(is_undo_or_redo=True)

            # 2. Re-execute all AddFieldCommands to restore fields
            for field_key in self.stored_fields:
                field_type, field_name = field_key
                add_field_command = AddFieldCommand(
                    uml_model=self.uml_model,
                    class_name=self.class_name,
                    type=field_type,
                    field_name=field_name,
                    view=self.view,
                    class_box=self.class_box,
                    is_gui=True
                )
                add_field_command.execute(is_undo_or_redo=True)

            # 3. Re-execute all AddMethodCommands to restore methods
            for i, method_key in enumerate(self.stored_methods, start=1):
                method_type, method_name = method_key
                add_method_command = AddMethodCommand(
                    uml_model=self.uml_model,
                    class_name=self.class_name,
                    type=method_type,
                    method_name=method_name,
                    view=self.view,
                    class_box=self.class_box,
                    is_gui=True
                )
                add_method_command.execute(is_undo_or_redo=True)

                # 4. Re-execute all AddParameterCommands for each method
                parameters = self.stored_parameters.get(method_key, [])
                method_num = str(i)  # Assign method_num based on the order of restoration
                for param_type, param_name in parameters:
                    add_param_command = AddParameterCommand(
                        uml_model=self.uml_model,
                        class_name=self.class_name,
                        method_num=method_num,
                        param_type=param_type,
                        param_name=param_name,
                        view=self.view,
                        class_box=self.class_box,
                        is_gui=True
                    )
                    add_param_command.execute(is_undo_or_redo=True)

            # 5. Restore all relationships (arrow lines)
            for source_class_str, arrow_list in self.stored_relationships.items():
                # Retrieve the source class object from the view's class_name_list
                source_class_obj = self.view.class_name_list.get(source_class_str)
                if not source_class_obj:
                    continue  # Skip restoring this relationship if source class doesn't exist

                # Iterate over each relationship in the stored arrow_list
                for relationship in arrow_list:  # Each relationship is a dictionary
                    dest_class_str = relationship["dest_class"]  # Get the destination class name
                    arrow_line = relationship["arrow_list"]  # Get the corresponding arrow line
                    
                    # Retrieve the destination class object from the view's class_name_list
                    dest_class_obj = self.view.class_name_list.get(dest_class_str)
                    if not dest_class_obj:
                        continue  # Skip restoring this relationship if destination class doesn't exist

                    # Ensure that class_box is set to the source class's class_box
                    source_class_box = source_class_obj  

                    # Instantiate the AddRelationshipCommand with class objects
                    add_relationship_command = AddRelationshipCommand(
                        uml_model=self.uml_model,
                        source_class=source_class_str,  # Pass class object, not string
                        dest_class=dest_class_str,       # Pass class object, not string
                        rel_type=arrow_line.arrow_type,  # Use the stored relationship type
                        view=self.view,
                        class_box=source_class_box,      # Set to source class's class_box
                        is_gui=True
                    )
                    add_relationship_command.execute(is_undo_or_redo=True)
        else:
            # 1. Re-execute the AddClassCommand to add the class back
            if self.class_name in self.uml_model._get_class_list():
                return False
            main_data = self.cli_main_data
            class_data = main_data["classes"]
            relationship_data = main_data["relationships"]
            extracted_class_data = self.uml_model._extract_class_data(class_data)
 
            for each_pair in extracted_class_data:
                for class_name, data in each_pair.items():
                    field_list = data["fields"]
                    method_list = data["method_list"]

                    if class_name != self.class_name:
                        continue
                    add_class_command = AddClassCommand(
                        uml_model=self.uml_model,
                        class_name=self.class_name,
                        view=self.view,
                        class_box=self.class_box,
                    )
                    add_class_command.execute(is_undo_or_redo=True)
                    
                    # self.uml_model._add_class(self.class_name, is_undo_or_redo=True)
                    
                    for each_field in field_list:
                        field_name = each_field["name"]
                        field_type = each_field["type"]
                        # 2. Re-execute all AddFieldCommands to restore fields
                        add_field_command = AddFieldCommand(
                            uml_model=self.uml_model,
                            class_name=self.class_name,
                            type=field_type,
                            field_name=field_name,
                            view=self.view,
                            class_box=self.class_box,
                        )
                        add_field_command.execute(is_undo_or_redo=True)
                            
                        # self.uml_model._add_field(self.class_name, field_type, field_name, is_undo_or_redo=True)
                        
                    method_num = "0"
                    i = 0
                    for each_element in method_list:
                        i = i + 1
                        method_num = f"{i}"
                        method_name = each_element["name"]
                        return_type = each_element["return_type"]
                        parameter_list = each_element["params"]
                        
                        # 3. Re-execute all AddMethodCommands to restore methods
                        add_method_command = AddMethodCommand(
                            uml_model=self.uml_model,
                            class_name=self.class_name,
                            type=return_type,
                            method_name=method_name,
                            view=self.view,
                            class_box=self.class_box,
                        )
                        add_method_command.execute(is_undo_or_redo=True)
                            
                        # self.uml_model._add_method(class_name, return_type, method_name, is_loading=True)
                        
                        for param in parameter_list:
                            param_type = param["type"]
                            param_name = param["name"]
                            # 4. Re-execute all AddParameterCommands for each method
                            add_param_command = AddParameterCommand(
                                uml_model=self.uml_model,
                                class_name=self.class_name,
                                method_num=method_num,
                                param_type=param_type,
                                param_name=param_name,
                                view=self.view,
                                class_box=self.class_box,
                            )
                            add_param_command.execute(is_undo_or_redo=True)
                                
                            # self.uml_model._add_parameter(class_name, method_num, param_type, param_name, is_loading=True)
                            
            # Recreate relationships from the loaded data
            for each_dictionary in relationship_data:
                if each_dictionary["source"] == self.class_name:
                    self.uml_model._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True, is_gui=False)
                if each_dictionary["destination"] == self.class_name:
                    self.uml_model._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True, is_gui=False)
                
        self.stored_fields = []
        self.stored_methods = []
        self.stored_parameters = {}
        self.stored_relationships = {}
        return True

class RenameClassCommand(Command):
    def __init__(self, uml_model, class_name, new_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.new_name = new_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_class_renamed = self.uml_model._rename_class(self.class_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_renamed and self.is_gui:
            self.class_box.class_name_text.setPlainText(self.new_name)
            self.class_box.update_box()
        return is_class_renamed

    def undo(self):
        if self.is_gui:
            self.class_box.class_name_text.setPlainText(self.class_name)
        return self.uml_model._rename_class(self.new_name, self.class_name, is_undo_or_redo=True)
        
class AddFieldCommand(Command):
    def __init__(self, uml_model, class_name, type, field_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_type = type
        self.field_name = field_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_field_added = self.uml_model._add_field(self.class_name, self.field_type, self.field_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_added and self.is_gui:
            # Create a text item for the field and add it to the list
                field_text = self.class_box.create_text_item(self.field_type + " " + self.field_name, is_field=True, selectable=False, color=self.class_box.text_color)
                field_key = (self.field_type, self.field_name)
                self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                self.class_box.field_key_list.append(field_key)  # Track the field name in the name list
                self.class_box.update_box()
        return is_field_added

    def undo(self):
        if self.is_gui:
            for field_key in self.class_box.field_key_list:
                if field_key[1] == self.field_name:
                    self.class_box.field_key_list.remove(field_key)  # Remove from the name list
                    self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))  # Remove the text item from the scene
            self.class_box.update_box()
        return self.uml_model._delete_field(self.class_name, self.field_name, is_undo_or_redo=True)

class DeleteFieldCommand(Command):
    def __init__(self, uml_model, class_name, field_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_name = field_name
        self.field_type = None  # To store the type of the field when it's deleted
        self.view = view
        self.class_box = class_box
        self.position = None  # To store the position of the field when deleted
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        # Capture the field type before deleting the field
        if self.is_gui:
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
        if is_field_added and self.is_gui:
            # Create a text item for the field and add it to the list
                field_text = self.class_box.create_text_item(self.field_type + " " + self.field_name, is_field=True, selectable=False, color=self.class_box.text_color)
                field_key = (self.field_type, self.field_name)
                self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                self.class_box.field_key_list.insert(self.position, field_key)
                self.class_box.update_box()
        return is_field_added
    
class RenameFieldCommand(Command):
    def __init__(self, uml_model, class_name, old_field_name, new_field_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.old_name = old_field_name
        self.new_name = new_field_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_field_renamed = self.uml_model._rename_field(self.class_name, self.old_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_renamed and self.is_gui:
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
        if is_field_renamed and self.is_gui:
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
    def __init__(self, uml_model, class_name, type, method_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_type = type
        self.method_name = method_name
        self.method_text = None
        self.view = view
        self.class_box = class_box
        self.method_num = None
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_method_added = self.uml_model._add_method(self.class_name, self.method_type, self.method_name, is_undo_or_redo=is_undo_or_redo)
        if is_method_added and self.is_gui:
            method_text = self.class_box.create_text_item(self.method_type + " " + self.method_name + "()", is_method=True, selectable=False, color=self.class_box.text_color)
            method_key = (self.method_type, self.method_name)
            
            # Create a new method entry as a dictionary with method_key, method_text, and parameters
            method_entry = {
                "method_key": method_key,
                "method_text": method_text,
                "parameters": []
            }
            # Append this dictionary to method_list
            self.class_box.method_list.append(method_entry)
            self.method_num = str(len(self.class_box.method_list))
            if len(self.class_box.method_list) == 1:
                self.class_box.create_separator(is_first=False, is_second=True)
            self.class_box.update_box()  # Update the UML box
        return is_method_added

    def undo(self):
        method_and_parameter_list = self.uml_model._get_data_from_chosen_class(self.class_name, is_method_and_param_list=True)
        current_method_index_cli = len(method_and_parameter_list)
        is_method_deleted_cli = self.uml_model._delete_method(self.class_name, str(current_method_index_cli), is_undo_or_redo=True)
        if self.is_gui:
            is_method_deleted_gui = self.uml_model._delete_method(self.class_name, str(self.method_num), is_undo_or_redo=True)
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            # Check if the item is still in the scene before removing
            if method_entry["method_text"].scene() == self.view.scene():
                self.view.scene().removeItem(method_entry["method_text"])  # Remove the method's text item
            self.class_box.method_list.pop(int(self.method_num) - 1)  # Remove the method from method_list
            self.class_box.update_box()  # Refresh the UML box
            return is_method_deleted_gui
        return is_method_deleted_cli
    
class DeleteMethodCommand(Command):
    def __init__(self, uml_model, class_name, method_num, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.method_name = None
        self.method_type = None
        self.view = view
        self.old_param_list = []
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        # Capture the field type before deleting the method
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.method_type = chosen_method._get_type()
        self.method_name = chosen_method._get_name()
        
        # Access and remove the method entry directly from method_list
        method_entry = self.class_box.method_list[int(self.method_num) - 1]
        self.old_param_list = method_entry["parameters"]
        is_method_deleted = self.uml_model._delete_method(self.class_name, self.method_num, is_undo_or_redo=is_undo_or_redo)
        
        if is_method_deleted and self.is_gui:
            # Check if the item is still in the scene before removing
            if method_entry["method_text"].scene() == self.view.scene():
                self.view.scene().removeItem(method_entry["method_text"])  # Remove the method's text item
            self.class_box.method_list.pop(int(self.method_num) - 1)  # Remove the method from method_list
            self.class_box.update_box()  # Refresh the UML box
            
        return is_method_deleted
        
    def undo(self):
        if self.method_type and self.method_name:
            is_method_added = self.uml_model._add_method(self.class_name, self.method_type, self.method_name, is_undo_or_redo=True)
            if is_method_added and self.is_gui:
                method_text = self.class_box.create_text_item(self.method_type + " " + self.method_name + "()", is_method=True, selectable=False, color=self.class_box.text_color)
                method_key = (self.method_type, self.method_name)

                # Create a new method entry as a dictionary with method_key, method_text, and parameters
                method_entry = {
                    "method_key": method_key,
                    "method_text": method_text,
                    "parameters": self.old_param_list
                }
                # Append this dictionary to method_list
                self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                if len(self.class_box.method_list) == 1:
                    self.class_box.create_separator(is_first=False, is_second=True)
                self.class_box.update_box()  # Update the UML box
            return is_method_added
        return False
    
class RenameMethodCommand(Command):
    def __init__(self, uml_model, class_name, method_num, new_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_name = None
        self.new_name = new_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.old_name = chosen_method._get_name()
        
        is_method_renamed = self.uml_model._rename_method(self.class_name, self.method_num, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_method_renamed and self.is_gui:
            # Access the method entry to rename
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            old_method_key = method_entry["method_key"]
            method_type = old_method_key[0]

            # Create the new method key with the updated name
            new_method_key = (method_type, self.new_name)
            method_entry["method_key"] = new_method_key  # Update key in method entry
            
            # Update the display text of the method in the UI
            method_text = method_entry["method_text"]
            param_list = method_entry["parameters"]
            param_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_text.setPlainText(f"{method_type} {self.new_name}({param_str})")
            
            self.class_box.update_box()  # Refresh the UML box display
        return is_method_renamed

    def undo(self):
        if self.old_name:
            is_method_renamed = self.uml_model._rename_method(self.class_name, self.method_num, self.old_name, is_undo_or_redo=True)
            if is_method_renamed and self.is_gui:
                # Access the method entry to rename
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                old_method_key = method_entry["method_key"]
                method_type = old_method_key[0]

                # Create the new method key with the updated name
                new_method_key = (method_type, self.old_name)
                method_entry["method_key"] = new_method_key  # Update key in method entry
                
                # Update the display text of the method in the UI
                method_text = method_entry["method_text"]
                param_list = method_entry["parameters"]
                param_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
                method_text.setPlainText(f"{method_type} {self.old_name}({param_str})")
                
                self.class_box.update_box()  # Refresh the UML box display
            return is_method_renamed
    
class AddParameterCommand(Command):
    def __init__(self, uml_model, class_name: str = None, method_num: str = None, 
                 param_type: str = None, param_name: str = None, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_type = param_type
        self.param_name = param_name
        self.selected_param_index = None
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_param_added = self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=is_undo_or_redo)
        if is_param_added and self.is_gui:
            # Append the parameter to the method's parameter list
            param_tuple = (self.param_type, self.param_name)
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].append(param_tuple)
            self.class_box.param_num = len(method_entry["parameters"])
            self.selected_param_index = self.class_box.param_num - 1
            self.class_box.update_box()  # Update the UML box
        return is_param_added

    def undo(self):
        if self.is_gui:
            # Access the "parameters" list for the selected method and remove the parameter by index
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].pop(self.selected_param_index)
            self.class_box.param_num = len(method_entry["parameters"])
            self.class_box.update_box()  # Refresh the UML box
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=True)
    
class DeleteParameterCommand(Command):
    def __init__(self, uml_model, class_name, method_num, param_name, selected_param_index=None, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_name = param_name
        self.param_type = None
        self.selected_param_index = selected_param_index
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.param_name)
        if chosen_param is None:
            return False
        self.param_type = chosen_param._get_type()
        if self.is_gui:
            # Access the "parameters" list for the selected method and remove the parameter by index
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].pop(self.selected_param_index)
            self.class_box.update_box()  # Refresh the UML box
            self.class_box.param_num -= 1
        return self.uml_model._delete_parameter(self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=is_undo_or_redo)
        
    def undo(self):
        if self.param_type:
            param_tuple = (self.param_type, self.param_name)
            if self.is_gui:
                # Access and remove the method entry directly from method_list
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                method_entry["parameters"].append(param_tuple)
                self.selected_param_index = len(method_entry["parameters"]) - 1
                # Append the parameter to the method's parameter list
                self.class_box.param_num += 1
                self.class_box.update_box()  # Update the UML box
            return self.uml_model._add_parameter(self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=True)
        
class RenameParameterCommand(Command):
    def __init__(self, uml_model, class_name, method_num, old_param_name, new_param_name, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_name = old_param_name
        self.new_param_name = new_param_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        is_param_renamed = self.uml_model._rename_parameter(self.class_name, self.method_num, self.old_param_name, self.new_param_name, is_undo_or_redo=is_undo_or_redo)
        if is_param_renamed and self.is_gui:
            # Iterate through the parameters to find and replace the old parameter tuple
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            for i, param_tuple in enumerate(method_entry["parameters"]):
                if param_tuple[1] == self.old_param_name:
                    # Replace the old tuple with a new one containing the new parameter name
                    method_entry["parameters"][i] = (param_tuple[0], self.new_param_name)
                    break  # Exit the loop after renaming
            self.class_box.update_box()  # Refresh the UML box
        return is_param_renamed

    def undo(self):
        is_param_renamed = self.uml_model._rename_parameter(self.class_name, self.method_num, self.new_param_name, self.old_param_name, is_undo_or_redo=True)
        if is_param_renamed and self.is_gui:
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            for i, param_tuple in enumerate(method_entry["parameters"]):
                if param_tuple[1] == self.new_param_name:
                    # Replace the old tuple with a new one containing the new parameter name
                    method_entry["parameters"][i] = (param_tuple[0], self.old_param_name)
                    break  # Exit the loop after renaming
            self.class_box.update_box()  # Refresh the UML box
        return is_param_renamed
    
class ReplaceParameterListCommand(Command):
    def __init__(self, uml_model, class_name, method_num, 
                 new_param_list_obj=None, 
                 new_param_list_str=None, view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_list_str = None
        self.old_param_list_obj = None
        self.new_param_list_str = new_param_list_str
        self.new_param_list_obj = new_param_list_obj
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
    
    def execute(self, is_undo_or_redo=False):
        is_param_list_replaced = self.uml_model._replace_param_list(self.class_name, self.method_num, self.new_param_list_str, is_undo_or_redo=is_undo_or_redo)
        if is_param_list_replaced and self.is_gui:
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            self.old_param_list_obj = method_entry["parameters"]
            self.old_param_list_str = [f"{type} {param}" for type, param in self.old_param_list_obj]
            method_entry["parameters"] = self.new_param_list_obj
            self.class_box.param_num = len(method_entry["parameters"])
            # Update the box to reflect changes
            self.class_box.update_box()
        return is_param_list_replaced

    def undo(self):
        is_param_list_replaced = self.uml_model._replace_param_list(self.class_name, self.method_num, self.old_param_list_str, is_undo_or_redo=True)
        if is_param_list_replaced and self.is_gui:
            # Access and remove the method entry directly from method_list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            self.new_param_list_obj = method_entry["parameters"]
            method_entry["parameters"] = self.old_param_list_obj
            self.class_box.param_num = len(method_entry["parameters"])
            # Update the box to reflect changes
            self.class_box.update_box()
        return is_param_list_replaced
    
class AddRelationshipCommand(Command):
    def __init__(self, uml_model, source_class, dest_class, rel_type, view=None, class_box=None, is_gui=False):
        super().__init__()
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = rel_type
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
        self.arrow_line = None
    
    def execute(self, is_undo_or_redo=False):
        is_relationship_added = self.uml_model._add_relationship(
            self.source_class, 
            self.dest_class, 
            self.rel_type, 
            is_gui=self.is_gui, 
            is_undo_or_redo=is_undo_or_redo
        )
        if is_relationship_added and self.is_gui:
            self.class_box.is_source_class = True
            source_class_obj = self.class_box
            dest_class_obj = self.view.class_name_list[self.dest_class]

            # Check for existing arrows and remove them if needed
            existing_arrow = next((arrow for arrow in self.class_box.arrow_line_list if arrow.dest_class == self.dest_class), None)
            if existing_arrow:
                self.view.scene().removeItem(existing_arrow)
                self.class_box.arrow_line_list.remove(existing_arrow)

            # Create the arrow line between the GUI components
            self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.rel_type)

            # Track the relationship in the view
            value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
            if self.source_class not in self.view.relationship_track_list:
                self.view.relationship_track_list[self.source_class] = []
            self.view.relationship_track_list[self.source_class].append(value)

            # Add the arrow to the scene to display it
            self.view.scene().addItem(self.arrow_line)
            self.class_box.update_box()
        return is_relationship_added
    
    def undo(self):
        is_relationship_deleted = self.uml_model._delete_relationship(
            self.source_class, 
            self.dest_class, 
            is_undo_or_redo=True
        )
        if is_relationship_deleted and self.is_gui:
            relationships = self.view.relationship_track_list.get(self.source_class)
            for relationship in relationships:
                if relationship["dest_class"] == self.dest_class:
                    arrow_line = relationship["arrow_list"]
                    if arrow_line.scene() == self.view.scene():
                        self.view.scene().removeItem(arrow_line)
                    relationships.remove(relationship)
                    break

            if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                self.class_box.is_source_class = False
        return is_relationship_deleted



class DeleteRelationshipCommand(Command):
    def __init__(self, uml_model, source_class, dest_class, view=None, class_box=None, is_gui=False):
        super().__init__()
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = None
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        self.rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
        is_relationship_deleted = self.uml_model._delete_relationship(
            self.source_class, 
            self.dest_class, 
            is_undo_or_redo=is_undo_or_redo
        )
        if is_relationship_deleted and self.is_gui:
            relationships = self.view.relationship_track_list.get(self.source_class)
            for relationship in relationships:
                if relationship["dest_class"] == self.dest_class:
                    arrow_line = relationship["arrow_list"]
                    if arrow_line.scene() == self.view.scene():
                        self.view.scene().removeItem(arrow_line)
                    relationships.remove(relationship)
                    break

            if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                self.class_box.is_source_class = False
        return is_relationship_deleted

    def undo(self):
        if self.rel_type:
            is_relationship_added = self.uml_model._add_relationship(
                self.source_class, 
                self.dest_class, 
                self.rel_type, 
                is_gui=False, 
                is_undo_or_redo=True
            )
            if is_relationship_added and self.is_gui:
                self.class_box.is_source_class = True
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]

                # Create the arrow line between the GUI components
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.rel_type)

                # Track the relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)

                # Add the arrow to the scene to display it
                self.view.scene().addItem(self.arrow_line)
                self.class_box.update_box()
            return is_relationship_added


class ChangeTypeCommand(Command):
    def __init__(self, uml_model, 
                 class_name: str=None, method_num:int = None, 
                 input_name: str=None, source_class: str=None,
                 dest_class: str=None, new_type: str=None, arrow_line=None,
                 is_field: bool=None, is_method: bool=None, 
                 is_param: bool=None, is_rel: bool=None,
                 view=None, class_box=None, is_gui=False):
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.input_name = input_name
        self.source_class = source_class
        self.dest_class = dest_class
        self.new_type = new_type
        self.arrow_line = arrow_line
        self.class_box = class_box
        self.view = view
        self.is_field = is_field
        self.is_method = is_method
        self.is_param = is_param
        self.is_rel = is_rel
        self.original_field_type = None  # To store the original type
        self.original_method_type = None
        self.original_param_type = None
        self.original_rel_type = None
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        # Determine if it's a field or method and capture the original type
        if self.is_field:
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                self.original_field_type = chosen_field._get_type()
                is_field_type_changed = self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, 
                                                                         new_type=self.new_type, is_field=True, is_undo_or_redo=is_undo_or_redo)
                if is_field_type_changed and self.is_gui:
                    for index, field_key in enumerate(self.class_box.field_key_list):
                        if field_key[1] == self.input_name:
                            self.position = index
                            self.class_box.field_key_list.remove(field_key)  # Remove from the name list
                            self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))  # Remove the text item from the scene
                    field_text = self.class_box.create_text_item(self.new_type + " " + self.input_name, is_field=True, selectable=False, color=self.class_box.text_color)
                    field_key = (self.new_type, self.input_name)
                    self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                    self.class_box.field_key_list.insert(self.position, field_key)
                    self.class_box.update_box()
                return is_field_type_changed

        elif self.is_method:
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is not None:
                self.original_method_type = chosen_method._get_type()
                is_method_return_type_changed = self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num,
                                                                                new_type=self.new_type, is_method=True, is_undo_or_redo=is_undo_or_redo)
                # Check if the item is still in the scene before removing
                if is_method_return_type_changed and self.is_gui:
                    method_entry = self.class_box.method_list[int(self.method_num) - 1]  # Directly use self.method_num
                    if method_entry["method_text"].scene() == self.view.scene():
                        self.view.scene().removeItem(method_entry["method_text"])  # Remove the method's text item
                    self.class_box.method_list.pop(int(self.method_num) - 1)  # Remove the method from method_list
                    method_key = method_entry["method_key"]
                    current_param_list = method_entry["parameters"]
                    # Create the new method text item with the new return type
                    new_method_text = self.class_box.create_text_item(self.new_type + " " + method_key[1] + "()", is_method=True, selectable=False, color=self.class_box.text_color)
                    new_method_key = (self.new_type, method_key[1])  
                    # Create a new method entry as a dictionary with method_key, method_text, and parameters
                    method_entry = {
                        "method_key": new_method_key,
                        "method_text": new_method_text,
                        "parameters": current_param_list
                    }
                    # Append this dictionary to method_list
                    self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                    if len(self.class_box.method_list) == 1:
                        self.class_box.create_separator(is_first=False, is_second=True)
                    self.class_box.update_box()
                return is_method_return_type_changed
        
        elif self.is_param:
            chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.input_name)
            if chosen_param is None:
                return False
            self.original_param_type = chosen_param._get_type()
            is_param_type_changed = self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, 
                                                                     new_type=self.new_type, is_param=True, is_undo_or_redo=is_undo_or_redo)
            if is_param_type_changed and self.is_gui:
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                for i, param_tuple in enumerate(method_entry["parameters"]):
                    if param_tuple[1] == self.input_name:
                        method_entry["parameters"][i] = (self.new_type, param_tuple[1])
                        break  # Exit the loop after renaming
                self.class_box.update_box()  # Refresh the UML box
            
            return is_param_type_changed
        
        elif self.is_rel:
            self.original_rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
            is_rel_type_changed = self.uml_model._change_data_type(
                source_class=self.source_class, dest_class=self.dest_class, 
                new_type=self.new_type, is_rel=True, is_undo_or_redo=is_undo_or_redo
            )
            if is_rel_type_changed and self.is_gui:
                # Update the relationship tracking list with the new type
                relationships = self.view.relationship_track_list.get(self.source_class)
                for relationship in relationships:
                    if relationship["dest_class"] == self.dest_class:
                        arrow_line = relationship["arrow_list"]
                        if arrow_line.scene() == self.view.scene():
                            self.view.scene().removeItem(arrow_line)
                        relationships.remove(relationship)
                        break
                if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                    self.class_box.is_source_class = False
                
                # Create the new arrow line with updated type
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.new_type)
                # Track the relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)

                # Add the arrow to the scene to display it
                self.view.scene().addItem(self.arrow_line)
                self.class_box.update_box()
            return is_rel_type_changed

    def undo(self):
        # Restore the original type
        if self.is_field and self.original_field_type:
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                is_field_type_changed = self.uml_model._change_data_type(class_name=self.class_name, input_name=self.input_name, 
                                                                         new_type=self.original_field_type, is_field=True, is_undo_or_redo=True)
                if is_field_type_changed and self.is_gui:
                    for index, field_key in enumerate(self.class_box.field_key_list):
                        if field_key[1] == self.input_name:
                            self.position = index
                            self.class_box.field_key_list.remove(field_key)  # Remove from the name list
                            if self.class_box.field_list.pop(field_key).scene() == self.view.scene():
                                self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))  # Remove the text item from the scene
                    field_text = self.class_box.create_text_item(self.original_field_type + " " + self.input_name, is_field=True, selectable=False, color=self.class_box.text_color)
                    field_key = (self.original_field_type, self.input_name)
                    self.class_box.field_list[field_key] = field_text  # Add the field to the internal list
                    self.class_box.field_key_list.insert(self.position, field_key)
                    self.class_box.update_box()
                return is_field_type_changed
        
        elif self.is_method and self.original_method_type:
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is not None:
                is_method_return_type_changed = self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, 
                                                                                 new_type=self.original_method_type, is_method=True, is_undo_or_redo=True)
                # Check if the item is still in the scene before removing
                if is_method_return_type_changed and self.is_gui:
                    method_entry = self.class_box.method_list[int(self.method_num) - 1]  # Directly use self.method_num
                    if method_entry["method_text"].scene() == self.view.scene():
                        self.view.scene().removeItem(method_entry["method_text"])  # Remove the method's text item
                    self.class_box.method_list.pop(int(self.method_num) - 1)  # Remove the method from method_list
                    method_key = method_entry["method_key"]
                    current_param_list = method_entry["parameters"]
                    # Create the new method text item with the new return type
                    new_method_text = self.class_box.create_text_item(self.original_method_type + " " + method_key[1] + "()", is_method=True, selectable=False, color=self.class_box.text_color)
                    new_method_key = (self.original_method_type, method_key[1])  
                    # Create a new method entry as a dictionary with method_key, method_text, and parameters
                    method_entry = {
                        "method_key": new_method_key,
                        "method_text": new_method_text,
                        "parameters": current_param_list
                    }
                    # Append this dictionary to method_list
                    self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                    if len(self.class_box.method_list) == 1:
                        self.class_box.create_separator(is_first=False, is_second=True)
                    self.class_box.update_box()
                    
                return is_method_return_type_changed
        
        elif self.is_param and self.original_param_type:
            is_param_type_changed = self.uml_model._change_data_type(class_name=self.class_name, method_num=self.method_num, input_name=self.input_name, 
                                                                     new_type=self.original_param_type, is_param=True, is_undo_or_redo=True)
            if is_param_type_changed and self.is_gui:
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                for i, param_tuple in enumerate(method_entry["parameters"]):
                    if param_tuple[1] == self.input_name:
                        method_entry["parameters"][i] = (self.original_param_type, param_tuple[1])
                        break  # Exit the loop after renaming
                self.class_box.update_box()  # Refresh the UML box
            
            return is_param_type_changed
        
        elif self.is_rel and self.original_rel_type:
            is_rel_type_changed = self.uml_model._change_data_type(
                source_class=self.source_class, dest_class=self.dest_class, 
                new_type=self.original_rel_type, is_rel=True, is_undo_or_redo=True
            )
            if is_rel_type_changed and self.is_gui:
                # Update the relationship tracking list with the new type
                relationships = self.view.relationship_track_list.get(self.source_class)
                for relationship in relationships:
                    if relationship["dest_class"] == self.dest_class:
                        arrow_line = relationship["arrow_list"]
                        if arrow_line.scene() == self.view.scene():
                            self.view.scene().removeItem(arrow_line)
                        relationships.remove(relationship)
                        break
                
                if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                    self.class_box.is_source_class = False
                
                # Create the new arrow line with updated type
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.original_rel_type)
                # Track the relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)

                # Add the arrow to the scene to display it
                self.view.scene().addItem(self.arrow_line)
                self.class_box.update_box()
                return is_rel_type_changed
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