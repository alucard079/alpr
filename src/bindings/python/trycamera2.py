from openalpr import Alpr
import sys
import numpy as np
import cv2


alpr= Alpr("eu",  "openalpr/runtime_data/config/eu.conf", "openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")


cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.109:554/cam/realmonitor?channel=1&subtype=0")
ret, frame = cap.read()
ret,enc = cv2.imencode("*.bmp", frame)
while(True):

    ret,frame = cap.read()
    cv2.imshow('frame', frame)
    # cv.waitKey(1)
    # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    results = alpr.recognize_array(bytes(bytearray(enc)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

   # results = alpr.recognize_ndarray(gray)


    print results['results']
    i = 0
    for plate in results['results']:
        i += 1
        print "Plate #%d" % i
        print "   %12s %12s" % ("Plate", "Confidence")
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
                print "  %s %12s%12f"%(prefix, candidate['plate'], candidate['confidence'])
                           
alpr.unload()
cap.release()      
