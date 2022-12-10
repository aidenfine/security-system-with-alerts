import threading
import cv2
import imutils
from cvzone.PoseModule import PoseDetector
import cvzone
from datetime import datetime

cap = cv2.VideoCapture(0)

#set img 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# iii
fpsReader = cvzone.FPS()
detector = PoseDetector()

# counter 
count = 0
motion = False

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)


alarm = False
alarm_mode = False
alarm_counter = 0

# get date and time
timestamp = datetime.now()
dt_string = timestamp.strftime("%d-%m-%Y-%H-%M-%S")

# save img
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(f'/Users/aidenfine/security-system-with-alerts/security-system-with-alerts/main/output/{dt_string}.avi',fourcc, 20.0, size)

def beep_alarm():
    global alarm
    for _ in range(20):
        if not alarm_mode:
            break
        print("!!!!!!!!!!!!!!!!!!!!!!!")
    alarm = False

while True:
    success, frame = cap.read()

    # detect human
    frame = detector.findPose(frame)
    mlist,bbox = detector.findPosition(frame)
    
    frame = imutils.resize(frame, width=500)


    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)


        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 50,255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold,None,iterations=2)
        start_frame = frame_bw

        if threshold.sum() > 10000:
            alarm_counter += 1
            print("MOTON ")
        else:
            print("-------------------------------")
            if alarm_counter > 0:
                alarm_counter -= 1          

        cv2.imshow("Cam", threshold)
        cv2.imshow("footage", frame)
        
    else:
        cv2.imshow("Cam", frame)
       
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('t'):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord('q'):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()