import cv2
import sys
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size

video = ffmpeg_streaming.input('rtsp://chungus.co.uk/live/id0')
#print(dir(video))
#print(video.input)
stream = video.hls(Formats.h264())
#print(stream)
videoFile = video.stream2file(Formats.h264())
videoFile.output('/media/repositories/IGP-2020-Group1/src/myoutput.mp4')

#video = ffmpeg_streaming.input('rtmp://chungus.co.uk/live/id0')
#print(dir(video))
#stream = video.hls(Formats.h264())
#print(type(video))
#stream = video.stream2file(Formats.h264())
#print(type(stream))
#stream.output('/media/repositories/IGP-2020-Group1/src/output.mp4')

#cap = cv2.VideoCapture(hls)
'''
cap = cv2.VideoCapture('rtmp://chungus.co.uk/live/id0')
if(cap.isOpened() == False):
   print('Failed to open video capture')
   sys.exit(-1)

while(True):
   # read frame by frame
   ret, frame = cap.read()

   print(frame)

   # display frame
   #cv2.imshow('frame', frame)

cap.release()
'''
