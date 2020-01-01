import cv2
import matplotlib.pyplot as plt
import numpy as np


# <editor-fold desc="HSV Values">
# blue: 110,50,50; 130,255,255
# Yellow: 22, 60, 200; 60,255,255
# Red: 170, 100, 0; 180, 255, 255
# Green_Approx: 66,50,50; 87,255,255
# Green_Accurate: 66,100,200; 75,255,255
# </editor-fold>


def tStamp_post_processing(timeStampList):
	"""
	:param timeStampList: This should be float dType list of significant timestamps.
	:return: tStamps_processed{list}: This will be list of unique timestamps and minimum separation is of 1 sec.
	"""
	# Create new list with rounded-off numbers from original timestamp list
	tStamps_processed = [np.round(tStamp) for tStamp in timeStampList]
	
	# Remove Duplicates
	tStamps_processed_series = set(tStamps_processed)
	
	# Converting back to List
	tStamps_processed = list(tStamps_processed_series)
	tStamps_processed = sorted(tStamps_processed)
	
	# Convert into minutes
	tStamps_processed = sec2min(tStamps_processed)
	
	return tStamps_processed


def sec2min(secs_list):
	"""
	:param secs_list: This is list of second values to iterate over.
	:return: minuteList: This is list of minutes corresponding to seconds.
	:rtype: {List}{str}
	"""
	
	minuteList = []
	for seconds in secs_list:
		minute = int(seconds // 60)
		seconds = int(seconds % 60)
		minuteList.append(str(minute) + ':' + str(seconds))
	
	return minuteList


def greenPixels(frame_array):
	"""
	:parameter: frame_array: This is a frame having green content above threshold
	:return:(x,y): List of of X and Y co-ordinate for a frame
	"""
	
	xyGreenFrame = []
	
	for row in frame_array:
		for col in row:
			if col[1] > 210:
				x = col
				y = row
				xy = (x, y)
				xyGreenFrame.append(xy)
			else:
				pass
		
		print('Done with Pixel Find')
		return xyGreenFrame


def main(videofile):
	nGreen = []
	nGreenFrame_index = []
	xy_green = []
	nGreenFrame = []
	tStamps = []
	
	frame_count = 0
	
	cap = cv2.VideoCapture(videofile)
	fps = cap.get(cv2.CAP_PROP_FPS)
	print('FPS is: ' + str(fps))
	# tStamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
	# This drives the program into an infinite loop.
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
		res_np = np.asarray(res)
		res_np_mean = res_np.mean()
		
		if res_np_mean > 0.200:
			nGreen.append(res_np_mean)
			nGreenFrame_index.append(frame_count)
			nGreenFrame.append(res_np)
			# print(nGreenFrame[0][254][1072][1])
			# print(xy_green)
			tStamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
		else:
			nGreen.append(0.00)
		
		frame_count += 1
		# print(res_np.dtype)
		# print(res_np.ndim)
		# print(res_np.shape)
		# print(res_np.size)
		
		(ret, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		for pic, contour in enumerate(contours):
			Area = cv2.contourArea(contour)
			if Area > 300:
				x, y, w, h = cv2.boundingRect(contour)
				frame = cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 0, 255), 2)
				cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255))
			
			cv2.imshow('IMG', frame)
		
		# cv2.imshow('frame', frame)
		# cv2.imshow('mask',mask)
		# cv2.imshow('res', res)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	plt.plot(np.arange(0, frame_count, 1), nGreen)
	plt.show()
	
	# print(tStop_m)
	
	tStamps_P = tStamp_post_processing(timeStampList=tStamps)
	# plt.plot(nGreen, tStamps_P)
	# plt.show()
	print('Green can found at timestamps given below\n')
	
	if len(tStamps_P) != 0:
		for i in tStamps_P:
			print(i)
	else:
		print('No Green Content Found In The Video Feed')
	
	cv2.destroyAllWindows()
	cap.release()
	
	return None


if __name__ == '__main__':
	main('vid_2.mp4')
