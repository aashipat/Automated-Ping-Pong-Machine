from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

#initialize motors
Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
print("Setup complete")

error = 8
middle = 120

def isset(v):
    try:
        type (eval(v))
    except:
        return 0
    else:
        return 1

#changes hsv values to rgb values
def nothing(x):
    pass

#initializes the camera object
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

#editing PiRGBArray
rawCapture = PiRGBArray(camera, size=(320,240))

#reading frames from camera module
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    #setting up color recognition
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    B = 0
    G = 255
    R = 0

    green = np.uint8([[[B,G,R]]])
    hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
    upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

    #adjusting the threshold of the HSV image for range of selected color
    mask = cv2.inRange(hsv, lowerLimit, upperLimit)

    #actually taking out the objects of the colors in the frame
    result = cv2.bitwise_and(image, image, mask=mask)

    #find contours in threshold (filtered) image
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__.split('.'))

    #findContours() has different form for opencv2 and opencv3 (includes boolean or not)
    if major_ver == "2" or major_ver == "3":
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #find contour with max area (most of that color, likely the object) and store it
    max_area = 0
    for cont in contours:
        area = cv2.contourArea(cont)
        if area > max_area:
            max_area = area
            best_cont = cont

    #find centroids of best_cont and draw a circle there
    cy = 0
    if isset('best_cont'):
        M = cv2.moments(best_cont)
        cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
        print("Central pos: (%d, %d)" % (cx, cy))
        if (abs(cy - middle) > error):
            if (cy - middle) > 0:
                GPIO.output(Motor1A, GPIO.LOW)
                GPIO.output(Motor1B, GPIO.HIGH)
                GPIO.output(Motor1E, GPIO.HIGH)
                print("Moving backwards")
            elif (cy - middle) < 0:
                GPIO.output(Motor1A, GPIO.HIGH)
                GPIO.output(Motor1B, GPIO.LOW)
                GPIO.output(Motor1E, GPIO.HIGH)
                print("Moving forwards")
        else:
            GPIO.output(Motor1E, GPIO.LOW)
            print("Stop")
    else:
        print("[Warning]Tag lost...")
        GPIO.output(Motor1E, GPIO.LOW)
        print("Stop")
    key = cv2.waitKey(1)

    #clearing the stream
    rawCapture.truncate(0)
    if key != -1:
        break

camera.close()
print("Clean up")
GPIO.cleanup()