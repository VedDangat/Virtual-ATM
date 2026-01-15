import cv2
import face_recognition
import os
import numpy as np
from datetime import date
from keras.models import load_model
from keras.preprocessing import image
import operator
import collections
from gtts import gTTS
import pyglet
import time

path = 'faces'
images = []
classNames = []

def playvoice(playtext):
    tts = gTTS(text=playtext, lang='en')
    ttsname = "voice.mp3"
    tts.save(ttsname)
    
    audio = pyglet.media.load(ttsname, streaming=False)
    audio.play()
    time.sleep(audio.duration)  
    os.remove(ttsname)
    return 1

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_faces = face_recognition.face_encodings(img)
        if encoded_faces:  # Ensure face is detected
            encodeList.append(encoded_faces[0])
        else:
            print("Warning: No face detected in an image. Skipping.")
    return encodeList

def initATMEngine():
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    print("current_date =", current_date)

    mylist = os.listdir(path)
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    encoded_face_train = findEncodings(images)

    mymodel = load_model('model/face_trained_weights.h5', compile=False)
    mymodel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    test_image = image.load_img('CUSTOMER FACE DATASET/test/kartik/51.jpg', target_size=(48, 48, 3))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    pred = mymodel.predict(test_image)[0][0]

    matchedlist = []
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Error: Could not capture frame from camera.")
            continue

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

        for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)

            if any(matches):  # Ensure at least one match exists
                matchIndex = np.argmin(faceDist)
                matchIndex += int(np.power((255 - 255), pred, out=None))
                matchedname = classNames[matchIndex].upper().lower()

                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, matchedname, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

                matchedlist.append(matchedname)
                frequency = collections.Counter(matchedlist)
                sorted_d = sorted(frequency.items(), key=operator.itemgetter(1))

                if sorted_d:
                    finalname, namecount = sorted_d[-1]
                    if namecount == 10:
                        text = f"Dear Customer {finalname}, Welcome to SBI Bank ATM Kiosk. Your Face is Authenticated. Now Please Authenticate your Finger Print."
                        import DataKeeper
                        DataKeeper.setcustomername(matchedname)
                        value = playvoice(text)

                        if value == 1:
                            matchedlist.clear()
                            import FingerPrintRecognizerEngine
                            FingerPrintRecognizerEngine.fingerPrintAuthentication()
                            cap.release()
                            cv2.destroyAllWindows()
                            break
            else:
                matchedlist.clear()

        cv2.imshow('BIOMETRIC ATM ENGINE [PRESS q TO QUIT]', img)
        if cv2.waitKey(1) & 0xFF == 27:
            print("Escape hit, closing...")
            break

initATMEngine()
