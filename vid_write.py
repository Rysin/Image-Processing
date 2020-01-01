import cv2

cap = cv2.VideoCapture('vid_3.mp4')
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
# Define the codec and create VideoWriter object
try:
	out = cv2.VideoWriter('output.avi', fourcc=fourcc, fps=20, frameSize=(1920, 1080))
except:
	print('Something is wrong with Conversions!')

while (cap.isOpened()):
	ret, frame = cap.read()
	if ret == True:
		frame = cv2.flip(frame, 0)
		
		# write the flipped frame
		out.write(frame)
		
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
