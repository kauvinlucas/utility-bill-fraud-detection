import numpy as np
import cv2

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    """Function to apply brightness and contrast to an image"""
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

def find_best_contours(image):
    """Function to find the best contour to obtain a top-down view of the image"""
    # Output image
    output_image = image.copy()

    # Define len and contour with min len
    len_contour_area = 99999999
    contours_with_min_len = 0

    # Iterate over brightness
    for brightness in range(0, 100, 10):
        # Apply brightness
        gray = apply_brightness_contrast(image.copy(), brightness = brightness, contrast = 127)

        # Adaptive Threshold
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        _, edges = cv2.threshold(gray, 200, 255, cv2.THRESH_TRIANGLE)

        # Find Contours
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)

        # Save contour with min len
        if len(largest_contour) < len_contour_area and len(largest_contour) > 100:
            len_contour_area = len(largest_contour)
            contours_with_min_len = largest_contour
        print("The brightness", brightness, "and constrat 127 minimizes the lenth of the list of contour to", len_contour_area)

    # If len_contour_area > 1000, draw rectangle instead of contour
    if len_contour_area > 2000:
        x, y, w, h = cv2.boundingRect(contours_with_min_len)
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("Applying rectangle instead of contour")
        screenCnt = np.array([[[x, y]], [[x + w, y]], [[x,y+h]], [[x+w,y+h]]])

    # If len_contour_area < 1000, draw contour
    else:
        peri = cv2.arcLength(contours_with_min_len, True)
        screenCnt = cv2.approxPolyDP(contours_with_min_len,  0.02*peri, True)
        print("Applying approximated contour")
        cv2.drawContours(output_image, [screenCnt], -1, (0, 255, 0), 2)
    return screenCnt, output_image, gray

def order_points(pts):
    """Function to obtain a consistent order of the points in the image"""
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    """Function to obtain a top-down view of the image via Perspective Transform"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
