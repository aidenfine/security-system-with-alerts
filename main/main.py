import threading
import cv2
import imutils

cap = cv2.VideoCapture(0)
first_frame = None

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)


alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print('xxx')
    alarm = False

while True:
    if first_frame is None:
        first_frame=start_frame
        continue
    _, frame = cap.read()
    
    frame = imutils.resize(frame, width=500)


    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(first_frame, start_frame)
        threshold = cv2.threshold(difference, 50,255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold,None,iterations=2)
        start_frame = frame_bw

            # delta_frame = cv2.absdiff(first_frame,gray)
            # threshold_frame = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
            # threshold_frame = cv2.dilate(threshold_frame,None,iterations=2)

        # (cntr,_)=cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # for contour in cntr:
        #     if cv2.contourArea(contour)<1000:
        #         continue
        #     (x,y,w,h)=cv2.boundingRect(contour)
        #     cv2.rectangle(frame,(x,y),(0,255,0),3)

        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
        
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