import cv2
import numpy as np


def generate_object(screen_width, existing_objects, min_dist=60):
    # Define margin as a percentage of screen width
    x_margin = 0.1  # 10% margin on each side of the screen
    screen_x_margin = int(np.ceil(x_margin * screen_width))

    for _ in range(100):  # Try to generate a non-overlapping object
        # Random position within the margins
        x_position = np.random.randint(screen_x_margin, screen_width - screen_x_margin)
        y_position = 0

        # Increase size range for larger objects
        size = np.random.randint(30, 60)  # Increased object sizes

        # Check for overlap with existing objects
        if all(np.sqrt((x_position - obj["position"][0]) ** 2 + (y_position - obj["position"][1]) ** 2) >= (
                size + obj["size"] + min_dist) for obj in existing_objects):
            # Determine shape and color
            shape = np.random.choice(["circle", "square", "triangle"])  # Example shapes
            color = tuple(np.random.randint(0, 255) for _ in range(3))  # Random color

    print(f"Generated object: {shape}, Position: ({x_position}, {y_position}), Size: {size}")
    return {"shape": shape, "size": size, "position": (x_position, y_position), "color": color}

    # Fallback to return any object if conditions are too strict
    # This situation should rarely happen if the screen is large enough relative to the number of objects
    shape = np.random.choice(["circle", "square", "triangle"])
    color = tuple(np.random.randint(0, 255) for _ in range(3))
    return {"shape": shape, "size": size, "position": (x_position, y_position), "color": color}


def update_position(obj, speed, frame_height):
    x, y = obj["position"]
    y += speed  # Move object down the screen
    return {"shape": obj["shape"], "size": obj["size"], "position": (x, y), "color": obj["color"]}

def draw_objects(frame, objects):
    for obj in objects:
        position = obj["position"]
        size = obj["size"]
        color = obj["color"]
        alpha_value = 0.05

        # Create a blank image with the same dimensions as the frame

        # Draw the shapes on the overlay image
        if obj["shape"] == "circle":
            cv2.circle(frame, position, size, color, 2)
        elif obj["shape"] == "triangle":
            points = np.array([position,
                               (position[0] - size, position[1] + size),
                               (position[0] + size, position[1] + size)], np.int32)
            cv2.polylines(frame, [points], isClosed=True, color=color, thickness=2)

        # Blend the overlay with the original frame
        '''elif obj["shape"] == "square":
            top_left = (position[0] - size, position[1] - size)
            bottom_right = (position[0] + size, position[1] + size)
            cv2.rectangle(frame, top_left, bottom_right, color, -1)'''
