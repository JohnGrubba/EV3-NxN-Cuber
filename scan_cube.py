import cv2
import numpy as np

colors = {
    "R": [(0, 0, 100), (80, 80, 255)],
    "G": [(0, 80, 0), (120, 240, 120)],
    "B": [(50, 0, 0), (255, 150, 150)],
    "Y": [(0, 130, 150), (130, 255, 255)],
    "O": [(0, 50, 110), (100, 180, 255)],
    "W": [(100, 100, 100), (250, 250, 250)],
}


def get_squares(image, color, debug_mode=False):
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

    if debug_mode:
        cv2.imwrite("./images/" + color + "-mask.png", res)
    return res


def process_image(image: cv2.Mat, cube_size: int, debug_mode: bool = False):
    image = cv2.convertScaleAbs(image, alpha=1, beta=0)
    cv2.imwrite("./images/cube.png", image)
    unprocessed_img = image.copy()
    normalizedImg = np.zeros((800, 800))
    image = cv2.normalize(image, normalizedImg, 0, 255, cv2.NORM_MINMAX)

    # COPIED STUFF
    imgs = []
    for color in colors.keys():
        imgs.append(get_squares(image, color, debug_mode))
    result = None
    # Loop through all images in the imgs list
    for img in imgs:
        # If the result is None, set it to be the current image
        if result is None:
            result = img
        # Otherwise, add the current image to the result
        else:
            result = cv2.addWeighted(result, 1, img, 1, 0)
    cv2.imwrite("./images/all_merged.png", result)
    # Copy Pasta
    result = cv2.erode(result, np.ones((5, 5), np.uint8), iterations=3)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 75)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    sharpen = cv2.erode(sharpen, np.ones((5, 5), np.uint8), iterations=4)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)
    close = cv2.bitwise_not(close)
    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]

    min_area = 40000
    max_area = 65000
    res_colors = None
    for c in cnts:
        area = cv2.contourArea(c)
        print(area)
        if area > min_area and area < max_area:
            x, y, w, h = cv2.boundingRect(c)
            result = unprocessed_img[y : y + h, x : x + w]
            res_colors = result.copy()
            # cv2.rectangle(result, (x, y), (x + w, y + h), (36, 255, 12), 2)
    if res_colors is None:
        exit("No cube found")
    side_color_list = []
    idx = 0
    for i in range(1, cube_size + 1):
        for j in range(1, cube_size + 1):
            width = result.shape[1]
            height = result.shape[0]
            x = int(width / 4 * j) - int(width / 8)
            y = int(height / 4 * i) - int(height / 8)
            side_color_list.append(tuple(res_colors[y, x])[::-1])
            result = cv2.circle(result, (x, y), 5, (255, 255, 255), -1)
            cv2.putText(
                result,
                str(idx),
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            idx += 1

    return (result, side_color_list)


if __name__ == "__main__":
    # Take photo of cube using opencv with webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    prcsd = process_image(frame, 4, True)
    cv2.imwrite("./images/img.png", prcsd[0])
    print(prcsd[1])
