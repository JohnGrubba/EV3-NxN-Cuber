import ev3_dc as ev3


def flip_cube(flipper: ev3.Motor, speed: int = 25):
    flipper.move_by(500, speed=speed, brake=True).start(thread=False)
    flipper.move_by(-140, speed=speed, brake=True).start(thread=False)


def grab_cube(flipper: ev3.Motor, speed: int = 25):
    flipper.move_by(140, speed=speed, brake=True).start(thread=False)


def release_cube(flipper: ev3.Motor, speed: int = 25):
    flipper.move_by(-140, speed=speed, brake=True).start(thread=False)


def turn_cube(turntable: ev3.Motor, n: int = 1, speed: int = 50):
    turntable.move_by(n * 630, speed=speed, brake=True).start(thread=False)


def turn_side(turntable: ev3.Motor, n: int = 1, speed: int = 100, overturn: int = 230):
    turntable.move_by(n * 630 + overturn, speed=speed, brake=True).start(thread=False)
    turntable.move_by(-overturn, speed=speed, brake=True).start(thread=False)


def turn_side_inverted(
    turntable: ev3.Motor, n: int = -1, speed: int = 100, overturn: int = 230
):
    turntable.move_by(n * 630 - overturn, speed=speed, brake=True).start(thread=False)
    turntable.move_by(+overturn, speed=speed, brake=True).start(thread=False)


def lower_cube(tower: ev3.Motor, speed: int = 50):
    tower.move_by(-110, speed=speed, brake=True).start(thread=False)


def raise_cube(tower: ev3.Motor, speed: int = 50):
    tower.move_by(110, speed=speed, brake=True).start(thread=False)


def reset(turntable: ev3.Motor, turntable_sensor: ev3.Color):
    turntable.start_move(speed=15, direction=-1)

    while not turntable_sensor.reflected > 20:
        continue
    turntable.stop(brake=True)
    turntable.move_by(237).start(thread=False)
