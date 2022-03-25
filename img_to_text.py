import cv2
import matplotlib.pyplot as plt
import pytesseract
import PIL
import numpy as np
import config

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 1)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def iterative_levenshtein(s, t):
    if s == ''or t == '':
        return max(len(s), len(t))

    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for i in range(1, rows):
        dist[i][0] = i

    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
 
    return dist[row][col]

def image_to_text(filepath, track=False):
    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Remove noise
    # img_bin = cv2.medianBlur(img_bin, 5)
    # img_bin = dilate(img_bin)
    
    # Tesseract OCR
    custom_config = r'--psm 11'
    res = pytesseract.image_to_string(img_bin, lang='vie', config=custom_config)
    
    if track:
        cv2.imshow('', img)
        cv2.waitKey()

        cv2.imshow('', img_bin)
        cv2.waitKey()

   
    return res

def find_closest_subject(text, SUBJECTS_DATABASE):
    res_subject, res_distance = '', len(text)
    for subject in SUBJECTS_DATABASE:
        min_distance = len(subject)
        for line in text.splitlines():
            line = ''.join([i for i in line if not (i.isdigit() or i == '.')])
            line = line.strip()
            tmp_distance = iterative_levenshtein(line.upper(), subject.upper())
            min_distance = min(min_distance, tmp_distance)
        if min_distance < res_distance:
            res_subject, res_distance = subject, min_distance
        
    return res_subject, res_distance

def find_grade(text, GRADES_DATABASE):
    for line in text.splitlines():
        for grade in GRADES_DATABASE[::-1]:
            if grade in line:
                return grade
    return '0'
        


if __name__ == '__main__':
    text = image_to_text('images_success_grade/toan_2.png', track=True)
    print(text)
    # print(find_grade(text, config.GRADES))
    # print(find_closest_subject(text, config.SUBJECTS))