# Create Pictures with cam in a loop

import cv2
import os

# Create a directory to save the pictures
if not os.path.exists('data'):
    os.makedirs('data')

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Create a loop to take pictures
for x in range(100):
    input(f"Hit Enter for {x} picture")
    ret, frame = cap.read()
    cv2.imwrite('data/{}.png'.format(x), frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break