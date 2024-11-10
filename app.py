from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import subprocess
import cv2
import tkinter
from tkinter import messagebox
#import atexit
#import os
import logging
#import pyautogui as pag

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, transports=['websocket'])

#To hide the main tkinter window
tkinter.Tk().withdraw()

camera = None
camera_on = False

logging.basicConfig(level=logging.DEBUG)

def gen_frames():
    global camera
    camera = cv2.VideoCapture(0)
    while camera_on:
        success, frame = camera.read()
        if not success:
            logging.error("FAILURE")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')  #Main section
def index():
    return render_template('ind.html')

@app.route('/run_script', methods=['POST'])  #To get the data from user while data creation
def run_script():
    id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    
    # Run the Python script with the provided inputs
    subprocess.run(['python', 'create_data.py', id, name, age])

    #Message box
    messagebox.showinfo("SUCCESS", "Data added successfully")
    return 'Script executed successfully!'

@app.route('/train', methods=['POST']) #To train the dataset
def train():
    try:
        subprocess.run(['python', 'train.py'])

        return 'Training completed successfully!'
    except Exception as e:
        return f'Error during training: {str(e)}'
    
@app.route('/detect', methods=['POST']) #To train the dataset
def detect():
    try:
        subprocess.run(['python', 'detect.py'])

        return 'Detection completed successfully!'
    except Exception as e:
        return f'Error during detection: {str(e)}'

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    # if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False: #WERKZEUG_RUN_MAIN
    #     camera = cv2.VideoCapture(0)
    # app.run(debug=True)
    socketio.start_background_task(gen_frames)
    socketio.run(app)
