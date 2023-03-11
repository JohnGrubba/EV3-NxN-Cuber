import cv2
import numpy as np
import math
from itertools import combinations

# Read Locations
with open("coords.txt", "r") as f:
    coords = f.read().splitlines()
    coords = [tuple([int(i) for i in x.split(",")]) for x in coords]

light = 160

colors_dict = {
    (3, 20, light): "B",
    (0, light, 6): "G",
    (light, 12, 29): "R",
    (light, light, light / 3): "Y",
    (light, light, light): "W",
    (light, light / 2, 50): "O",
}


def closest(color, colors_dict):
    # Color is a tuple of (r, g, b)
    # colors_dict is a dictionary of colors with (r,g,b) as key and color name as value
    # Returns the closest color name to the given color
    return colors_dict[
        min(colors_dict, key=lambda x: sum((a - b) ** 2 for a, b in zip(color, x)))
    ]


def get_fix_points(image: cv2.Mat):
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Create default parametrization LSD
    lsd = cv2.createLineSegmentDetector(0, 1, 50, 1, 20)

    # Detect lines in the image
    lines = list(lsd.detect(grayimg)[0])
    real_lines = []
    for line, i in zip(lines, range(len(lines))):
        difx = max(line[0][0], line[0][2]) - min(line[0][0], line[0][2])
        dify = max(line[0][1], line[0][3]) - min(line[0][1], line[0][3])
        lens = math.sqrt(difx**2 + dify**2)
        if lens > 100:
            real_lines.append(
                [(int(line[0][0]), int(line[0][1])), (int(line[0][2]), int(line[0][3]))]
            )
            cv2.line(
                image,
                (int(line[0][0]), int(line[0][1])),
                (int(line[0][2]), int(line[0][3])),
                (0, 0, 255),
                3,
            )
    print(real_lines)
    return image


def process_image(image: cv2.Mat):
    # COPIED STUFF

    # MY STUFF
    side_list = []
    side_str = ""
    print("NEW SIDE ------------------")
    for piece in coords:
        x = piece[0]
        y = piece[1]
        w = 20
        h = 20
        b, g, r = image[y, x]
        clst = closest([r, g, b], colors_dict)
        side_list.append(tuple[r, g, b])
        side_str += clst
        # print([r, g, b])
        cv2.putText(
            image, str(clst), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        cv2.rectangle(
            image,
            (x - 10, y - 10),
            (x + 10, y + 10),
            tuple([int(b), int(g), int(r)]),
            2,
        )
    return (image, side_str)
