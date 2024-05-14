import ev3_dc as ev3

OVERTURN_VALUES = {4: 240, 5: 220, 3: 340, 2: 350}

def flip_cube(flipper: ev3.Motor, speed: int = 25):
    flipper.move_by(500, speed=speed, brake=True).start().join()
    flipper.move_by(-140, speed=speed, brake=True).start().join()


def grab_cube(flipper: ev3.Motor, speed: int = 30):
    flipper.move_by(140, speed=speed, brake=True).start().join()


def release_cube(flipper: ev3.Motor, speed: int = 30):
    flipper.move_by(-140, speed=speed, brake=True).start().join()


def turn_cube(turntable: ev3.Motor, n: int = 1, speed: int = 100):
    turntable.move_by(n * 630, speed=speed, brake=True).start().join()

def flip_and_grab(flipper: ev3.Motor, speed: int = 30):
    flipper.move_by(500, speed=speed, brake=True).start().join()

def flip2_and_grab(flipper: ev3.Motor, speed:int = 30):
    flipper.move_by(860, speed=speed, brake=True).start().join()

def turn_side(turntable: ev3.Motor, cube_size: int, n: int = 1, speed: int = 100):
    
    if not OVERTURN_VALUES.get(cube_size):
        raise Exception("Unsupported Cube Size in turn side function")
    turntable.move_by(n * 630 + OVERTURN_VALUES[cube_size], speed=speed, brake=True).start().join()
    turntable.move_by(-OVERTURN_VALUES[cube_size], speed=speed, brake=True).start().join()


def turn_side_inverted(
    turntable: ev3.Motor, cube_size: int, n: int = -1, speed: int = 100
):
    if not OVERTURN_VALUES.get(cube_size):
        raise Exception("Unsupported Cube Size in turn side function")
    turntable.move_by(n * 630 - OVERTURN_VALUES[cube_size], speed=speed, brake=True).start().join()
    turntable.move_by(OVERTURN_VALUES[cube_size], speed=speed, brake=True).start().join()


def lower_cube(tower: ev3.Motor, speed: int = 100):
    tower.move_by(-110, speed=speed, brake=True).start().join()


def raise_cube(tower: ev3.Motor, speed: int = 100):
    tower.move_by(110, speed=speed, brake=True).start().join()


def reset(turntable: ev3.Motor, turntable_sensor: ev3.Color):
    turntable.start_move(speed=15, direction=-1)

    while not turntable_sensor.reflected > 20:
        continue
    turntable.stop(brake=True)
    turntable.move_by(237).start().join()

if __name__ == "__main__":
    # Connect to EV3
    my_ev3 = ev3.EV3(protocol=ev3.USB, sync_mode="ASYNC", host="00:16:53:47:27:F4")
    print(my_ev3.host)
    my_ev3.verbosity = 2

    print(my_ev3.battery)
    debug_colors = False

    # Motors and Sensors
    turntable = ev3.Motor(ev3.PORT_A, ev3_obj=my_ev3)
    tower = ev3.Motor(ev3.PORT_B, ev3_obj=my_ev3)
    flipper = ev3.Motor(ev3.PORT_C, ev3_obj=my_ev3)
    turntable_sensor = ev3.Color(ev3.PORT_4, ev3_obj=my_ev3)

    turntable.stop(brake=False)
    flipper.stop(brake=False)
    tower.stop(brake=False)
    turntable.position = 0
    flipper.position = 0
    tower.position = 0

    # reset(turntable, turntable_sensor)
    flip_cube(flipper)

    turntable.stop(brake=False)
    flipper.stop(brake=False)
    tower.stop(brake=False)