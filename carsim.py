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
ax = plt.axes(xlim = (-2.0,2.5), ylim = (-2.0,2.0))
ax.set_aspect(1)

def init():
	ax.add_patch(patch)
	ax.add_patch(patch2)
	ax.add_patch(patch3)
	return patch, patch2, patch3 

def animate(i, FINALX_VALS, FINALY_VALS, theta, f_bup, f_bdown, b_bup, b_bdown, car_angs):
	patch.set_xy([FINALX_VALS[i], FINALY_VALS[i]])
	patch2.set_xy([f_bup,f_bdown])
	patch3.set_xy([b_bup,b_bdown])
	deg = np.rad2deg(car_angs[i])
	#patch._angle(deg)
	#print deg
	return patch, patch2, patch3

if __name__ == "__main__": # main function
	# ----------- LET'S DEFINE THE COORDINATES OF THE FRONT STATIC CAR -----------
	frontcar = Car(
		Coordinate(0.0,0), Coordinate(0.0,0.0), Coordinate(1.0,0.5), Coordinate(1.0,0.1)
		)

	frontcar.set_fup(frontcar.b_up.x + frontcar.len_car, frontcar.b_up.y)
	frontcar.set_fdown(frontcar.b_down.x + frontcar.len_car, frontcar.b_down.y)
	# ----------------------------------------------------------------------------
	# ---------- AND NOW THE COORDINATES OF THE BACK STATIC CAR ------------------
	backcar = Car(
		Coordinate(0.0,0.4), Coordinate(0.0,0.1), Coordinate(0.0,0.0), Coordinate(0.0,0.0)
		) 
	backcar.set_bup(backcar.f_up.x - backcar.len_car, backcar.f_up.y)
	backcar.set_bdown(backcar.f_down.x - backcar.len_car, backcar.f_down.y)
	lencar_part = frontcar.len_car / 5.0
	# ----------------------------------------------------------------------------
	# ------------- DEFINE PRELIMINARY CONSTRAINTS TO LOCATE MOVING CAR ----------
	parkspace_len =  uf.get_parkspace_len(frontcar, backcar) # DEFINE PARKING SPACE LENGTH
	len_moveto_fup = .3 # LENGTH OF BACK OF MOVING CAR TO FRONT STATIC CAR
	# ----------------------------------------------------------------------------
	# --------- DEFINE ALL PRELIMINARY COMPUTATIONS OF THE MOVING CAR ------------
	bbotm_coordy = frontcar.b_up.y + len_moveto_fup
	btop_coordy = bbotm_coordy + frontcar.width_car
	fbotm_coordy = frontcar.f_up.y + len_moveto_fup
	ftop_coordy = fbotm_coordy + frontcar.width_car
	movecar = Car(
		Coordinate(frontcar.f_up.x,ftop_coordy), Coordinate(frontcar.f_up.x,fbotm_coordy), 
		Coordinate(frontcar.b_up.x,btop_coordy), Coordinate(frontcar.b_up.x,bbotm_coordy)
	)
	# -----------------------------------------------------------------------------
	# ----------- FIGURE OUT INITIAL COORDINATES OF AXLE MIDPOINTS ----------------
	axle_len = movecar.frontaxle_midpt.x - movecar.backaxle_midpt.x
	dist_backofcar_tobackaxle = lencar_part
	dist_bottomcar_to_axlemidpt = movecar.backaxle_midpt.y - movecar.b_down.y
	# -----------------------------------------------------------------------------b
	# -------------------------SKETCH OUT ORIGINAL PLAN----------------------------
	steer_ang = m.pi / 9.0 # start off with static steer angle

	turn_radius = uf.get_turn_radius(axle_len, steer_ang) # figure out initial turn radius

	err_len = 0.1 # use this to get the closest we can get to the back car

	xf = uf.gen_xf(backcar, err_len, dist_backofcar_tobackaxle, axle_len) # figure out final position of midbackaxle

	c1 = uf.gen_c1(frontcar, movecar.frontaxle_midpt, turn_radius) # generate center of circle 1

	delta_x = uf.gen_delta_x(movecar.backaxle_midpt, xf)

	delta_y = uf.gen_delta_y(movecar.backaxle_midpt, xf)

	theta = uf.get_theta(delta_x, turn_radius)

	c2 = uf.gen_c2(backcar, err_len, dist_backofcar_tobackaxle, xf, turn_radius, axle_len)
	
	xm = uf.get_middlept(c1, c2, turn_radius, theta)

	arc_height = uf.calc_archeight(turn_radius, theta)
	print uf.check_archeight_biggerthanhalfy(arc_height, delta_y)
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

	[arc1x_vals, arc1y_vals] = df.generate_arc(c1.x, c1.y, theta, turn_radius, 1, dist_bottomcar_to_axlemidpt)
	[arc2x_vals, arc2y_vals] = df.generate_arc(c2.x, c2.y, theta, turn_radius, 2, dist_bottomcar_to_axlemidpt)
	#plt.plot([arc1x_vals], [arc1y_vals], "m+")
	#plt.plot([arc2x_vals], [arc2y_vals], "m+")
	[FINALX_VALS, FINALY_VALS] = df.trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals)
	#plt.plot([FINALX_VALS],[FINALY_VALS], "m+")
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
	print movecar.backaxle_midpt.x, ", ", movecar.backaxle_midpt.y
	plt.plot([fx],[fy], "rp")
	plt.plot([bx],[by], "rp")
	plt.plot([move_x],[move_y], "rp")

	car_angs = uf.gen_angles(FINALX_VALS, FINALY_VALS)
	print car_angs

	'''
	patch = patches.Rectangle((0, 0), len_car, width_car, fc='indianred')	

	patch2 = patches.Rectangle((frontcar.b_down.x, frontcar.b_down.y), len_car, width_car, fc='rebeccapurple')
	patch3 = patches.Rectangle((backcar.b_down.x, backcar.b_down.y), len_car, width_car, fc = 'limegreen')
	'''
	'''
	ani = animation.FuncAnimation(fig, animate, init_func=init, frames= total_len, fargs = (
		FINALX_VALS,
		FINALY_VALS,
		theta,
		frontcar.b_down.x,
		frontcar.b_down.y,
		backcar.b_down.x,
		backcar.b_down.y,
		car_angs
		), interval=200, blit=True)
	'''
	plt.show()


	
