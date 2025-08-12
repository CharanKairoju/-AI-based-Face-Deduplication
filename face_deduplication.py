import cv2
import os
import face_recognition
import numpy as np
from scipy.spatial import distance as dist

IMAGE_FOLDER = "dataset"  
DEDUP_FOLDER = "deduplicated"  
SIMILARITY_THRESHOLD = 0.6  
EYE_AR_THRESH = 0.2  
EYE_AR_CONSEC_FRAMES = 3  

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear

def deduplicate_faces():
    if not os.path.exists(DEDUP_FOLDER):
        os.makedirs(DEDUP_FOLDER)

    encodings_list = []
    processed_images = []

    for img_name in os.listdir(IMAGE_FOLDER):
        img_path = os.path.join(IMAGE_FOLDER, img_name)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            print(f"No face found in {img_name}")
            continue

        encoding = encodings[0]
        is_duplicate = False

        for existing_encoding in encodings_list:
            distance = face_recognition.face_distance([existing_encoding], encoding)[0]
            if distance < SIMILARITY_THRESHOLD:
                print(f"Duplicate found: {img_name}")
                is_duplicate = True
                break

        if not is_duplicate:
            encodings_list.append(encoding)
            processed_images.append(img_path)
            output_path = os.path.join(DEDUP_FOLDER, img_name)
            cv2.imwrite(output_path, cv2.imread(img_path))

    print(f"\nDeduplication complete. {len(processed_images)} unique faces saved in '{DEDUP_FOLDER}'.")

def liveness_check():
    print("\n[INFO] Starting liveness check... Press 'q' to quit.")

    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    cap = cv2.VideoCapture(0)
    blink_counter = 0
    total_blinks = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) >= 2:
                blink_counter += 1
            else:
                if blink_counter >= EYE_AR_CONSEC_FRAMES:
                    total_blinks += 1
                    print(f"[INFO] Blink detected! Total blinks: {total_blinks}")
                blink_counter = 0

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Liveness Check", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[INFO] Liveness check complete. Total blinks detected: {total_blinks}")

if __name__ == "__main__":
    print("Step 1: Deduplicating faces...")
    deduplicate_faces()
    print("\nStep 2: Performing liveness check...")
    liveness_check()
