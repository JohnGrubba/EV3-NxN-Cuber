import ev3_dc as ev3
from move_cube import (
    flip_cube,
    grab_cube,
    turn_side,
    release_cube,
    reset,
    turn_cube,
    lower_cube,
    raise_cube,
    turn_side_inverted,
    flip_and_grab,
    flip2_and_grab
)
from scan_cube import process_image
from solver import solve_cube_from_string
import cv2
from sklearn.cluster import KMeans
from cube_corr import fix_colors

CUBE_SIZE = 4

# Connect to EV3
my_ev3 = ev3.EV3(protocol=ev3.USB)

print(my_ev3.battery)
debug_colors = False

# Motors and Sensors
turntable = ev3.Motor(ev3.PORT_A, ev3_obj=my_ev3)
tower = ev3.Motor(ev3.PORT_B, ev3_obj=my_ev3)
flipper = ev3.Motor(ev3.PORT_C, ev3_obj=my_ev3)
turntable_sensor = ev3.Color(ev3.PORT_4, ev3_obj=my_ev3)
# start_sensor = ev3.Touch(ev3.PORT_3, ev3_obj=my_ev3)

# while not start_sensor.touched:
#    continue

# Don't make those mfs lock position
# reset(turntable, turntable_sensor)
turntable.stop(brake=False)
flipper.stop(brake=False)
tower.stop(brake=False)
input("Hit Enter to set Motors")
turntable.position = 0
flipper.position = 0
tower.position = 0


def get_side_colors(file_ext:str = "") -> list:
    # Take photo of cube using opencv with webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    prcsd = process_image(frame, CUBE_SIZE)
    cv2.imwrite(f"./images/img{file_ext}.png", prcsd[0])
    return prcsd[1]


def find_color_groups(colors):
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(colors)
    labels = kmeans.labels_
    groups = [[] for _ in range(6)]
    for i, label in enumerate(labels):
        groups[label].append(i + 1)
    output = []
    for color in colors:
        for i, group in enumerate(groups):
            if colors.index(color) + 1 in group:
                output.append(str(i + 1))
    return output


def scan_cube():
    # Scan Cube
    # Top
    up = get_side_colors("up")
    if debug_colors:
        input("Press Enter to continue...")
    flip_cube(flipper)
    # Front
    front = get_side_colors("front")
    if debug_colors:
        input("Press Enter to continue...")
    flip_cube(flipper)
    # Down
    down = get_side_colors("down")
    if debug_colors:
        input("Press Enter to continue...")
    flip_cube(flipper)
    # Back
    back = get_side_colors("back")[::-1]
    if debug_colors:
        input("Press Enter to continue...")
    flip_cube(flipper)
    flip_cube(flipper)

    turn_cube(turntable)
    flip_cube(flipper)
    turn_cube(turntable, -1)

    # Left
    left = get_side_colors("left")
    if debug_colors:
        input("Press Enter to continue...")
    turn_cube(turntable, -1)
    flip_cube(flipper)
    flip_cube(flipper)
    turn_cube(turntable, 1)
    # Right
    right = get_side_colors("right")

    cube_list = up + right + front + down + left + back
    # Find Color Groups
    colors_numbers = "".join(find_color_groups(cube_list))
    print(colors_numbers)
    cube_str = (
        colors_numbers.replace("1", "F")
        .replace("2", "D")
        .replace("3", "L")
        .replace("4", "B")
        .replace("5", "R")
        .replace("6", "U")
    )
    print(cube_str)
    cube_str = fix_colors(cube_str)
    print(cube_str)
    return cube_str


# Turn Side function
def execute_move(move: str):
    # We don't need to flip the cube to do this move
    # Should we lower the cube?
    if "w" in move:
        lower_cube(tower)
    if "2" in move:
        # Grab the cube before turning
        turn_side(turntable, CUBE_SIZE, 2)
    else:
        if "'" in move:
            turn_side_inverted(turntable, CUBE_SIZE, -1)
        else:
            turn_side(turntable, CUBE_SIZE, 1)

    # Release Cube
    release_cube(flipper)
    # Should we raise it again?
    if "w" in move:
        raise_cube(tower)


if __name__ == "__main__":
    cube_str = ""
    # Reset the Turntable
    # Other things have to be manually reset for now
    # reset(turntable, turntable_sensor)
    scanned = scan_cube()
    solution = solve_cube_from_string(scanned)

    # Reset Cube to original Position
    turn_cube(turntable, 2)
    flip_cube(flipper)
    turn_cube(turntable, -1)

    # The cubes initial state
    cube = ["U", "R", "F", "D", "L", "B"]
    #        0    1    2    3    4    5

    def back_to_down(iterations: int = 1):
        for _ in range(iterations):
            up, back, down, front = cube[0], cube[5], cube[3], cube[2]
            cube[5], cube[3], cube[2], cube[0] = up, back, down, front
        if iterations == 2: flip2_and_grab(flipper)
        if iterations == 1: flip_and_grab(flipper)

    def solve_turn_cube(n=1):
        if n >= 1:
            for _ in range(n):
                left, front, back, right = cube[4], cube[2], cube[5], cube[1]
                cube[1], cube[5], cube[4], cube[2] = front, right, back, left
            turn_cube(turntable, n)
        elif n == -1:
            left, front, back, right = cube[4], cube[2], cube[5], cube[1]
            cube[1], cube[5], cube[4], cube[2] = back, left, front, right
            turn_cube(turntable, -1)

    # Solve Cube
    for move in solution:
        print(move)
        if cube[3] in move:
            print("I can directly do this move")
            grab_cube(flipper)
            execute_move(move)
        else:
            # We still have to position the cube correctly
            wanted_side = move[0]
            print(f"We have {cube[3]} at the bottom and want to side {wanted_side}")
            if cube[0] == wanted_side:
                back_to_down(2)
            if cube[1] == wanted_side:
                solve_turn_cube(), back_to_down()
            if cube[2] == wanted_side:
                solve_turn_cube(2), back_to_down()
            if cube[4] == wanted_side:
                solve_turn_cube(-1), back_to_down()
            if cube[5] == wanted_side:
                back_to_down()
            # CUBE IS ALREADY GRABBED
            execute_move(move)

    # Lock Motors
    turntable.stop(brake=True)
    flipper.stop(brake=True)
    tower.stop(brake=True)
    print("Program Finished")
