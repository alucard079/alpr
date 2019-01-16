from openalpr import Alpr
import sys
import numpy as np
import cv2


alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")

if not alpr.is_loaded():
	print("Error loading OpenALPR")
	sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while(True):

	ret,frame = cap.read()
	results = alpr.recognize_ndarray(gray)

	print (results['results'])
	i = 0
	for plate in results['results']:
		i += 1
		print ("Plate #%d" % i)
		print ("   %12s %12s" % ("Plate", "Confidence"))
		for candidate in plate['candidates']:
                	prefix = "-"
                	if candidate['matches_template']:
                        	prefix = "*"
                	print ("  %s %12s%12f"%(prefix, candidate['plate'], candidate['confidence']))
                           
alpr.unload()
cap.release()
