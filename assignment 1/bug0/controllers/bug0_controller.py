"""bug_0_controller controller."""

from controller import Supervisor
import sys
import numpy as np
import math
from assign1_Q1 import distance_between_points

supervisor = Supervisor()
def robot(supervisor):
    timestep = 32
    destination = [0,2,0]
    start_point = [0.5,-1,0]
    
    node = supervisor.getFromDef("e-puck")
    
    left_motor=supervisor.getDevice("left wheel motor")
    right_motor=supervisor.getDevice("right wheel motor")
    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    trans_field = node.getField("translation")
    rot_field = node.getField("rotation")
 
    sonar = []
    ps_val = []
    for i in range(8):
        ps_num = f"ps{str(i)}"
        sonar.append(supervisor.getDevice(ps_num))
        sonar[i].enable(timestep)
        ps_val.append(0)
        
    while supervisor.step(timestep) != -1:
        for i, s in enumerate(sonar):
            ps_val[i] = s.getValue()
            # print('ps_val[0] *************************************',ps_val[0] )
 
        trans_values = trans_field.getSFVec3f()
        rot_values = rot_field.getSFRotation()
        current_angle = rot_values[2]*(rot_values[3])
      
        target_angle = (np.arctan((destination[1] - trans_values[1])/(destination[0] - trans_values[0])))  #Change this slope
        # print('target_angle _____:' ,target_angle)
        
        hit_wall = (ps_val[0] >= 78 or ps_val[7] >= 78 or ps_val[2] >= 78)
        p1 = (trans_values[0],trans_values[1])
        if distance_between_points(destination, p1) < 0.1:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            print("!!! Target reached !!!")
        else:
            if not hit_wall:
                if (trans_values[0]<0.0 and trans_values[1]<=0.0):
                    rot_angle=target_angle
                    # print(rot_angle, target_angle)
                    print('moving towards target')
                    if (np.abs(rot_angle-current_angle)>0.1):
                        left_speed=-6.28*0.25
                        right_speed=6.28*0.25
                    else:
                        left_speed=6.28*0.5
                        right_speed=6.28*0.5
                
                elif (trans_values[0]<0.0 and trans_values[1]>0.0):
                    # print(target_angle)
                    
                    rot_angle=target_angle
                    # print(rot_angle, current_angle)
                    if (np.abs(rot_angle-current_angle)>0.1):
                        left_speed=-6.28*0.25
                        right_speed=6.28*0.25
                    else:
                        left_speed=6.28*0.5
                        right_speed=6.28*0.5
                        print('move_to_target')
                elif (trans_values[0]>0.0 and trans_values[1]>0.0):
                    rot_angle=target_angle-3.14
                    # print(rot_angle, current_angle)
                    if (np.abs(rot_angle-current_angle)>0.1):
                        print('elif1')
                        left_speed=-6.28*0.25
                        right_speed=6.28*0.25
                    else:
                        left_speed=6.28*0.5
                        right_speed=6.28*0.5
                        print('else_elif1')
                elif (trans_values[0]>0.0 and trans_values[1]<0.0):
                    rot_angle=3.14+target_angle
                    # print(rot_angle, current_angle)
                    print('moving_towards_target')
                    if (np.abs(rot_angle-current_angle)>0.1):
                        left_speed=-6.28*0.25
                        right_speed=6.28*0.25
                    else:
                        left_speed=6.28*0.5
                        right_speed=6.28*0.5
           
            else:
                print('obstacle')
                if ps_val[0] >= 78 or ps_val[7] >= 78:
                    print('turn_left')
                    left_speed = -6.28 * 0.25
                    right_speed = 6.28 * 0.25
                elif ps_val[2] >= 78 and ps_val[0] < 78 and ps_val[7] < 78:
                    print('wall_follow')
                    left_speed = 6.28 * 0.75
                    right_speed = 6.28 * 0.75
     
            left_motor.setVelocity(left_speed)
            right_motor.setVelocity(right_speed)
            pass
    

robot(supervisor)
        
            
