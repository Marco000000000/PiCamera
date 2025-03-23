import time
import datetime
from Prediction import *
from Notification import *
from picamera2 import Picamera2, Preview
import io
import threading
from flask import Flask, Response , send_file ,render_template
import os
picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)
predicter=predictor()
#full_res=picam.sensor_resolution

#half_res=tuple([dim // 2 for dim in picam.sensor_resolution])

#configure full format highest res mode RGB 
#still_config=picam.create_still_configuration(main={"size":(1296, 972),"format":"RGB888"}, raw={"size":full_res})

#configure full format half resolution binned mode BGR
#still_config=picam.create_still_configuration(main={"size":(1296, 972),"format":"BGR888"}, raw={"size":half_res})

#picam.configure(still_config)
#picam.start_preview(Preview.QTGL)

app = Flask(__name__)
semaforo="verde"

picam.start()
picam.capture_file("test-python.jpg")
data = io.BytesIO()
picam.capture_file(data, format='jpeg')
def generate_frames():
    while True:
        stream = io.BytesIO()
        picam.capture_file(stream, format='jpeg')
        stream.seek(0)
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
        stream.seek(0)
        stream.truncate()
        time.sleep(0.02)
        
@app.route("/lastCaptures")
def getNames():
	search_dir = "Capture"
	#os.chdir(search_dir)
	#print(os.listdir(search_dir))
	files =  os.listdir(search_dir)
	files = [os.path.join(search_dir, f) for f in files] # add path to each file
	#print(files)
	files.sort(key=lambda x: os.path.getmtime(x))
	files.reverse()
	return files[:12]
	
@app.route("/semaforo")
def getColor():
    global semaforo
    return semaforo
    
@app.route('/Capture/<fileName>')
def get_image(fileName):
	print(fileName)
	return send_file("Capture/"+fileName,mimetype="image/jpeg")
	
@app.route("/")
def home():
	return render_template("index.html")
	
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
def loopFunc():
    array = picam.capture_array("main")
    global semaforo
    print(array.shape)
    while True:
        
        array = picam.capture_array("main")
        prediction,validity=predicter.predict(array)
        if validity>0.8:
            semaforo=prediction
            if prediction=="rosso":
                picam.capture_file("Capture/"+str(datetime.datetime.now())+".jpg")
                print("Predict true")
                notify()
        elif semaforo=="rosso":
            semaforo="giallo"
        time.sleep(60)    
        
        
if __name__ == '__main__':
    thread= threading.Thread(target=loopFunc)
    thread.start()
    app.run(host='0.0.0.0', port=80, threaded=True)

    


    picam.close()                                                                                                                                                                                                                                                                                                    
