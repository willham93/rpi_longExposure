# USAGE
# python long_exposure.py --video videos/river_02.mov --output river_02.png --time 5
#new --> python3 longExposure.py --fileName file --time 5

# import the necessary packages
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", required=True,
#	help="path to input video file")
#ap.add_argument("-o", "--output", required=True,
#	help="path to output 'long exposure'")
ap.add_argument("-f", "--fileName", required=True,
	help="filename")
ap.add_argument("-t", "--time",required = True,
	help="time to record video'")
args = vars(ap.parse_args())


# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter("/home/pi/Videos/"+args["fileName"]+".mp4",cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
startTime = time.time()
while(int(time.time())-startTime < int(args["time"])):
  ret, frame = cap.read()

  if ret == True: 
    
    # Write the frame into the file 'output.avi'
    #frame = cv2.flip(frame, flipCode = -1)
    out.write(frame)

    # Display the resulting frame    
    cv2.imshow('frame',frame)

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break  

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 
time.sleep(5)

# initialize the Red, Green, and Blue channel averages, along with
# the total number of frames read from the file
(rAvg, gAvg, bAvg) = (None, None, None)
total = 0

# open a pointer to the video file
print("[INFO] opening video file pointer...")
stream = cv2.VideoCapture("/home/pi/Videos/"+args["fileName"]+".mp4")
print("[INFO] computing frame averages (this will take awhile)...")

# loop over frames from the video file stream
while True:
	# grab the frame from the file stream
	(grabbed, frame) = stream.read()

	# if the frame was not grabbed, then we have reached the end of
	# the sfile
	if not grabbed:
		break

	# otherwise, split the frmae into its respective channels
	(B, G, R) = cv2.split(frame.astype("float"))

	# if the frame averages are None, initialize them
	if rAvg is None:
		rAvg = R
		bAvg = B
		gAvg = G

	# otherwise, compute the weighted average between the history of
	# frames and the current frames
	else:
		rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
		gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
		bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)

	# increment the total number of frames read thus far
	total += 1

# merge the RGB averages together and write the output image to disk
avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
cv2.imwrite("/home/pi/Pictures/"+args["fileName"]+".png", avg)

# do a bit of cleanup on the file pointer
stream.release()
