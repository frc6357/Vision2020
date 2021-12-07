import cv2
import itertools
import numpy as np
from create_bound import *
import hough_transform
import visionFunctions
import math
import multiprocessing
import time
from datetime import datetime
def test_process_frame(frame):
    #print(frame[0])
    h, w, d = frame.shape
    cv2.circle(frame, (int(w/2), int(h/2)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/4), int(h/4)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/6), int(h/6)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/8), int(h/8)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/10), int(h/10)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/12), int(h/12)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/14), int(h/14)), 3, (255, 0, 0))
    cv2.circle(frame, (int(w/16), int(h/16)), 3, (255, 0, 0))

    return frame

def rectCentr(input):
    Xs = [a[0] for a in input]
    Ys = [a[1] for a in input]
    bot_left = [min(Xs), min(Ys)]
    top_right = [max(Xs), max(Ys)]
    mid_point = (int((bot_left[1] + top_right[1])/2), int((bot_left[0] + top_right[0])/2))
    return mid_point

def findHoriAngle(cent, w):
    return abs(w-cent[0]) * 0.04499

def process_frame(frame):
    h, w, d = frame.shape


    im = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    cv2.cvtColor() takes in a variable storing a read image
    and then another method in cv2 that will tell cv2.cvtColor()
    which color space it is in and which color space it wants to convert to
    Ex: 
    
    cv2.cvtColor(im, cv2.BGR2HLS)
    this will read the image stored in im that is currently in the BGR color space
    and convert all pixels to HLS
    """
    #im3 = im
    # test 1 HSV color value: (173 deg, 48%, 76%)
    # upper bound +5%:
    # lower bound -5%:

    """
    bound_percent_cv2 method takes Hue(h), Saturation(s), Brightness(v), Threshold Percent(in decimal form so 100% = 1.0
    Ex: input HSV = [120, 100, 97] and threshold image by +5%
    image_upper_bound = bound_percent_cv2(120, 100, 97, 1.05)
    """

    image_lower_bound = bound_percent_cv2(175, 46, 44, 0.6)
    image_upper_bound = bound_percent_cv2(175, 46, 44, 1.6)

    """
    cv2.inRange() takes in a variable storing a read image, lower bound, and upper bound
    It then checks each each pixel to see if it lies within the lower and upper bound
    It will return a true(1) or false(0) and if the pixel returns 0 then this method
    turns that pixel black, if the pixel returns 1 then this method does nothing to it
    """
    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)

    """
    OpenCV displays all images in the BGR color space in order to look properly
    so after filtering the image in HSV color space the script needs to convert
    back to BGR in order to display interpretable images
    """
    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)
    #cv2.imshow("Filtered Image", imageFiltered)

    # Converts BGR to Grayscale image in preparation for thresholding by making a high contrast image
    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grayscale Image", grayscale_im)

    # uses OTSU and Binary Thresholding methods to maximize contrast in filtered image
    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("Grayscale Otsu Thresholded Image", th2)

    # uses canny edge detection to find the edges of segmented image
    edges = cv2.Canny(th2, 100, 200)



    #lines = cv2.HoughLines(edges, 1, np.pi / 180, 55, min_theta=-10*math.pi/180, max_theta=10*math.pi/180)
    #lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)

    # finds houghlines using Probabilistic Hough Lines Algorithm
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10)
    color_lines = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # turns houghlines output from [rho, theta] to [theta, b]
    if lines is not None:
        point_pairs_lines = []
        bucket = []
        lines = [line[0] for line in lines]

        for line in lines:
            x1, y1, x2, y2 = line
            """rho, theta = line
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))"""

            point_pairs_lines.append([x1, y1, x2, y2])
            #cv2.line(color_lines, (x1, y1), (x2, y2), (255,0,0), 2)
        #print(point_pairs_lines)
        theta_b_lines = [hough_transform.theta_b(i) for i in point_pairs_lines]

        # sorts duplicate lines into buckets
        while len(theta_b_lines) > 0:
            theta_b_lines, bucket = hough_transform.filter_lines(theta_b_lines, bucket)
        #print(bucket)

        # averages buckets together
        if bucket is not None:
            avg_lines = hough_transform.average_lines(bucket)
            print("average lines", avg_lines)
            print("\n")

        # find intersections
        intersect_points = [visionFunctions.intersections(i) for i in itertools.combinations(avg_lines,2)]
        intersect_points = [i for i in intersect_points if i is not None]
        intersect_points = visionFunctions.remove_dupe(intersect_points)
        #print("Intersection point count: {0}\n".format(len(intersect_points)))
        #print("Intersection point list: {0}\n".format(intersect_points))

        # draw centroid
        centroid = rectCentr(intersect_points)
        cv2.circle(frame, centroid, 5, (255,0,35))

        # draw intersections on original input frame
        for point in intersect_points:
            print("point: {0}/n".format(point))
            x,y = point
            print("{0}, {1}".format(x,y))
            cv2.circle(frame, (int(y), int(x)), 5, (0, 255, 0))


        # draws average lines on input frame
        try:
            for avg_line in avg_lines:
                theta, b = avg_line
                if theta == 90 * math.pi/180:
                    cv2.line(frame, (int(b), 1), (int(b), h-1), (255,0,0), 2)

                else:

                    print("theta: " + str(theta))
                    m = math.tan(theta)
                    x1 = 1
                    x2 = w-1
                    y1 = m*x1 + b
                    y2 = m*x2 +b
                    print("y1: " + str(y1))
                    print("y2: " + str(y2))
                    cv2.line(frame, (x1, int(y1)), (x2,int(y2)), (255, 0, 0), 3)
        except Exception as e:
            print(e)
        print("horizontal angle: " + str(findHoriAngle(centroid, w)))
        cv2.imshow("Frame " + str(datetime.now().strftime("%H:%M:%S")), frame)
        #cv2.imshow("Canny Edge Detection", edges)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
    return frame




def cap_frame():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_EXPOSURE, -11)
    key_values = {
        49 : 1,
        50 : 2,
        51 : 3,
        52 : 4,
        53 : 5,
        54 : 6,
        55 : 7,
        56 : 8,
        57 : 9,
        113 : "q",
        114 : "r"
    }

    while True:
        x = ord(input("How many frames: "))

        if x in key_values:

            if key_values[x] == "q":
                cap.release()
                return
            if key_values[x] == "r":
                cap.release()
                print("released")
                cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                cap.set(cv2.CAP_PROP_EXPOSURE, -11)
                continue

            frames = []
            for i in range(0, key_values[x]):
                tic = time.time()
                ret, frame = cap.read()
                if ret == False:
                    print("broke -> ", "pre release " + str(cap.isOpened()))
                    cap.release()
                    print("post release " + str(cap.isOpened()))
                    quit()

                frames.append(frame)



            print(str(frames) + "\n")
            with multiprocessing.Pool( processes=len(frames) ) as pool:
                processed_frames = pool.map(process_frame, frames)


            """else:
                with multiprocessing.Pool(processes=10) as pool:
                    processed_frames = pool.map(test_process_frame, frames)"""
            #processed_frames = [process_frame(i) for i in frames if i is not None]
            #print(processed_frames)
            #display_frames(processed_frames)

            toc = time.time()
            print(toc - tic)
            a = 1
            for frame in processed_frames:
                cv2.imshow("Processed frames " + str(a) + ": " + str(datetime.now().strftime("%H:%M:%S")), frame)
                a += 1
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                continue

if __name__ == "__main__":
    cap_frame()