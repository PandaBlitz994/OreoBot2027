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


def turn_to(angle, margain_of_error: int = 1, vel_margain: int = 1, max_time: int = 3000):
    bias_p = 4
    bias_d = 0.5
    bias_const = 14

    last_error = ((angle - hub.imu.heading() + 180) % 360) - 180
    time = StopWatch()
    last_time = time.time()
    error = last_error
    while (error > margain_of_error or hub.imu.angular_velocity() > 1 and time.time()<max_time):
        error = ((angle - hub.imu.heading() + 180) % 360) - 180
        current_time = time.time()
        time_diff = last_time-current_time
        time_diff=0.01 if time_diff==0 else time_diff
        d_error = (last_error-error)/time_diff
        float; turn_rate = d_error*bias_d+error*bias_p
        if turn_rate>0:
            turn_rate+=bias_const
        else:
            turn_rate-=bias_const

        last_time=time
        last_error=error
        chassis.drive(0, turn_rate)

def drive_pid_time(speed, time, angle: float = hub.imu.heading(), margain_of_error: int = 1, vel_margain: int = 1):
    bias_p = 4
    bias_d = 0.5
    bias_const = 14

    last_error = ((angle - hub.imu.heading() + 180) % 360) - 180
    time = StopWatch()
    last_time = time.time()
    error = last_error
    while (error > margain_of_error or hub.imu.angular_velocity() > 1 and time.time()>time):
        error = ((angle - hub.imu.heading() + 180) % 360) - 180
        current_time = time.time()
        time_diff = last_time-current_time
        time_diff=0.0001 if time_diff==0 else time_diff
        d_error = (last_error-error)/time_diff
        turn_rate = d_error*bias_d+error*bias_p
        if turn_rate>0:
            turn_rate+=bias_const
        else:
            turn_rate-=bias_const

        last_time=time
        last_error=error
        chassis.drive(speed, turn_rate)

def drive_to_color(speed, color):
    chassis.drive(speed, 0)
    while map_color_sensor.color!=color(True):
            print(map_color_sensor.color(True))
    chassis.stop()

# chassis.distance_control()
def yellow_run():  # Run 3
    hub.imu.reset_heading(0)
    chassis.drive(18, 0)
    chassis.straight(770)
    chassis.stop()
    drive_time(50, 5, 2000)
    turn_to(0)
    chassis.stop()
    drive_pid_time(-500, 3500)
    chassis.straight(100)
    chassis.turn(33.33, wait=False)
    drive_to_color(200, Color.NONE)
    turn_to(-85)
    drive_time(200, -3, 1500)
    chassis.drive(200, 2)
    left_arm_motor.run_time(500, 3000)
    chassis.stop()
    chassis.straight(-75)
    chassis.turn(-33.33, wait=False)
    chassis.drive(-1000, 0)

def black_run():
    chassis.straight(-520)
    chassis.curve(-110, -80)
    drive_time(-300, 767)
    chassis.straight(125)
    chassis.turn(80)
    chassis.curve(67, -90)
    drive_time(300, 676)
    chassis.straight(-130)
    chassis.turn(150)
    drive_time(400, 800)
    wait(2000)
    drive_time(-300, 1000)


def red_run():
    chassis.straight(500)
    right_arm_motor.run_time(-400, 2000)
    chassis.straight(-75)
    chassis.turn(49)
    chassis.straight(400)
    chassis.turn(-40)

def run():
    menu = hub_menu("#", "1", "2", "3", "4", "5", "6")
    if menu=="#":
        color = arm_color_sensor.color(True)
        hsv = arm_color_sensor.hsv(True)
        hub.light.on(color)
        print(color)
        print(hsv)
        if color==Color.YELLOW:
            yellow_run()
        elif color==Color.NONE:
            black_run()
        elif color==Color.RED:
            red_run()
    elif menu == "3":
        yellow_run()
    elif menu == "4":
        black_run()
    elif menu == "5":
        red_run()
run()