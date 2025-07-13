import scipy.spatial as spatial
import cv2
import dlib
from imutils import face_utils
import numpy as np


# This function will calculate the Eye Aspect Ratio (EAR) (Ankh kitne khuli hai)
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def eye_start_monitoring(threshold=0.25, consecutive_frames=20):
    #Threshold: EAR value below which we consider eyes are closed
    #Consecutive_frames: Number of consecutive frames with EAR below threshold before we consider eyes are closed
    COUNTER = 0

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    #ye index deta hai :  range for eye landmarks from the 68-point facial model.

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converted to gray for faster processing
        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)


            left_eye = shape[lStart:lEnd]
            right_eye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)
            ear = (leftEAR + rightEAR) / 2.0


            #main work : if eyes are closed

            if ear < threshold:
                COUNTER += 1
                if COUNTER >= consecutive_frames:
                    print("Drowsiness Alert")
                    cv2.putText(frame, "Drowsiness Alert", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "Wake up!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    COUNTER = 0
            else:
                COUNTER = 0

        cv2.imshow("Driver Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

            









    