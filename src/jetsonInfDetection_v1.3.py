import jetson.inference
import jetson.utils
import cv2
import argparse
import sys
import numpy
import requests_HTTP as req

#parse cmd line
parser = argparse.ArgumentParser(description="Locate objects in a camera feed", formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() + jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())
parser.add_argument("input_URI1", type=str, default="/media/Sam4.avi", nargs='?', help="URI of input camera stream")
parser.add_argument("input_URI2", type=str, default="/media/Sam4.avi", nargs='?', help="URI of 2nd input")
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
input2 = jetson.utils.videoSource(opt.input_URI2, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI1, argv=sys.argv+is_headless)
output2 = jetson.utils.videoOutput(opt.output_URI2, argv=sys.argv+is_headless)

#main loop
def main():
    token = req.login()
    while True:
        img1 = input.Capture()
        img2 = input2.Capture()
        detections = net.Detect(img1, overlay=opt.overlay)
        detections2 = net.Detect(img2, overlay=opt.overlay)
        print("Detected {:d} objects in image".format(len(detections)))
        for detection in detections:
            #print(detection)
            if(detection.Left < detection.Width/2):
                dirFlag = "In"
            else:
                dirFlag = "Out"
            print("Stream1", detection)
            print(dirFlag)
            #detection.__attribute__ to access individual attributes of the detection.
            mode(img1, detection.Top, detection.Left, detection.Bottom, detection.Right)
            req.updateBoundingBox('nothing', detection.Height, detection.Width, detection.Left, detection.Top, token)
        for detection in detections2:
            print("Stream 2", detection)
        matImg = convertToMatrix(img1)
        cv2.imshow("It works", matImg)
        output.Render(img1)
        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
        net.PrintProfilerTimes()
        if not input.IsStreaming() or not output.IsStreaming():
            break


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
    print(most_freq)
    return most_freq


# Query is first image of car
# Test is image we are trying to match
# The order that arguments are given matters
def is_match(query, test1):

    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(query, None)
    kp2, des2 = sift.detectAndCompute(test1, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test to matches that have a near enough
    # Euclidean distance
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # This distance threshold will need to be checked and changed
            good_matches.append([m])

    # does good_matches have enough good matches?
    if len(good_matches) > 10:
        return True
    else:
        return False

main()
