import cv2
import numpy as np
from matplotlib import pyplot as plt

tStamps = []


def visualDiff(capture1, capture2, *resolution):
	"""

	:param capture1:
	:param capture2:
	:param resolution:
	:return:
	"""
	diffFrames = []
	if not resolution:
		resolution = (800, 800)
	capture1 = cv2.VideoCapture(capture1)
	capture2 = cv2.VideoCapture(capture2)
	
	# f1, frame1 = capture.read()
	frame_count = 0
	
	while 1:
		f1, frame1 = capture1.read()
		frame1_r = cv2.resize(frame1, resolution)
		f2, frame2 = capture2.read()
		frame2_r = cv2.resize(frame2, resolution)
		
		# frame1_G = cv2.GaussianBlur(frame1, (5, 5), 0)
		# frame2_G = cv2.GaussianBlur(frame2, (5, 5), 0)
		
		diff = cv2.absdiff(frame1_r, frame2_r)
		print(diff)
		if np.nonzero(diff):
			tStamps.append(capture1.get(cv2.CAP_PROP_POS_MSEC) / 1000)
			diffFrames.append(diff)
		
		# diff = frame1 - frame2
		cv2.imshow('Frame 1', frame1_r)
		cv2.imshow('Frame 2', frame2_r)
		# cv2.imshow('Diff', diff)
		
		frame_count += 1
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	for timestamp in tStamps:
		print(timestamp)
	
	plt.plot(np.arange(0, frame_count, 1), tStamps)
	plt.show()
	
	cv2.destroyAllWindows()
	capture1.release()
	capture2.release()
	
	return tStamps, diffFrames


def showDiffs(frames):
	"""
	:rtype: None
	:param frames:
	"""
	if len(frames) != 0:
		for frame in frames:
			cv2.imshow('Results', frame)
	else:
		print('No difference  frames found in this video')
		print('Ignore this line')
	
	print('Done!')
	return None


timeStamps, diffF = visualDiff('CREW-1.wmv', 'CREW-1.wmv')

for i in timeStamps:
	print(i)
showDiffs(diffF)
