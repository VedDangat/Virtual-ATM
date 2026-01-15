import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import operator
import collections
from keras.models import load_model
import time
from mutagen.mp3 import MP3
from gtts import gTTS
import pyglet
import datetime
from datetime import datetime
import mysql.connector
import AttendanceInserter
def playvoice(playtext):
    #fetch project name
   tts = gTTS(text=playtext, lang='en')
   ttsname=("voice.mp3")
   
   tts.save(ttsname)
   audio = MP3("voice.mp3")
   val= audio.info.length
  
   x=int(val)+1
   print(" audio length",x)
   music = pyglet.media.load(ttsname, streaming = False)
   music.play()
   os.remove(ttsname)
   time.sleep(x)
   return 1
def startFPEngine(sem,subject,teacher):
    
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(96,96,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
        
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
        
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='softmax'))
    model.load_weights('model_CNN.h5')
        
        
            # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)
       
    
    path="FINGER DATASET FP/train"
    dir_list = os.listdir(path)
    fprint_dict={}
    i=0
    for x in dir_list:
        foldername=x
        fprint_dict[i]=foldername
        i=i+1
        
        
    cap = cv2.VideoCapture(1)
    x=50
    y=10
    h=450
    w=500
    
    
    while cap.isOpened():
        _,capimg=cap.read()
        # min_HSV = np.array([0, 58, 30], dtype = "uint8")
        # max_HSV = np.array([33, 255, 255], dtype = "uint8")
        # imageHSV = cv2.cvtColor(capimg, cv2.COLOR_BGR2HSV)
        # skinRegionHSV = cv2.inRange(imageHSV, min_HSV, max_HSV)
        # skinHSV = cv2.bitwise_and(capimg, capimg, mask = skinRegionHSV)
        # grayscaled = cv2.cvtColor(skinHSV, cv2.COLOR_BGR2GRAY)
        # sobelx = cv2.Sobel(grayscaled,cv2.CV_64F,1,0,ksize=5)
        # cv2.rectangle(sobelx,(x,y),(x+w,y+h),(255,255,255),3)
        # cv2.imshow('Finger print Authenticatione( Press esc to quit)',sobelx)
        dim = (96, 96)
        img1 = capimg[y:y+h, x:x+w]
        img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
        img_YCrCb = cv2.cvtColor(img1, cv2.COLOR_BGR2YCrCb)
        gaussian_blur = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
        gaussian_blur = cv2.morphologyEx(gaussian_blur, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
        gaussian_filter = cv2.bitwise_not(gaussian_blur)
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(gaussian_filter, (96, 96)), -1), 0)
        prediction = model.predict(cropped_img)
        maxindex = int(np.argmax(prediction))
        print("index : ",maxindex)
        
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            fingperprintname=fprint_dict[maxindex]
            print("FP  : ",fingperprintname)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            flag=AttendanceInserter.isInserted(teacher,sem,subject,fingperprintname,dt_string)
            if(flag==True):
                
                text=fingperprintname+" Your Attendance has been Registered Successfully,  You may go to class now "
                playvoice(text)
               
        
       
        
    cap.release()
    cv2.destroyAllWindows()
    
    
                
                  
                
            
            
      
        