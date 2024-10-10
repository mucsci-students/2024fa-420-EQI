###################################################################################################

import math  # For mathematical calculations (used in Arrow class)
from PyQt5 import QtWidgets, QtGui, QtCore

###################################################################################################

class Arrow(QtWidgets.QGraphicsLineItem):
    """
    Represents an arrow (relationship) between two UMLClassBox instances.
    Inherits from QGraphicsLineItem to draw lines in the scene.
    """

    def __init__(self, startItem, endItem, startKey, endKey, is_dark_mode=None):
        """
        Initializes a new Arrow instance.

        Parameters:
        - startItem (UMLClassBox): The starting class box.
        - endItem (UMLClassBox): The ending class box.
        - startKey (str): The connection point key on the starting box.
        - endKey (str): The connection point key on the ending box.
        """
        super().__init__()
        self.startItem = startItem  # Starting class box
        self.endItem = endItem  # Ending class box
        self.startKey = startKey  # Connection point key on starting box
        self.endKey = endKey  # Connection point key on ending box
        self.setZValue(2)  # Ensure the arrow is on top of other items
        
        # Check if it's in dark mode or not
        self.is_dark_mode = is_dark_mode

        # Set pen for drawing the line
        if self.is_dark_mode:
            pen = QtGui.QPen(QtCore.Qt.white)
        else:
            pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        self.setPen(pen)

        self.arrowSize = 10  # Size of the arrowhead

        # Allow the arrow to be selectable and focusable
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsSelectable |
            QtWidgets.QGraphicsItem.ItemIsFocusable
        )

        # Add this arrow to the connected class boxes
        self.startItem.addArrow(self)
        self.endItem.addArrow(self)

        self.updatePosition()  # Initial position update

    def updatePosition(self):
        """
        Update the position of the arrow based on connected class boxes.
        """
        # Get updated positions of the connection points
        startPoints = self.startItem.getConnectionPoints()
        endPoints = self.endItem.getConnectionPoints()
        startPoint = startPoints[self.startKey]
        endPoint = endPoints[self.endKey]

        # Create a line between the two points
        line = QtCore.QLineF(startPoint, endPoint)
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        """
        Custom paint method to draw the arrow with an arrowhead.

        Parameters:
        - painter (QPainter): The painter object.
        - option (QStyleOptionGraphicsItem): The style options.
        - widget (QWidget): The widget being painted on.
        """
        painter.setPen(self.pen())
        line = self.line()
        
        painter.drawLine(line)

        # Calculate angle of the line for arrowhead orientation
        angle = math.atan2(-line.dy(), line.dx())

        # Calculate points for the arrowhead polygon
        arrowP1 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi / 3) * self.arrowSize
        )
        arrowP2 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi - math.pi / 3) * self.arrowSize
        )

        # Create the arrowhead polygon
        arrowHead = QtGui.QPolygonF([line.p2(), arrowP1, arrowP2])

        painter.drawPolygon(arrowHead)  # Draw the arrowhead

    def mousePressEvent(self, event):
        """
        Handle mouse press event to allow selection of the arrow.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        self.setSelected(True)  # Select the arrow
        super().mousePressEvent(event)