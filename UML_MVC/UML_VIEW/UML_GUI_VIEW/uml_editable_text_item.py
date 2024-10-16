from PyQt5 import QtWidgets, QtGui, QtCore

###################################################################################################

class UMLEditableTextItem(QtWidgets.QGraphicsTextItem):
    """
    UMLEditableTextItem is a subclass of QGraphicsTextItem that allows for text editing when double-clicked.
    It enables inline text editing within a UML diagram by detecting mouse double-click events and
    toggling the text-editing mode. The text can be modified and saved when the user hits Enter,
    and the editing mode ends when focus is lost.

    Attributes:
        text (str): The initial text displayed in the item.
        parent: Optional. The parent QGraphicsItem this text item belongs to.
        editing (bool): Tracks whether the text is in editing mode.
    """

    def __init__(self, text="", parent=None, color="black", font="Arial", font_size=None):
        """
        Initialize the UMLEditableTextItem with a default text and an optional parent item.

        Args:
            text (str): The initial text to display in the QGraphicsTextItem. Defaults to an empty string.
            parent: Optional. The parent QGraphicsItem to which this text item belongs.
        """
        super().__init__(text, parent)
        
        # Set the default text color
        self.setDefaultTextColor(QtGui.QColor(color))
        
        # Set the font
        text_font = QtGui.QFont(font)
        
        if font_size is not None:
            text_font.setPointSize(font_size)
            
        self.setFont(text_font)
            
        # Disable text editing initially (read-only mode)
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        # A flag to track if the text item is currently in editing mode
        self.editing = False

    # def mouseDoubleClickEvent(self, event):
    #     """
    #     Handles the mouse double-click event to enable text editing.

    #     This method is triggered when the user double-clicks on the text item.
    #     It sets the item into editing mode, allowing the text to be modified.
    #     Focus is also set on the text item to capture user input immediately.

    #     Args:
    #         event: The QMouseEvent representing the double-click event.
    #     """
    #     # Enable text editing by setting the appropriate interaction flags
    #     self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
    #     # Ensure the text item gains focus so the user can start typing
    #     self.setFocus()
    #     # Set the editing mode to True
    #     self.editing = True
    #     # Call the parent class’s double-click event handler
    #     super().mouseDoubleClickEvent(event)

    # def keyPressEvent(self, event):
    #     """
    #     Handles the key press event to capture Enter or Return key presses.

    #     If the user presses the Enter/Return key while editing, this method saves the changes
    #     and exits the editing mode. For other key events, the default behavior is followed.

    #     Args:
    #         event: The QKeyEvent representing the key press event.
    #     """
    #     if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
    #         # Disable text editing when the Enter key is pressed
    #         self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
    #         # Clear focus from the text item (indicating end of editing)
    #         self.clearFocus()
    #         # Set the editing mode to False
    #         self.editing = False
    #         # Optional: Add callback logic here to save the text value or perform other actions
    #     else:
    #         # Pass other key events to the parent class’s handler
    #         super().keyPressEvent(event)

    # def focusOutEvent(self, event):
    #     """
    #     Handles the focus-out event, stopping editing if the user clicks outside the text item.

    #     When the text item loses focus (e.g., when the user clicks elsewhere), this method ensures
    #     that the text editing is disabled, and the item returns to read-only mode.

    #     Args:
    #         event: The QFocusEvent representing the focus-out event.
    #     """
    #     # If the item was in editing mode and focus is lost, stop editing
    #     if self.editing:
    #         # Disable text editing when focus is lost
    #         self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
    #         # Set the editing mode to False
    #         self.editing = False
    #     # Call the parent class’s focus-out event handler
    #     super().focusOutEvent(event)

###################################################################################################