import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from finch_bt_connector import FinchBluetooth

# Constants
POSENET_MODEL_PATH = "posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite"
POSE_THRESHOLD = 0.1
THUMBS_UP_ANGLE_THRESHOLD = 60

def load_model():
    interpreter = tflite.Interpreter(model_path=POSENET_MODEL_PATH)
    interpreter.allocate_tensors()
    return interpreter

def process_frame(interpreter, frame):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = cv2.resize(frame, (257, 257))
    input_data = np.expand_dims(input_data, axis=0)
    input_data = input_data.astype(np.float32)

    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    heatmaps = interpreter.get_tensor(output_details[0]["index"])
    offsets = interpreter.get_tensor(output_details[1]["index"])

    return heatmaps, offsets

def thumbs_up_pose(heatmaps, offsets):
    left_wrist = 9
    right_wrist = 10
    left_thumb = 4
    right_thumb = 5

    for i in [left_wrist, right_wrist, left_thumb, right_thumb]:
        confidence = heatmaps[0, 0, 0, i]
        if confidence < POSE_THRESHOLD:
            return False

    left_wrist_y = heatmaps[0, 0, 0, left_wrist + 1]
    right_wrist_y = heatmaps[0, 0, 0, right_wrist + 1]
    left_thumb_y = heatmaps[0, 0, 0, left_thumb + 1]
    right_thumb_y = heatmaps[0, 0, 0, right_thumb + 1]

    left_angle = abs(left_thumb_y - left_wrist_y)
    right_angle = abs(right_thumb_y - right_wrist_y)

    return left_angle > THUMBS_UP_ANGLE_THRESHOLD and right_angle > THUMBS_UP_ANGLE_THRESHOLD

def main():
    finch = FinchBluetooth()
    interpreter = load_model()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror the frame
        heatmaps, offsets = process_frame(interpreter, frame)

        if thumbs_up_pose(heatmaps, offsets):
            print("Two thumbs up detected!")
            finch.set_motors(30, 30)

        else:
            finch.set_motors(0, 0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    finch.disconnect()

