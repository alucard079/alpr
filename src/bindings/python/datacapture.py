from subprocess import Popen, PIPE
import json
from pprint import pprint
import numpy as np
import cv2
import threading
from thread import start_new_thread


#scan_plates()
cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.1.109:554/cam/realmonitor?channel=1&subtype=0')

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line

def process_output(output):

	if "connecting" in output:
		print("Connecting to video stream...")
	elif "connected" in output:
		print("Connected to video stream. Checking plates.")
	else:
		parse_json_data(output)

def parse_json_data(output):
	jsondata = json.loads(output)
	if jsondata["results"]:
		for data in jsondata["results"]:
			print(data)

#def process_results(results):
	
def disp_cam():
	while(cap.isOpened()):
	    ret, frame = cap.read()
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	cap.release()
	cv2.destroyAllWindows()

def scan_plates():
	for path in run("alpr -j -n 1 rtsp://admin:admin123@192.168.1.109:554/cam/realmonitor?channel=1&subtype=0/"):
		#print(path.decode("utf-8"))
		process_output(path.decode("utf-8"))

if __name__ == "__main__":
	t1 = threading.Thread(target=scan_plates)
	t2 = threading.Thread(target=disp_cam)
	t1.daemon = False
	t2.daemon = False
	t1.start()
	t2.start()
	#print("Hello World")
