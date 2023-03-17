# Author: @julikober


def fix_colors(cube):
    pieces = [cube[i * 16 : i * 16 + 16] for i in range(0, 6)]
    print(pieces)

    # pattern: URFDLB

    corners = []

    corners.append((pieces[0][0], pieces[4][0], pieces[5][3]))
    corners.append((pieces[0][12], pieces[2][0], pieces[4][3]))
    corners.append((pieces[0][3], pieces[5][0], pieces[1][3]))
    corners.append((pieces[0][15], pieces[1][0], pieces[2][3]))
    corners.append((pieces[3][0], pieces[4][15], pieces[2][12]))
    corners.append((pieces[3][3], pieces[2][15], pieces[1][12]))
    corners.append((pieces[3][12], pieces[5][15], pieces[4][12]))
    corners.append((pieces[3][15], pieces[1][15], pieces[5][12]))

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

    return cube
