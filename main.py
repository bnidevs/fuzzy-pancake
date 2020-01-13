from __future__ import print_function
import cv2 as cv
import serial

center_tolerance = []

#             Device name   port
try:
	srl = serial.Serial('COM4', 9600, timeout=1)
except:
	srl = None

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    global center_tolerance

    faces = face_cascade.detectMultiScale(frame_gray)

    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)

        if center[0] < center_tolerance[0][0]:
        	print('left')
        	if not srl == None:
        		srl.write(b'left')
        elif center[0] > center_tolerance[0][1]:
        	print('right')
        	if not srl == None:
        		srl.write(b'right')

        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        eyes = eyes_cascade.detectMultiScale(faceROI)

        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)

    cv.imshow('Capture - Face detection', frame)

face_cascade_name = 'cv2_data/haarcascade_frontalface_alt.xml'
eyes_cascade_name = 'cv2_data/haarcascade_eye_tree_eyeglasses.xml'

face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

camera_device = 0
cap = cv.VideoCapture(camera_device)

center_tolerance.append([cap.get(3) * 0.3, cap.get(3) * 0.7])
center_tolerance.append([cap.get(4) * 0.3, cap.get(4) * 0.7])

if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break
