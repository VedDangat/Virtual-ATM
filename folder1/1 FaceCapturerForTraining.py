import cv2
import os


typename="train"
customer_name="rohit"

datasetpath="CUSTOMER FACE DATASET" 
if not  os.path.exists(datasetpath):
    os.makedirs(datasetpath)         
    

typedataset=datasetpath+"//"+typename
if not os.path.exists(typedataset):
    os.makedirs(typedataset)          
        
customerdatasetpath=datasetpath+"//"+typename+"//"+customer_name
if not os.path.exists(customerdatasetpath):
    os.makedirs(customerdatasetpath) 
    
 
cap=cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
imageno=0
while cap.isOpened():
    _,img=cap.read()
    face=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=4)
    k = cv2.waitKey(1)
    for(x,y,w,h) in face:
       cropimage = img[y:y+h, x:x+w]
 
       cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
       filename=str(imageno)   
       newfilepath=customerdatasetpath+"//"+filename+".jpg"
       dim = (48, 48)
       resized = cv2.resize(cropimage, dim, interpolation = cv2.INTER_AREA)
       if k%256 == 32:
           cv2.imwrite(newfilepath,resized)
           print("Image Stored at ",newfilepath)
           imageno=imageno+1  
            
          
    cv2.imshow('CAPTURE FACE ( Press ESC to quit)',img)
   
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    
cap.release()
cv2.destroyAllWindows()