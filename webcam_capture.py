import cv2

def access_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    print("Camera activated. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not grab a frame from the camera.")
            break

        cv2.imshow('Live Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Ending capture...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    access_webcam()