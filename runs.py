from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import hub_menu

leftArmMotor = Motor(Port.A)
rightArmMotor = Motor(Port.B)
leftWheelMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
rightWheelMotor = Motor(Port.D)
mapColorSensor = ColorSensor(Port.E)
armColorSensor = ColorSensor(Port.F)

chassis = DriveBase(
    left_motor=leftWheelMotor,
    right_motor=rightWheelMotor,
    wheel_diameter=62.4,
    axle_track=96,
)

chassis.use_gyro(True)
# chassis.distance_control()
def yellow_run():  # Run 3
    chassis.straight(740)
    chassis.drive(18, 0)
    chassis.turn(-65)
    chassis.turn(65)
    chassis.stop()
    chassis.straight(-500)

yellow_run()
