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

        # Detect self-referential relationship
        self.is_self_relation = (self.source_class == self.dest_class)

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

        # Initialize path for self-referential arrow
        if self.is_self_relation:
            self.path = QtGui.QPainterPath()
        
        self.update_position()  # Initial position update

    def update_position(self):
        """
        Update the arrow's position based on the closest connection points between the two boxes.
        """
        self.prepareGeometryChange()
        if self.is_self_relation:
            # Handle self-referential arrow
            self.calculate_self_arrow()
        else:
            # Existing code for normal arrows
            startPoint, endPoint = self.calculate_closest_points()
            if startPoint is None or endPoint is None:
                return  # Prevent errors if points are not found
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

    def calculate_self_arrow(self):
        """
        Calculate the path for a self-referential arrow (loop) on top of the class box.
        Ensures the arrowhead does not overlap with the class box by adjusting the end point.
        """
        # Get the bounding rectangle of the class in scene coordinates
        rect = self.source_class.mapToScene(self.source_class.rect()).boundingRect()

        # Start and end points on the class box (top side)
        start_point = rect.topLeft() + QtCore.QPointF(rect.width() / 3, 0)
        end_point = rect.topRight() - QtCore.QPointF(rect.width() / 3, 0)

        # Define an additional offset to prevent arrowhead from overlapping
        arrow_offset_x = 10  # Adjust this value as needed
        arrow_offset_y = 10
        
        if self.relationship_type in ["Inheritance", "Realization"]:
            # Subtract the arrow_offset from the y-coordinate to move the end_point upwards
            end_point = end_point - QtCore.QPointF(arrow_offset_x, 0)
        elif self.relationship_type in ["Aggregation", "Composition"]:
            start_point = start_point - QtCore.QPointF(0, arrow_offset_y)

        # Offset for control points to shape the loop (above the class box)
        control_offset = 40  # Adjust this value to change loop height

        # Control points to create a loop above the class
        control_point1 = start_point - QtCore.QPointF(0, control_offset)
        control_point2 = end_point - QtCore.QPointF(0, control_offset)

        # Create the path for the loop
        self.path = QtGui.QPainterPath()
        self.path.moveTo(start_point)
        self.path.cubicTo(control_point1, control_point2, end_point)


    def paint(self, painter, option, widget=None):
        """
        Custom paint method to draw the arrow with the correct arrowhead based on relationship type.
        """
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(self.pen())

        if self.is_self_relation:
            # Draw the self-referential arrow
            painter.drawPath(self.path)

            # Calculate angle for the arrowhead at the end of the path
            last_tangent = self.path.angleAtPercent(1.0)
            angle = math.radians(-last_tangent)

            # Draw arrowhead at the end of the loop
            end_point = self.path.pointAtPercent(1.0)

            # Draw the correct arrowhead based on relationship type
            if self.relationship_type in ["Inheritance", "Realization"]:
                dashed = (self.relationship_type == "Realization")
                self.draw_triangle_head_at_point(painter, end_point, angle, dashed=dashed)
            elif self.relationship_type in ["Aggregation", "Composition"]:
                filled = (self.relationship_type == "Composition")
                self.draw_diamond_head_at_point(painter, start_point=self.path.pointAtPercent(0.0), angle=angle, filled=filled)
            else:
                # For other types, draw a simple arrowhead at the end
                self.draw_arrow_head(painter, end_point, angle)
        else:
            # Existing code for normal arrows
            line = self.line()
            painter.drawLine(line)

            # Calculate angle of the line for arrowhead orientation
            angle = math.atan2(-line.dy(), line.dx())

            # Adjust based on the relationship type
            if self.relationship_type in ["Aggregation", "Composition"]:
                # Draw the diamond at the start (source)
                self.draw_diamond_head(painter, line, angle, filled=(self.relationship_type == "Composition"))
            elif self.relationship_type in ["Inheritance", "Realization"]:
                # Draw the triangle at the end (destination)
                dashed = (self.relationship_type == "Realization")
                self.draw_triangle_head(painter, line, angle, dashed=dashed)
            else:
                # For other types, draw a simple arrowhead at the end
                end_point = line.p2()
                self.draw_arrow_head(painter, end_point, angle)

    def draw_arrow_head(self, painter, point, angle):
        """
        Draws a simple arrowhead at a given point and angle.
        """
        arrow_size = self.arrow_size

        # Calculate points for the arrowhead triangle
        p1 = point + QtCore.QPointF(
            math.cos(angle + math.pi / 6) * arrow_size,
            math.sin(angle + math.pi / 6) * arrow_size
        )
        p2 = point + QtCore.QPointF(
            math.cos(angle - math.pi / 6) * arrow_size,
            math.sin(angle - math.pi / 6) * arrow_size
        )

        # Create the arrowhead polygon
        arrow_head = QtGui.QPolygonF([point, p1, p2])

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(arrow_head)

    def draw_diamond_head_at_point(self, painter, start_point, angle, filled):
        """
        Draws a diamond-shaped arrowhead at a given point and angle.
        """
        arrow_size = self.arrow_size

        # Base point (start_point)
        base = start_point

        # Calculate points for the diamond
        # Tip point (forward along the angle)
        tip = base + QtCore.QPointF(
            math.cos(angle) * arrow_size,
            math.sin(angle) * arrow_size
        )

        # Left and right points (perpendicular to the angle)
        left = base + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * arrow_size / 2,
            math.sin(angle + math.pi / 2) * arrow_size / 2
        )
        right = base + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * arrow_size / 2,
            math.sin(angle - math.pi / 2) * arrow_size / 2
        )

        # Back point (behind the base)
        back = base - QtCore.QPointF(
            math.cos(angle) * arrow_size / 2,
            math.sin(angle) * arrow_size / 2
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

    def draw_triangle_head_at_point(self, painter, end_point, angle, dashed):
        """
        Draws a triangle-shaped arrowhead at a given point and angle.
        """
        arrow_size = self.arrow_size

        # Tip point (end_point)
        tip = end_point

        # Base center point (back along the angle)
        base_center = tip - QtCore.QPointF(
            math.cos(angle) * arrow_size,
            math.sin(angle) * arrow_size
        )

        # Left and right points (perpendicular to the angle)
        left = base_center + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * arrow_size / 2,
            math.sin(angle + math.pi / 2) * arrow_size / 2
        )
        right = base_center + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * arrow_size / 2,
            math.sin(angle - math.pi / 2) * arrow_size / 2
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

    def draw_diamond_head(self, painter, line, angle, filled):
        """
        Draws a diamond-shaped arrowhead at the start of the line.
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
        """
        if self.is_self_relation:
            return self.path.boundingRect().adjusted(-self.arrow_size, -self.arrow_size, self.arrow_size, self.arrow_size)
        else:
            extra = (self.pen().width() + self.arrow_size) / 2.0
            return QtCore.QRectF(self.line().p1(), self.line().p2()).normalized().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        """
        Returns the shape of the item as a QPainterPath.
        """
        if self.is_self_relation:
            path_stroker = QtGui.QPainterPathStroker()
            path_stroker.setWidth(self.pen().width() + self.arrow_size)
            return path_stroker.createStroke(self.path)
        else:
            path = QtGui.QPainterPath()
            path.moveTo(self.line().p1())
            path.lineTo(self.line().p2())
            return path
