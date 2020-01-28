import numpy
import cv2
from src.create_bound import *
import time

ts_start = time.time()
cap = cv2.VideoCapture(1)
ts_mid = time.time()

print(ts_mid-ts_start, "seconds to recog")
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()


    im = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image_lower_bound = bound_percent_cv2(126, 100, 100, 0.5)
    image_upper_bound = bound_percent_cv2(126, 100, 100, 1.5)
    imageFilter = cv2.inRange(im, image_lower_bound, image_upper_bound)
    imageFiltered = cv2.bitwise_and(im, im, mask=imageFilter)
    imageFiltered = cv2.cvtColor(imageFiltered, cv2.COLOR_HSV2BGR)

    grayscale_im = cv2.cvtColor(imageFiltered, cv2.COLOR_BGR2GRAY)

    ret2, th2 = cv2.threshold(grayscale_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edges = cv2.Canny(th2, 100, 200)

    cv2.imshow("Canny Edge Detection", edges)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()