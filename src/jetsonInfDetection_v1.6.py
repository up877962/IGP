import time
import jetson.inference
import jetson.utils
import cv2
import argparse
import sys
import numpy
import requests_HTTP as req
import webcolors

compRoute = []
matchListIn = []
matchListOut = []
motorClasses = [3,4,6,8]

#parse cmd line
parser = argparse.ArgumentParser(description="Locate objects in a camera feed", formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() + jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())
parser.add_argument("input_URI2", type=str, default="/media/C2.avi", nargs='?', help="URI of second input")
parser.add_argument("input_URI1", type=str, default="/media/Sam2.avi", nargs='?', help="URI of first input")
parser.add_argument("output_URI1", type=str, default="/media/JID_output.avi", nargs='?', help="URI of the ouput camera stream")
parser.add_argument("output_URI2", type=str, default="/media/JID_output2.avi", nargs='?', help="Output number 2")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="predetection overlay flags")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold")

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [" "]

try:
    opt = parser.parse_known_args()[0]
except:
    print(" ")
    parser.print_help()
    sys.exit

#obtain token and open http connection
#token = req.login()
#conn = req.openConnection()

#load network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

#video sources
input = jetson.utils.videoSource(opt.input_URI1, argv=sys.argv)
startTime1 = time.time()
input2 = jetson.utils.videoSource(opt.input_URI2, argv=sys.argv)
startTime2 = time.time()
output = jetson.utils.videoOutput(opt.output_URI1, argv=sys.argv+is_headless)
output2 = jetson.utils.videoOutput(opt.output_URI2, argv=sys.argv+is_headless)

class Objdetection:
    def __init__(self, time, objsource, detect, dir, col):
        self.source = objsource
        self.detection = detect
        self.colour = col
        self.direction = dir
        self.capTime = time


#main loop
def main():
    #obtain token for http requests
    token = req.login()
    c = 0
    filtered = []
    while True:
        #capture frames from video streams
        img1 = input.Capture()
        img2 = input2.Capture()
        #create  list of detection objects for each frame
        detections = net.Detect(img1, overlay=opt.overlay)
        detections2 = net.Detect(img2, overlay=opt.overlay)
        #display number of streams detected in image regardless of location on frame

        for detection in detections:
            #only take detection from specific section of the frame to  mitigate duplicate detections
            #if detection.Top > img1.height*0.4 and detection.ClassID in motorClasses:
            if img1.height * 0.25 <= detection.Center[1] <= img1.height * 0.75  and detection.ClassID in motorClasses:
                #print(c, " Stream 1", detection)

                #logic to determin which side of the road the car is on
                if(detection.Left < img1.width*0.45):
                    dirFlag = "Out"
                else:
                    dirFlag = "In"
                #print(dirFlag)
                #detection.__attribute__ to access individual attributes of the detection.

                #get the colour that is most frequent in the bounding box area
                col = mode(img1, detection.Top, detection.Left, detection.Bottom, detection.Right)
                #associate rgb value with its english name e.g Red, Blue, Green, Orange
                col_name = get_colour_name((col[0][0],col[0][1],col[0][2]))  #matches rgb values to a colour name
                #print(col_name)

                #Get time
                endTime1 = time.time()
                timestamp = endTime1 - startTime1

                #send request to chungus.co.uk
                req.updateBoundingBox(token, 'id0', input.GetHeight(), input.GetWidth(), timestamp, detection.Height, detection.Width, detection.Left, detection.Top)

                #create detection object for comparison
                d1 = Objdetection(endTime1,"id0", detection, dirFlag, col_name)
                #print("{} {} {} {} {}".format(d1.source, d1.direction, d1.detection.ClassID, d1.colour, d1.capTime))

                addToList(d1)

        #repeat above process for second stream
        for detection in detections2:
            #if detection.Top > img2.height*0.4 and detection.ClassID in motorClasses:
            if img2.height * 0.25 <= detection.Center[1] <= img2.height*0.75 and  detection.ClassID in motorClasses:
                #print(c, " Stream 2", detection)
                if(detection.Left < img2.width/2):
                    dirFlag = "Out"
                else:
                    dirFlag = "In"
                col = mode(img2, detection.Top, detection.Left, detection.Bottom, detection.Right)
                col_name = get_colour_name((col[0][0],col[0][1],col[0][2]))
                #print(col_name)
                endTime2 = time.time()
                timestamp = endTime2 - startTime2
                req.updateBoundingBox(token, "id1", input2.GetHeight(), input2.GetWidth(), timestamp, detection.Height, detection.Width, detection.Left, detection.Top)
                d2 = Objdetection(endTime2, "id1", detection, dirFlag, col_name)
                #print("{} {} {} {} {}".format(d2.source, d2.direction, d2.detection.ClassID, d2.colour, d2.capTime))
                addToList(d2)

       # matImg = convertToMatrix(img1)
       # cv2.imshow("It works", matImg)

        #pass detection objects to matchDetections
        #try:
        result = checkRoutes(token)
            #if(result):
        for i in result:
            if i != "NULL":
                filtered.append(i)
                print("\n\n\n\n\n\n", i, "\n\n\n\n\n")
                #print("\n\n\n\n\n %%% - got identifier: " + i + " - %%% \n\n\n\n\n")
                #req.newVehicle(token, result)
            #else:
                #print("got nothing")
        #except:
            #print("No object detected within region")

        output.Render(img1)
        output2.Render(img2)

        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
        output2.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

        net.PrintProfilerTimes()

        c = c+1

        #for i in matchListIn:
            #print("In: {} {} {}".format(i.source, i.colour, i.direction))
        #for j in matchListOut:
            #print("Out: {} {} {}".format(j.source, j.colour, j.direction))

        if not input.IsStreaming() or not output.IsStreaming():
            break

#Function to return a numpy matrix from an img
def convertToMatrix(img):
    matrix = numpy.zeros([img.height, img.width, 3])
    for y in range(img.height):
        for x in range(img.width):
            pixel = img[x,y]
            matrix[y,x,:] = pixel
            return matrix 

# COLOUR FREQUENCY SOLUTION - produces [[r, g, b], count] for the most frequent rgb value
def mode(img, top, left, bottom, right):
    x1 = int(top)
    y1 = int(left)
    x2 = int(bottom)
    y2 = int(right)
    #x2 = int(bbox[0][0] * x)
    #y2 = int(bbox[0][1] * y)
    #x1 = int(bbox[0][2] * x)
    #y1 = int(bbox[0][3] * y)
    bbox_main_col = {}  # dictionary for counting occurrences inside bbox_cols array
    bbox_cols = []
    #image = cv2.imread(img)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for x in range(y1, y2):
        for y in range(x1, x2):
            #(b, g, r) = img[x, y]  # openCV uses BGR colour format, not RGB, so remember to reverse the order
            #rgb = [r, g, b]
            (r,g,b) = img[y, x]
            bbox_cols.append("{}-{}-{}".format(r, g, b))
    for colour in bbox_cols:
        bbox_main_col.setdefault(colour, 0)
        bbox_main_col[colour] += 1
    most_freq = ["", 0]
    for i, count in bbox_main_col.items():
        if count > most_freq[1]:
            most_freq[1] = count
            most_freq[0] = i
    most_freq[0] = most_freq[0].split('-')
    most_freq[0][0] = int(most_freq[0][0])
    most_freq[0][1] = int(most_freq[0][1])
    most_freq[0][2] = int(most_freq[0][2])
    #print(most_freq)
    return most_freq

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name

def addToList(obj):
    if(obj.direction == "In"):
        matchListIn.append(obj)

    elif(obj.direction == "Out"):
        matchListOut.append(obj)

timeBuf = []

def checkRoutes(token):
    #isMatch = False
    for i in matchListOut:
        for j in matchListIn:
            class1 = i.detection.ClassID
            class2 = j.detection.ClassID
            col1 = i.colour
            col2 = j.colour
            src1 = i.direction
            src2 = j.direction
            time1 = int(i.capTime)
            time2 = int(j.capTime)
            if(class1 == class2 and col1 == col2 and src1 != src2 and i.source != j.source and time1 not in timeBuf and time2 not in timeBuf):
                #isMatch = True
                #matchListOut.remove(i)
                #matchListIn.remove(j)
                #i.capTime = entry time
                #i.colour = colour
                #i.direction = direction
                #i.detection. = detection object
                #encode string addNewVehicle(id)
                timeBuf.append(time1)
                timeBuf.append(time2)
                encoded1 = "{}{}{}{}{:.2f}".format(i.source, i.direction, i.colour[0], i.detection.ClassID, i.capTime)
                encoded2 = "{}{}{}{}{:.2f}".format(j.source, j.direction, j.colour[0], j.detection.ClassID, j.capTime)
                route = "{}->{}".format(encoded2, encoded1)
                compRoute.append(route)
                req.addNewVehicle(token, route, i.source, i.capTime, j.source, j.capTime)
            else:
                compRoute.append("NULL")

    return(compRoute)

main()
