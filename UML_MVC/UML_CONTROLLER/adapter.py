import math
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple


class UMLToImageAdapter:
    def __init__(self, model: object) -> None:
        self.model = model
        self.default_margin = 10  # Margin for padding
        self.line_color = "#0090ff"
        self.box_color = "#00ffff"
        self.title_color = "#00ffff"
        self.canvas_margin = 50  # Additional margin for the canvas

    def generate_image(self, output_file: str) -> None:
        main_data = self.model._get_main_data()
        visualization_data = self._extract_visualization_data(main_data)

        # Determine dynamic offsets and dimensions
        min_x = min(item["position"]["x"] for item in visualization_data if "position" in item)
        min_y = min(item["position"]["y"] for item in visualization_data if "position" in item)
        max_x = max(item["position"]["x"] for item in visualization_data if "position" in item) + 200
        max_y = max(item["position"]["y"] for item in visualization_data if "position" in item) + 200

        offset_x = -min_x + self.canvas_margin if min_x < 0 else self.canvas_margin
        offset_y = -min_y + self.canvas_margin if min_y < 0 else self.canvas_margin

        # Convert dimensions to integers
        img_width = int(max_x + offset_x + self.canvas_margin)
        img_height = int(max_y + offset_y + self.canvas_margin)

        # Create the image with higher resolution
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)
        
        # Font settings with fallback
        try:
            self.title_font = ImageFont.truetype("arial.ttf", 16)
            self.body_font = ImageFont.truetype("arial.ttf", 14)
        except IOError:
            self.title_font = ImageFont.load_default()
            self.body_font = ImageFont.load_default()

        # Draw each class box
        for item in visualization_data:
            if "name" in item:
                x = int(item["position"]["x"]) + offset_x
                y = int(item["position"]["y"]) + offset_y
                self.draw_class_box(draw, item, x, y)

        # Draw relationships
        for item in visualization_data:
            if "source" in item and "destination" in item:
                if item["source"] == item["destination"]:
                    # Handle self-referential relationship
                    class_position = next(cls for cls in visualization_data if cls["name"] == item["source"])["position"]
                    self.draw_self_relationship(draw, class_position, item["type"], offset_x, offset_y)
                else:
                    # Handle normal relationship
                    self.draw_relationship(draw, visualization_data, item, offset_x, offset_y)

        # Save the final image
        self.save_image(image, output_file)

    def calculate_box_dimensions(self, item: Dict[str, object]) -> tuple[int, int]:
        """Calculate the dimensions for the class box based on content, minimizing extra space at the bottom."""
        class_name = item["name"]
        fields = item["fields"]
        methods = item["methods"]

        # Calculate max width for each section
        max_class_name_width = self.title_font.getbbox(class_name)[2]
        max_field_width = max(
            (self.body_font.getbbox(f"{field.get('type', '')} {field.get('name', '')}")[2] for field in fields),
            default=0
        )
        max_method_width = max(
            (self.body_font.getbbox(f"{method.get('return_type', '')} {method.get('name', '')}()")[2] for method in methods),
            default=0
        )

        # Determine the largest width among all components
        content_max_width = max(max_class_name_width, max_field_width, max_method_width)
        box_width = content_max_width + self.default_margin * 2  # Add padding

        # Calculate height with minimal padding
        class_name_height = self.title_font.getbbox(class_name)[3] + 5  # Add small padding for the title
        fields_text_height = len(fields) * 20 if fields else 0  # Adjust line height for fields
        methods_text_height = len(methods) * 20 if methods else 0  # Adjust line height for methods
        separator_height = 5 if fields and methods else 0  # Separator if both fields and methods exist
        bottom_buffer = 10  # Additional space at the bottom for visual breathing room

        # Total height with minimal padding
        box_height = (
            class_name_height + fields_text_height + methods_text_height +
            separator_height + self.default_margin * 2 + bottom_buffer
        )

        return max(box_width, 170), box_height  # Ensure minimum width if needed

    def draw_class_box(self, draw: ImageDraw.Draw, item: Dict[str, object], x: int, y: int) -> None:
        """Draw the UML class box including title, fields, and methods, and add connection points."""
        box_width, box_height = self.calculate_box_dimensions(item)

        # Draw main box with updated colors
        draw.rectangle([x, y, x + box_width, y + box_height], fill=self.box_color, outline=self.line_color)
        
        # Draw title background
        draw.rectangle([x, y, x + box_width, y + 25], fill=self.title_color, outline=self.line_color)
        
        # Center the title text within the title background
        title_text = item["name"]
        title_text_width = self.title_font.getbbox(title_text)[2]
        title_x = x + (box_width - title_text_width) // 2  # Calculate centered x position
        draw.text((title_x, y + 5), title_text, fill="black", font=self.title_font)

        # Draw fields section
        field_y = y + 25 + self.default_margin
        for field in item["fields"]:
            field_text = f"{field.get('type', '')} {field.get('name', '')}"
            draw.text((x + self.default_margin, field_y), field_text, fill="black", font=self.body_font)
            field_y += 20  # line height

        # Draw a separator line between fields and methods
        if item["fields"]:
            draw.line([(x, field_y), (x + box_width, field_y)], fill=self.line_color)
            field_y += self.default_margin  # Add margin below the separator line

        # Draw methods section
        method_y = field_y
        for method in item["methods"]:
            method_text = f"{method.get('return_type', '')} {method.get('name', '')}()"
            draw.text((x + self.default_margin, method_y), method_text, fill="black", font=self.body_font)
            method_y += 20  # line height

        # Create and draw connection points
        connection_points = self.create_connection_points(draw, x, y, box_width, box_height)
        item["connection_points"] = connection_points  # Store connection points in the item data

    def draw_self_relationship(self, draw: ImageDraw.Draw, position: Dict[str, int], relationship_type: str, offset_x: int, offset_y: int) -> None:
        """Draw a self-referential (loop) relationship using the top connection point."""
        x = int(position["x"]) + offset_x
        y = int(position["y"]) + offset_y
        loop_start = (x + 120, y)  # Start from the top center of the box
        loop_control1 = (x + 120, y - 60)  # Control point above the top center
        loop_control2 = (x + 50, y - 60)  # Control point for the arc
        loop_end = (x + 50, y)  # End at the top center

        # Draw the curve
        if relationship_type == "Realization":
            self.draw_dashed_curve(draw, loop_start, loop_control1, loop_control2, loop_end, fill="black", width=2)
        else:
            self.draw_solid_curve(draw, loop_start, loop_control1, loop_control2, loop_end, fill="black", width=2)

        # Add relationship-specific symbols
        if relationship_type == "Composition":
            self.draw_filled_diamond(draw, loop_start)
        elif relationship_type == "Aggregation":
            self.draw_open_diamond(draw, loop_start)
        elif relationship_type in ["Inheritance", "Realization"]:
            self.draw_arrowhead(draw, loop_end, loop_control2, loop_end)

            
    def draw_relationship(self, draw: ImageDraw.Draw, visualization_data: List[Dict[str, Dict[str, int]]], item: Dict[str, str], offset_x: int, offset_y: int) -> None:
        """Draw relationships between UML classes with aligned symbols at endpoints."""

        # Get source and destination classes
        source_class = next(cls for cls in visualization_data if cls["name"] == item["source"])
        dest_class = next(cls for cls in visualization_data if cls["name"] == item["destination"])

        # Calculate positions and dimensions with offsets
        src_x = int(source_class["position"]["x"]) + offset_x
        src_y = int(source_class["position"]["y"]) + offset_y
        src_box_width, src_box_height = self.calculate_box_dimensions(source_class)
        dest_x = int(dest_class["position"]["x"]) + offset_x
        dest_y = int(dest_class["position"]["y"]) + offset_y
        dest_box_width, dest_box_height = self.calculate_box_dimensions(dest_class)

        # Define connection points for both classes
        src_connection_points = {
            'top': (src_x + src_box_width // 2, src_y),
            'bottom': (src_x + src_box_width // 2, src_y + src_box_height),
            'left': (src_x, src_y + src_box_height // 2),
            'right': (src_x + src_box_width, src_y + src_box_height // 2),
        }
        dest_connection_points = {
            'top': (dest_x + dest_box_width // 2, dest_y),
            'bottom': (dest_x + dest_box_width // 2, dest_y + dest_box_height),
            'left': (dest_x, dest_y + dest_box_height // 2),
            'right': (dest_x + dest_box_width, dest_y + dest_box_height // 2),
        }

        # Calculate the closest connection points
        start_point, end_point = self.calculate_closest_points(src_connection_points, dest_connection_points)

        # Adjust the start_point and end_point based on relationship type
        margin = 10  # Margin to prevent overlap
        if item["type"] in ["Aggregation", "Composition"]:
            # For Aggregation and Composition, adjust the start_point to prevent overlap
            start_point = self.adjust_endpoint_towards_box(start_point, end_point, margin)
    
        else:
            # For Inheritance and Realization, adjust only the end_point
            end_point = self.adjust_endpoint_towards_box(end_point, start_point, margin)

        # Draw the line between classes
        if item["type"] == "Realization":
            self.draw_dashed_line(draw, start_point, end_point, fill="black", width=2)
        else:
            draw.line([start_point, end_point], fill="black", width=2)

        # Draw the symbol at the appropriate end (ensure the arrowhead is drawn at the exact end_point)
        if item["type"] == "Composition":
            self.draw_filled_diamond(draw, start_point)  # Symbol at source
        elif item["type"] == "Aggregation":
            self.draw_open_diamond(draw, start_point)  # Symbol at source
        elif item["type"] in ["Inheritance", "Realization"]:
            # Ensure the arrowhead is placed at the end_point (no offset or adjustment)
            self.draw_arrowhead(draw, end_point, start_point, end_point, filled=False)  # Arrowhead at destination

    def adjust_endpoint(self, endpoint: Tuple[int, int], reference_point: Tuple[int, int], margin: int, towards_box: bool = True) -> Tuple[int, int]:
        """
        Adjusts the endpoint either towards or away from a reference point by a specified margin.

        Parameters:
            endpoint (tuple): The endpoint to adjust (x, y).
            reference_point (tuple): The reference point to adjust relative to (x, y).
            margin (int): The distance to adjust.
            towards_box (bool): If True, adjust towards the reference point; otherwise, adjust away.

        Returns:
            tuple: The adjusted endpoint.
        """
        ex, ey = endpoint
        rx, ry = reference_point

        # Calculate the direction vector
        vector_x = rx - ex if towards_box else ex - rx
        vector_y = ry - ey if towards_box else ey - ry
        vector_length = math.sqrt(vector_x**2 + vector_y**2)

        if vector_length == 0:
            return endpoint  # Avoid division by zero if points are the same

        # Normalize and scale the vector
        unit_x = vector_x / vector_length
        unit_y = vector_y / vector_length
        adjusted_x = ex + unit_x * margin
        adjusted_y = ey + unit_y * margin

        return int(adjusted_x), int(adjusted_y)

    def adjust_endpoint_towards_box(self, point, target, margin):
        """ Adjust the endpoint to move slightly outward from the box. """
        px, py = point
        tx, ty = target
        dx, dy = tx - px, ty - py
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:  # Prevent division by zero
            return point

        # Calculate the adjustment
        adjustment_x = margin * dx / distance  # Keep as float
        adjustment_y = margin * dy / distance  # Keep as float

        # Apply the adjustment
        adjusted_point = (px + adjustment_x, py + adjustment_y)

        # Optionally, round the final result
        return (round(adjusted_point[0]), round(adjusted_point[1]))


    def offset_along_line(self, point1, point2, offset):
        """Calculate a point along the line from point1 to point2 at a given offset distance."""
        line_length = math.hypot(point2[0] - point1[0], point2[1] - point1[1])
        if line_length == 0:
            return point1
        # Calculate offset point
        ratio = offset / line_length
        x = point1[0] + (point2[0] - point1[0]) * ratio
        y = point1[1] + (point2[1] - point1[1]) * ratio
        return (x, y)

    def calculate_closest_points(self, src_points, dest_points):
        """Find the closest connection points between source and destination."""
        min_distance = float('inf')
        closest_src = closest_dest = None
        for sp_name, sp in src_points.items():
            for ep_name, ep in dest_points.items():
                distance = math.hypot(sp[0] - ep[0], sp[1] - ep[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_src, closest_dest = sp, ep
        return closest_src, closest_dest

    def draw_solid_curve(self, draw, start, control1, control2, end, fill="black", width=2):
        """Draw a solid Bezier curve using the start, control, and end points."""
        points = self._generate_bezier_points(start, control1, control2, end)
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=fill, width=width)

    def draw_dashed_curve(self, draw, start, control1, control2, end, fill="black", width=2, dash_length=10):
        """Draw a dashed Bezier curve using the start, control, and end points."""
        points = self._generate_bezier_points(start, control1, control2, end)
        total_length = 0
        draw_dash = True
        for i in range(len(points) - 1):
            segment_start = points[i]
            segment_end = points[i + 1]
            segment_length = math.hypot(segment_end[0] - segment_start[0], segment_end[1] - segment_start[1])
            total_length += segment_length
            if draw_dash:
                draw.line([segment_start, segment_end], fill=fill, width=width)
            if total_length >= dash_length:
                draw_dash = not draw_dash  # Toggle dash drawing
                total_length = 0

    def _generate_bezier_points(self, start, control1, control2, end, steps=20):
        """Generate points along a Bezier curve for given start, control, and end points."""
        points = []
        for t in range(steps + 1):
            t /= steps
            x = (1 - t) ** 3 * start[0] + 3 * (1 - t) ** 2 * t * control1[0] + 3 * (1 - t) * t ** 2 * control2[0] + t ** 3 * end[0]
            y = (1 - t) ** 3 * start[1] + 3 * (1 - t) ** 2 * t * control1[1] + 3 * (1 - t) * t ** 2 * control2[1] + t ** 3 * end[1]
            points.append((x, y))
        return points

    def draw_filled_diamond(self, draw, position):
        """Draw a filled diamond for Composition."""
        diamond_size = 10
        x, y = position
        draw.polygon([
            (x - diamond_size, y),
            (x, y - diamond_size),
            (x + diamond_size, y),
            (x, y + diamond_size)
        ], fill="black")                    

    def draw_open_diamond(self, draw, position):
        """Draw an open diamond for Aggregation."""
        diamond_size = 6
        x, y = position
        draw.polygon([
            (x - diamond_size, y),
            (x, y - diamond_size),
            (x + diamond_size, y),
            (x, y + diamond_size)
        ], outline="black", fill=None)

    def draw_arrowhead(self, draw: ImageDraw.Draw, position: Tuple[int, int], start: Tuple[int, int], end: Tuple[int, int], filled: bool = False) -> None:
        """Draw an open or filled arrowhead (triangle) at the end of the line."""
        arrow_size = 10  # Size of the arrowhead
        # Calculate angle between the line defined by start and end points
        angle = math.atan2(end[1] - start[1], end[0] - start[0])  # Direction of the line

        # Position is where the arrowhead base will be drawn (at the end of the line)
        x, y = end  # The base of the arrowhead should be at the line's end

        # Calculate the left and right points of the arrowhead based on angle
        left_point = (x - arrow_size * math.cos(angle - math.pi / 6),
                    y - arrow_size * math.sin(angle - math.pi / 6))
        right_point = (x - arrow_size * math.cos(angle + math.pi / 6),
                    y - arrow_size * math.sin(angle + math.pi / 6))

        # Adjust the tip of the arrowhead
        if filled:
            # Draw the filled arrowhead
            draw.polygon([position, left_point, right_point], fill="black")
        else:
            # Draw the open arrowhead
            draw.polygon([position, left_point, right_point], outline="black", fill=None)
            
    def draw_dashed_line(self, draw, start, end, fill="black", width=2, dash_length=10):
        """Draw a dashed line for Realization."""
        total_length = math.hypot(end[0] - start[0], end[1] - start[1])
        num_dashes = int(total_length // dash_length)
        for i in range(num_dashes):
            segment_start = (
                start[0] + (end[0] - start[0]) * i / num_dashes,
                start[1] + (end[1] - start[1]) * i / num_dashes,
            )
            segment_end = (
                start[0] + (end[0] - start[0]) * (i + 0.5) / num_dashes,
                start[1] + (end[1] - start[1]) * (i + 0.5) / num_dashes,
            )
            draw.line([segment_start, segment_end], fill=fill, width=width)

    def create_connection_points(self, draw, x, y, box_width, box_height):
        """
        Create four connection points (top, bottom, left, right) for linking arrows between UML boxes.
        Each connection point is represented by a small circle at the edge of the UML box.
        
        Parameters:
        - draw: The ImageDraw instance used for drawing.
        - x, y: Top-left coordinates of the UML box.
        - box_width, box_height: Dimensions of the UML box.
        
        Returns:
        - A Dictionary with connection points coordinates.
        """
        connection_points = {
            'top': (x + box_width // 2, y),
            'bottom': (x + box_width // 2, y + box_height),
            'left': (x, y + box_height // 2),
            'right': (x + box_width, y + box_height // 2)
        }

        # Draw connection points as small circles
        connection_point_radius = 3
        for position in connection_points.values():
            cx, cy = position
            draw.ellipse(
                (cx - connection_point_radius, cy - connection_point_radius, 
                cx + connection_point_radius, cy + connection_point_radius),
                fill="white", outline="DodgerBlue"
            )

        return connection_points

    def save_image(self, image, output_file):
        """Save the image at high quality."""
        image.save(output_file, "PNG", dpi=(300, 300))
        print(f"Image saved to {output_file}")

    def _extract_visualization_data(self, main_data):
        visualization_data = []
        
        for each_class in main_data.get("classes", []):
            class_Dict = {
                "name": each_class["name"],
                "fields": each_class.get("fields", []),
                "methods": each_class.get("methods", []),
                "position": each_class.get("position", {"x": 0, "y": 0})
            }
            visualization_data.append(class_Dict)
        
        for relationship in main_data.get("relationships", []):
            visualization_data.append({
                "source": relationship["source"],
                "destination": relationship["destination"],
                "type": relationship["type"]
            })
        
        return visualization_data