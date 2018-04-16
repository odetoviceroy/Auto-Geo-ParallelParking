import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


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

def get_theta(parkspace_len, turn_radius):
	return m.pi + m.asin(parkspace_len/ (2 * turn_radius))

def get_middlept(parkspace_len, turn_radius, c1): 
	theta = get_theta(parkspace_len, turn_radius)
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

def gen_xy_vals(c, center_flag, theta, turn_radius):
	time = [x*0.2 for x in range(0, 100)]
	theta_list = []
	x_vals = []
	y_vals = []
	for t in time:
		theta_list.append(t * (theta)/10)
	if(center_flag == 1):
		for i in range(0, len(theta_list)):
			if(theta_list[i] <= theta and theta_list[i] >= m.pi/2):
				x_vals.append(c.x + turn_radius * m.cos(theta_list[i]))
				y_vals.append(c.y + turn_radius * m.sin(theta_list[i]))
	if(center_flag == 2):
		for i in range(0, len(theta_list)):
			if(theta_list[i] >= theta + m.pi/3 and theta_list[i] <= 2 * m.pi):
				x_vals.append(c.x + turn_radius * m.cos(theta_list[i]))
				y_vals.append(c.y + turn_radius * m.sin(theta_list[i]))

	return [x_vals, y_vals]    

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

def c2_x(turn_radius, xm, xf):
	radsq = turn_radius * turn_radius
	q = m.sqrt(((xf.x - xm.x) * (xf.x - xm.x)) + ((xf.y - xm.y) * (xf.y - xm.y)))
	x3 = (xf.x + xm.x) / 2
	return x3 - m.sqrt(radsq - ((q / 2) * (q / 2))) * ((xm.y - xf.y) / q)

def c2_y(turn_radius, xm, xf):
	radsq = turn_radius * turn_radius
	q = m.sqrt(((xf.x - xm.x) * (xf.x - xm.x)) + ((xf.y - xm.y) * (xf.y - xm.y)))
	y3 = (xf.y + xm.y) / 2
	return y3 - m.sqrt(radsq - ((q / 2) * (q / 2))) * ((xf.x-xm.x) / q)

fig = plt.figure()
ax = plt.axes(xlim = (-8,8), ylim = (-8,8))
N = 2
points = ax.plot(*([[], []]*N), color = 'green', linestyle ='--', marker = 'o')

patch = patches.Rectangle((0, 0), 0, 0, fc='y')

def trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals):
	FINALX_VALS = []
	FINALY_VALS = []
	for point in arc1x_vals:
		FINALX_VALS.append(point)
	for i in range(len(arc2x_vals) - 1, -1, -1):
		FINALX_VALS.append(arc2x_vals[i])

	for point in arc1y_vals:
		FINALY_VALS.append(point)
	for i in range(len(arc2y_vals) - 1, -1, -1):
		FINALY_VALS.append(arc2y_vals[i])

	return [FINALX_VALS, FINALY_VALS]

def animate(i, FINALX_VALS, FINALY_VALS):
    points[0].set_data([0],[0])
    points[1].set_data([FINALX_VALS[i], FINALY_VALS[i]])
    return points

def init():
	for line in points:
		line.set_data([],[])
	return points

patch = patches.Rectangle((0, 0), 0, 0, fc='y')

ex = [0, 1, 3]
why = [0, 1, 4]

yaw = [0.0, 0.7,1.7]

def init2():
	ax.add_patch(patch)
	return patch,

def animate2(i):
	patch.set_width(1.2)
	patch.set_height(1.0)
	patch.set_xy([ex[i], why[i]])
	patch._angle = -np.rad2deg(yaw[i])
	return patch,


if __name__ == "__main__": # main function
	turn_radius = get_turn_radius(m.pi/9)
	movecar_axlept = Coordinate(4,10)
	frontcar_up = Coordinate(4,5)
	frontcar_down = Coordinate(4,.1)
	backcar_up = Coordinate(0,5)
	backcar_down = Coordinate(0,.1)

	c1 = Coordinate(movecar_axlept.x, movecar_axlept.y - turn_radius)


	parkspace_len = frontcar_up.x - backcar_up.x

	xm = get_middlept(parkspace_len, turn_radius, c1)
	xf = Coordinate(0,(backcar_up.y - backcar_down.y) /2)

	c2 = Coordinate( c2_x(turn_radius,xm,xf), c2_y(turn_radius,xm,xf) )

	plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down, c1)

	[x_vals, y_vals] = robot_draw_circle(turn_radius, c1)

	[x_vals2, y_vals2] = robot_draw_circle(turn_radius, c2)

	theta = get_theta(parkspace_len, turn_radius)
	[arc1x_vals, arc1y_vals] = gen_xy_vals(c1, 1, theta, turn_radius)

	[arc2x_vals, arc2y_vals] = gen_xy_vals(c2, 2, theta, turn_radius)

	[FINALX_VALS, FINALY_VALS] = trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals)

	#plt.plot(x_vals,y_vals, 'bo')
	#plt.plot(x_vals2,y_vals2, 'bo')

	plt.plot([xm.x],[xm.y], "ko")
	plt.plot([xf.x],[xf.y], "ko")

	plt.plot([c1.x],[c1.y], "mo")
	plt.plot([c2.x],[c2.y], "mo")

	'''
	plt.plot([arc1x_vals],[arc1y_vals], "m+")
	plt.plot([arc2x_vals],[arc2y_vals], "m+")
	'''

	plt.plot([FINALX_VALS],[FINALY_VALS], "m+")

	plt.xlabel('X')
	plt.ylabel('Y')

	total_len = len(arc1x_vals) + len(arc2x_vals)
	print "LEN(ARC1X_VALS)", len(arc1x_vals), "\nLEN(ARC2X_VALS):", len(arc2x_vals)

	ani = animation.FuncAnimation(fig, animate, init_func=init, frames= total_len, fargs = (
		FINALX_VALS,
		FINALY_VALS,
		), interval=100, blit=True)

	anim = animation.FuncAnimation(fig, func = animate2,
		init_func=init2,
		frames=50,
		interval=500,
		blit=True)
	plt.show()

