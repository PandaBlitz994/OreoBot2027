from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import hub_menu
import math

hub = PrimeHub()


left_arm_motor = Motor(Port.A)
right_arm_motor = Motor(Port.B)
left_wheel_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
right_wheel_motor = Motor(Port.D)
map_color_sensor = ColorSensor(Port.E)
arm_color_sensor = ColorSensor(Port.F)


# Color.BLACK = Color(220, 7, 15)
# Color.WHITE = Color(0, 0, 100)
# Color.RED = Color(352, 91, 78)
# Color.YELLOW = Color(51, 70, 98)
# Color.BLUE = Color(216, 87, 62)


# arm_color_sensor.detectable_colors([Color.BLACK, Color.WHITE, Color.RED, Color.YELLOW, Color.BLUE, Color.GRAY])


chassis = DriveBase(
    left_motor=left_wheel_motor,
    right_motor=right_wheel_motor,
    wheel_diameter=62.4,
    axle_track=96,
)


chassis.use_gyro(True)
chassis.settings(700)


def reset():
    global skip_done
    print(arm_color_sensor.color())
    print(arm_color_sensor.hsv())
    # This function uses the arm color sensor to automatically start its run.
    # Reset the heading of the robot.
    hub.imu.reset_heading(0)
    right_arm_motor.stop()
    left_arm_motor.stop()


def turn_time(time, turn_rate):
    chassis.drive(0, turn_rate)
    wait(time)
    chassis.stop()


def drive_time(speed, time, turn_rate: int = 0):
    chassis.drive(speed, turn_rate)
    wait(time)
    chassis.stop()


def turn_to(
    angle, margain_of_error: int = 1, vel_margain: int = 1, max_time: int = 3000
):
    bias_p = 4
    bias_d = 0.5
    bias_const = 14

    last_error = ((angle - hub.imu.heading() + 180) % 360) - 180
    time = StopWatch()
    last_time = time.time(1)
    error = last_error
    while (
        error > margain_of_error
        or hub.imu.angular_velocity() > 1
        and time.time() < max_time
    ):
        error = ((angle - hub.imu.heading() + 180) % 360) - 180
        current_time = time.time()
        time_diff = last_time - current_time
        time_diff = 0.01 if time_diff == 0 else time_diff
        d_error = (last_error - error) / time_diff
        float
        turn_rate = d_error * bias_d + error * bias_p
        if turn_rate > 0:
            turn_rate += bias_const
        else:
            turn_rate -= bias_const

        last_time = time
        last_error = error
        chassis.drive(0, turn_rate)


def drive_pid_time(
    speed,
    time,
    angle: float = hub.imu.heading(),
    margain_of_error: int = 1,
    vel_margain: int = 1,
):
    bias_p = 4
    bias_d = 0.5
    bias_const = 14

    last_error = ((angle - hub.imu.heading() + 180) % 360) - 180
    time = StopWatch()
    last_time = time.time()
    error = last_error
    while (
        error > margain_of_error
        or hub.imu.angular_velocity() > 1
        and time.time() > time
    ):
        error = ((angle - hub.imu.heading() + 180) % 360) - 180
        current_time = time.time()
        time_diff = last_time - current_time
        time_diff = 0.0001 if time_diff == 0 else time_diff
        d_error = (last_error - error) / time_diff
        turn_rate = d_error * bias_d + error * bias_p
        if turn_rate > 0:
            turn_rate += bias_const
        else:
            turn_rate -= bias_const

        last_time = time
        last_error = error
        chassis.drive(speed, turn_rate)


def drive_to_color(speed, color):
    chassis.drive(speed, 0)
    while map_color_sensor.color != color(True):
        print(map_color_sensor.color(True))
    chassis.stop()


def drive_to_black(speed):
    chassis.drive(speed, 0)
    while map_color_sensor.reflection() > 12:
        print(map_color_sensor.hsv(True))
    chassis.stop()


def drive_to_blue(speed):
    chassis.drive(speed, 0)
    onBlue = False
    while not onBlue:
        print(map_color_sensor.hsv(True))
        if (
            190 < map_color_sensor.hsv(True).h < 210
            and 55 < map_color_sensor.hsv(True).s < 70
            and 70 < map_color_sensor.hsv(True).v < 90
        ):
            onBlue = True


# chassis.distance_control()
def yellow_run():  # Run 3
    chassis.settings(250)
    chassis.straight(600)
    chassis.turn(-9)
    chassis.straight(-800)
    # drive_time(200, 2750)
    # drive_time(200, 4250)
    chassis.straight(200)
    print(hub.buttons.pressed())
    while hub.buttons.pressed() != [Button.BLUETOOTH]:
        wait(1)
    print("Continue")
    chassis.arc(600, 1500)
    # chassis.settings(200)
    # chassis.drive(0, -45)
    # wait(1250)
    # drive_time(100, 500)
    # drive_time(-200, 250)
    # chassis.turn(-90, absolute=True)
    # # chassis.drive(0, -20)
    # wait(1000)
    # chassis.settings(350)
    # drive_time(-425, 3000)
    # chassis.straight(450)


def black_run():
    chassis.use_gyro(True)
    hub.imu.reset_heading(0)
    chassis.settings(straight_acceleration=200)
    chassis.straight(-580)
    left_arm_motor.run_time(6000, 1500)
    chassis.arc(-110, -80)
    chassis.straight(-200)
    left_arm_motor.run_time(-1250, 1500)
    chassis.straight(215)
    chassis.turn(-40, absolute=True)
    chassis.straight(55)
    print(hub.imu.heading())
    chassis.turn(-160, absolute=True)
    print(hub.imu.heading())
    drive_time(200, 2000)
    left_arm_motor.run_time(1670, 1500, wait=False)
    right_arm_motor.run_time(-850, 10000)
    left_arm_motor.run_time(-2100, 1000, wait=False)
    chassis.straight(-100)
    chassis.arc(700, -90)


def green_run():
    chassis.arc(450, 80)
    chassis.straight(80)
    chassis.turn(0, absolute=True)
    chassis.settings(150)
    chassis.straight(300)
    right_arm_motor.run_time(300, 2000)
    chassis.straight(-200)
    chassis.arc(300, -25)


def red_run():
    menu = hub_menu("S", ">", "X")
    while hub!="X":
        if menu=="S":
            hub.imu.reset_heading(0)
            chassis.settings(straight_acceleration=300)
            chassis.straight(600)
            drive_time(-1000, 2000)
            chassis.straight(50)
        elif menu==">":
            chassis.straight(500)
            right_arm_motor.run_time(-550, 1510)
            right_arm_motor.run_time(-500, 100, wait=False)
            chassis.straight(-100)
            chassis.straight(30)
            chassis.turn(45, absolute=True)
            chassis.straight(150)
            drive_to_black(300)
            chassis.straight(100)
            left_arm_motor.run_angle(300, -200)
            left_arm_motor.run_angle(140, 200, wait=False)
            chassis.straight(300)
            left_arm_motor.run_angle(300, -450)
            left_arm_motor.run_angle(140, 200)
            chassis.arc(650, 80)
            exit()
    menu = hub_menu("S", ">", "X")


def alt_yellow_run():
    drive_time(200, 500)
    chassis.straight(-20)
    chassis.turn(45)
    chassis.turn(-45)
    chassis.settings(straight_speed=320, turn_rate=10)
    drive_to_blue(500)
    chassis.straight(250)
    drive_to_blue(100)
    # drive_to_blue(300)
    chassis.stop()
    left_arm_motor.run_time(-1000, 2000, wait=False)
    turn_time(1000, -35)
    # chassis.straight(900, then=Stop.COAST)
    # chassis.straight(-30)
    # # chassis.turn(35, wait=False)
    # # chassis.arc(-50, 45, wait=False)
    # left_arm_motor.run_time(-1000, 4500)
    # chassis.turn(-30)
    # chassis.straight(50)
    # chassis.settings(300, 300, 500, 300)
    # chassis.turn(-45)
    # chassis.straight(85)
    # chassis.turn(15)
    # drive_time(-300, 4000)
    # # chassis.arc(50, -45, wait=False)
    # # drive_time(200, 500)
    # # chassis.settings(300, 300, 300)
    # # chassis.turn(-50)
    # # chassis.straight(50)
    # # chassis.turn(50)
    # # drive_time(-300, 4000)


def blue_run():
    # right_arm_motor.run_angle(500, 360)
    # drive_time(300, 4000)
    # chassis.straight(-55)
    # right_arm_motor.run_angle(500, -300)
    # chassis.straight(70)
    # right_arm_motor.run_time(-5000, 5000)
    
    isTrapped=False
    left_arm_motor.run(100)
    time = StopWatch()
    time.reset(); time.resume()
    while not isTrapped:
        current_load=left_arm_motor.load()
        print("Load: ", current_load, "mNm | time: ", time.time(), "ms")
        if time.time() > 1000 or abs(current_load)>55:
            isTrapped=True
    left_arm_motor.brake()
    print("Halted!")



def run():
    menu = hub_menu("#", "1", "2", "3", "4", "5", "6")
    if menu == "#":
        color = arm_color_sensor.color(True)
        hsv = arm_color_sensor.hsv(True)
        print(color)
        print(hsv)
        hub.light.on(color)
        if color == Color.BLUE:
            blue_run()
        # elif color==color.GREEN:
        #     green_run()
        elif color == Color.YELLOW:
            yellow_run()
        elif color == Color.RED:
            red_run()
        elif color == Color.NONE:
            black_run()
        # elif color==color.WHITE:
        #     hub.light.on(WHITE)
        #     white_run()
    elif menu == "1":
        blue_run()
    elif menu == "3":
        alt_yellow_run()
    elif menu == "4":
        black_run()
    elif menu == "5":
        red_run()


run()
