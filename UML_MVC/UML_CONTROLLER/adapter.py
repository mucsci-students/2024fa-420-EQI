from PIL import Image, ImageDraw, ImageFont

class UMLToImageAdapter:
    def __init__(self, model):
        self.model = model

    def generate_image(self, output_file):
        main_data = self.model._get_main_data()
        visualization_data = self._extract_visualization_data(main_data)

        # Determine dynamic offsets and dimensions
        min_x = min(item["position"]["x"] for item in visualization_data if "position" in item)
        min_y = min(item["position"]["y"] for item in visualization_data if "position" in item)
        max_x = max(item["position"]["x"] for item in visualization_data if "position" in item) + 200
        max_y = max(item["position"]["y"] for item in visualization_data if "position" in item) + 200

        offset_x = -min_x if min_x < 0 else 0
        offset_y = -min_y if min_y < 0 else 0

        # Convert dimensions to integers
        img_width = int(max_x + offset_x + 50)
        img_height = int(max_y + offset_y + 50)

        # Create the image with higher resolution
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)
        
        # Font settings with fallback
        try:
            title_font = ImageFont.truetype("arial.ttf", 16)
            body_font = ImageFont.truetype("arial.ttf", 14)
        except IOError:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()

        # Box styling
        box_margin = 10
        title_height = 25
        line_height = 20  # Increased line height for readability

        # Draw classes
        for item in visualization_data:
            if "name" in item:
                class_name = item["name"]
                position = item["position"]
                fields = item["fields"]
                methods = item["methods"]
                
                x = int(position["x"]) + offset_x
                y = int(position["y"]) + offset_y

                # Calculate the box width based on the longest text element, with a default minimum width
                max_text_width = max(
                    (body_font.getbbox(f"{field.get('type', '')} {field.get('name', '')}")[2] for field in fields + methods),
                    default=100  # Default minimum width if fields + methods is empty
                ) + box_margin * 2
                box_width = max(180, max_text_width)  # Minimum width 180, adjusted based on text
                box_height = title_height + box_margin + line_height * (len(fields) + len(methods))

                # Draw main box
                draw.rectangle([x, y, x + box_width, y + box_height], fill="#E0FFFF", outline="black")
                
                # Draw title background
                draw.rectangle([x, y, x + box_width, y + title_height], fill="#00BFFF", outline="black")
                draw.text((x + box_margin, y + 5), class_name, fill="black", font=title_font)
                
                # Draw fields and methods
                field_y = y + title_height + box_margin
                for field in fields:
                    field_text = f"{field.get('type', '')} {field.get('name', '')}"
                    draw.text((x + box_margin, field_y), field_text, fill="black", font=body_font)
                    field_y += line_height
                
                method_y = field_y + box_margin
                for method in methods:
                    method_text = f"{method.get('return_type', '')} {method.get('name', '')}()"
                    draw.text((x + box_margin, method_y), method_text, fill="black", font=body_font)
                    method_y += line_height

        # Draw relationships
        for item in visualization_data:
            if "source" in item and "destination" in item:
                source_class = next(cls for cls in visualization_data if cls["name"] == item["source"])
                dest_class = next(cls for cls in visualization_data if cls["name"] == item["destination"])
                
                # Get the positions for relationship lines
                src_x = int(source_class["position"]["x"]) + offset_x + box_width
                src_y = int(source_class["position"]["y"]) + offset_y + box_height // 2
                dest_x = int(dest_class["position"]["x"]) + offset_x
                dest_y = int(dest_class["position"]["y"]) + offset_y + box_height // 2
                
                # Draw the line for the relationship
                draw.line([(src_x, src_y), (dest_x, dest_y)], fill="black", width=2)
                
                # Add a diamond for composition at the source box's right edge
                if item["type"] == "Composition":
                    diamond_size = 6
                    diamond_x = src_x - diamond_size
                    diamond_y = src_y
                    draw.polygon([
                        (diamond_x - diamond_size, diamond_y),
                        (diamond_x, diamond_y - diamond_size),
                        (diamond_x + diamond_size, diamond_y),
                        (diamond_x, diamond_y + diamond_size)
                    ], fill="black")

        # Save the image at high quality
        image.save(output_file, "PNG", dpi=(300, 300))
        print(f"Image saved to {output_file}")

    def _extract_visualization_data(self, main_data):
        visualization_data = []
        
        for each_class in main_data.get("classes", []):
            class_dict = {
                "name": each_class["name"],
                "fields": each_class.get("fields", []),
                "methods": each_class.get("methods", []),
                "position": each_class.get("position", {"x": 0, "y": 0})
            }
            visualization_data.append(class_dict)
        
        for relationship in main_data.get("relationships", []):
            visualization_data.append({
                "source": relationship["source"],
                "destination": relationship["destination"],
                "type": relationship["type"]
            })
        
        return visualization_data
