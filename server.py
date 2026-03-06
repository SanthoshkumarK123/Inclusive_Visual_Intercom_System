from flask import Flask, render_template_string
import cv2
import os
import threading
import time

app = Flask(__name__)

IMAGE_PATH = "static/captured.jpg"
capture_running = False

if not os.path.exists("static"):
    os.makedirs("static")

def capture_loop():
    global capture_running
    camera = cv2.VideoCapture(0)

    while capture_running:
        ret, frame = camera.read()
        if ret:
            cv2.imwrite(IMAGE_PATH, frame)
        time.sleep(5)

    camera.release()

@app.route('/')
def home():
    return render_template_string('''
    <html>
    <head>
        <title>Inclusive Visual Intercom</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h2>Live Image (Refresh every 5 sec)</h2>
        <img src="/static/captured.jpg" width="500">
    </body>
    </html>
    ''')

@app.route('/start')
def start_capture():
    global capture_running
    if not capture_running:
        capture_running = True
        threading.Thread(target=capture_loop).start()
    return "Capture Started"

@app.route('/stop')
def stop_capture():
    global capture_running
    capture_running = False
    return "Capture Stopped"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)