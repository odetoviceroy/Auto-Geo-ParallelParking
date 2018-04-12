import math as m
import numpy as np
import matplotlib.pyplot as plt



# What we are given: center point of the back axle of the moving car: movecar_axlept
# D = length of the parking space: parkspace_len
# 4 coordinates of the two cars we want to park between: frontcar_up, frontcar_down, backcar_up, backcar_down
# Steering angle: steer_ang

# X0 = position of movecar_axlept when the back of the cars are aligned
# X1 = position of movecar_axlept when the back axle and the back of the front car are aligned

def get_turn_radius(steer_ang):
	return 1 / m.tan(steer_ang) # this is in radians

def temp(parkspace_len, turn_radius, c1): 
	theta = m.pi + m.asin(parkspace_len/ (2 * turn_radius))
	arc_length = theta * turn_radius
	print "PARK SPACE LEN: ", parkspace_len
	print "TURN RADIUS: ", turn_radius
	print "THETA: ", theta
	print "ARC LENGTH: ", arc_length
	print "END COORDINATE OF C1 (", c1.x, ",", c1.y, ")"


	xm = Coordinate(c1.x + (turn_radius * m.cos(theta)), c1.y + (turn_radius * m.sin(theta) ))
	print "END COORDINATE OF XM: (", xm.x, ", ", xm.y, " )"
	return xm

def plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down, c1):
	x = [movecar_axlept.x, frontcar_up.x, frontcar_down.x, backcar_up.x, backcar_down.x, c1.x]
	y = [movecar_axlept.y, frontcar_up.y, frontcar_down.y, backcar_up.y, backcar_down.x, c1.y]
	plt.plot(x,y, 'ro')
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.autoscale()

def robot_draw_circle(radius, center):
    time = [x*0.2 for x in range(0, 51)]
    theta = []
    x_vals = []
    y_vals = []
    for t in time:
        theta.append(t * (2 * m.pi)/10)
    for i in range(0, len(theta)):
        x_vals.append(center.x + radius * m.cos(theta[i]))
        y_vals.append(center.y + radius * m.sin(theta[i]))

    return [x_vals, y_vals]


if __name__ == "__main__": # main function
	turn_radius = get_turn_radius(m.pi/12)
	movecar_axlept = Coordinate(5,10)
	frontcar_up = Coordinate(5,5)
	frontcar_down = Coordinate(5,.1)
	backcar_up = Coordinate(0,5)
	backcar_down = Coordinate(0,.1)

	c1 = Coordinate(movecar_axlept.x, movecar_axlept.y - turn_radius)

	parkspace_len = frontcar_up.x - backcar_up.x

	xm = temp(parkspace_len, turn_radius, c1)

	plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down, c1)

	[x_vals, y_vals] = robot_draw_circle(turn_radius, c1)

	plt.plot(x_vals,y_vals, 'bo')

	plt.plot([xm.x],[xm.y], "ko")
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.show()

