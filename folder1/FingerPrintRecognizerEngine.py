import numpy as np


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
import GUIstarter

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

def fingerPrintAuthentication():
    num_of_classes=3
    
    
        
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
    model.add(Dense(num_of_classes, activation='softmax'))
    model.load_weights('model/FP_model_CNN.weights.h5')
        
        
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
        
        
    cap = cv2.VideoCapture(3)
    x=50
    y=10
    h=450
    w=500
    
    fplist=[]
    while cap.isOpened():
        _,capimg=cap.read()
        min_HSV = np.array([0, 58, 30], dtype = "uint8")
        max_HSV = np.array([33, 255, 255], dtype = "uint8")
        imageHSV = cv2.cvtColor(capimg, cv2.COLOR_BGR2HSV)
        skinRegionHSV = cv2.inRange(imageHSV, min_HSV, max_HSV)
        skinHSV = cv2.bitwise_and(capimg, capimg, mask = skinRegionHSV)
        grayscaled = cv2.cvtColor(skinHSV, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(grayscaled,cv2.CV_64F,1,0,ksize=5)
        cv2.rectangle(sobelx,(x,y),(x+w,y+h),(255,255,255),3)
        cv2.imshow('Finger print Authenticatione( Press esc to quit)',sobelx)
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
      #  print("index : ",maxindex)
        fingperprintname=fprint_dict[maxindex]
       # print("FP  : ",fingperprintname)
       
        cv2.putText(sobelx, fingperprintname, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        fplist.append(fingperprintname)
        frequency = collections.Counter(fplist)
        fpfreq=dict(frequency)
        sorted_d = sorted(fpfreq.items(), key=operator.itemgetter(1))
        print('Dictionary in ascending order by value : ',sorted_d)
        index=len(sorted_d)-1
        mxvaluefp=sorted_d[index]
        # print("Matched ",mxvaluegesture)
        finalname=mxvaluefp[0]
        fpcount=mxvaluefp[1]
        print("finalname ",finalname)
        print("fpcount ",fpcount)
        count=int(fpcount)
              
        cv2.imshow('Fingerprint Authentication Process',sobelx)
        if(count>=50):
            print("Detected FP Name is  ",finalname)
            fplist.clear()
            if(finalname !="blank"):
                    import DataKeeper
                    if(finalname==DataKeeper.customername):
                        text="Dear "+DataKeeper.customername+" Your Face and Finger prints are identified successfully. Now You can Perform your Transactions"
                        value=playvoice(text)
                        fplist.clear()
                        GUIstarter.startGUI(finalname)
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                       # break
                   
                    else:
                        text="Dear "+DataKeeper.customername+" Your Finger print are not Authenticated. Please Try again"
                        value=playvoice(text)
                        if(value==1):
                            fplist.clear()
        
        if cv2.waitKey(1)==ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
    
                
                  
                
            
            
      
        