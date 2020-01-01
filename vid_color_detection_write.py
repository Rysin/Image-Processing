import cv2
import numpy as np

'''
Here I am going to write the output into a video file, let's see!!
'''
# blue: 110,50,50; 130,255,255
# Yellow: 22, 60, 200; 60,255,255
# Red: 170, 100, 0; 180, 255, 255
# Green: 80,100,200; 90,255,255

cap = cv2.VideoCapture('vid_3.mp4')
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
# Define the codec and create VideoWriter object, Taking original size of the video
out = cv2.VideoWriter('output.avi', fourcc=fourcc, fps=20, frameSize=(1920, 1080))

# This drives the program into an infinite loop.
while (1):
	# Captures the live stream frame-by-frame
	ret, frame = cap.read()
	# Converts images from BGR to HSV
	try:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	except:
		print('The Video Feed has been ended\nHence Exiting')
		break
	
	lower_blue = np.array([80, 100, 200])
	upper_blue = np.array([90, 255, 255])
	
	# Here we are defining range of bluecolor in HSV
	# This creates a mask of blue coloured
	# objects found in the frame.
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	
	# The bitwise and of the frame and mask is done so
	# that only the blue coloured objects are highlighted
	# and stored in res
	res = cv2.bitwise_and(frame, frame, mask=mask)
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()
