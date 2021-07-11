import cv2
import numpy as np


def get_image():
    """
    Hàm này dùng để đọc ảnh và thay đổi kích thước hiển thị của
    :return:
    """
    img = cv2.imread('6.png')
    copy_image = np.copy(img)
    copy_image = cv2.resize(copy_image, (0, 0), fx=0.3, fy=0.3)
    # print(copy_image.shape)
    return copy_image

def processing_image(copy_image):
    """
    hàm này dùng để xử lý ảnh đầu vào, bao gồm đọc ảnh, thay đổi kích thước, phát hiện biên, giãn những dòng text trong
    :return: ảnh gốc và ảnh có những dòng text bị giãn ra
    """
    copy_img = cv2.cvtColor(copy_image, cv2.COLOR_BGR2GRAY)
    edge_img= cv2.Canny(copy_img,100, 200)

    kernel = np.ones((1,1), dtype=np.uint8)
    erosion = cv2.erode(edge_img, kernel, iterations=1)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    dilation = cv2.dilate(erosion, kernel, iterations=2)

    # cv2.imshow('image', dilation)
    return dilation


def finding_contours(dilation):
    """
    tìm contours của ảnh
    :param dilation: ảnh mà có những dong text đã giãn ra
    :return: contours
    """
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

def draw_tictoe(copy_image):
    """
    hàm này dùng để vẽ ngẫu nhiên 20 dấu tic toe
    :param copy_image:
    :return: ảnh đã vẽ tic toe
    """
    positions = [(np.random.randint(0, 600), np.random.randint(0, 850)) for i in range(20)]
    for pos in positions:
        cv2.drawMarker(copy_image, pos, (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=15,
                       thickness=3, line_type=8)
    cv2.imshow('image', copy_image)
    return positions


def detecting_text(copy_image, contours):
    """
    Hàm này dùng để phát hiện những đoạn text và vẽ boudingbox cho nó
    :param dilation: ảnh mà bên trong có những dòng text bị giãn
    :param copy_image: ảnh được copy từ ảnh gốc
    :return:
    """
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 5000 and area > 100:
            x,y,w,h = cv2.boundingRect(cnt)
            x2, y2 = x+w, y+h
            cv2.rectangle(copy_image, (x,y), (x2, y2), (0,255,0), 3)
    cv2.imshow('image', copy_image)

def detecting_box(copy_image, contours):
    """
    Hàm này dùng để phát hiện những ô trả lời lớn và vẽ contours cho nó
    :param dilation: ảnh mà bên trong có những dòng text bị giãn
    :param copy_image: ảnh được copy từ ảnh gốc
    :return:
    """
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 15000:
            cv2.drawContours(copy_image, cnt, -1, (0, 0, 255), 5)
    cv2.imshow('image', copy_image)


def detect_tictoe(copy_image, contours, positions):
    """
    hàm này dùng để vẽ contours lên các ô trả lời lớn nếu các ô này chứa dấu tictioe
    :param copy_image: ảnh đầu vào
    :param contours: các contour
    :param positions: vị trí của các dấu tictoe
    :return:
    """
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 15000:
            retval = [cv2.pointPolygonTest(cnt, pos, measureDist= False) for pos in positions]
            for each in retval:
                if each > 0:
                    cv2.drawContours(copy_image, cnt, -1, (0, 0, 255), 2)

    cv2.imshow('image', copy_image)



if __name__ == '__main__':
    copy_image = get_image()
    dilation = processing_image(copy_image)
    contours = finding_contours(dilation)
    # detecting_text(dilation, copy_image)
    # box = detecting_box(copy_image, contours)
    positions = draw_tictoe(copy_image)
    detect_tictoe(copy_image, contours, positions)

    cv2.waitKey()
    cv2.destroyAllWindows()