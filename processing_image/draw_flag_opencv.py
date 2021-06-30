import numpy as np
import cv2

def indo_flag():
    """
    Quốc kì nước ndonesia
    :return:
    """
    indo = np.zeros((600, 800, 3), dtype=np.uint8)
    for i in range(indo.shape[0]):
        for j in range(indo.shape[1]):
            if i < 299:
                indo[i][j] = np.asarray([39, 53,245])
            else:
                indo[i][j] = np.asarray([255, 255, 255])
    cv2.imshow('Indonesia Flag', indo)

def janpan():
    """
    Quốc kì của Nhật
    :return:
    """
    circle = np.zeros((600, 800, 3), dtype=np.uint8)
    cv2.rectangle(circle, (0, 0), (800, 600), (255, 255, 255), -1)
    cv2.circle(circle, (399, 299), 100, (0, 0, 255), -1)
    cv2.imshow('Indonesia Flag', circle)

def guyana_flag():
    """
    Quốc kì nước Guyana
    :return:
    """
    guyana = np.zeros((600, 800, 3), dtype=np.uint8)
    # hinh chu nhat mau Xanh
    cv2.rectangle(guyana, (0, 0), (800, 600), (109, 161, 29), -1)
    # ve duong mau trang
    white_line = np.array([[0,0],[800, 299],[0,600]],np.int32)
    cv2.polylines(guyana,[white_line],True,(255,255,255), 5)
    # ve mau vang
    yellow = np.array([[0,0],[790, 299],[0,600]],np.int32)
    cv2.fillPoly(guyana, pts = [yellow], color =(74, 247,236))
    # black
    black_line = np.array([[0,0],[399,299],[0,600]],np.int32)
    cv2.polylines(guyana,[black_line],True,(0,0,0),7)
    # ve mau do
    red = np.array([[0,0],[395,299],[0,600]],np.int32)
    cv2.fillPoly(guyana, pts=[red], color =(7,7,138))
    cv2.imshow('Indonesia Flag', guyana)


# indo_flag()
# janpan()
guyana_flag()
cv2.waitKey(0)
cv2.destroyAllWindows()