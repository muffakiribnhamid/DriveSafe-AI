import cv2
import dlib
import scipy.spatial
from alarm import play_alarm  # You must create alarm.py separately

# Calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    A = scipy.spatial.distance.euclidean(eye[1], eye[5])
    B = scipy.spatial.distance.euclidean(eye[2], eye[4])
    C = scipy.spatial.distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Drowsiness detection logic
def detect_drowsiness():
    EAR_THRESHOLD = 0.25
    EAR_CONSEC_FRAMES = 20
    COUNTER = 0

    print("📦 Loading face detector and predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = (42, 48)
    (rStart, rEnd) = (36, 42)

    print("🎥 Accessing webcam...")
    cap = None
    for idx in range(3):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            print(f"✅ Webcam opened at index {idx}.")
            break
        else:
            cap.release()
            cap = None
    if cap is None or not cap.isOpened():
        print("❌ Cannot access any webcam (tried 0, 1, 2). Check permissions or hardware.")
        return False

    import time
    print("⏳ Warming up camera...")
    for i in range(10):
        ret, frame = cap.read()
        time.sleep(0.05)
    print("✅ Webcam initialized. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            if ear < EAR_THRESHOLD:
                COUNTER += 1
                if COUNTER >= EAR_CONSEC_FRAMES:
                    print("😴 Drowsiness Detected!")
                    play_alarm()
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
            else:
                COUNTER = 0

        cv2.imshow("Driver Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

if __name__ == "__main__":
    detect_drowsiness()
