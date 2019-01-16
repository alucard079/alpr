import numpy as np
import cv2
from openalpr import Alpr

alpr = Alpr("ph", "openalpr/runtime_data/config/ph.conf", "openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(12)
alpr.set_default_region("ph")


cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.109:554/cam/realmonitor?channel=1&subtype=1")
#to see what the output must be
#cap = cv2.VideoCapture("lp3.jpg")
#sample video
#cap = cv2.VideoCapture("numPlates.mpg")

while(True):    
    ret, frame = cap.read() 

    if ret:        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imwrite("img.jpg", frame)

        results = alpr.recognize_file("img.jpg")

        i = 0
        
        for plate in results['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"

                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))       
    else:
        break;

    

# When everything done, release the capture
cap.release()
alpr.unload()
cv2.destroyAllWindows()
