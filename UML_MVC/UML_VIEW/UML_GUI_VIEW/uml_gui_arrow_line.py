import math
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox as ClassBox

class UMLArrow(QtWidgets.QGraphicsPathItem):
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
        self.arrow_line = None
        self.arrow_start_line = None

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

        # self.update_position()  # Initial position update

    def update_position(self):
        """
        Update the arrow's position based on the closest connection points between the two boxes.
        """
        self.prepareGeometryChange()
        if self.is_self_relation:
            # Handle self-referential arrow
            self.calculate_self_arrow()
        else:
            # Calculate the best connection points and path
            startPoint, endPoint, startSide, endSide = self.calculate_closest_points(self.source_class, self.dest_class)
            if startPoint is None or endPoint is None:
                return  # Prevent errors if points are not found

            # Now compute the path with horizontal and vertical segments
            self.calculate_arrow_path(startPoint, endPoint, startSide, endSide)
            
            # Adjust the path if it collides with any obstacles
            self.reroute_path_if_collide(self.path())

    def calculate_closest_points(self, source_class, dest_class):
        """
        Calculate the closest connection points between the two boxes.

        Returns:
        - (QPointF, QPointF, str, str): Closest points on start and end boxes and their sides.
        """
        startPoints = source_class.connection_points_list
        endPoints = dest_class.connection_points_list

        minDistance = float('inf')
        closestStart = closestEnd = None
        startSide = endSide = None

        # Loop over each connection point in the source and destination classes
        for sp_name, sp_item in startPoints.items():
            # Get the scene position of the start point
            if isinstance(sp_item, QtWidgets.QGraphicsItem):
                sp = sp_item.scenePos()
            else:
                sp = self.source_class.scenePos() + sp_item

            for ep_name, ep_item in endPoints.items():
                # Get the scene position of the end point
                if isinstance(ep_item, QtWidgets.QGraphicsItem):
                    ep = ep_item.scenePos()
                else:
                    ep = self.dest_class.scenePos() + ep_item

                distance = QtCore.QLineF(sp, ep).length()
                if distance < minDistance:
                    minDistance = distance
                    closestStart, closestEnd = sp, ep
                    startSide, endSide = sp_name, ep_name

        return closestStart, closestEnd, startSide, endSide

    def calculate_arrow_path(self, startPoint, endPoint, startSide, endSide):
        path = QtGui.QPainterPath()
        path.moveTo(startPoint)

        # Decide directions based on sides
        side_directions = {
            'left': QtCore.QPointF(-1, 0),
            'right': QtCore.QPointF(1, 0),
            'top': QtCore.QPointF(0, -1),
            'bottom': QtCore.QPointF(0, 1),
        }

        # Get direction vectors
        startDir = side_directions.get(startSide, QtCore.QPointF(0, 0))
        endDir = side_directions.get(endSide, QtCore.QPointF(0, 0))

        # Move away from the boxes
        offset = 10
        startOffsetPoint = startPoint + startDir * offset
        endOffsetPoint = endPoint + endDir * offset

        # Create an L-shaped path
        if startSide in ['left', 'right']:
            # Horizontal then vertical
            intermediatePoint = QtCore.QPointF(startOffsetPoint.x(), endOffsetPoint.y())
        else:
            # Vertical then horizontal
            intermediatePoint = QtCore.QPointF(endOffsetPoint.x(), startOffsetPoint.y())

        path.lineTo(startOffsetPoint)
        path.lineTo(intermediatePoint)
        path.lineTo(endOffsetPoint)
        path.lineTo(endPoint)
        
        self.setPath(path)

        # Store lines for angle calculations
        self.arrow_line = QtCore.QLineF(endOffsetPoint, endPoint)
        self.arrow_start_line = QtCore.QLineF(startOffsetPoint, startPoint)
        

    def get_relative_direction(self, source_center, dest_center):
        """
        Determines the relative direction from source to destination.

        Returns:
            A tuple indicating the vertical and horizontal direction.
            For example, ('above', 'right') means the destination is above and to the right of the source.
        """
        vertical_direction = 'below' if source_center.y() > dest_center.y() else 'above'
        horizontal_direction = 'right' if dest_center.x() > source_center.x() else 'left'
        return (vertical_direction, horizontal_direction)
   
    
    def reroute_path_if_collide(self, path):
        """
        Adjusts the given path to wrap around obstacles if it collides with any ClassBox items in the scene (excluding source and destination).
        """
        offset = 15  # Distance to offset from the obstacle
        if self.scene() is None:
            return  # Scene is not set yet; exit the method

        for item in self.scene().items():
            if not isinstance(item, ClassBox) or item in [self.source_class, self.dest_class]:
                continue
            if not path.intersects(item.sceneBoundingRect()):
                continue
            
            obstacle_rect = item.sceneBoundingRect()

            # Get the current path elements
            elements = [path.elementAt(i) for i in range(path.elementCount())]

            # Get the corners of the obstacle rectangle in scene coordinates
            top_left = obstacle_rect.topLeft()
            top_right = obstacle_rect.topRight()
            bottom_right = obstacle_rect.bottomRight()
            bottom_left = obstacle_rect.bottomLeft()

            # Define the edges of the rectangle as lines
            rect_lines = [
                (QtCore.QLineF(top_left, top_right), "horizontal"),        # Top edge
                (QtCore.QLineF(top_right, bottom_right), "vertical"),      # Right edge
                (QtCore.QLineF(bottom_right, bottom_left), "horizontal"),  # Bottom edge
                (QtCore.QLineF(bottom_left, top_left), "vertical")         # Left edge
            ]

            vertical_intersections = []    # List to store vertical intersection points
            horizontal_intersections = []  # List to store horizontal intersection points

            # Iterate over each segment in the path
            for i in range(len(elements) - 1):
                point1 = QtCore.QPointF(elements[i].x, elements[i].y)
                point2 = QtCore.QPointF(elements[i+1].x, elements[i+1].y)
                segment_line = QtCore.QLineF(point1, point2)

                # Check for intersections with each side and categorize them
                for rect_line, orientation in rect_lines:
                    intersection_point = QtCore.QPointF()
                    intersection_type = segment_line.intersect(rect_line, intersection_point)
                    if intersection_type != QtCore.QLineF.BoundedIntersection:
                        continue
                    if orientation == "vertical":
                        vertical_intersections.append((intersection_point.x(), intersection_point.y()))
                    elif orientation == "horizontal":
                        horizontal_intersections.append((intersection_point.x(), intersection_point.y()))

            # Output the intersection points for debugging
            if vertical_intersections or horizontal_intersections:
                # for point in vertical_intersections:
                #     if point[1] >= item.connection_points_list["left"].scenePos().y():
                #         first_horizontal_offset = QtCore.QPointF(point[0] - offset , point[1])
                #         second_horizontal_offset = QtCore.QPointF(top_left.x() - offset, top_left.y() - (offset + item.boundingRect().height()))
                #         third_horizontal_offset = QtCore.QPointF(bottom_right.x() + offset, bottom_right.y() + offset)
                #         fourth_horizontal_offset = QtCore.QPointF(point[0], point[1] + offset)
                #     else:
                #         first_horizontal_offset = QtCore.QPointF(point[0], point[1] - (offset + item.boundingRect().height()))
                #         second_horizontal_offset = QtCore.QPointF(top_left.x() - offset, top_left.y() - offset)
                #         third_horizontal_offset = QtCore.QPointF(bottom_left.x() - offset, bottom_left.y() + offset)
                #         fourth_horizontal_offset = QtCore.QPointF(point[0], point[1] + offset)
                        
                #     new_path = QtGui.QPainterPath()
                #     # Adjust the path to route around the obstacle
                #     new_path.moveTo(elements[0].x, elements[0].y)  # Start point

                #     # Add waypoints to reroute around the obstacle
                #     new_path.lineTo(first_horizontal_offset)
                #     new_path.lineTo(second_horizontal_offset)
                #     new_path.lineTo(third_horizontal_offset)
                #     new_path.lineTo(fourth_horizontal_offset)
                #     new_path.lineTo(elements[-1].x, elements[-1].y)  # End point
                    
                #     # Update the path
                #     self.setPath(new_path)
                    
                # Calculate center points of source and destination for direction determination
                source_center = self.source_class.scenePos() + self.source_class.boundingRect().center()
                dest_center = self.dest_class.scenePos() + self.dest_class.boundingRect().center()
                vertical_dir, horizontal_dir = self.get_relative_direction(source_center, dest_center)
                
                for point in horizontal_intersections:
                    new_path = QtGui.QPainterPath()
                    if point[0] >= item.connection_points_list["top"].scenePos().x():
                        first_vertical_offset = QtCore.QPointF(point[0], point[1] - (offset + item.boundingRect().height()))
                        second_vertical_offset = QtCore.QPointF(top_right.x() + offset, top_right.y() - offset)
                        third_vertical_offset = QtCore.QPointF(bottom_right.x() + offset, bottom_right.y() + offset)
                        fourth_vertical_offset = QtCore.QPointF(point[0], point[1] + offset)     
                    else:
                        first_vertical_offset = QtCore.QPointF(point[0], point[1] - (offset + item.boundingRect().height()))
                        second_vertical_offset = QtCore.QPointF(top_left.x() - offset, top_left.y() - offset)
                        third_vertical_offset = QtCore.QPointF(bottom_left.x() - offset, bottom_left.y() + offset)
                        fourth_vertical_offset = QtCore.QPointF(point[0], point[1] + offset)   

                    if vertical_dir == "above":
                        # Adjust the path to route around the obstacle
                        new_path.moveTo(elements[0].x, elements[0].y)  # Start point
                        # Add waypoints to reroute around the obstacle
                        new_path.lineTo(first_vertical_offset)
                        new_path.lineTo(second_vertical_offset)
                        new_path.lineTo(third_vertical_offset)
                        new_path.lineTo(fourth_vertical_offset)
                        new_path.lineTo(elements[-1].x, elements[-1].y)  # End point
                    else:
                        # Adjust the path to route around the obstacle
                        new_path.moveTo(elements[0].x, elements[0].y)  # Start point
                        # Add waypoints to reroute around the obstacle
                        new_path.lineTo(fourth_vertical_offset)
                        new_path.lineTo(third_vertical_offset)
                        new_path.lineTo(second_vertical_offset)
                        new_path.lineTo(first_vertical_offset)
                        new_path.lineTo(elements[-1].x, elements[-1].y)  # End point
                        
                    # Update the path
                    self.setPath(new_path)
                    print(f"({point[0]}, {point[1]})")

    def calculate_self_arrow(self):
        """
        Calculate the path for a self-referential arrow (loop) on top of the class box.
        Ensures the arrowhead does not overlap with the class box by adjusting the end point.
        """
        # Get the bounding rectangle of the class in scene coordinates
        rect = self.source_class.mapToScene(self.source_class.rect()).boundingRect()
        
        # Define an additional offset to prevent arrowhead from overlapping
        arrow_offset_x = 10
        arrow_offset_y = 10

        # Start and end points on the class box (top side)
        start_point = rect.topLeft() + QtCore.QPointF(rect.width() / 3, 0)
        end_point = rect.topRight() - QtCore.QPointF(rect.width() / 3, 0)
        
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
        path = QtGui.QPainterPath()
        path.moveTo(start_point)
        path.cubicTo(control_point1, control_point2, end_point)
        self.setPath(path)

        # Store line for angle calculation
        self.arrow_line = QtCore.QLineF(control_point2, end_point)

    def paint(self, painter, option, widget=None):
        """
        Custom paint method to draw the arrow with the correct arrowhead based on relationship type.
        """
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(self.pen())

        if self.is_self_relation:
            # Draw the self-referential arrow
            painter.drawPath(self.path())

            # Calculate angle for the arrowhead at the end of the path
            end_point = self.path().pointAtPercent(1.0)
            angle = math.radians(self.path().angleAtPercent(1.0))

            # Draw the correct arrowhead based on relationship type
            if self.relationship_type in ["Inheritance", "Realization"]:
                dashed = (self.relationship_type == "Realization")
                self.draw_triangle_head_at_point(painter, end_point, angle, dashed=dashed)
            elif self.relationship_type in ["Aggregation", "Composition"]:
                filled = (self.relationship_type == "Composition")
                # For diamond, we need the angle at the start
                start_point = self.path().pointAtPercent(0.0)
                start_angle = -math.radians(self.path().angleAtPercent(0.0))
                self.draw_diamond_head_at_point(painter, start_point, start_angle, filled=filled)
            else:
                # For other types, draw a simple arrowhead at the end
                self.draw_arrow_head(painter, end_point, angle)
        else:
            # Draw the path
            painter.drawPath(self.path())

            # Calculate angle for the arrowhead at the end
            line = self.arrow_line
            angle = math.atan2(-line.dy(), line.dx())

            # Adjust based on the relationship type
            if self.relationship_type in ["Aggregation", "Composition"]:
                # Draw the diamond at the start (source)
                line_start = self.arrow_start_line
                angle_start = math.atan2(-line_start.dy(), line_start.dx())
                filled = (self.relationship_type == "Composition")
                self.draw_diamond_head_at_point(painter, line_start.p1(), angle_start, filled=filled)
            elif self.relationship_type in ["Inheritance", "Realization"]:
                # Draw the triangle at the end (destination)
                dashed = (self.relationship_type == "Realization")
                end_point = line.p2()
                self.draw_triangle_head_at_point(painter, end_point, angle, dashed=dashed)
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
            -math.sin(angle + math.pi / 6) * arrow_size
        )
        p2 = point + QtCore.QPointF(
            math.cos(angle - math.pi / 6) * arrow_size,
            -math.sin(angle - math.pi / 6) * arrow_size
        )

        # Create the arrowhead polygon
        arrow_head = QtGui.QPolygonF([point, p1, p2])

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(arrow_head)

    def draw_diamond_head_at_point(self, painter, point, angle, filled):
        """
        Draws a diamond-shaped arrowhead at a given point and angle.
        """
        arrow_size = self.arrow_size

        # Base point (point)
        base = point

        # Calculate points for the diamond
        # Tip point (forward along the angle)
        tip = base + QtCore.QPointF(
            math.cos(angle) * arrow_size,
            -math.sin(angle) * arrow_size
        )

        # Left and right points (perpendicular to the angle)
        left = base + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * arrow_size / 2,
            -math.sin(angle + math.pi / 2) * arrow_size / 2
        )
        right = base + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * arrow_size / 2,
            -math.sin(angle - math.pi / 2) * arrow_size / 2
        )

        # Back point (behind the base)
        back = base - QtCore.QPointF(
            math.cos(angle) * arrow_size / 2,
            -math.sin(angle) * arrow_size / 2
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

    def draw_triangle_head_at_point(self, painter, point, angle, dashed):
        """
        Draws a triangle-shaped arrowhead at a given point and angle.
        """
        arrow_size = self.arrow_size

        # Tip point (point)
        tip = point

        # Base center point (back along the angle)
        base_center = tip - QtCore.QPointF(
            math.cos(angle) * arrow_size,
            -math.sin(angle) * arrow_size
        )

        # Left and right points (perpendicular to the angle)
        left = base_center + QtCore.QPointF(
            math.cos(angle + math.pi / 2) * arrow_size / 2,
            -math.sin(angle + math.pi / 2) * arrow_size / 2
        )
        right = base_center + QtCore.QPointF(
            math.cos(angle - math.pi / 2) * arrow_size / 2,
            -math.sin(angle - math.pi / 2) * arrow_size / 2
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
        extra = (self.pen().width() + self.arrow_size) / 2.0
        return self.path().boundingRect().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        """
        Returns the shape of the item as a QPainterPath.
        """
        path_stroker = QtGui.QPainterPathStroker()
        path_stroker.setWidth(self.pen().width() + self.arrow_size)
        return path_stroker.createStroke(self.path())
