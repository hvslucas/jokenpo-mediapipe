import random

def count_fingers(hand_landmarks):
    raised_fingers = 0
    tips = [8, 12, 16, 20]

    for tip in tips:
        if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
            raised_fingers += 1

    # thumb
    if hand_landmarks[4].x < hand_landmarks[3].x:
        raised_fingers += 1

    return raised_fingers

def map_gesture(fingers):
    if fingers == 0:
        return "Rock"
    elif fingers == 2:
        return "Scissors"
    elif fingers == 5:
        return "Paper"
    else:
        return "Invalid"