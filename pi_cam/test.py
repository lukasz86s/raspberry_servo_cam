import pigpio
from gpiozero import Servo
from time import sleep

pi1 = pigpio.pi('0.0.0.0', 6555)

#servo1 = Servo(17)
#servo2 = Servo(27)

#servo1.min()
#servo2.value = 0.2
pi1.set_servo_pulsewidth(17, 1500)
pi1.set_servo_pulsewidth(27, 1500)

sleep(2)
pi1.set_servo_pulsewidth(17, 0)
pi1.set_servo_pulsewidth(27, 0)


#servo2.max()
#servo1.max()

