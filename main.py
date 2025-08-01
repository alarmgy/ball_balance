import cv2 as cv
import math
import numpy as np
import time
import inverse_kinematics as ik
import visualize as vis

# Constants
x = 0
y = 1

max_angle = 10

# Positions
ball = [-1, -1]
origin = [-1, -1]

# PID
Kp = 0.05
Kd = 0
prev_time = time.time()
prev_error = [0, 0]

# Color Ranges
# Magenta
lower_color_magenta = np.array([145,100,100])
upper_color_magenta = np.array([160,255,255])

# Red
upper_color1 = np.array([180,255,255])
lower_color1 = np.array([170,120,70])
upper_color2 = np.array([10,255,255])
lower_color2 = np.array([0,120,70])


def find_center(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Threshold the HSV image to get only magenta colors
    mask = cv.inRange(hsv, lower_color_magenta, upper_color_magenta)

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cnt = 0
    corners = []
    for i in contours:
        M = cv.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # cv.drawContours(frame, [i], -1, (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            # cv.putText(frame, str(cx) + ", " + str(cy), (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (215, 250, 0), 1)

            corners.append([cx, cy])

            cnt += 1

    if cnt == 4:
        for i in range(3):
            for j in range(i + 1, 4):
                if (corners[i][x] - 100 > corners[j][x]) or (abs(corners[i][x] - corners[j][x]) < 100 and corners[i][y] - 100 > corners[j][y]):
                    corners[i], corners[j] = corners[j], corners[i]

        # print(corners)

        A = np.array([
            [corners[3][x] - corners[0][x], corners[2][x] - corners[1][x]],
            [corners[3][y] - corners[0][y], corners[2][y] - corners[1][y]]
        ])
        b = np.array([
            corners[2][x] - corners[0][x],
            corners[2][y] - corners[0][y]
        ])
        t = np.linalg.solve(A, b)
        intersection = (corners[0][x] + t[0] * (corners[3][x] - corners[0][x]),
                        corners[0][y] + t[0] * (corners[3][y] - corners[0][y]))

        origin[x] = int(intersection[x])
        origin[y] = int(intersection[y])
        # print(str(origin[x]) + ", " + str(origin[y]))

    cv.circle(frame, (origin[x], origin[y]), 7, (0, 0, 255), -1)
    cv.putText(frame, "Center: " + str(origin[x]) + ", " + str(origin[y]), (origin[x] - 40, origin[y] - 20),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

def find_ball(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask1 = cv.inRange(hsv, lower_color1, upper_color1)
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
        else:
            ball[x] = origin[x]
            ball[y] = origin[y]
    else:
        ball[x] = origin[x]
        ball[y] = origin[y]

def constrain(val, min_val, max_val):
    if val < min_val: return min_val
    if val > max_val: return max_val
    return val


def PD():
    global prev_time

    error_x = origin[x] - ball[x]
    error_y = -(origin[y] - ball[y])

    curr_time = time.time()
    dt = curr_time - prev_time
    prev_time = time.time()

    de = [error_x - prev_error[x], error_y - prev_error[y]]
    derivative = [de[x] / dt, de[y] / dt]

    prev_error[x] = error_x
    prev_error[y] = error_y

    out = [-(error_y * Kp + derivative[y] * Kd), error_x * Kp + derivative[x] * Kd]
    out[x] = constrain(out[x], -max_angle, max_angle)
    out[y] = constrain(out[y], -max_angle, max_angle)

    return int(out[x]), int(out[y])

def len_2_pressure(length):
    return 797192270.26400 * pow(length, 4) + -84918177.62388 * pow(length, 3) + 3165367.07235 * pow(length, 2) + -45766.30128 * length + 147.49474


cap = cv.VideoCapture(4)

while True:

    # Take each frame
    _, frame = cap.read()

    find_center(frame)
    find_ball(frame)

    out_x, out_y = PD()
    # print(out_x, out_y)

    lengths = ik.IK(out_x, out_y, [0.035, 0.035, 0.035])
    # print(lengths)
    pressures = []
    for l in lengths:
        pressures.append(len_2_pressure(l))
    # print(pressures)

    vis.p1 = [0, 0.04, lengths[0]]
    vis.p2 = [-0.04 * math.cos(math.pi / 6), -0.04 * math.sin(math.pi / 6), lengths[1]]
    vis.p3 = [0.04 * math.cos(math.pi / 6), -0.04 * math.sin(math.pi / 6), lengths[2]]
    vis.update()

    #cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
# vis.plt.ioff()
# vis.plt.show()
