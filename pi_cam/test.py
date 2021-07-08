import pigpio
from time import sleep

pi1 = pigpio.pi('0.0.0.0', 6555)

pi1.set_servo_pulsewidth(17, 1500)
pi1.set_servo_pulsewidth(27, 1500)

sleep(2)
pi1.set_servo_pulsewidth(17, 0)
pi1.set_servo_pulsewidth(27, 0)



