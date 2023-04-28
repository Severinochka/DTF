import cv2
import time

cap = cv2.VideoCapture('cam_video.mp4')
count_left = 0
count_right = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    line_pos = frame.shape[1] // 2

    gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv2.threshold (gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2. CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect (c)
        cv2. rectangle (frame, (x, y), (x+w, y+h), (0,255,0), 2)

        # find the center of the contour
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # update the count variables based on the position of the contour
        if cx < line_pos:
            count_left += 1
            cv2.putText(frame, 'Left Count: ' + str(count_left), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Right Count: ' + str(count_right), (frame.shape[1] // 2 + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            count_right += 1
            cv2.putText(frame, 'Left Count: ' + str(count_left), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Right Count: ' + str(count_right), (frame.shape[1] // 2 + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release
cv2.destroyAllWindows()
