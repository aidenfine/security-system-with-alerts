import cv2
from cvzone.PoseModule import PoseDetector
import cvzone
from datetime import datetime

# ---------------------------------------------------------------------------------------------
fpsReader = cvzone.FPS()
detector = PoseDetector()

# set img 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# set 
count = 0
motion = False

#get w and h
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)

# get date and time
timestamp = datetime.now()
dt_string = timestamp.strftime("%d-%m-%Y-%H-%M-%S")

# save video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(f'/Users/aidenfine/security-system-with-alerts/security-system-with-alerts/main/output/{dt_string}.avi',fourcc, 20.0, size)

first_frame = None
while True:
    success, img = cap.read()
    # fps, img = fpsReader.update(img,pos=(25,50),color=(0,255,0),scale=3,thickness=3)

    img = detector.findPose(img)
    imlist,bbox = detector.findPosition(img)
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray= cv2.GaussianBlur(gray, (21,21),0)
    if first_frame is None:
        first_frame=gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    threshold_frame = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame,None,iterations=2)

    (cntr,_)=cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in cntr:
        if cv2.contourArea(contour)>10000: 
            motion = True
            # write out flipped frame
            print("motion and recording")
            continue
        else: 
            motion = False
    if motion:
        out.write(img)
    else:
        print("no motion :)")
    

    cv2.imshow("wd2uh", img)

    key_pressed = cv2.waitKey(5)
    if cv2.waitKey(1)== ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()