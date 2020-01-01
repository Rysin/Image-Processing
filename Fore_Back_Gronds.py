import cv2


# cap = cv2.VideoCapture('vid_3.mp4')
# fgbg = cv2.createBackgroundSubtractorMOG2()
#
# while True:
# 	ret, frame = cap.read()
# 	fgmask = fgbg.apply(frame)
#
# 	cv2.imshow('Original', frame)
# 	cv2.imshow('foreG', fgmask)
#
# if cv2.waitKey(1) & 0xFF == ord('q'):
# 	break
#
# cap.release()
# cv2.destroyAllWindows()


def getForeGround(videoInput):
	cap = cv2.VideoCapture(videoInput)
	fgbg = cv2.createBackgroundSubtractorMOG2()
	
	try:
		while True:
			ret, frame = cap.read()
			fgmask = fgbg.apply(frame)
			
			cv2.imshow('Original', frame)
			cv2.imshow('foreG', fgmask)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			return frame
	
	except cv2.error as e:
		print('Program has to terminate on due of openCV error: {}'.format(e))
		return None


getForeGround('vid_1.mp4')
