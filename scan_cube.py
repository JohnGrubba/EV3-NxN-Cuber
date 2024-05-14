import cv2

cords = {
    4: [
        [247, 136], [294, 136], [339, 136], [384, 136],
        [247, 177], [294, 177], [339, 177], [384, 177],
        [247, 218], [294, 218], [339, 218], [384, 218],
        [247, 260], [294, 260], [339, 260], [384, 260],
    ],
    5: [
        [241, 134], [280, 134], [314, 134], [349, 134], [390, 134],
        [241, 165], [280, 165], [314, 165], [349, 165], [390, 165],
        [241, 195], [280, 195], [314, 195], [349, 195], [390, 195],
        [241, 226], [280, 226], [314, 226], [349, 226], [390, 226],
        [241, 264], [280, 264], [314, 264], [349, 264], [390, 264]
    ]
}

def process_image(image: cv2.Mat, cube_size: int, debug_mode: bool = False):
    md_img = cv2.medianBlur(image, 1)
    # Get RGB of all the cords depending on cube size
    cords_cube = cords.get(cube_size)
    if not cords_cube:
        raise Exception("Unsupported Cube")
    clrs = []
    for cord in cords_cube:
        clrs.append(list(md_img[cord[1], cord[0]]))
        cv2.circle(image, (cord[0], cord[1]), 5, (0, 0, 255), -1)
    return (image, clrs)

if __name__ == "__main__":
    # Take photo of cube using opencv with webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    prcsd = process_image(frame, 5, True)
    cv2.imwrite("./images/img.png", prcsd[0])
    print(prcsd[1])
