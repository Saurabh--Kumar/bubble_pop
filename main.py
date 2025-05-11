import cv2
import time
from video_capture import setup_video_capture, display_frame
from hand_detection import setup_hand_detection
from gameplay import generate_object, update_position, draw_objects
from screeninfo import get_monitors


def update_objects_and_collisions(objects, fists, speed, frame_height, health_decrement, score, health):
    new_objects = []

    for obj in objects:
        updated_obj = update_position(obj, speed, frame_height)
        if is_hit_by_fist(updated_obj, fists):
            score += 1
            continue  # Object is "hit" and disappears

        if object_fell_through(updated_obj, frame_height):
                health -= health_decrement
        else:
            new_objects.append(updated_obj)

    return new_objects, score, health


def is_hit_by_fist(updated_obj, fists):
    obj_x, obj_y = updated_obj["position"]
    obj_size = updated_obj["size"]

    return any((obj_x - obj_size <= fist[0] <= obj_x + obj_size and
                obj_y - obj_size <= fist[1] <= obj_y + obj_size) for fist in fists)


def object_fell_through(updated_obj, frame_height):
    return updated_obj["position"][1] >= frame_height


def get_screen_resolution():
    for monitor in get_monitors():
        return monitor.width, monitor.height


def initialize_game_state(screen_width):
    max_objects = 5
    objects = [generate_object(screen_width, []) for _ in range(max_objects)]
    score = 0
    health = 100
    return objects, score, health


def setup_camera(screen_width, screen_height):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    return cap


def run_pre_game_countdown(cap, duration=10):
    start_time = time.time()
    while time.time() - start_time < duration:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        elapsed_time = int(time.time() - start_time)
        countdown_time = duration - elapsed_time

        frame_height, frame_width = frame.shape[:2]
        cv2.putText(frame, f'Game starts in: {countdown_time}', (frame_width // 2 - 150, frame_height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        display_frame(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            return False
    return True


def process_frame(frame, hands):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    fists = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_landmark = hand_landmarks.landmark[0]
            frame_height, frame_width = frame.shape[:2]
            wrist_x = int(wrist_landmark.x * frame_width)
            wrist_y = int(wrist_landmark.y * frame_height)
            fists.append((wrist_x, wrist_y))
            cv2.circle(frame, (wrist_x, wrist_y), 10, (0, 255, 0), -1)

    return fists


def display_game_status(frame, score, health):
    cv2.rectangle(frame, (10, 50), (210, 70), (0, 0, 0), -1)  # Background box
    cv2.rectangle(frame, (10, 50), (10 + int(2 * health), 70), (0, 255, 0), -1)  # Health bar
    cv2.putText(frame, f'Score: {score}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


def check_game_over(frame, health):
    return health <= 0


def game_loop():
    screen_width, screen_height = get_screen_resolution()
    cap = setup_camera(screen_width, screen_height)
    hands = setup_hand_detection()
    objects, score, health = initialize_game_state(screen_width)
    if not objects:
        objects = [generate_object(screen_width, objects)]
    speed = 7
    health_decrement = 10

    if not run_pre_game_countdown(cap):
        cap.release()
        cv2.destroyAllWindows()
        return

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)

            fists = process_frame(frame, hands)

            objects, score, health = update_objects_and_collisions(
                objects, fists, speed, screen_height, health_decrement, score, health
            )

            if not objects:
                objects = [generate_object(screen_width, []) for _ in range(5)]

            display_game_status(frame, score, health)

            draw_objects(frame, objects)

            if check_game_over(frame, health):
                frame_height, frame_width = frame.shape[:2]
                cv2.putText(frame, "Game Over!", (frame_width // 2 - 100, frame_height // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4, cv2.LINE_AA)
                display_frame(frame)
                cv2.waitKey(3000)  # Display game over message for 3 seconds
                break

            display_frame(frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    game_loop()
