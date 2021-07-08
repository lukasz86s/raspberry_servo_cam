from RPi import GPIO as gpio
import pigpio
import time


pi = pigpio.pi('0.0.0.0', 6555)

class Sprinkler():
    def __init__(self, pump_pin=20, valve_pin=21 ):
        self.gpio = pi
        self.pump_pin = pump_pin
        self.valve_pin = valve_pin
        
    def init_gpio(self):
        self.gpio.set_mode(self.pump_pin, pigpio.OUTPUT)
        self.gpio.write(self.pump_pin, 0)
        
        self.gpio.set_mode(self.valve_pin, pigpio.OUTPUT)
        self.gpio.write(self.valve_pin, 0)
    
    def pump_ON(self):
        self.gpio.write(self.pump_pin, 1)
        
    def pump_OFF(self):
        self.gpio.write(self.pump_pin, 0)
        
    def valve_ON(self):
        self.gpio.write(self.valve_pin, 1)
        
    def valve_OFF(self):
        self.gpio.write(self.valve_pin, 0)
    
    def spray(self):
        self.pump_ON()
        time.sleep(4)
        self.pump_OFF()
        self.valve_ON()
        time.sleep(4)
        self.valve_OFF()
        

        

class MoveCamera():
    BOTH = 3
    def __init__(self, servo_horizontal = 27, servo_vertical = 17):
        gpio.setwarnings(False)
        
        self.dc_horizontal = 1500
        self.dc_vertical = 1500
        #gpio.setmode(gpio.BCM) # set mode to the gpio pins numbers
        #gpio.setup(servo_horizontal, gpio.OUT)
        self.servo_horizontal = servo_horizontal  # set pin for horizontal move
        self.servo_vertical = servo_vertical # set pin for vertical move
        #create instance to controll pwm
        self.pwm = pi
        self.start_pwm()     

        
    def start_pwm(self, pwm_nr=BOTH ):
        if pwm_nr & 1:
            self.pwm.set_servo_pulsewidth(self.servo_horizontal, 1500)
        if pwm_nr & 2:
            self.pwm.set_servo_pulsewidth(self.servo_vertical, 1500)
            
    
    def stop_pwm(self, pwm_nr=BOTH):
        if pwm_nr & 1:
            self.pwm.set_servo_pulsewidth(self.servo_horizontal, 0)
        if pwm_nr & 2:
            self.pwm.set_servo_pulsewidth(self.servo_vertical, 0)
        
    def update_pwm(self, pwm_nr=BOTH):
        if pwm_nr & 1:
            self.pwm.set_servo_pulsewidth(self.servo_horizontal, self.dc_horizontal)
        if pwm_nr & 2:
            self.pwm.set_servo_pulsewidth(self.servo_vertical, self.dc_vertical)
            
    def add_to_pwm(self, direction, value=50):

        if direction == 'right' and self.dc_horizontal > 1000:
            self.dc_horizontal -= value
        elif direction == 'left' and self.dc_horizontal < 2100:
            self.dc_horizontal += value
            
        elif direction == 'up' and self.dc_vertical > 1000:
            self.dc_vertical -= value
        elif direction == 'down' and self.dc_vertical < 2000 :
            self.dc_vertical += value
        if direction == "right" or direction == "left": 
            self.update_pwm(1)
        else:
            self.update_pwm(2)

        

if __name__ == ("__main__"):
    import time
    pwm = MoveCamera()
    pwm.start_pwm()
    time.sleep(10)
    pwm.stop_pwm()