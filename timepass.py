import logging
import cv2
import numpy as np
from matplotlib import pyplot as plt

tStamps = []

logging.basicConfig(filename="Diff_Results.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def getForeGround(capture):
	cap = capture
	fgbg = cv2.createBackgroundSubtractorMOG2()
	
	try:
		while True:
			# ret, frame = cap.read()
			fgmask = fgbg.apply(cap)
			
			cv2.imshow('Original', cap)
			cv2.imshow('foreG', fgmask)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			return fgbg
	
	except cv2.error as e:
		print('Program has to terminate on due of openCV error: \n{}'.format(e))
		return None


def visualDiff(capture1, capture2, *resolution):
	"""

	:param capture1:
	:param capture2:
	:param resolution:
	:return:
	"""
	diffFrames = []
	diff_mean_frames = []
	if not resolution:
		resolution = (800, 800)
	capture1 = cv2.VideoCapture(capture1)
	capture2 = cv2.VideoCapture(capture2)
	fgbg = cv2.createBackgroundSubtractorMOG2()
	
	# f1, frame1 = capture.read()
	frame_count = 0
	try:
		while 1:
			f1, frame1 = capture1.read()
			frame1_r = cv2.resize(frame1, resolution)
			f2, frame2 = capture2.read()
			frame2_r = cv2.resize(frame2, resolution)
			
			kernel = np.ones((5, 5), np.uint8)
			
			fgbgmask1 = fgbg.apply(frame1_r)
			# fgbgmask1 = cv2.erode(fgbgmask1, kernel, iterations=1)
			fgbgmask2 = fgbg.apply(frame2_r)
			# fgbgmask2 = cv2.erode(fgbgmask2, kernel, iterations=1)
			
			diff = cv2.absdiff(fgbgmask1, fgbgmask2)
			diff = cv2.erode(diff, kernel, iterations=1)
			print(diff)
			diff_mean = np.mean(diff)
			diff_mean_frames.append(diff_mean)
			print(np.argmax(diff_mean))
			diff_median = np.median(diff)
			print(np.argmax(diff_median))
			print(diff_mean)
			print(diff_median)
			logger.info('Mean value is: {}'.format(diff_mean))
			logger.info('Median value is: {} '.format(diff_median))
			if 10 < diff_mean < 20:
				tStamps.append(capture1.get(cv2.CAP_PROP_POS_MSEC) / 1000)
				diffFramesArray = np.array(diff)
				diffFrames.append(diffFramesArray)
				logger.info('The Difference Frame array look like: {}'.format(diffFramesArray))
				logger.info('\n')
			
			# diff = frame1 - frame2
			# cv2.imshow('Frame 1', frame1_r)
			# cv2.imshow('Frame 2', frame2_r)
			cv2.imshow('Diff', diff)
			cv2.imshow('ForeGround1', fgbgmask1)
			cv2.imshow('ForeGround2', fgbgmask2)
			frame_count += 1
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		
		plt.plot(np.arange(0, len(diff_mean_frames), 1), diff_mean_frames)
		plt.show()
		
		cv2.destroyAllWindows()
		capture1.release()
		capture2.release()
	
	except cv2.error as e:
		print('Video feed has ended with error: {}'.format(e))
		
		return tStamps, diffFrames


def showDiffs(frames):
	"""
	:rtype: None
	:param frames: This is the frames array list to be processed.
	"""
	diffLen = len(frames)
	print(diffLen)
	logger.info('We have total {} difference frames'.format(diffLen))
	if diffLen != 0:
		for frame in frames:
			cv2.imshow('Results', frame)
			logger.info('Difference Frame: {}'.format(frame))
	else:
		print('No difference  frames found in this video')
	
	print('!!Done')
	return None


timeStamps, diffF = visualDiff('x.mp4', 'x_edited.mp4')

for i in timeStamps:
	print('Difference found at: {}'.format(i))
	logger.info('Timestamp for the difference frame: {}'.format(i))

showDiffs(frames=diffF)
