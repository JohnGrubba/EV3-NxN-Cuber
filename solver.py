from rubikscubennnsolver.RubiksCube222 import RubiksCube222
from rubikscubennnsolver.RubiksCube333 import RubiksCube333
from rubikscubennnsolver.RubiksCube444 import RubiksCube444
from rubikscubennnsolver.RubiksCube555 import RubiksCube555
import logging
from math import sqrt


def solve_cube_from_string(inp_str: str, order: str = "URFDLB"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(filename)25s:%(lineno)d %(levelname)8s: %(message)s",
    )

    # Replace colors with readable letters by our solver
    inp_str = (
        inp_str.replace("G", "F").replace("Y", "D").replace("O", "L").replace("W", "U")
    )

    # Get Size of cube
    size = int(sqrt((len(inp_str) / 6)))

    # Currently Implemented Cubes
    if size == 2:
        cube = RubiksCube222(
            inp_str,
            order,
            None
        )
    if size == 3:
        cube = RubiksCube333(
            inp_str,
            order,
            None
        )
    if size == 4:
        cube = RubiksCube444(
            inp_str,
            order,
            None,
        )
    if size == 5:
        cube = RubiksCube555(
            inp_str,
            order,
            None,
        )
    # Output the current cube
    cube.print_cube("Initial Cube")
    cube.sanity_check()
    cube.solve([])
    solution = [x for x in cube.solution if "COMMENT" not in x]
    print(len(solution))
    print(solution)
    return solution


if __name__ == "__main__":
    solve_cube_from_string(
        "UUURRRUUUULUUDRLRUULRULFFURDDFDFLLRLFLRUBFFRURBUUUFRRD"
    )
