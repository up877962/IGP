import cv2
#from PIL import Image
import numpy
import jetson.inference
import jetson.utils
import argparse
import sys
#import ffmpeg_streaming
#from ffmpeg_streaming import Formats, Bitrate, Representation, Size

#video = ffmpeg_streaming.input('rtmp://chungus.co.uk/live/id0')
#print(dir(video))
#stream = video.hls(Formats.h264())
#print(type(video))
#stream = video.stream2file(Formats.h264())
#print(type(stream))
#stream.output('/media/repositories/IGP-2020-Group1/src/output.mp4')

parser = argparse.ArgumentParser(description="Detect Objects in real time from video stream")
parser.add_argument("input_URI", type=str, default=" ", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="/media/repositories/IGP-2020-Group1/src/Output.avi", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 


try:
    opt = parser.parse_known_args()[0]
except:
    print(" ")
    parser.print_help()
    sys.exit(0)

net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

#cap = cv2.VideoCapture(hls)
cap = cv2.VideoCapture('rtmp://chungus.co.uk/live/id0')
if(cap.isOpened() == False):
    print('Failed to open video capture')
    sys.exit(-1)

while(True):
    # read frame by frame
    ret, frame = cap.read()
    #img = Image.open(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = numpy.asarray(frame)
    cuda_mem = jetson.utils.cudaFromNumpy(image)
    detections = net.Detect(cuda_mem, overlay=opt.overlay)
    output.Render(cuda_mem)
    #display frame
    #cv2.imshow('frame', frame)

cap.release()
