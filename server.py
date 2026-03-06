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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inclusive Visual Intercom</title>

        <meta http-equiv="refresh" content="5">

        <style>
            body{
                font-family: Arial, sans-serif;
                background-color:#f4f6f9;
                text-align:center;
                margin:0;
                padding:0;
            }

            header{
                background:#2c3e50;
                color:white;
                padding:20px;
                font-size:28px;
                font-weight:bold;
            }

            .container{
                margin-top:40px;
            }

            .camera-box{
                display:inline-block;
                background:white;
                padding:20px;
                border-radius:10px;
                box-shadow:0px 4px 15px rgba(0,0,0,0.2);
            }

            img{
                width:640px;
                border-radius:8px;
            }

            .status{
                margin-top:15px;
                font-size:18px;
                color:#27ae60;
                font-weight:bold;
            }

            footer{
                margin-top:40px;
                padding:15px;
                background:#2c3e50;
                color:white;
                font-size:14px;
            }

        </style>
    </head>

    <body>

        <header>
            Inclusive Visual Intercom System
        </header>

        <div class="container">

            <div class="camera-box">

                <h2>Live Camera Feed</h2>

                <img src="/static/captured.jpg">

                <div class="status">
                    Refreshing every 5 seconds
                </div>

            </div>

        </div>

        <footer>
            ESP32 Based Internal Communication System
        </footer>

    </body>
    </html>
    ''')

call_status = "IDLE"

@app.route('/start')
def start_capture():
    global capture_running, call_status
    call_status = "ACTIVE"
    if not capture_running:
        capture_running = True
        threading.Thread(target=capture_loop).start()
    return "STARTED"

@app.route('/stop')
def stop_capture():
    global capture_running, call_status
    capture_running = False
    call_status = "ENDED"
    return "STOPPED"

@app.route('/status')
def status():
    return call_status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)