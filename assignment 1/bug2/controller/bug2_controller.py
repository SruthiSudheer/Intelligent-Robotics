"""bug2_controller controller."""

from controller import Supervisor
from math import sqrt
import numpy as np
from sympy import Point, Line,Segment
# from assign1_Q1 import distance_between_points, distance_from_point_to_line
supervisor = Supervisor()

def distance_between_points(p1,p2):
    p1 = Point(p1)
    p2 = Point(p2)
    distance = sqrt(((p1[0]-p2[0])**2 )+ ((p1[1]-p2[1])**2))
    return distance
def distance_from_point_to_line(x, p1, p2):
    seg = Segment(p1, p2)    
    return seg.distance(x) 
       
def on_line(trans_values, start_point, destination, threshold=0.02):   
    distance = distance_from_point_to_line(trans_values, start_point, destination)
    if distance > threshold:
          return False
    else:
          return True
          
def desired_orientation():
    if trans_values[0] < 0: #merge below if-else
        if trans_values[1] < 0:
            desired_angle = target_angle
        else:
            desired_angle = target_angle
    else :
        if trans_values[1] > 0:
            desired_angle = target_angle-3.14            
        else :
            desired_angle = target_angle+3.14
           
    return desired_angle
    
def robot(supervisor):
    global destination,start_point
    timestep = 32
    destination = [2.5,-0.8,0]
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
        global trans_values
        global target_angle
        trans_values = trans_field.getSFVec3f()
        rot_values = rot_field.getSFRotation()
        print('rot_values',rot_values)
        current_angle = rot_values[2]*(rot_values[3])
        
        target_angle = (np.arctan((destination[1] - start_point[1])/(destination[0] - start_point[0])))  #Change this slope
        # print('target_angle _____:' ,target_angle)
        hit_wall = (ps_val[0] >= 78 or ps_val[7] >= 78 or ps_val[2] >= 78)        
        
        # print('ps_val[2]*************************',ps_val[2])
        # print('ps_val[0]*****================',ps_val[0])
        # print('ps_val[1]*****',ps_val[1])
        # print('ps_val[7]*****================',ps_val[7])
        
        line_follow = on_line(trans_values, start_point, destination, threshold=0.02)
        # print('line_follow:',line_follow)
        p1 = (trans_values[0],trans_values[1])
        desired_angle = desired_orientation()
        if distance_between_points(destination, p1) < 0.1:
            left_motor.setVelocity(0)
            right_motor.setVelocity(0)
            print("!!! Target reached !!!")
        else:
            if not hit_wall:  # maintains the line
                if np.abs(desired_angle - current_angle) < 0.1 :
                    right_speed= 6.28
                    left_speed = 6.28 
                # elif (trans_values[0]<0.0 and trans_values[1]<=0.0):
                   
                # elif np.abs(desired_angle - current_angle) > 0.1 :
                else:    
                    # If the difference of desired angle and z_theta value is significant we need to rotate
                        print('line_to_goal')
                        print('desired_angle:',desired_angle)
                        print('current_angle:',current_angle)
                        if desired_angle>current_angle:
                            left_speed = -6.28 * 0.25
                            right_speed = 6.28 * 0.25
                        else :
                            right_speed= -6.28 * 0.25
                            left_speed = 6.28 * 0.25
                   
                              
                # elif ps_val[2] < 78 and ps_val[0] < 78 or ps_val[7] < 78: 
                #     print('corner')
                #     left_speed = 6.28 * 0.25  
                #     right_speed = -6.28 * 0.25    
                
                # if (trans_values[0]<0.0 and trans_values[1]<=0.0):
                        # rot_angle=target_angle
                        # print(rot_angle, target_angle)
                        # print('moving towards target') # here line follow function
                        
                        # if (np.abs(rot_angle-current_angle)>0.1):
                            # left_speed=-6.28
                            # right_speed=6.28
                            # print('moving towards target **** if')
                        # else:
                            # print('moving towards target //// else')
                            # left_speed=6.28
                            # right_speed=6.28
            else: 
                print('obstacle')
                while desired_angle != current_angle:           
                
                    if ps_val[0] >= 78 or ps_val[7] >= 78:
                        print('turn_left')
                        left_speed = -6.28 * 0.25
                        right_speed = 6.28 * 0.25
                    # print('ps_val[2]*************************',ps_val[2])
                    # print('ps_val[0]*****================',ps_val[0])
                    # print('ps_val[7]*****================',ps_val[7])
    
                    elif ps_val[2] >= 78 and ps_val[0] < 78 or ps_val[7] < 78:
                        print('wall_follow')
                        left_speed = 6.28 * 0.75
                        right_speed = 6.28 * 0.75
                        
                    
                    elif ps_val[2] < 78 and ps_val[0] < 78 or ps_val[7] < 78: 
                        print('corner_after_wall_following')
                        left_speed = 6.28 * 0.25  
                        right_speed = -6.28 * 0.25  
                    
       
                left_motor.setVelocity(left_speed)
                right_motor.setVelocity(right_speed)
                pass
        

robot(supervisor)
