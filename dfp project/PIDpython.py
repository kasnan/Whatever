'''
Kp : 목표점 도달에 이용하는 계수
Ki : 목표점의 도달에 정밀성, 즉 목표점과의 오차를 좁히기 위한 계수
Kd : 목표점의 도달과정에서 오버슛, 즉 목표점을 초과해 나오는 목표점과의 오차를 좁이기 위한 계수

'''

from pid_module import PID
import time

de = 0.0
dt = 0.0
tolerance = 0.01
dt_sleep = 0.001

error = 0.0
error_prev = 0.0

time_prev = 0.0

#initialize a new pid controller class
pidinst = PID()

targetVelo = pidinst.getTarget()
currentVelo = 0 #GetData From Sensor Later

time_prev = time.time()

while True:
    
    #Get current velocity from sensor
    currentVelo = 10

    #Get difference
    error = targetVelo - currentVelo
    
    #Gap of error & time
    de = error-error_prev
    dt = time.time() - time_prev

    #Get control PID value
    control = pidinst.getKp()*error + pidinst.getKd()*de/dt + pidinst.getKi()*error*dt
    print("control: "+str(control))

    #Set new error & time previous value
    error_prev = error
    time_prev = time.time()

    #Control Part
    #IO.output(controlPin, control >= 0)
    #p.ChangeDutyCycle(min(abs(control), 100))
    

    #if abs(error) <= tolerance:
    #    IO.output(dirPin, control >= 0)
    #    p.ChangeDutyCycle(0)
    #    break

    #pause for constant time gap
    time.sleep(dt_sleep)