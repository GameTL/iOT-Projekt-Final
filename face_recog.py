# conda install -c conda-forge deepface
print("initializing...")
from deepface import DeepFace
import cv2
import time
import os


models = [
    "VGG-Face",
    "Facenet",
    "Facenet512",
    "OpenFace",
    "DeepFace",
    "DeepID",
    "ArcFace",
    "Dlib",
    "SFace",
]


# Camera Config
[X_RESOLUTION, Y_RESOLUTION, VIDEO_FPS] = [1280, 720, 30]
cap = cv2.VideoCapture(0)  # if mac then 1 if pi then 0
cap.set(3, X_RESOLUTION)
cap.set(4, Y_RESOLUTION)
cap.set(5, VIDEO_FPS)


def get_lastest_pic_name(previous=False):
    """ previous=False Get the lastest image number for saving

    previous=True will return the previous captured image """

    # Directory containing the image files
    directory = "img_database"

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out the image files and extract numbers
    image_numbers = [int(f.split(".")[0]) for f in files if f.endswith(".jpg")]

    # Determine the number for the new file
    if image_numbers:
        if previous:
            max_number = max(image_numbers)
            new_number = max_number - 1

        else:
            # Find the file with the highest number
            max_number = max(image_numbers)
            new_number = max_number + 1
    else:
        # Start with 1 if no JPG files are found
        new_number = 1

    return os.path.join(directory, f"{new_number}.jpg")


def take_picture(timer = 2):

    print("taking a take_picture")
    start = time.time()
    # Initialize the camera
    try:
        while cap.isOpened():
            time_count = time.time() - start
            count_down = timer - (time_count // 1)
            ret, frame = cap.read()

            # Print the countdown
            output_text = "Capturing in " + str(int(count_down))
            print(output_text)
            cv2.putText(
                img=frame,
                text=output_text,
                org=(10, int(cap.get(4)) - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 255, 0),
                thickness=2,
            )
            cv2.imshow("frame", frame)

            print(time_count)
            if time_count > timer:
                if ret:
                    print("Frame captured successfully")
                    # Display the captured frame
                    cv2.imshow("Captured Frame", frame)
                    saved_path = get_lastest_pic_name()

                    # Save the frame as an image file
                    cv2.imwrite(saved_path, frame)
                    print("Frame written to file")
                    break
                else:
                    print("Error: Can't capture a frame")
                    return False

            if cv2.waitKey(1) == ord("q"):
                cap.release()

        # time.sleep(2)
        cap.release()
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()
        quit()

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    print("saved at ", saved_path)

    return saved_path


def compare(target="img_database/1.jpg", input="", threshold=0.4, debug=False) -> bool:
    # >>> True == match
    # >>> False == not a match
    print(f"""Comparing:
    - {target=}
    - {input=}
    """)

    result = DeepFace.verify(
        img1_path=target,
        img2_path=input,
        model_name=models[3],
    )

    """ result = {
        "verified": False,
        "distance": 0.43280642428513993,
        "threshold": 0.3,
        "model": "Facenet512",
        "detector_backend": "opencv",
        "similarity_metric": "cosine",
        "facial_areas": {
            "img1": {"x": 518, "y": 252, "w": 320, "h": 320},
            "img2": {"x": 498, "y": 313, "w": 254, "h": 254},
        },
        "time": 66.93,
    }
"""
    if debug:
        print(f"{result=}")

    if result['distance'] < threshold:
        return True
    else:
        return False


if __name__ == "__main__":
    print("Ready...")
    # target = take_picture()
    # input = take_picture()
    # compare(target, input)
    compare_pic = take_picture()
    # x = compare("img_database/4.jpg", compare_pic, debug=True)
    x = compare(get_lastest_pic_name(previous=True), compare_pic,  threshold=0.6, debug=True)
    if x:
        print("SAME PERSON")
    else:
        print("NOT SAME PERSON")
    print()
