import cv2
import mediapipe as mp
import time
import os
import sys
import gesture_utils

BEST_OF = 3 # Best of X rounds (odd number)

if BEST_OF % 2 == 0:
    print(f"[WARNING] 'BEST_OF' must be an odd number. Adjusting to {BEST_OF + 1}")
    BEST_OF += 1

WINS_NEEDED = (BEST_OF // 2) + 1

def access_webcam():
    model_path = "hand_landmarker.task"
    point_color = (200, 217, 66)
    connection_color = (33, 22, 147)
    score_color = (74, 29, 17)
    result_color = (50, 130, 36)
    os.environ["GLOG_minloglevel"] = "2"
    
    print("\n[INFO] Starting webcam...")
    print(f"[INFO] Best of {BEST_OF} match... First to {WINS_NEEDED} wins!")
    print("[INFO] Show your gesture and press 'SPACE' to play a round.")
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
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # 1280x720 (640x480 is default)

    player_score = 0
    computer_score = 0
    round_result_text = ""
    computer_gesture_text = ""

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int(time.time() * 1000)
            if timestamp_ms <= last_timestamp_ms:
                timestamp_ms = last_timestamp_ms + 1
            last_timestamp_ms = timestamp_ms

            hand_landmarker_result = landmarker.detect_for_video(mp_image, timestamp_ms)
            player_gesture = "Invalid"

            if hand_landmarker_result.hand_landmarks:
                for hand_landmarks in hand_landmarker_result.hand_landmarks:
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
            
            cv2.putText(frame, f"Gesture: {player_gesture}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, point_color, 2, cv2.LINE_AA)
            cv2.putText(frame, f"Score -> Player: {player_score} | Computer: {computer_score}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, score_color, 2, cv2.LINE_AA)
            cv2.putText(frame, "Press SPACE to lock move", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            if round_result_text:
                cv2.putText(frame, f"Computer: {computer_gesture_text} | Result: {round_result_text}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, result_color, 2, cv2.LINE_AA)

            cv2.imshow("Jo Ken Po - Gesture Game", frame)

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("q"):
                break
                
            elif key == ord(" ") and player_gesture in ["Rock", "Paper", "Scissors"]:
                computer_gesture_text = gesture_utils.computer_move()
                round_result_text = gesture_utils.decide_winner(player_gesture, computer_gesture_text)

                if round_result_text == "Player":
                    player_score += 1
                elif round_result_text == "Computer":
                    computer_score += 1

                if player_score == WINS_NEEDED or computer_score == WINS_NEEDED:
                    final_winner = "PLAYER" if player_score == WINS_NEEDED else "COMPUTER"
                    
                    cv2.putText(frame, f"MATCH OVER! {final_winner} WINS!", (50, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.imshow("Jo Ken Po - Gesture Game", frame)
                    
                    cv2.waitKey(3000) 
                    break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    access_webcam()