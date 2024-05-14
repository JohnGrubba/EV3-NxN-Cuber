def get_cube_str_pos(cube_size: int, face: str, side_idx: int) -> int:
    if side_idx > cube_size**2:
        raise ValueError("You are changing face with this side_idx")
    face_idxes = {
        "U": 0,
        "R": 1,
        "F": 2,
        "D": 3,
        "L": 4,
        "B": 5,
    }
    return ((cube_size**2) * face_idxes[face]) + side_idx


def list_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    missing_in_list2 = set1 - set2
    extra_in_list2 = set2 - set1

    if len(missing_in_list2) == 1 and len(extra_in_list2) == 1:
        return [extra_in_list2.pop(), missing_in_list2.pop()]
    else:
        return []


def fix_colors(kcs: str, depth: int = 1):
    print(f"Fixing Iteration {depth}")
    cube_size = int((len(kcs) // 6) ** 0.5)
    print("Cube Size: ", cube_size, "x", cube_size)
    lt = 0
    rt = cube_size - 1
    lb = (cube_size**2) - cube_size
    rb = cube_size**2 - 1
    correct_corners = [
        ["U", "R", "B"],
        ["U", "F", "L"],
        ["U", "L", "F"],
        ["U", "B", "R"],
        ["D", "R", "F"],
        ["D", "F", "L"],
        ["D", "L", "B"],
        ["D", "B", "R"],
    ]
    # Get the corners of the cube
    corners = [
        [
            kcs[get_cube_str_pos(cube_size, "U", lt)],
            kcs[get_cube_str_pos(cube_size, "L", lt)],
            kcs[get_cube_str_pos(cube_size, "B", rt)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "U", lb)],
            kcs[get_cube_str_pos(cube_size, "F", lt)],
            kcs[get_cube_str_pos(cube_size, "L", rt)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "U", rt)],
            kcs[get_cube_str_pos(cube_size, "B", lt)],
            kcs[get_cube_str_pos(cube_size, "R", rt)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "U", rb)],
            kcs[get_cube_str_pos(cube_size, "R", lt)],
            kcs[get_cube_str_pos(cube_size, "F", rt)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "D", lt)],
            kcs[get_cube_str_pos(cube_size, "L", rb)],
            kcs[get_cube_str_pos(cube_size, "F", lb)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "D", rt)],
            kcs[get_cube_str_pos(cube_size, "F", rb)],
            kcs[get_cube_str_pos(cube_size, "R", lb)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "D", lb)],
            kcs[get_cube_str_pos(cube_size, "B", rb)],
            kcs[get_cube_str_pos(cube_size, "L", lb)],
        ],
        [
            kcs[get_cube_str_pos(cube_size, "D", rb)],
            kcs[get_cube_str_pos(cube_size, "R", rb)],
            kcs[get_cube_str_pos(cube_size, "B", lb)],
        ],
    ]
    # ----------------
    print(corners)
    layer = []
    color = corners[0][0]

    for corner in corners:
        if color in corner:
            corner = corner[corner.index(color) :] + corner[: corner.index(color)]
            for piece in layer:
                if piece[2] == corner[1]:
                    layer.insert(layer.index(piece) + 1, corner)
                    break
            else:
                layer.append(corner)

    original_colors = [layer[0][0], layer[0][1], layer[1][1], layer[2][1], layer[3][1]]
    # add missing color
    original_colors.insert(3, list(set("URFDLB") - set(original_colors))[0])
    cube = kcs
    cube = cube.replace(original_colors[0], "u")
    cube = cube.replace(original_colors[1], "r")
    cube = cube.replace(original_colors[2], "f")
    cube = cube.replace(original_colors[3], "d")
    cube = cube.replace(original_colors[4], "l")
    cube = cube.replace(original_colors[5], "b")

    cube = cube.replace("u", "U")
    cube = cube.replace("r", "R")
    cube = cube.replace("f", "F")
    cube = cube.replace("d", "D")
    cube = cube.replace("l", "L")
    cube = cube.replace("b", "B")
    # --------------
    return cube


# FIRST 16 are U SIDE
# RDBB  0 1 2 3
# FRLF  4 5 6 7
# RFBD  8 9 10 11
# BFLD  12 13 14 15

# SECOND 16 are R SIDE
# FBDF  16 17 18 19
# DBLF  20 21 22 23
# LRBU  24 25 26 27
# ULRL  28 29 30 31

# THIRD 16 are F SIDE
# FBUU  32 33 34 35
# BLFR  36 37 38 39
# DDUF  40 41 42 43
# DLLL  44 45 46 47

# FOURTH 16 are D SIDE
# RFRF  48 49 50 51
# RDRU  52 53 54 55
# DFUB  56 57 58 59
# URRR  60 61 62 63

# FIFTH 16 are L SIDE
# DUUD  64 65 66 67
# DUUL  68 69 70 71
# BBDF  72 73 74 75
# RRBB  76 77 78 79

# SIXTH 16 are B SIDE
# LDUU  80 81 82 83
# BRLU  84 85 86 87
# FFDL  88 89 90 91
# BLUL  92 93 94 95
