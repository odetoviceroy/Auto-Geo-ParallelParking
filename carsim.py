import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

from ppobjs import Car
from ppobjs import Coordinate
import utilfuncts as uf
import drawfuncts as df

fig = plt.figure()
ax = plt.axes(xlim = (-2,2), ylim = (-2,2))
ax.set_aspect(1)
	
def gen_xy_vals(center, center_flag, theta, turn_radius):
	theta_list = robot_draw_circle(turn_radius, center, theta)
	x_vals = []
	y_vals = []
	if(center_flag == 1):
		for i in range(0, len(theta_list)):
			#and 
			if(theta_list[i] <= theta and theta_list[i] >= m.pi/2):
				x_vals.append(center.x + turn_radius * m.cos(theta_list[i]))
				y_vals.append(center.y + turn_radius * m.sin(theta_list[i]))
	if(center_flag == 2):
		for i in range(0, len(theta_list)):
			if(theta_list[i] >= theta + m.pi/3 and theta_list[i] <= (2 * m.pi) - (m.pi/9)):
				x_vals.append(center.x + turn_radius * m.cos(theta_list[i]))
				y_vals.append(center.y + turn_radius * m.sin(theta_list[i]))
	return [x_vals, y_vals]    

def init():
	ax.add_patch(patch)
	ax.add_patch(patch2)
	ax.add_patch(patch3)
	return patch, patch2, patch3 

def animate(i, FINALX_VALS, FINALY_VALS, theta, f_bup, f_bdown, b_bup, b_bdown, steer_ang):
	patch.set_xy([FINALX_VALS[i], FINALY_VALS[i]])
	patch2.set_xy([f_bup,f_bdown])
	patch3.set_xy([b_bup,b_bdown])
	#patch._angle = -np.rad2deg(car_ang[i])
	return patch, patch2, patch3

if __name__ == "__main__": # main function
	len_car = .300 # static length of a car
	# ----------- LET'S DEFINE THE COORDINATES OF THE FRONT STATIC CAR -----------
	frontcar = Car(
		Coordinate(0.0,0), Coordinate(0.0,0.0), Coordinate(.75,.50), Coordinate(.75,0.01)
		)

	frontcar.f_up.x = frontcar.b_up.x + len_car
	frontcar.f_down.x = frontcar.b_down.x + len_car
	frontcar.f_up.y = frontcar.b_up.y
	frontcar.f_down.y = frontcar.b_down.y
	# ----------------------------------------------------------------------------
	# ---------- AND NOW THE COORDINATES OF THE BACK STATIC CAR ------------------
	backcar = Car(
		Coordinate(0.0,0.5), Coordinate(0.0,0.01), Coordinate(0.0,0.0), Coordinate(0.0,0.0)
		)
	backcar.b_up.x = backcar.f_up.x - len_car
	backcar.b_down.x = backcar.f_down.x - len_car
	backcar.b_up.y = backcar.f_up.y
	backcar.b_down.y = backcar.f_down.y
	# ----------------------------------------------------------------------------
	parkspace_len =  uf.get_parkspace_len(frontcar, backcar) # DEFINE PARKING SPACE LENGTH
	width_car = frontcar.b_up.y - frontcar.b_down.y
	len_moveto_fup = .1 # LENGTH OF BACK OF MOVING CAR TO FRONT STATIC CAR
	# --------- DEFINE ALL PRELIMINARY COMPUTATIONS OF THE MOVING CAR ------------
	bbotm_coordy = frontcar.b_up.y + len_moveto_fup
	btop_coordy = bbotm_coordy + width_car
	fbotm_coordy = frontcar.f_up.y + len_moveto_fup
	ftop_coordy = fbotm_coordy + width_car
	movecar = Car(
		Coordinate(frontcar.f_up.x,ftop_coordy), Coordinate(frontcar.f_up.x,fbotm_coordy), 
		Coordinate(frontcar.b_up.x,btop_coordy), Coordinate(frontcar.b_up.x,bbotm_coordy)
	)

	lencar_part = len_car / 5.0
	# -----------------------------------------------------------------------------
	# ----------- FIGURE OUT INITIAL COORDINATES OF AXLE MIDPOINTS ----------------
	backaxle_midpt = Coordinate(frontcar.b_up.x + lencar_part, bbotm_coordy + (width_car / 2.0))
	frontaxle_midpt = Coordinate(frontcar.f_up.x - lencar_part, fbotm_coordy + (width_car / 2.0))
	axle_len = frontaxle_midpt.x - backaxle_midpt.x

	dist_backofcar_tobackaxle = lencar_part
	# -----------------------------------------------------------------------------

	# -------------------------SKETCH OUT ORIGINAL PLAN----------------------------
	steer_ang = m.pi / 12.0 # start off with static steer angle

	turn_radius = uf.get_turn_radius(axle_len, steer_ang) # figure out initial turn radius

	err_len = 0.001 # use this to get the closest we can get to the back car

	xf = uf.gen_xf(backcar, err_len, dist_backofcar_tobackaxle, width_car, axle_len) # figure out final position of midbackaxle

	c1 = uf.gen_c1(frontcar, frontaxle_midpt, turn_radius) # generate center of circle 1

	delta_x = uf.gen_delta_x(xf.x, parkspace_len, err_len, dist_backofcar_tobackaxle, axle_len)

	delta_y = uf.gen_delta_y(backaxle_midpt, xf)

	theta = uf.get_theta(delta_x, turn_radius)

	c2 = uf.gen_c2(backcar, err_len, dist_backofcar_tobackaxle, xf, turn_radius, axle_len)
	
	xm = uf.get_middlept(c1, c2)

	print uf.check_arcs_toobig(delta_y, turn_radius)
	# -----------------------------------------------------------------------------
	[c1x, c1y] = df.sketch_circle(c1, turn_radius)
	plt.plot([c1x],[c1y], "bo")
	[c2x, c2y] = df.sketch_circle(c2, turn_radius)
	plt.plot([c2x],[c2y], "ro")
	plt.plot([c1.x],[c1.y],"b+")
	plt.plot([c2.x],[c2.y], "r+")

	#plt.plot([c1.x + turn_radius * (m.cos(theta))],[c1.y + turn_radius * (m.sin(theta))], "g+")
	#plt.plot([c1.x + turn_radius * m.cos(theta)],[c1.y + turn_radius * m.sin(-theta)], "r+")
	plt.plot([xm.x],[xm.y], "g^")
	plt.plot([xf.x],[xf.y], "g^")

	[arc1x_vals, arc1y_vals] = df.generate_arc(c1.x, c1.y, theta, turn_radius, 1)
	[arc2x_vals, arc2y_vals] = df.generate_arc(c2.x, c2.y, theta, turn_radius, 2)
	#plt.plot([arc1x_vals], [arc1y_vals], "m+")
	#plt.plot([arc2x_vals], [arc2y_vals], "m+")
	[FINALX_VALS, FINALY_VALS] = df.trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals)
	plt.plot([FINALX_VALS],[FINALY_VALS], "m+")
	total_len = len(arc1x_vals) + len(arc2x_vals)
	# -----------------------------------------------------------------------------
	# -----------------------------------------------------------------------------
	# -----------------------------------------------------------------------------
	
	# -----------------------------------------------------------------------------
	print "LEN(ARC1X_VALS)", len(arc1x_vals), "\nLEN(ARC2X_VALS):", len(arc2x_vals)
	'''
	# -----------------------------------------------------------------------------
	test_coord = Coordinate(movecar.b_down.x, movecar.b_down.y)
	plt.plot([test_coord.x],[test_coord.y], "b^")
	# -----------------------------------------------------------------------------
	'''

	[fx, fy] = frontcar.genGraphPts()
	[bx, by] = backcar.genGraphPts()
	[move_x, move_y] = movecar.genGraphPts()

	print move_x, "\t", move_y
	print backaxle_midpt.x, ", ", backaxle_midpt.y
	plt.plot([fx],[fy], "rp")
	plt.plot([bx],[by], "rp")
	plt.plot([move_x],[move_y], "rp")

	car_ang = uf.gen_angles(movecar)

	patch = patches.Rectangle((0, 0), len_car, width_car, fc='indianred')
	patch2 = patches.Rectangle((frontcar.b_down.x, frontcar.b_down.y), len_car, width_car, fc='rebeccapurple')
	patch3 = patches.Rectangle((backcar.b_down.x, backcar.b_down.y), len_car, width_car, fc='limegreen')

	ani = animation.FuncAnimation(fig, animate, init_func=init, frames= total_len, fargs = (
		FINALX_VALS,
		FINALY_VALS,
		theta,
		frontcar.b_down.x,
		frontcar.b_down.y,
		backcar.b_down.x,
		backcar.b_down.y,
		steer_ang
		), interval=150, blit=True)
	
	plt.show()


	
