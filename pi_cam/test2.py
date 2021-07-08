from RPIO import PWM
from time import sleep
servo1 = PWM.Servo()

servo1.set_servo(17, 1200)
sleep(4)
servo1.stop_servo(17)