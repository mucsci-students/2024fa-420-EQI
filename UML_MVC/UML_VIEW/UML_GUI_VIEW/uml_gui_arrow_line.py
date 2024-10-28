import math
from PyQt5 import QtWidgets, QtGui, QtCore

class UMLArrow(QtWidgets.QGraphicsLineItem):
    """
    Represents an arrow connecting two movable boxes with connection points.
    """

    def __init__(self, source_class, dest_class, relationship_type):
        """
        Initializes a new Arrow instance connecting source_class to dest_class.
        """
        super().__init__()
        self.source_class = source_class
        self.dest_class = dest_class
        self.relationship_type = relationship_type
        self.arrow_size = 10  # Size of the arrowhead
        self.arrow_type = relationship_type

        # Set pen for drawing the line
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        if self.relationship_type == "Realization":
            pen.setStyle(QtCore.Qt.DashLine)
        self.setPen(pen)

        # Add this arrow to the connected boxes
        self.source_class.arrow_line_list.append(self)
        self.dest_class.arrow_line_list.append(self)
        
        # Ensure arrow is drawn on top
        self.setZValue(1)

        self.update_position()  # Initial position update

    def update_position(self):
        """
        Update the arrow's position based on the closest connection points between the two boxes.
        Adjusts the line so it starts or ends at the base of the arrowhead.
        """
        startPoint, endPoint = self.calculate_closest_points()
        line = QtCore.QLineF(startPoint, endPoint)

        # Calculate the angle of the line
        angle = math.atan2(-line.dy(), line.dx())
        # Adjust the line based on the relationship type
        if self.relationship_type in ["Inheritance", "Realization"]:
            # Shorten the line at the end by arrow_size
            offset = QtCore.QPointF(
                math.cos(angle) * self.arrow_size,
                -math.sin(angle) * self.arrow_size
            )
            line.setP2(line.p2() - offset)
        elif self.relationship_type in ["Aggregation", "Composition"]:
            # Shorten the line at the start by arrow_size
            offset = QtCore.QPointF(
                math.cos(angle) * self.arrow_size,
                -math.sin(angle) * self.arrow_size
            )
            line.setP1(line.p1() + offset)

        self.setLine(line)
        # Inform the scene that the item's geometry has changed
        self.prepareGeometryChange()

    def calculate_closest_points(self):
        """
        Calculate the closest connection points between the two boxes.

        Returns:
        - (QPointF, QPointF): Closest points on start and end boxes.
        """
        startPoints = self.source_class.connection_points_list
        endPoints = self.dest_class.connection_points_list

        minDistance = float('inf')
        closestStart = closestEnd = None

        # Loop over each connection point in the source and destination classes
        for sp_name, sp in startPoints.items():
            start_scene_pos = sp.mapToScene(sp.rect().center())
            for ep_name, ep in endPoints.items():
                end_scene_pos = ep.mapToScene(ep.rect().center())
                distance = QtCore.QLineF(start_scene_pos, end_scene_pos).length()
                if distance < minDistance:
                    minDistance = distance
                    closestStart, closestEnd = start_scene_pos, end_scene_pos

        return closestStart, closestEnd

    def paint(self, painter, option, widget=None):
        """
        Custom paint method to draw the arrow with the correct arrowhead based on relationship type.

        Parameters:
        - painter (QPainter): The painter object.
        """
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        line = self.line()

        # Draw the line
        painter.setPen(self.pen())
        painter.drawLine(line)

        # Calculate angle of the line for arrowhead orientation
        angle = math.atan2(-line.dy(), line.dx())

        # Define the arrowhead size
        arrow_size = self.arrow_size

        # Adjust based on the relationship type
        if self.relationship_type in ["Aggregation", "Composition"]:
            # Draw the diamond at the start (source)
            self.draw_diamond_head(painter, line, angle, filled=(self.relationship_type == "Composition"))
        elif self.relationship_type in ["Inheritance", "Realization"]:
            # Draw the triangle at the end (destination)
            dashed = (self.relationship_type == "Realization")
            self.draw_triangle_head(painter, line, angle, dashed=dashed)

    def draw_diamond_head(self, painter, line, angle, filled):
        """
        Draws a diamond-shaped arrowhead at the start of the line.

        Parameters:
        - painter (QPainter): The painter object.
        - line (QLineF): The line where the diamond is to be drawn.
        - angle (float): The angle of the line.
        - filled (bool): Whether the diamond is filled (Composition) or not (Aggregation).
        """
        # Base point (line start)
        base = line.p1()

        # Calculate points for the diamond
        # Tip point (forward along the line)
        tip = base + QtCore.QPointF(
            math.cos(angle) * self.arrow_size,
            -math.sin(angle) * self.arrow_size
        )

        # Left and right points (perpendicular to the line)
        left = base + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * self.arrow_size / 2,
            -math.sin(angle + math.pi / 2) * self.arrow_size / 2
        )
        right = base + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * self.arrow_size / 2,
            -math.sin(angle - math.pi / 2) * self.arrow_size / 2
        )

        # Back point (behind the base)
        back = base - QtCore.QPointF(
            math.cos(angle) * self.arrow_size / 2,
            -math.sin(angle) * self.arrow_size / 2
        )

        # Create the diamond polygon
        diamond = QtGui.QPolygonF([back, left, tip, right])

        # Set brush
        if filled:
            painter.setBrush(QtCore.Qt.black)
        else:
            painter.setBrush(QtCore.Qt.white)

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.drawPolygon(diamond)

    def draw_triangle_head(self, painter, line, angle, dashed):
        """
        Draws a triangle-shaped arrowhead at the end of the line.

        Parameters:
        - painter (QPainter): The painter object.
        - line (QLineF): The line where the triangle is to be drawn.
        - angle (float): The angle of the line.
        - dashed (bool): Whether the line is dashed (Realization) or solid (Inheritance).
        """
        # Tip point (line end)
        tip = line.p2()

        # Base center point (back along the line)
        base_center = tip - QtCore.QPointF(
            math.cos(angle) * self.arrow_size,
            -math.sin(angle) * self.arrow_size
        )

        # Left and right points (perpendicular to the line)
        left = base_center + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * self.arrow_size / 2,
            -math.sin(angle + math.pi / 2) * self.arrow_size / 2
        )
        right = base_center + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * self.arrow_size / 2,
            -math.sin(angle - math.pi / 2) * self.arrow_size / 2
        )

        # Create the triangle polygon
        triangle = QtGui.QPolygonF([tip, left, right])

        # Set brush and pen
        painter.setBrush(QtCore.Qt.white)

        if dashed:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine))
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))

        painter.drawPolygon(triangle)

    def boundingRect(self):
        """
        Returns the bounding rectangle of the item.

        This method is necessary to ensure the item is redrawn correctly when moved.
        """
        extra = (self.pen().width() + self.arrow_size) / 2.0
        return QtCore.QRectF(self.line().p1(), self.line().p2()).normalized().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        """
        Returns the shape of the item as a QPainterPath.

        This method is useful for collision detection and precise redrawing.
        """
        path = QtGui.QPainterPath()
        path.moveTo(self.line().p1())
        path.lineTo(self.line().p2())
        return path