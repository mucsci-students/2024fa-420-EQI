from PyQt5 import QtWidgets, QtGui
from typing import Dict, List

###################################################################################################

from UML_ENUM_CLASS.uml_enum import BoxDefaultStat as Default
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_editable_text_item import UMLEditableTextItem as Text

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    UMLTestBox represents a resizable, movable UML class box in a UML diagram.
    It contains attributes like class name, fields, methods, parameters, 
    and provides handles for resizing the box.
    """
    def __init__(self, interface, class_name="ClassName", x=None, y=None, parent=None):
        """
        Initialize the UMLTestBox with default settings, including the class name, fields, methods, and handles.
        
        Args:
            interface: The interface for communication with UML components.
            class_name (str): The initial name of the class. Defaults to "ClassName".
            field_list (list): A list of fields for the class. Defaults to an empty list if not provided.
            method_list (list): A list of methods for the class. Defaults to an empty list if not provided.
            parameter_list (list): A list of parameters for the methods. Defaults to an empty list if not provided.
            parent: The parent item, usually a QGraphicsScene. Defaults to None.
        """
        #################################################################
        # Calling constructor from parent class
        super().__init__(parent)

        # Interface to communicate with UMLInterface
        self.interface = interface

        #################################################################
        ### FIELD, METHOD, PARAMETER, HANDLE AND CONNECT POINT LIST ###
        # Initialize lists for fields, methods, parameters, and resize handles.
        self.field_list: Dict = {}
        self.field_key_list: List = []
        
        self.method_list: List = []
        
        # Parameter track
        self.param_num = 0
        
        self.handles_list: List = []
        self.connection_points_list: Dict = {}
        self.arrow_line_list: List = []
        
        self.box_position = {
            "x" : x, 
            "y" : y
        } 

        #################################################################
        ### UML CLASS BOX DEFAULT SETUP ###
        
        # Default position, dimensions, handle (for resize), and connect points for the class box.
        self.default_box_x = Default.BOX_DEFAULT_X.value
        self.default_box_y = Default.BOX_DEFAULT_Y.value
        self.default_box_width = Default.BOX_DEFAULT_WIDTH.value
        self.default_box_height = Default.BOX_DEFAULT_HEIGHT.value
        self.default_margin = Default.BOX_DEFAULT_MARGIN.value
        # Handle points and connection points size
        self.handle_size = 10
        self.connection_point_size = 6
        # Initialize resizing and connection properties
        self.is_box_dragged = False
        # self.is_resizing = False
        self.is_source_class= False
        self.current_handle = None
        
        #################################
        
        # Define bounding rectangle of the class box
        self.setRect(self.default_box_x, self.default_box_y, 
                     self.default_box_width + self.default_margin, 
                     self.default_box_height)
        # Set border color (Dodger Blue)
        self.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  
        # Set background color (cyan)
        self.setBrush(QtGui.QBrush(QtGui.QColor(0,255,255)))  
        # Set class box selectable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # Set class box movable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True) 
        # Enable the box to send geometry change events.
        # This allows the box to notify the parent item (the class box) when it moves or is resized.
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        # Enable hover events
        self.setAcceptHoverEvents(True)
        # Class name text box and make it appear at the center of the box.
        self.class_name_text = self.create_text_item(class_name, selectable=False)
        # Connect the text change callback to ensure it re-centers when the text changes.
        self.class_name_text.document().contentsChanged.connect(self.centering_class_name)
        # Default text color
        self.text_color = self.class_name_text.defaultTextColor()
        self.text_font = self.class_name_text.font()
        self.font_size = self.text_font.pointSize()
        # Create separator below class name
        self.create_separator()
        # Centering class name initially.
        self.centering_class_name()
        # # Create handles for resizing the class box.
        # self.create_resize_handles()
        # Create connection point for arrow line.
        self.create_connection_points()

    #################################################################
    ### MEMBER FUNCTIONS ###
    
    #################################
    ## UPDATE BOX AND IS COMPONENTS ##
    
    def update_box(self):
        """
        Update the dimensions and layout of the UML box based on the contents 
        (class name, fields, methods, parameters, and relationships).

        This method recalculates and updates all aspects of the UML box to fit the content, including:
        - Repositioning the class name.
        - Adjusting the box height and width.
        - Updating the positions of resize handles.
        - Aligning fields, methods, and parameters.
        - Updating the separators.
        """
        # Align method and its parameters within the UML box
        self.update_method_and_param_alignment()
        
        # Adjust the box's height and width based on its contents
        self.update_box_dimension()

        # Reposition the class name in the center of the UML box
        self.centering_class_name()

        # Align the fields within the UML box
        self.update_field_alignment()

        # # Update the position of the resize handles at the corners of the UML box
        # self.update_handle_positions()

        # Update the connection points for relationships
        self.update_connection_point_positions()

        # Update the separators between the class name, fields, and methods
        self.update_separators()
        
        self.update_arrow_lines()
        
        self.update_box_position()
        
    def update_box_position(self):
        self.box_position["x"] = self.pos().x()
        self.box_position["y"] = self.pos().y()
        print(f"Current location: ({self.box_position["x"]} , {self.box_position["y"]})")
        
    def set_box_position(self):
        # Retrieve the desired x and y positions from the box_position dictionary
        new_x = self.box_position.get("x", 0)  # Default to 0 if 'x' not found
        new_y = self.box_position.get("y", 0)  # Default to 0 if 'y' not found
        
        # Set the new position using setPos()
        self.setPos(new_x, new_y)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            # Update arrow positions when the position of the box changes
            self.update_arrow_lines()
            self.update_box_position()
        return super().itemChange(change, value)
    
    def update_arrow_lines(self):
        for arrow_line in self.arrow_line_list:
            arrow_line.update_position()

    def update_box_dimension(self):
        """
        Recalculate and update the dimensions of the UML box based on its contents.

        The box will be resized to fit the class name, fields, methods, and parameters,
        shrinking or growing as necessary.
        """
        # Get total height and maximum width based on the current content
        total_height = self.get_total_height() + 3
        max_width = self.get_maximum_width()

        # Ensure the box shrinks as well as expands
        # Check if the box's current size is larger than needed and adjust accordingly
        default_width = self.default_box_width + self.default_margin
        
        # Allow the box to shrink when content decreases
        if max_width < default_width:
            # Shrink the box dimensions
            self.setRect(self.rect().x(), self.rect().y(), default_width, total_height)

        # If the content grows, resize the box to fit it
        else:
            # Expand the box dimensions
            self.setRect(self.rect().x(), self.rect().y(), max_width, total_height)
            
    def centering_class_name(self):
        """
        Centers the class name text inside the UML class box horizontally.

        This function calculates the position of the class name text based on the width of the UML class box 
        and the width of the text. It adjusts the position of the text so that it is horizontally centered 
        within the class box. The vertical position is fixed using a default margin.

        Steps:
        1. Retrieve the width of the UML class box using self.rect().
        2. Calculate the width of the class name text using self.class_name_text.boundingRect().width().
        3. Compute the new x-position for the class name by centering it within the box.
        4. Set the new position for the class name text at the calculated x-position, with the y-position 
        remaining fixed at the default margin.

        Parameters:
        None
        """
        # Get the current width of the UML class box
        box_width = self.rect().width()

        # Get the width of the class name text using its bounding rectangle
        class_name_width = self.class_name_text.boundingRect().width()

        # If the class name is longer than the box, resize the box to fit the name
        if class_name_width > box_width:
            # Adjust the width of the UML class box to fit the class name
            new_box_width = class_name_width + self.default_margin  # Add some margin to the width
            self.setRect(self.rect().x(), self.rect().y(), new_box_width, self.rect().height())

        # Recalculate the box width after potential resizing
        box_width = self.rect().width()

        # Calculate the x-position to center the class name horizontally
        class_name_x_pos = self.rect().topLeft().x() + (box_width - class_name_width) / 2
        
        # Calculate y-position to center class name vertically (with the separator below it)
        class_name_y_pos = self.rect().topLeft().y() + self.default_margin / 2

        # Set the class name's position, ensuring it stays horizontally centered
        self.class_name_text.setPos(class_name_x_pos, class_name_y_pos)
        
        self.update_separators()
        
    def update_separators(self):
        """
        Update positions of the separator lines based on current box size.
        This function keeps the separator anchored at a fixed y-position relative to the class name.
        """
        if hasattr(self, 'separator_line1'):
            # Update the separator line based on the current size of the UML box
            class_name_height = self.class_name_text.boundingRect().height()
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin
            # Set the new position of the separator line
            self.separator_line1.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
            )
            self.separator_line1.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  
             
        if hasattr(self, 'separator_line2') and self.separator_line2.scene() == self.scene():
            if len(self.method_list) > 0:
                class_name_height = self.class_name_text.boundingRect().height()
                field_section_height = self.get_field_text_height()
                y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin
                self.separator_line2.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
                )
                self.separator_line2.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  
            else:
                self.scene().removeItem(self.separator_line2)
                
    # def update_handle_positions(self):
    #     """
    #     Update the positions of the resize handles based on the current size of the UML box.
    #     This ensures the handles remain at the corners of the box.
    #     """
    #     rect = self.rect()
    #     self.handles_list['top_left'].setPos(rect.topLeft())
    #     self.handles_list['top_right'].setPos(rect.topRight())
    #     self.handles_list['bottom_left'].setPos(rect.bottomLeft())
    #     self.handles_list['bottom_right'].setPos(rect.bottomRight())

    def update_connection_point_positions(self):
        """
        Update the positions of the connection points based on the size of the UML box.
        Connection points are positioned at the center of the edges (top, bottom, left, right).
        """
        rect = self.rect()
        self.connection_points_list['top'].setPos(rect.center().x(), rect.top() - 1)
        self.connection_points_list['bottom'].setPos(rect.center().x(), rect.bottom() + 5)
        self.connection_points_list['left'].setPos(rect.left() - 1, rect.center().y())
        self.connection_points_list['right'].setPos(rect.right() + 5, rect.center().y() + 2)
        
    def update_field_alignment(self):
        """
        Align field text items in the UML class box row by row.

        Each field will be displayed on a new line, aligned to the left of the box.
        """
        # Starting y-position for the first field (below the class name)
        y_offset = self.class_name_text.boundingRect().height() + self.default_margin

        for field_name in self.field_key_list:
            # Get the text item for the field
            field_text = self.field_list[field_name]
        
            # Calculate the x-position to center the field text horizontally
            field_x_pos = self.rect().topLeft().x() + self.default_margin
        
            # Set the position of the field text, each field below the previous one
            field_text.setPos(field_x_pos, self.rect().topLeft().y() + y_offset)
        
            # Increment y_offset for the next field (adding field height and margin)
            y_offset += field_text.boundingRect().height()
            
    def update_method_and_param_alignment(self):
        """
        Align methods and parameters in the UML class box row by row.

        Each method will be displayed on a new line, with its parameters indented beneath it.
        """
        # Starting y-position for the first method (below the class name and fields)
        y_offset = self.class_name_text.boundingRect().height() + self.get_field_text_height() + self.default_margin

        # Iterate through each method and align them, along with their parameters
        for method_entry in self.method_list:
            method_key = method_entry["method_key"]
            method_text = method_entry["method_text"]
            param_list = method_entry["parameters"]
            
            # Calculate the x-position for the method text (aligned to the left)
            method_x_pos = self.rect().topLeft().x() + self.default_margin
            # Set the position of the method text item
            method_text.setPos(method_x_pos, self.rect().topLeft().y() + y_offset)
            
            if len(param_list) == 0:
                method_text.setPlainText(f"{method_key[0]} {method_key[1]}()")
                
            temp_param_list = []
            # Align parameters under the current method
            for param_type, param_name in param_list:
                temp_param_list.append(f"{param_type} {param_name}")   
                # Combine method name with its parameters, separated by commas
                param_text_str = ", ".join(temp_param_list)
                method_with_params = f"{method_key[0]} {method_key[1]}({param_text_str})"         
                # Update the method text to show the method name with parameters
                method_text.setPlainText(method_with_params)

           # Update y_offset for the next method or parameter (incremented by the height of this method)
            y_offset += method_text.boundingRect().height()
                
    #################################
    
    def create_separator(self, is_first=True, is_second=True):
        """
        Create a separator line between different sections of the UML class box.

        This method is used to visually separate the class name, fields, and methods in the UML class box.
        It creates a horizontal line that spans the width of the UML box and adjusts its position based on 
        the content (class name and fields).

        Args:
            is_first (bool): 
                - If True, creates the first separator line below the class name.
            is_second (bool):
                - If True, creates the second separator line below the fields.

        Steps:
        1. Determine the height of the class name using boundingRect().
        2. For the first separator, place it below the class name with some margin.
        3. For the second separator, place it below the fields section.
        4. Use QGraphicsLineItem to draw the line across the box width.
        """
        
        # Check if it's the first separator (placed below the class name)
        if is_first:
            # Calculate the height of the class name text item to determine where the separator should be positioned.
            class_name_height = self.class_name_text.boundingRect().height()

            # Set the y-position for the separator line just below the class name, leaving a small margin.
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin

            # Create the first separator as a horizontal line (QGraphicsLineItem) spanning the entire width of the UML box.
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the class name)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent for this line item.
            )

        # If it's the second separator, create a separator (placed below the fields section)
        elif is_second:
            # Calculate the height of the class name to start the separator calculation.
            class_name_height = self.class_name_text.boundingRect().height()

            # Calculate the total height of all the field text items to place the separator correctly.
            field_section_height = self.get_field_text_height()

            # Set the y-position for the second separator line just below the fields, with some margin.
            y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin

            # Create the second separator as a horizontal line (QGraphicsLineItem) spanning the entire width of the UML box.
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the fields section)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent for this line item.
            )
            
    # def create_resize_handles(self):
    #     """
    #     Create four resize handles at the corners of the UML box.
    #     These handles will be used to resize the UML box by dragging.
    #     Each QGraphicsEllipseItem(self) creates an ellipse 
    #     (a small circular handle) and links it to the current object (self), which is the UML box.
    #     """
    #     self.handles_list = {
    #         'top_left': QtWidgets.QGraphicsEllipseItem(self),
    #         'top_right': QtWidgets.QGraphicsEllipseItem(self),
    #         'bottom_left': QtWidgets.QGraphicsEllipseItem(self),
    #         'bottom_right': QtWidgets.QGraphicsEllipseItem(self),
    #     }

    #     for handle_name, handle in self.handles_list.items():
    #         # Set handle size and position based on the size of the box
    #         handle.setRect(-self.handle_size / 2, -self.handle_size / 2, self.handle_size, self.handle_size)

    #         # Set the appearance of the handle
    #         handle.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  # Dodger Blue border
    #         handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White fill

    #         # Set the handle to be non-movable and send geometry changes to the parent
    #         handle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
    #         handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

    #         # Allow hover events to change the cursor during interaction
    #         handle.setAcceptHoverEvents(True)

    #         # Set hover events to trigger custom cursor change for each handle
    #         handle.hoverEnterEvent = partial(self.handle_hoverEnterEvent, handle_name=handle_name)
    #         handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

    #     # Initial handle positions based on the current size of the box
    #     self.update_handle_positions()

    def create_connection_points(self):
        """
        Create four connection points (top, bottom, left, right) for linking arrows between UML boxes.
        Each connection point is represented by a small ellipse at the edge of the UML box.
        """
        self.connection_points_list = {
            'top': QtWidgets.QGraphicsEllipseItem(self),
            'bottom': QtWidgets.QGraphicsEllipseItem(self),
            'left': QtWidgets.QGraphicsEllipseItem(self),
            'right': QtWidgets.QGraphicsEllipseItem(self),
        }

        # point_name will be used later for 
        for point_name, cp_item in self.connection_points_list.items():
            # Set the size and position of the connection point
            cp_item.setRect(-5, -5, self.connection_point_size, self.connection_point_size)

            # Set the appearance of the connection point
            cp_item.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  # Dodger Blue border
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White fill

            # Disable movement and selection of connection points
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)

        # Update the positions of the connection points based on the size of the box
        self.update_connection_point_positions()

    #################################
    ## CLASS NAME TEXT RELATED ##
    
    def create_text_item(self, text:str, selectable=False, is_field=None, is_method=None, is_parameter=None, color=None, font=None):
        """
        Create and return a QGraphicsTextItem with editing capabilities.

        Parameters:
        - text (str): The initial text of the item.
        - change_callback (function): Optional function to call when text content changes.
        - editable (bool): Whether the text item is editable.

        Returns:
        - EditableTextItem: The created text item.
        """
        # Both color and font are valid
        if color is not None and font is not None:
            text_item = Text(text=text, parent=self, color=color, font=font)  
            self.text_color = color
            self.text_font = font
        # Only color is valid
        elif color is not None and font is None:
            text_item = Text(text=text, parent=self, color=color) 
            self.text_color = color 
        # Only font is valid
        elif color is None and font is not None:
            text_item = Text(text=text, parent=self, font=font)  
            self.text_font = font
        # Both color and font are invalid
        else:
            text_item = Text(text=text, parent=self)  
        
        if selectable:
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        return text_item
                  
    #################################
    ## MOUSE EVENT RELATED ##

    # def handle_hoverEnterEvent(self, event, handle_name):
    #     """
    #     Change cursor to resize when hovering over the resize handle.
    
    #     Parameters:
    #     - event (QGraphicsSceneHoverEvent): The hover event.
    #     - handle_name (str): The name of the handle that is hovered over (top_left, top_right, bottom_left, bottom_right).
    #     """ 
    #     # Change the cursor based on which handle is being hovered
    #     if handle_name == 'top_left' or handle_name == 'bottom_right':
    #         self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Backward diagonal resize cursor
    #     elif handle_name == 'top_right' or handle_name == 'bottom_left':
    #         self.setCursor(QtCore.Qt.SizeBDiagCursor)  # Forward diagonal resize cursor
    #     event.accept()
        
    # def handle_hoverLeaveEvent(self, event):
    #     """
    #     Reset cursor when leaving the resize handle.

    #     Parameters:
    #     - event (QGraphicsSceneHoverEvent): The hover event.
    #     """
    #     self.setCursor(QtCore.Qt.ArrowCursor)  # Reset cursor to default arrow
    #     event.accept()
            
    # def mousePressEvent(self, event):
    #     """
    #     Handle mouse press events for dragging or resizing.

    #     Parameters:
    #     - event (QGraphicsSceneMouseEvent): The mouse event.
    #     """
    #     if event.button() == QtCore.Qt.LeftButton:
    #         if self.isUnderMouse() and not any(
    #             handle.isUnderMouse() for handle in self.handles_list.values()
    #         ):
    #             self.is_box_dragged = True  # Start dragging the box
    #         elif any(handle.isUnderMouse() for handle in self.handles_list.values()):
    #             # Determine which handle is being pressed for resizing
    #             for handle_name, handle in self.handles_list.items():
    #                 if handle.isUnderMouse():
    #                     self.current_handle = handle_name
    #                     # self.is_resizing = True
    #                     self.update_box()
    #                     event.accept()
    #                     return
    #             # Normal drag logic for the box if no handle is under the mouse
    #             self.is_box_dragged = True
    #             event.accept()
    #     super().mousePressEvent(event)
        
    # def mouseMoveEvent(self, event):
    #     """
    #     Handle the mouse movement event for resizing the UML box.

    #     This function updates the size of the UML box based on the handle being dragged during resizing.
    #     It ensures that the box maintains a minimum width and height based on the content (class name, fields, methods, etc.)
    #     to prevent them from being cut off. The handle being dragged determines which part of the box 
    #     (top-left, top-right, bottom-left, or bottom-right) is adjusted. The new dimensions are calculated 
    #     based on the mouse position, and the box is updated accordingly.

    #     Parameters:
    #         event (QGraphicsSceneMouseEvent): The event that provides the mouse movement data.
    #     """
    #     # Check if the box is being resized and if a specific handle is active
    #     if self.is_resizing and self.current_handle:
    #         new_rect = self.rect()  # Get the current rectangle (box) dimensions
            
    #         # Convert the global mouse position to the local coordinate system of the box.
    #         pos = self.mapFromScene(event.scenePos())

    #         # Calculate the total height of all elements (class name, fields, methods, parameters)
    #         total_height = self.get_total_height()
            
    #         # Set the maximum width and minimum height for resizing
    #         max_width = max(self.default_box_width, self.get_maximum_width())

    #         # Adjust size based on the specific handle being dragged
    #         if self.current_handle == 'top_left':
    #             # Resize from the top-left corner
    #             new_width = self.rect().right() - pos.x()  # Calculate the new width
    #             new_height = self.rect().bottom() - pos.y()  # Calculate the new height

    #             # If width and height are valid, resize the box and adjust the position of the left and top sides
    #             if new_width > max_width:
    #                 new_rect.setWidth(new_width)
    #                 new_rect.moveLeft(pos.x())  # Move the left side
    #             if new_height > total_height:
    #                 new_rect.setHeight(new_height)
    #                 new_rect.moveTop(pos.y())  # Move the top side

    #         elif self.current_handle == 'top_right':
    #             # Resize from the top-right corner
    #             new_width = pos.x() - self.rect().left()
    #             new_height = self.rect().bottom() - pos.y()

    #             if new_width > max_width:
    #                 new_rect.setWidth(new_width)
    #             if new_height > total_height:
    #                 new_rect.setHeight(new_height)
    #                 new_rect.moveTop(pos.y())  # Move the top side

    #         elif self.current_handle == 'bottom_left':
    #             # Resize from the bottom-left corner
    #             new_width = self.rect().right() - pos.x()
    #             new_height = pos.y() - self.rect().top()

    #             if new_width > max_width:
    #                 new_rect.setWidth(new_width)
    #                 new_rect.moveLeft(pos.x())  # Move the left side
    #             if new_height > total_height:
    #                 new_rect.setHeight(new_height)

    #         elif self.current_handle == 'bottom_right':
    #             # Resize from the bottom-right corner
    #             new_width = pos.x() - self.rect().left()
    #             new_height = pos.y() - self.rect().top()

    #             if new_width > max_width:
    #                 new_rect.setWidth(new_width)
    #             if new_height > total_height:
    #                 new_rect.setHeight(new_height)

    #         # Apply the new rectangle dimensions to the UML box
    #         self.setRect(new_rect)
            
    #         # Update the internal layout and content of the box (e.g., text, handles, connection points)
    #         self.update_box()
    #         event.accept()
    #     else:
    #         super().mouseMoveEvent(event)  # Call the parent method if not resizing

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing the UML box.
        
        This method stops the resizing or dragging action once the mouse is released.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_box_dragged:
            self.is_box_dragged = False  # Reset dragging flag
            event.accept()
        # # If the box was being resized, stop the resizing process
        # elif self.is_resizing:
        #     self.is_resizing = False  # Reset resizing flag
        #     self.current_handle = None  # Reset the handle being resized
        #     event.accept()
        super().mouseReleaseEvent(event)  # Call the parent method

    #################################################################
    ### UTILITY FUNCTIONS ###

    def get_field_text_height(self):
        """
        Calculate the total height of all field text items in the box.
        
        Returns:
        - field_tex_height (int): The total height of all field text items.
        """
        field_tex_height = 0
        # Sum the heights of all field text items
        for field_text in self.field_list.values():
            field_tex_height += field_text.boundingRect().height()
        return field_tex_height

    def get_method_text_height(self):
        """
        Calculate the total height of all method text items in the box.
        
        Returns:
        - method_tex_height (int): The total height of all method text items.
        """
        method_tex_height = 0
        # Sum the heights of all method text items
        for each_pair in self.method_list:
            # Get the method text item
            method_text = each_pair["method_text"]
            method_tex_height += method_text.boundingRect().height()
        return method_tex_height

    def get_maximum_width(self):
        """
        Calculate the maximum width of the UML box based on the widths of its fields, methods, and parameters.

        This function ensures that the box has enough width to display all content without truncation.

        Returns:
        - max_width (int): The maximum width required for the box based on its contents.
        """
        # Get the maximum width of class name text item
        max_class_name_width = self.class_name_text.boundingRect().width()
        
        # Get the maximum width of all field text items
        max_field_width = max([self.field_list[field_key].boundingRect().width() for field_key in self.field_key_list], default=0)
        
        # Get the maximum width of all method text items, including parameters
        max_method_width = max(
            [
                entry["method_text"].boundingRect().width() 
                for entry in self.method_list  # Assuming `self.method_key_list` is the list of dictionaries
            ],
            default=0
        )
        
        # Determine the largest width among all components
        content_max_width = max(
            max_class_name_width,
            max_field_width,
            max_method_width
        )
        
        # Return the largest width between fields, methods, and parameters
        return content_max_width + self.default_margin * 2
    
    def get_total_height(self):
        # Default height
        default_height = self.default_margin * 2
        
        # Get the height of the class name text
        class_name_height = self.class_name_text.boundingRect().height()

        # Get the total height of the fields section
        fields_text_height = self.get_field_text_height()

        # Get the total height of the methods section
        method_text_height = self.get_method_text_height()

        # Calculate the total height required for the box, including margins
        total_height = (class_name_height 
                        + fields_text_height 
                        + method_text_height 
                        + default_height)
        
        return total_height

###################################################################################################