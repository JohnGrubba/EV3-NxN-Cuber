import cv2
import numpy as np
import math
from itertools import combinations

# Read Locations
with open("coords.txt", "r") as f:
    coords = f.read().splitlines()
    coords = [tuple([int(i) for i in x.split(",")]) for x in coords]

colors = {
    "R": [(0, 0, 100), (100, 100, 255)],
    "G": [(0, 50, 0), (120, 240, 120)],
    "B": [(70, 0, 0), (255, 120, 120)],
    "Y": [(0, 120, 124), (120, 255, 255)],
    "O": [(0, 50, 150), (140, 140, 255)],
    "W": [(100, 100, 100), (250, 250, 250)],
}


def closest(color, colors):
    # Get the color name and value of the closest color
    color_name = min(
        colors,
        key=lambda x: math.sqrt(sum((a - b) ** 2 for a, b in zip(color, colors[x][0]))),
    )
    return color_name


def get_squares(image, color):
    # Get color range
    lower = np.array(colors[color][0])
    upper = np.array(colors[color][1])
    # Create mask
    mask = cv2.inRange(image, lower, upper)

    # Clean up mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=10)
    mask = cv2.dilate(mask, kernel, iterations=11)

    res = cv2.bitwise_and(image, image, mask=mask)

    cv2.imwrite("./images/" + color + "-mask.png", res)
    return res


def process_image(image: cv2.Mat, cube_size: int):
    normalizedImg = np.zeros((800, 800))
    image = cv2.normalize(image, normalizedImg, 0, 255, cv2.NORM_MINMAX)
    # COPIED STUFF
    imgs = []
    for color in colors.keys():
        imgs.append(get_squares(image, color))
    result = None
    # Loop through all images in the imgs list
    for img in imgs:
        # If the result is None, set it to be the current image
        if result is None:
            result = img
        # Otherwise, add the current image to the result
        else:
            result = cv2.addWeighted(result, 1, img, 1, 0)

    # Convert the result to grayscale
    amongus = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    amongus = cv2.GaussianBlur(amongus, (25, 25), 5)

    # Threshold the image
    amongus = cv2.threshold(amongus, 0, 255, cv2.THRESH_BINARY)[1]

    # Line Segment Detection
    detector = cv2.createLineSegmentDetector(0, 0.3, 3)
    lines = detector.detect(amongus)[0]

    cv2.imwrite("./images/lines.png", amongus)

    paralell_lines = []
    min_len = 10000
    max_len = 0
    # Draw lines on the image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        mini = min(x1, x2)
        maxi = max(x1, x2)
        if mini < maxi - 80:
            if length > 150:
                cv2.line(result, (x1, y1), (x2, y2), (0, 255, 255), 2)
                paralell_lines.append((int(max(x1, x2)), int(y1)))
                max_len = max(max_len, length)
                min_len = min(min_len, length)
    print(len(paralell_lines))
    first_x = min(paralell_lines[0][0], paralell_lines[1][0])
    second_x = max(paralell_lines[1][0], paralell_lines[0][0])

    first_y = min(paralell_lines[0][1], paralell_lines[1][1])
    second_y = max(paralell_lines[1][1], paralell_lines[0][1])

    # Side Line
    cv2.line(
        result,
        (first_x, first_y),
        (second_x, second_y),
        (0, 255, 255),
        2,
    )

    diff_y = max(paralell_lines[0][1], paralell_lines[1][1]) - min(
        paralell_lines[0][1], paralell_lines[1][1]
    )
    middl_len = (max_len + min_len) / 2
    # Get Circles with colors. Use right Line as anchor
    right_top = (first_x, paralell_lines[0][1])
    for i in range(cube_size):
        for j in range(cube_size):
            x = (
                right_top[0]
                - int(i * (middl_len / cube_size))
                - int((middl_len / cube_size) / 2)
            )
            y = (
                right_top[1]
                - int(j * (diff_y / cube_size))
                - int((diff_y / cube_size) / 2)
            )
            print("Drawing Circle at: ", x, y)
            cv2.circle(result, (x, y), 5, (0, 255, 0), -1)

    return (result, "")


if __name__ == "__main__":
    # Take photo of cube using opencv with webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    prcsd = process_image(frame, 4)
    cv2.imwrite("./images/img.png", prcsd[0])
