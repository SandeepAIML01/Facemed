import cv2
import numpy as np
import os
import sqlite3
import threading
from fpdf import FPDF
import pyttsx3       #to setup audio
from fpdf import FPDF   
from colorama import Fore, Back, Style #print text in colors

#setup engine to get vocal
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#function for speaking
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


facedetect=cv2.CascadeClassifier("C:/AI/face detection/haarcascade_frontalface_default.xml")
cam=cv2.VideoCapture(0)

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingdata.yml")

def getprofile(id):
    conn=sqlite3.connect("students.db")
    cursor=conn.execute("SELECT * FROM students WHERE id=?",(id,))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

# Function to generate PDF report
def generate_pdf(profile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 20, txt="ID, NAME    , AGE", ln=1, align='C')
    if profile:
        data = f"{profile[0]}, {profile[1]}, {profile[2]}"
        pdf.cell(200, 20, txt=data, ln=2, align='C')
    else:
        pdf.cell(200, 20, txt="No profile data available", ln=2, align='C')
    name = f'{profile[1]}.pdf'
    pdf.output(name)

while(True):
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id,conf=recognizer.predict(gray[y:y+h,x:x+w])
        profile=getprofile(id)
       # print(profile)
        if(id!=None):
            cv2.putText(img,"Name:" +str(profile[1]), (x,y+h+20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,127),2)
            cv2.putText(img, "Age:" + str(profile[2]), (x, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127), 2)

            ado = f'Match found!, ID number {str(profile[0])} with name {str(profile[1])} of {str(profile[2])} years old.'
            threading.Thread(target=speak, args=(ado,)).start()
            generate_pdf(profile)
            #threading.Thread(target=generate_pdf, args=(profile,)).start()
            
    cv2.imshow("FACE",img);
    if(cv2.waitKey(1)==ord('q')):                    # q - exit
        break;

cam.release()
cv2.destroyAllWindows()
