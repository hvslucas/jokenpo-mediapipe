import cv2
import mediapipe as mp
import time
import os
import sys
import gesture_utils

def access_webcam():
    model_path = "hand_landmarker.task"
    point_color = (200, 217, 66)
    connection_color = (33, 22, 147)
    os.environ["GLOG_minloglevel"] = "2"
    print("\n[INFO] Starting webcam...")
    print("[INFO] Press 'q' to quit the application.\n")
    
    if not os.path.exists(model_path):
        print(f"\n[ERROR] Model '{model_path}' not found! Please check the documentation to download\n")
        sys.exit(1)

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1
    )

    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
    ]

    cap = cv2.VideoCapture(0)
    last_timestamp_ms = 0

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int(time.time() * 1000)
            if timestamp_ms <= last_timestamp_ms:
                timestamp_ms = last_timestamp_ms + 1
            last_timestamp_ms = timestamp_ms

            hand_landmarker_result = landmarker.detect_for_video(mp_image, timestamp_ms)

            if hand_landmarker_result.hand_landmarks:
                for hand_landmarks in hand_landmarker_result.hand_landmarks:
                    h, w, _ = frame.shape
                    points = []

                    for landmark in hand_landmarks:
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        points.append((cx, cy))
                        cv2.circle(frame, (cx, cy), 4, point_color, -1)

                    for connection in HAND_CONNECTIONS:
                        pt1 = points[connection[0]]
                        pt2 = points[connection[1]]
                        cv2.line(frame, pt1, pt2, connection_color, 2)

                    fingers = gesture_utils.count_fingers(hand_landmarks)
                    player_gesture = gesture_utils.map_gesture(fingers)

                    cv2.putText(frame, f"Gesture: {player_gesture}", (10, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow("Hand Tracking - Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    access_webcam()
