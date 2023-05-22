from flask import Flask, render_template, Response
import cv2
#Initialize the Flask app
app = Flask(__name__)
 
# camera = cv2.VideoCapture("rtsp://admin:Kib#1234@192.168.1.1:8800/Streaming/live/ch00_0")
camera = cv2.VideoCapture("http://admin:Kib%25201234@192.168.1.1/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr=admin&pwd=Kib%25201234")

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame o

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
