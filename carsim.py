import math as m
import numpy as np
import matplotlib.pyplot as plt

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

# What we are given: center point of the back axle of the moving car: movecar_axlept
# D = length of the parking space: parkspace_len
# 4 coordinates of the two cars we want to park between: frontcar_up, frontcar_down, backcar_up, backcar_down
# Steering angle: steer_ang

# X0 = position of movecar_axlept when the back of the cars are aligned
# X1 = position of movecar_axlept when the back axle and the back of the front car are aligned

def get_turn_radius(steer_ang):
	return 1 / m.tan(steer_ang) # this is in radians

def temp(parkspace_len, turn_radius): 
	theta = m.asin(parkspace_len/ (2 * turn_radius))
	arc_length = theta * turn_radius
	print "PARK SPACE LEN: ", parkspace_len
	print "TURN RADIUS: ", turn_radius
	print "THETA: ", theta
	print "ARC LENGTH: ", arc_length

def plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down):
	x = [movecar_axlept.x, frontcar_up.x, frontcar_down.x, backcar_up.x, backcar_down.x]
	y = [movecar_axlept.y, frontcar_up.y, frontcar_down.y, backcar_up.y, backcar_down.y]
	plt.plot(x,y, 'ro')
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.xlim(-5, 8)
	plt.ylim(-1, 15)
	plt.show()


if __name__ == "__main__": # main function
	turn_radius = get_turn_radius(m.pi/9)
	movecar_axlept = Coordinate(5,10)
	frontcar_up = Coordinate(5,5)
	frontcar_down = Coordinate(5,.1)
	backcar_up = Coordinate(0,5)
	backcar_down = Coordinate(0,.1)

	c1 = Coordinate(movecar_axlept, move_axlept - turn_radius)
	
	parkspace_len = frontcar_up.x - backcar_up.x

	# plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down)
	temp(parkspace_len, turn_radius)