import cv2
import numpy as np

cap = cv2.VideoCapture("vid_2.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
print('FPS is: ' + str(fps))

while 1:
	# Captures the live stream frame-by-frame
	ret, frame = cap.read()
	# Converts images from BGR to HSV
	try:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	except:
		print('The Video Feed has been ended\nHence Exiting')
		break
	
	lower_green = np.array([66, 100, 200])
	upper_green = np.array([75, 255, 255])
	
	mask = cv2.inRange(hsv, lower_green, upper_green)
	kernel = np.ones((5, 5), "uint8")
	green = cv2.dilate(mask, kernel)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	# res = cv2.bitwise_and(frame, frame, mask=green)
	
	# Finding contours
	(ret, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		Area = cv2.contourArea(contour)
		if Area > 300:
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (200, 0, 75), 2)
			cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (200, 0, 75))
		
		cv2.imshow('IMG', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
