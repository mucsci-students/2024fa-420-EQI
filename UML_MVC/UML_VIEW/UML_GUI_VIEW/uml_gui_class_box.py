import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial
from typing import Dict, List

###################################################################################################
# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(root_path)

from UML_ENUM_CLASS.uml_enum import BoxDefaultStat as Default
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_editable_text_item import UMLEditableTextItem as Text

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    UMLTestBox represents a resizable, movable UML class box in a UML diagram.
    It contains attributes like class name, fields, methods, parameters, 
    and provides handles for resizing the box.
    """
    def __init__(self, interface, class_name="ClassName", field_list=None, method_list=None, parameter_list=None, relationship_list=None, parent=None):
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
        self.field_list: Dict = field_list if field_list is not None else {}
        self.field_name_list: List = []
        
        self.method_list: Dict = method_list if method_list is not None else {}
        self.method_name_list: Dict = {}
        
        self.parameter_list: Dict = parameter_list if parameter_list is not None else {}
        self.parameter_name_list: List = []
        
        self.relationship_list: Dict = relationship_list if relationship_list is not None else []
        self.source_class_list: List = []
        self.dest_class_list: List = []
        
        self.handles_list: List = []
        self.connection_points_list: List = []

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
        self.is_resizing = False
        self.is_selected = False
        self.current_handle = None
        
        #################################
        
        # Define bounding rectangle of the class box
        self.setRect(self.default_box_x, self.default_box_y, self.default_box_width + self.default_margin * 3, self.default_box_height + self.default_margin)
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
        self.class_name_text = self.create_text_item(class_name, selectable=True)
        # Connect the text change callback to ensure it re-centers when the text changes.
        self.class_name_text.document().contentsChanged.connect(self.centering_class_name)
        # Default text color
        self.text_color = self.class_name_text.defaultTextColor()
        self.text_font = self.class_name_text.font()
        self.font_size = self.text_font.pointSize()
        # Create separator below class name
        self.create_separator()
        # Draw first separator
        self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))
        # Centering class name initially.
        self.centering_class_name()
        # Create handles for resizing the class box.
        self.create_resize_handles()
        # Create connection point for arrow line.
        self.create_connection_points()

    #################################################################
    ### MEMBER FUNCTIONS ###
    
    #################################
    ## UPDATE BOX AND IS COMPONENTS ##
    
    def update_box(self):
        """
        Update the dimensions and layout of the UML box.

        This method recalculates and updates all aspects of the UML box, including:
        - Repositioning the class name.
        - Adjusting the box height and width.
        - Updating the positions of resize handles.
        - Adjusting connection points for relationships.
        - Aligning fields, methods, and parameters.
        - Aligning relationships.
        - Updating the separators between different sections (class name, fields, methods).

        This ensures that all elements in the UML box are correctly positioned and scaled 
        based on the current content of the box.
        """
        # Reposition the class name in the center of the UML box
        self.centering_class_name()

        # Adjust the box's height and width based on its contents
        self.update_box_dimension()

        # Update the position of the resize handles at the corners of the UML box
        self.update_handle_positions()

        # Update the connection points (e.g., for relationships) around the box
        self.update_connection_point_positions()

        # Align the fields within the UML box
        self.update_field_alignment()

        # Align the methods and parameters within the UML box
        self.update_method_and_param_alignment()
        
        # Align the relationship within the UML box
        self.update_relationship_alignment()

        # Update the separators between the class name, fields, and methods
        self.update_separators()

    def update_box_dimension(self):
        """
        Recalculate and update the dimensions of the UML box.

        This function calculates the total height of the UML box based on the height of the class name,
        fields, methods, and parameters. The width is set to the larger of the default width or the maximum width 
        required by the text contents (fields, methods, or parameters). If the box is not being manually resized 
        or dragged, it adjusts the box dimensions to fit the content.

        Steps:
        1. Get the height of the class name, fields, methods, and parameters.
        2. Calculate the total height and maximum width required.
        3. Update the box size if it is not currently being resized or dragged.
        """
        # Get the height of the class name text
        class_name_height = self.class_name_text.boundingRect().height()

        # Get the total height of the fields section
        fields_text_height = self.get_field_text_height()

        # Get the total height of the methods section
        method_text_height = self.get_method_text_height()

        # Get the total height of the parameters section
        parameter_text_height = self.get_total_param_text_height()
        
        # Get the total height of the relationship section
        relationship_text_height = self.get_relationship_height()

        # Calculate the total height required for the box, including margins
        total_height = (class_name_height + fields_text_height + method_text_height 
                        + parameter_text_height + relationship_text_height + self.default_margin * 3)

        # Calculate the maximum width required by the content
        max_width = max(self.default_box_width, self.get_maximum_width()) + self.default_margin * 3

        # If the box is not being resized manually or dragged, adjust the size of the box
        # Ensure the total height is greater than the current height before resizing
        if not self.is_resizing and not self.is_box_dragged and total_height >= self.rect().height():
            # Update the rectangle (box) size with the new width and height
            self.setRect(0, 0, max_width, total_height)
        
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
            
        if hasattr(self, 'separator_line2') and self.separator_line2.scene() == self.scene():
            if len(self.method_name_list) > 0:
                class_name_height = self.class_name_text.boundingRect().height()
                field_section_height = self.get_field_text_height()
                y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin
                self.separator_line2.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
                )
            else:
                self.scene().removeItem(self.separator_line2)
                
        if hasattr(self, 'separator_line3') and self.separator_line3.scene() == self.scene():
            if len(self.relationship_list) > 0:
                class_name_height = self.class_name_text.boundingRect().height()
                field_section_height = self.get_field_text_height()
                method_section_height = self.get_method_text_height() + self.get_total_param_text_height()
                y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + method_section_height + self.default_margin
                self.separator_line3.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
                )
            else:
                self.scene().removeItem(self.separator_line3)
                
    def update_handle_positions(self):
        """
        Update the positions of the resize handles based on the current size of the UML box.
        This ensures the handles remain at the corners of the box.
        """
        rect = self.rect()
        self.handles_list['top_left'].setPos(rect.topLeft())
        self.handles_list['top_right'].setPos(rect.topRight())
        self.handles_list['bottom_left'].setPos(rect.bottomLeft())
        self.handles_list['bottom_right'].setPos(rect.bottomRight())

    def update_connection_point_positions(self):
        """
        Update the positions of the connection points based on the size of the UML box.
        Connection points are positioned at the center of the edges (top, bottom, left, right).
        """
        rect = self.rect()
        self.connection_points_list['top'].setPos(rect.center().x(), rect.top())
        self.connection_points_list['bottom'].setPos(rect.center().x(), rect.bottom())
        self.connection_points_list['left'].setPos(rect.left(), rect.center().y())
        self.connection_points_list['right'].setPos(rect.right(), rect.center().y())
        
    def update_field_alignment(self):
        """
        Align field text items in the UML class box row by row.

        Each field will be displayed on a new line, aligned to the left of the box.
        """
        # Starting y-position for the first field (below the class name)
        y_offset = self.class_name_text.boundingRect().height() + self.default_margin

        for field_name in self.field_name_list:
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
        for method_name in self.method_name_list:
            # Get the method text item
            method_text = self.method_list[method_name]

            # Calculate the x-position for the method text (aligned to the left)
            method_x_pos = self.rect().topLeft().x() + self.default_margin

            # Set the position of the method text item
            method_text.setPos(method_x_pos, self.rect().topLeft().y() + y_offset)

            # Update y_offset for the next method or parameter (incremented by the height of this method)
            y_offset += method_text.boundingRect().height()

            # Align parameters under the current method
            if method_name in self.method_name_list:
                for param_name in self.method_name_list[method_name]:
                    # Get the parameter text item
                    param_text = self.parameter_list[param_name]

                    # Calculate the x-position for the parameter text (indented)
                    param_x_pos = self.rect().topLeft().x() + self.default_margin * 2

                    # Set the position of the parameter text item
                    param_text.setPos(param_x_pos, self.rect().topLeft().y() + y_offset)

                    # Update y_offset after positioning the parameter (incremented by the height of the parameter)
                    y_offset += param_text.boundingRect().height()
    
    def update_relationship_alignment(self):
        """
        Aligns the relationship text items (source, dest, type) in the UML class box, 
        explicitly using labels for "Source: ", "Dest: ", and "Type: ".
        """
        # Starting y-position for the first relationship (below the class name, fields, and methods)
        y_offset = (self.class_name_text.boundingRect().height() 
                    + self.get_field_text_height() 
                    + self.get_method_text_height() 
                    + self.get_total_param_text_height() 
                    + self.default_margin)

        # Iterate over the relationships in the list and reposition them
        for relationship in self.relationship_list:
            source_text = relationship["source"]
            dest_text = relationship["dest"]
            type_text = relationship["type"]

            # Calculate the x-position for the relationship text (aligned to the left of the box)
            rel_x_pos = self.rect().topLeft().x() + self.default_margin

            # Check if the labels already exist before creating them
            if "source_label" not in relationship:
                source_label = self.create_text_item("Source: ", selectable=False)
                relationship["source_label"] = source_label
                self.scene().addItem(source_label)
            else:
                source_label = relationship["source_label"]

            if "dest_label" not in relationship:
                dest_label = self.create_text_item("Dest: ", selectable=False)
                relationship["dest_label"] = dest_label
                self.scene().addItem(dest_label)
            else:
                dest_label = relationship["dest_label"]

            if "type_label" not in relationship:
                type_label = self.create_text_item("Type: ", selectable=False)
                relationship["type_label"] = type_label
                self.scene().addItem(type_label)
            else:
                type_label = relationship["type_label"]

            # Set the position of Source label and text
            source_label.setPos(rel_x_pos, self.rect().topLeft().y() + y_offset)
            source_text.setPos(rel_x_pos + source_label.boundingRect().width(), self.rect().topLeft().y() + y_offset)

            # Increment y_offset to display Dest below the Source
            y_offset += source_text.boundingRect().height()

            # Set the position of Dest label and text
            dest_label.setPos(rel_x_pos, self.rect().topLeft().y() + y_offset)
            dest_text.setPos(rel_x_pos + dest_label.boundingRect().width(), self.rect().topLeft().y() + y_offset)

            # Increment y_offset to display Type below the Dest
            y_offset += dest_text.boundingRect().height()

            # Set the position of Type label and text
            type_label.setPos(rel_x_pos, self.rect().topLeft().y() + y_offset)
            type_text.setPos(rel_x_pos + type_label.boundingRect().width(), self.rect().topLeft().y() + y_offset)

            # Increment y_offset for the next relationship
            y_offset += type_text.boundingRect().height() + self.default_margin

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
        # If it's not the second separator, create a separator (placed below the method section)
        else:
            # Calculate the height of the class name to start the separator calculation.
            class_name_height = self.class_name_text.boundingRect().height()

            # Calculate the total height of all the field text items to place the separator correctly.
            field_section_height = self.get_field_text_height()
            
            # Calculate the total height of the method text items to place the separator correctly.
            method_section_height = self.get_method_text_height() + self.get_total_param_text_height()
            
            # Set the y-position for the second separator line just below the fields, with some margin.
            y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + method_section_height + self.default_margin
            
            # Create the second separator as a horizontal line (QGraphicsLineItem) spanning the entire width of the UML box.
            self.separator_line3 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the fields section)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent for this line item.
            )
            
    def create_resize_handles(self):
        """
        Create four resize handles at the corners of the UML box.
        These handles will be used to resize the UML box by dragging.
        Each QGraphicsEllipseItem(self) creates an ellipse 
        (a small circular handle) and links it to the current object (self), which is the UML box.
        """
        self.handles_list = {
            'top_left': QtWidgets.QGraphicsEllipseItem(self),
            'top_right': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_left': QtWidgets.QGraphicsEllipseItem(self),
            'bottom_right': QtWidgets.QGraphicsEllipseItem(self),
        }

        for handle_name, handle in self.handles_list.items():
            # Set handle size and position based on the size of the box
            handle.setRect(-self.handle_size / 2, -self.handle_size / 2, self.handle_size, self.handle_size)

            # Set the appearance of the handle
            handle.setPen(QtGui.QPen(QtGui.QColor(30,144,255)))  # Dodger Blue border
            handle.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White fill

            # Set the handle to be non-movable and send geometry changes to the parent
            handle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

            # Allow hover events to change the cursor during interaction
            handle.setAcceptHoverEvents(True)

            # Set hover events to trigger custom cursor change for each handle
            handle.hoverEnterEvent = partial(self.handle_hoverEnterEvent, handle_name=handle_name)
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

        # Initial handle positions based on the current size of the box
        self.update_handle_positions()

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
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))  # Black color fill
            cp_item.setPen(QtGui.QPen(QtCore.Qt.black))  # Black border

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

        # Calculate the x-position to center the class name horizontally
        class_name_x_pos = self.rect().topLeft().x() + (box_width - class_name_width) / 2

        # Set the class name's position at the top, ensuring it stays horizontally centered
        # The y-position remains fixed at a margin from the top
        self.class_name_text.setPos(class_name_x_pos, self.rect().topLeft().y() + self.default_margin / 2)
                  
    #################################
    ## MOUSE EVENT RELATED ##

    def handle_hoverEnterEvent(self, event, handle_name):
        """
        Change cursor to resize when hovering over the resize handle.
    
        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        - handle_name (str): The name of the handle that is hovered over (top_left, top_right, bottom_left, bottom_right).
        """ 
        # Change the cursor based on which handle is being hovered
        if handle_name == 'top_left' or handle_name == 'bottom_right':
            self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Backward diagonal resize cursor
        elif handle_name == 'top_right' or handle_name == 'bottom_left':
            self.setCursor(QtCore.Qt.SizeBDiagCursor)  # Forward diagonal resize cursor
        event.accept()
        
    def handle_hoverLeaveEvent(self, event):
        """
        Reset cursor when leaving the resize handle.

        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(QtCore.Qt.ArrowCursor)  # Reset cursor to default arrow
        event.accept()
            
    def mousePressEvent(self, event):
        """
        Handle mouse press events for dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if event.button() == QtCore.Qt.LeftButton:
            if self.isUnderMouse() and not any(
                handle.isUnderMouse() for handle in self.handles_list.values()
            ):
                self.is_box_dragged = True  # Start dragging the box
            elif any(handle.isUnderMouse() for handle in self.handles_list.values()):
                # Determine which handle is being pressed for resizing
                for handle_name, handle in self.handles_list.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name
                        self.is_resizing = True
                        self.update_box()
                        event.accept()
                        return
                # Normal drag logic for the box if no handle is under the mouse
                self.is_box_dragged = True
                event.accept()
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        Handle the mouse movement event for resizing the UML box.

        This function updates the size of the UML box based on the handle being dragged during resizing.
        It ensures that the box maintains a minimum width and height based on the content (class name, fields, methods, etc.)
        to prevent them from being cut off. The handle being dragged determines which part of the box 
        (top-left, top-right, bottom-left, or bottom-right) is adjusted. The new dimensions are calculated 
        based on the mouse position, and the box is updated accordingly.

        Parameters:
            event (QGraphicsSceneMouseEvent): The event that provides the mouse movement data.
        """
        # Check if the box is being resized and if a specific handle is active
        if self.is_resizing and self.current_handle:
            new_rect = self.rect()  # Get the current rectangle (box) dimensions
            
            # Convert the global mouse position to the local coordinate system of the box.
            pos = self.mapFromScene(event.scenePos())

            # Calculate the total height of all elements (class name, fields, methods, parameters)
            class_name_height = self.class_name_text.boundingRect().height()
            fields_text_height = self.get_field_text_height()
            method_text_height = self.get_method_text_height()
            param_text_height = self.get_total_param_text_height()
            relationship_text_height = self.get_relationship_height()
            total_height = class_name_height + fields_text_height + method_text_height + param_text_height + relationship_text_height + self.default_margin * 3
            
            # Set the maximum width and minimum height for resizing
            max_width = max(self.default_box_width, self.get_maximum_width()) + self.default_margin * 3
            min_string_height = total_height

            # Adjust size based on the specific handle being dragged
            if self.current_handle == 'top_left':
                # Resize from the top-left corner
                new_width = self.rect().right() - pos.x()  # Calculate the new width
                new_height = self.rect().bottom() - pos.y()  # Calculate the new height

                # If width and height are valid, resize the box and adjust the position of the left and top sides
                if new_width > max_width:
                    new_rect.setWidth(new_width)
                    new_rect.moveLeft(pos.x())  # Move the left side
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)
                    new_rect.moveTop(pos.y())  # Move the top side

            elif self.current_handle == 'top_right':
                # Resize from the top-right corner
                new_width = pos.x() - self.rect().left()
                new_height = self.rect().bottom() - pos.y()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)
                    new_rect.moveTop(pos.y())  # Move the top side

            elif self.current_handle == 'bottom_left':
                # Resize from the bottom-left corner
                new_width = self.rect().right() - pos.x()
                new_height = pos.y() - self.rect().top()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                    new_rect.moveLeft(pos.x())  # Move the left side
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)

            elif self.current_handle == 'bottom_right':
                # Resize from the bottom-right corner
                new_width = pos.x() - self.rect().left()
                new_height = pos.y() - self.rect().top()

                if new_width > max_width:
                    new_rect.setWidth(new_width)
                if new_height > min_string_height:
                    new_rect.setHeight(new_height)

            # Apply the new rectangle dimensions to the UML box
            self.setRect(new_rect)
            
            # Update the internal layout and content of the box (e.g., text, handles, connection points)
            self.update_box()
            event.accept()
        else:
            super().mouseMoveEvent(event)  # Call the parent method if not resizing

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing the UML box.
        
        This method stops the resizing or dragging action once the mouse is released, 
        and it may snap the box to the nearest grid position if the box is being dragged.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        # If the box was being dragged, snap it to the nearest grid and stop dragging
        if self.is_box_dragged:
            self.is_box_dragged = False  # Reset dragging flag
            self.snap_to_grid()  # Snap the box to the nearest grid position
            event.accept()
        # If the box was being resized, stop the resizing process
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset the handle being resized
            event.accept()
        super().mouseReleaseEvent(event)  # Call the parent method

    #################################################################
    ### UTILITY FUNCTIONS ###
    
    def snap_to_grid(self, current_grid_size=15):
        """
        Snap the UML box to the nearest grid position.

        This method calculates the nearest grid coordinates based on the current position of the box
        and adjusts the position to align it with the grid. The grid size can be adjusted using the parameter.

        Parameters:
        - current_grid_size (int): The size of the grid to snap to (default is 20).
        """
        grid_size = current_grid_size * self.transform().m11()  # Adjust for zoom factor
        pos = self.pos()  # Get the current position of the box

        # Calculate new x and y positions by snapping to the nearest grid points
        new_x = round(pos.x() / grid_size) * grid_size
        new_y = round(pos.y() / grid_size) * grid_size

        # Update the box's position and internal content
        self.setPos(new_x, new_y)
        self.update_box()

    def get_field_text_height(self):
        """
        Calculate the total height of all field text items in the box.
        
        Returns:
        - field_tex_height (int): The total height of all field text items.
        """
        field_tex_height = 0
        # Sum the heights of all field text items
        for field_name in self.field_name_list:
            field_text = self.field_list[field_name]  # Get the text item for each field
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
        for method_name in self.method_name_list:
            method_text = self.method_list[method_name]  # Get the text item for each method
            method_tex_height += method_text.boundingRect().height()
        return method_tex_height

    def get_param_text_height_of_single_method(self, method_name):
        """
        Calculate the total height of all parameter text items for a specific method.
        
        Parameters:
        - method_name (str): The name of the method to get the parameter heights for.
        
        Returns:
        - param_tex_height (int): The total height of all parameter text items for the method.
        """
        param_tex_height = 0
        # Sum the heights of all parameter text items for the specified method
        for param_name in self.method_name_list[method_name]:
            param_text = self.parameter_list[param_name]  # Get the text item for each parameter
            param_tex_height += param_text.boundingRect().height()
        return param_tex_height

    def get_total_param_text_height(self):
        """
        Calculate the total height of all parameter text items for all methods in the box.
        
        Returns:
        - total_param_tex_height (int): The total height of all parameter text items.
        """
        total_param_tex_height = 0
        # Loop through all methods and sum the heights of their parameter text items
        for method_name in self.method_name_list:
            total_param_tex_height += self.get_param_text_height_of_single_method(method_name)
        return total_param_tex_height
    
    def get_relationship_height(self):
        relationship_text_height = 0
        for relationship in self.relationship_list:
            relationship_text_height += (relationship["source"].boundingRect().height() 
                                         + relationship["dest"].boundingRect().height() 
                                         + relationship["type"].boundingRect().height())
        return relationship_text_height
    
    def get_relationship_max_text_width(self):
        """
        Calculates the maximum width among the boundingRect().width() of the 'source', 'dest', and 'type' QGraphicsTextItems in the relationship list.

        Args:
            relationship_list (list): A list of dictionaries, each containing 'source', 'dest', and 'type' keys with QGraphicsTextItem values.

        Returns:
            float: The maximum width among the boundingRect().width() of the text items.
        """
        max_width = 0.0

        # Iterate over the dictionaries in the relationship_list
        for rel_dict in self.relationship_list:
            source_text = rel_dict.get('source')
            dest_text= rel_dict.get('dest')
            type_text = rel_dict.get('type')

            # Calculate the widths of the text items
            source_width = source_text.boundingRect().width() if source_text is not None else 0
            dest_width = dest_text.boundingRect().width() if dest_text is not None else 0
            type_width = type_text.boundingRect().width() if type_text is not None else 0

            # Find the maximum width among the three
            max_width_in_dict = max(source_width, dest_width, type_width)

            # Update the overall maximum width if necessary
            if max_width_in_dict > max_width:
                max_width = max_width_in_dict

        return max_width

    def get_maximum_width(self):
        """
        Calculate the maximum width of the UML box based on the widths of its fields, methods, and parameters.

        This function ensures that the box has enough width to display all content without truncation.

        Returns:
        - max_width (int): The maximum width required for the box based on its contents.
        """
        # Get the maximum width of all field text items
        max_field_width = max([self.field_list[field_name].boundingRect().width() for field_name in self.field_name_list], default=0)
        
        # Get the maximum width of all method text items
        max_method_width = max([self.method_list[method_name].boundingRect().width() for method_name in self.method_name_list], default=0)
        
        # Get the maximum width of all parameter text items
        max_param_width = 0
        for method_name in self.method_name_list:
            # Check for parameters under the current method and calculate their widths
            if method_name in self.method_name_list:
                param_widths = [self.parameter_list[param_name].boundingRect().width() for param_name in self.method_name_list[method_name]]
                max_param_width = max(max_param_width, max(param_widths, default=0))
        
        # Get maximum width of relationship text items
        max_rel_width = self.get_relationship_max_text_width()
        
        # Return the largest width between fields, methods, and parameters
        return max(max_field_width, max_method_width, max_param_width, max_rel_width)

###################################################################################################