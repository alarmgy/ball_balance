import cv2 as cv
import numpy as np

x = 0
y = 1

ball = [-1, -1]
center = [-1, -1]

cap = cv.VideoCapture(4)

def findCenter(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of magenta color in HSV
    lower_color = np.array([145,100,100])
    upper_color = np.array([160,255,255])

    # Threshold the HSV image to get only magenta colors
    mask = cv.inRange(hsv, lower_color, upper_color)

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    x_avg = 0
    y_avg = 0
    cnt = 0
    for i in contours:
        M = cv.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # cv.drawContours(frame, [i], -1, (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            # cv.putText(frame, str(cx) + ", " + str(cy), (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (215, 250, 0), 1)

            x_avg += cx;
            y_avg += cy;
            cnt += 1

    if cnt == 4:
        x_avg = int(x_avg / 4)
        y_avg = int(y_avg / 4)
        center[x] = x_avg
        center[y] = y_avg

    cv.circle(frame, (center[x], center[y]), 7, (0, 0, 255), -1)
    cv.putText(frame, "Center: " + str(center[x]) + ", " + str(center[y]), (center[x] - 40, center[y] - 20),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

def findBall(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    upper_color1 = np.array([180,255,255])
    lower_color1 = np.array([170,120,70])
    mask1 = cv.inRange(hsv, lower_color1, upper_color1)

    upper_color2 = np.array([10,255,255])
    lower_color2 = np.array([0,120,70])
    mask2 = cv.inRange(hsv, lower_color2, upper_color2)

    mask = mask1 + mask2

    # Clean the mask with morphological operations
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Only consider the largest contour
    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest_contour)
        if 1000 <= area <= 3000:  # Filter small noise
            (x1, y1), radius = cv.minEnclosingCircle(largest_contour)
            center = (int(x1), int(y1))
            radius = int(radius)
            cv.circle(frame, center, radius, (0, 255, 0), 2)
            cv.putText(frame, f"Red Ball ({center[0]}, {center[1]})", (center[0]-40, center[1]-radius-10),
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            ball[x] = center[x]
            ball[y] = center[y]

while True:

    # Take each frame
    _, frame = cap.read()
    frame = cv.flip(frame, 0)
    frame = cv.flip(frame, 1)


    findCenter(frame)
    findBall(frame)


    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
