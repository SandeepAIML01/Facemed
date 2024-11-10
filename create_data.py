import cv2                 #opencv camera
import numpy as np         #numpy array
import sqlite3             #sqlite is database
import sys

faceDetect=cv2.CascadeClassifier('C:/AI/face detection/haarcascade_frontalface_default.xml');   #to detect the faces in camera
cam=cv2.VideoCapture(0)        #0 is for web camera

def insertorupdate(Id,Name,age):               #function is for sqlite database
    conn=sqlite3.connect("students.db")         #connect database
    cmd="SELECT * FROM students WHERE ID="+str(Id)
    cursor=conn.execute(cmd)             #cursor to execute statement
    isRecordExist=0              #assume there is no record in our table
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):                            #if there is a record exist in our table
        conn.execute("UPDATE students SET Name=? WHERE Id=?",(Name,Id,))
        conn.execute("UPDATE students SET age=? WHERE Id=?", (age, Id,))
    else:                                #if there is no record exist we insert the values
        conn.execute("INSERT INTO students (Id,Name,age) values(?,?,?)",(Id,Name,age))

    conn.commit()
    conn.close()

#insert user defined values into table

Id=sys.arg #input('Enter User Id:')
Name=sys.argv[2] #input('Enter User Name:')
age=sys.argv[3] #input('Enter User Age:')

insertorupdate(Id,Name,age)

#detect face in web camera coding

sampleNum=0;              #assume ther is no samples in dataset
while(True):
    ret,img=cam.read();                    #OPEN CAMERA
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)             # IMAGE CONVERT INTO BGRGRAY COLOR
    faces=faceDetect.detectMultiScale(gray,1.3,5)            #scale faces
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;              #if face is detected incremnets
        cv2.imwrite("dataset/user."+str(Id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)                     #delay time
    cv2.imshow("Face",img)                 #show faces detected in web camera
    cv2.waitKey(1);
    if(sampleNum>35):                 #if the dataset is > 25 break
        break;

cam.release()
cv2.destroyAllWindows()                    #quit

