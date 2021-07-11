import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

# capturing Video from Webcam
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

cap.set(10, 150)

myColors = [[20,40,40,70,255,255],
            [100,169,121,135,255,255],
            [0, 90, 90, 41, 255, 255]]
color_value = [[255, 0, 0], [0, 255, 0], [14, 107, 237]]
x, y, w, h = 0, 0, 0, 0
my_points = []

def find_color(img, color_value, myColors):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(hsv, lower, upper)
        x, y = contour_detect(mask)

        cv2.circle(frame_copy, (x,y), 20,color_value[count], -1)
        if x != 0 and y != 0:
            new_points.append([x,y,count])
        count += 1
    return new_points



def contour_detect(mask):
    x,y,w,h = 0, 0, 0, 0
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01*perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

def canvas(my_points, color_value):
    for point in my_points:
        cv2.circle(frame_copy, (point[0], point[1]),
                   15, color_value[point[2]], -1)


while True:

    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()

    new_point = find_color(frame, color_value, myColors)
    if len(new_point) != 0:
        for i in new_point:
            my_points.append(i)
    if len(my_points) != 0:
        canvas(my_points, color_value)

    cv2.imshow('frame', frame_copy)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

