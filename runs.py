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




def run_by_color():
    reset()
    acolor = arm_color_sensor.color()
    ahsv = arm_color_sensor.hsv()


    if arm_color_sensor.color(True) == Color.BLUE:
        hub.display.number(1)
        hub.light.on(ahsv)
        run1()
    elif arm_color_sensor.color(True) == Color.GREEN:
        hub.display.number(2)
        hub.light.on(ahsv)
        run2()
    elif arm_color_sensor.color(True) == Color.YELLOW:
        hub.display.number(3)
        hub.light.on(ahsv)
        run3()
    elif arm_color_sensor.color() == Color.RED:
        hub.display.number(4)
        hub.light.on(ahsv)
        run4()
    elif arm_color_sensor.color() == Color.NONE:
        hub.display.number(5)
        hub.light.on(ahsv)
        black_run()
    elif arm_color_sensor.color(True) == Color.WHITE:
        hub.display.number(6)
        hub.light.on(ahsv)
        run6()




def turn_time(time, turn_rate):
    chassis.drive(0, turn_rate)
    wait(time)
    chassis.stop()




def drive_time(speed, turn_rate, time):
    chassis.drive(speed, turn_rate)
    wait(time)
    chassis.stop()


def turn_to(angle, margain_of_error: int = 1, vel_margain: int = 1):
    bias_p = 4
    bias_d = 0.5
    bias_const = 14

    last_error = ((angle - hub.imu.heading() + 180) % 360) - 180
    time = StopWatch()
    last_time = time.time()
    error = last_error
    while error > margain_of_error or hub.imu.angular_velocity() > 1:
        error = ((angle - hub.imu.heading() + 180) % 360) - 180
        current_time = time.time()
        d_error = (last_error-error)/(last_time-current_time)
        turn_rate = d_error*bias_d+error*bias_p
        if turn_rate>0:
            turn_rate+=bias_const
        else:
            turn_rate-=bias_const

        last_time=time
        last_error=error
        chassis.drive(0, turn_rate)

# chassis.distance_control()
def yellow_run():  # Run 3
    hub.imu.reset_heading(0)
    chassis.straight(770)
    chassis.drive(18, 0)
    turn_time(2300, -300)
    turn_to(0)
    chassis.stop()
    drive_time(-500, -3, 3000)
    chassis.straight(100)




# yellow_run()




def black_run():
    chassis.straight(-600)
    # chassis.curve(-110, 45)
    chassis.curve(-110, -80)
    drive_time(-200, 767)
    chassis.straight(115)
    chassis.turn(20)
    chassis.curve(200, -55)
    drive_time(300, 676)
    chassis.straight(-130)
    chassis.turn(150)
    drive_time(400, 800)
    wait(2000)
    drive_time(-300, 1000)




# black_run()


def run_by_color():
    print(arm_color_sensor.color())
    print(arm_color_sensor.hsv())
    hub.imu.reset_heading(0)
    right_arm_motor.stop()
    left_arm_motor.stop()
    acolor = arm_color_sensor.color()
    ahsv = arm_color_sensor.hsv()




    if arm_color_sensor.color(True) == Color.BLACK:
        hub.display.number(1)
        hub.light.on(ahsv)
        black_run()
    elif arm_color_sensor.color() == Color.YELLOW:
        hub.display.number(5)
        hub.light.on(ahsv)
        yellow_run()


if Button.CENTER in hub.buttons.pressed():
    print(color_sensor.color())

hub.imu.reset_heading(0)
gyro_turn(90)
# turn_to(90)
wait(1000)
print(hub.imu.heading())