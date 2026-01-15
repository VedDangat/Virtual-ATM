import numpy as np
import cv2
import os


typename="train"
name="kartik"

datasetpath1="FINGER DATASET FP"
if not os.path.exists(datasetpath1):
    os.makedirs(datasetpath1)         
    
    
typedataset1=datasetpath1+"//"+typename
if not os.path.exists(typedataset1):
    os.makedirs(typedataset1)          
        

fingerimgpath1=typedataset1+"//"+name
if not os.path.exists(fingerimgpath1):
    os.makedirs(fingerimgpath1)   
    
 #########################################   
datasetpath2="FINGER DATASET FP"
if not os.path.exists(datasetpath2):
    os.makedirs(datasetpath2)         
    
    
typedataset2=datasetpath2+"//"+typename
if not os.path.exists(typedataset2):
    os.makedirs(typedataset2)          
        

fingerimgpath2=typedataset2+"//"+name
if not os.path.exists(fingerimgpath2):
    os.makedirs(fingerimgpath2)   
        
    
    
    
      
cap=cv2.VideoCapture(2)
imgeno=1
x=50
y=10
h=450
w=500
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
    cv2.imshow('Capture Image( Press q to quit)',sobelx)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
    # SPACE pressed
        filename=str(imgeno)
        dim = (128, 128)
        img1 = capimg[y:y+h, x:x+w]
        newfilepath1=fingerimgpath1+"//"+filename+".jpg"
        img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
        img_YCrCb = cv2.cvtColor(img1, cv2.COLOR_BGR2YCrCb)
        YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
        YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
        YCrCb_result = cv2.bitwise_not(YCrCb_mask)
        cv2.imwrite(newfilepath1,YCrCb_result)
       
        
        dim = (128, 128)
        img2 = sobelx[y:y+h, x:x+w]
        newfilepath2=fingerimgpath2+"//"+filename+".jpg"
        finp = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(newfilepath2,finp)
        print(newfilepath2)
        imgeno=imgeno+1                     
        print("Stored image no ",imgeno)
      
                
          


cap.release()
cv2.destroyAllWindows()