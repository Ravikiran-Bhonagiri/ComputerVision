import cv2
import mediapipe as mp
import time


class FaceMeshDetector:
    def __init__(self, static_mode=False, max_faces=2, min_detection_conf=0.5, min_tracking_conf=0.5):
        self.static_mode = static_mode
        self.max_faces = max_faces
        self.min_detection_conf = min_detection_conf
        self.min_tracking_conf = min_tracking_conf

        # Initialize MediaPipe Face Mesh and drawing utilities
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=self.static_mode,
            max_num_faces=self.max_faces,
            min_detection_confidence=self.min_detection_conf,
            min_tracking_confidence=self.min_tracking_conf,
        )
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=2)

    def find_face_mesh(self, img, draw=True):
        # Convert the image to RGB format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        faces = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                face = []
                for id, lm in enumerate(face_landmarks.landmark):
                    h, w, _ = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    face.append([x, y])

                if draw:
                    self.mp_draw.draw_landmarks(
                        img, face_landmarks, self.mp_face_mesh.FACE_CONNECTIONS, self.draw_spec, self.draw_spec
                    )

                faces.append(face)

        return img, faces


def main():
    cap = cv2.VideoCapture("Videos/1.mp4")
    prev_time = 0
    detector = FaceMeshDetector(max_faces=2)

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("End of video or cannot read the video stream.")
            break

        img, faces = detector.find_face_mesh(img)

        if faces:
            print(f"Face landmarks (first face): {faces[0]}")

        # Calculate and display FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time - prev_time > 0 else 0
        prev_time = curr_time

        cv2.putText(img, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Face Mesh", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
