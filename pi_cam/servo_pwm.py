from RPi import GPIO as gpio

import time


class MoveCamera():
    BOTH = 3
    def __init__(self, servo_horizontal = 27, servo_vertical = 17, period=50):
        gpio.setwarnings(False)
        self.delay = 2
        self.dc_horizontal = 8.0
        self.dc_vertical = 8.0
        gpio.setmode(gpio.BCM) # set mode to the gpio pins numbers
        gpio.setup(servo_horizontal, gpio.OUT)
        gpio.setup(servo_vertical, gpio.OUT)
        self.servo_horizontal = 27 # set pin for horizontal move
        self.servo_vertical = 17 # set pin for vertical move
        self.counter = self.delay

        self.pwm_horizontal = gpio.PWM(servo_horizontal,period)
        self.pwm_vertical = gpio.PWM(servo_vertical, period)
        self.start_pwm()
        self.stop_servo()


        
    def stop_servo(self):
        gpio.setup(self.servo_horizontal, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.servo_vertical, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        
    def start_pwm(self, pwm_nr=BOTH ):
        if pwm_nr & 1:
            self.pwm_horizontal.start(self.dc_horizontal)
        if pwm_nr & 2:
            self.pwm_vertical.start(self.dc_vertical)
    
    def stop_pwm(self, pwm_nr=BOTH):
        if pwm_nr & 1:
            self.pwm_horizontal.stop()
        if pwm_nr & 2:
            self.pwm_vertical.stop()
        
    def update_pwm(self, pwm_nr=BOTH):
        if pwm_nr & 1:
            self.pwm_horizontal.ChangeDutyCycle(self.dc_horizontal)
        if pwm_nr & 2:
            self.pwm_vertical.ChangeDutyCycle(self.dc_vertical)
            
    def add_to_pwm(self, direction, value=1):

        if direction == 'right' and self.dc_horizontal > 5:
            self.dc_horizontal -= value
            gpio.setup(self.servo_horizontal, gpio.OUT)
        if direction == 'left' and self.dc_horizontal < 10:
            self.dc_horizontal += value
            gpio.setup(self.servo_horizontal, gpio.OUT)
            
        if direction == 'up' and self.dc_vertical > 5:
            self.dc_vertical -= value
            gpio.setup(self.servo_vertical, gpio.OUT)
        if direction == 'down' and self.dc_vertical < 11 :
            self.dc_vertical += value
            gpio.setup(self.servo_vertical, gpio.OUT)
            
        if self.dc_vertical > 5 and self.dc_vertical < 11 and self.dc_horizontal >5 and self.dc_horizontal < 10 :
            self.counter = self.delay
        #if direction == "right" or direction ==  "left":
            #gpio.setup(self.servo_horizontal, gpio.OUT)
        #if direction == "up" or direction ==  "down":
            #gpio.setup(self.servo_vertical, gpio.OUT)
        self.update_pwm()
        #self.th = Thread(target=self.wait_to_stop)
        #self.th.start()
        

if __name__ == ("__main__"):
    import time
    pwm = MoveCamera()
    pwm.start_pwm()
    time.sleep(10)
    pwm.stop_pwm()