import math as m
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

from ppobjs import Car
from ppobjs import Coordinate
import utilfuncts as uf
import drawfuncts as df

fig, ax = plt.subplots()
#ax = plt.axes(xlim = (0,3), ylim = (0,3))
xfixdata, yfixdata = 14, 8
xdata, ydata = 5, None
ln, = plt.plot([], [], 'ro-', animated=True)
patch = patches.Rectangle((0, 0), 5, 5, fc='indianred', alpha = .5)	

#plt.plot([xfixdata], [yfixdata], 'bo', ms=10)

def init():
	ax.add_patch(patch)
	ax.add_patch(patch2)
	ax.add_patch(patch3)

	return patch, patch2, patch3, 

def update(i, movecar, FINALX_VALS, FINALY_VALS, car_angs, dist_bottomcar_to_axlemidpt, dist_backofcar_tobackaxle,
	curbdanger_zone):

	lamb_da = car_angs[i]
	phi1 = lamb_da - m.pi/2
	phi2 = lamb_da - m.pi

	first_joint = Coordinate(FINALX_VALS[i], FINALY_VALS[i])
	second_joint = Coordinate(
		first_joint.x + dist_bottomcar_to_axlemidpt * m.cos(phi1),
		first_joint.y + dist_bottomcar_to_axlemidpt * m.sin(phi1),
		)
	end_effector = Coordinate(
		second_joint.x + dist_backofcar_tobackaxle * m.cos(phi2),
		second_joint.y + dist_backofcar_tobackaxle * m.sin(phi2)
		)


	patch.set_width(movecar.len_car)
	patch.set_height(movecar.width_car)
	end_effector = uf.gen_end_effector(lamb_da, car_angs[i], FINALX_VALS[i], FINALY_VALS[i], 
		dist_bottomcar_to_axlemidpt, dist_backofcar_tobackaxle)
	
	'''
	if(lamb_da != m.pi/2):
		while end_effector.y <= curbdanger_zone.y:
			lamb_da = lamb_da - m.pi/20
			end_effector = uf.gen_end_effector(lamb_da, car_angs[i], FINALX_VALS[i], FINALY_VALS[i], 
			dist_bottomcar_to_axlemidpt, dist_backofcar_tofrontaxle)
	'''	

	t2 = mpl.transforms.Affine2D().rotate_deg_around(end_effector.x, end_effector.y, np.rad2deg(lamb_da)) + ax.transData
	patch.set_transform(t2)
	patch.set_xy((end_effector.x, end_effector.y))
	#print t2
	print "lamba: ", np.rad2deg(lamb_da), "\tPHI1:",  np.rad2deg(phi1), "\tPHI2:",  np.rad2deg(phi2)
	print "FIRST_JOINT X:",  first_joint.x, "\tFIRST_JOINT Y:", first_joint.y
	print "SECOND_JOINT X:",  second_joint.x, "\tSECOND_JOINT Y:", second_joint.y
	print "END EFFECTOR X:",  end_effector.x, "\tENDEFFECTOR Y:", end_effector.y, "\n-----------"
	return patch, patch2, patch3


if __name__ == "__main__": # main function
	# ----------- LET'S DEFINE THE COORDINATES OF THE FRONT STATIC CAR -----------
	frontcar = Car(
		Coordinate(0.0,0), Coordinate(0.0,0.0), Coordinate(1.0,0.4), Coordinate(1.0,0.1)
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
	len_moveto_fup = .33 # LENGTH OF BACK OF MOVING CAR TO FRONT STATIC CAR
	# ----------------------------------------------------------------------------
	# --------- DEFINE ALL PRELIMINARY COMPUTATIONS OF THE MOVING CAR ------------
	bbotm_coordy = frontcar.b_up.y + len_moveto_fup
	btop_coordy = bbotm_coordy + frontcar.width_car
	fbotm_coordy = frontcar.f_up.y + len_moveto_fup
	ftop_coordy = fbotm_coordy + frontcar.width_car
	movecarx = frontcar.b_up.x + (4.0 * lencar_part)
	movecar = Car(
		Coordinate(movecarx + backcar.len_car,ftop_coordy), Coordinate(movecarx + backcar.len_car,fbotm_coordy), 
		Coordinate(movecarx,btop_coordy), Coordinate(movecarx,bbotm_coordy)
	)
	# -----------------------------------------------------------------------------
	# ----------- FIGURE OUT INITIAL COORDINATES OF AXLE MIDPOINTS ----------------
	axle_len = uf.dist_twopoints(movecar.frontaxle_midpt,movecar.backaxle_midpt)
	dist_backofcar_tobackaxle = lencar_part
	dist_backofcar_tofrontaxle = dist_backofcar_tobackaxle + axle_len
	dist_bottomcar_to_axlemidpt = movecar.backaxle_midpt.y - movecar.b_down.y
	# -----------------------------------------------------------------------------b
	# -------------------------SKETCH OUT ORIGINAL PLAN----------------------------
	steer_ang = m.pi / 9.0 # start off with static steer angle

	turn_radius = uf.get_turn_radius(axle_len, steer_ang) # figure out initial turn radius

	err_len = 0.2 # use this to get the closest we can get to the back car

	xf = uf.gen_xf(backcar, err_len, dist_backofcar_tobackaxle) # figure out final position of midbackaxle

	xf_backup = Coordinate(xf.x, xf.y)

	plt.plot([xf.x],[xf.y], "gp")

	c1 = uf.gen_c1(frontcar, movecar.backaxle_midpt, turn_radius) # generate center of circle 1

	delta_x = uf.gen_delta_x(movecar.backaxle_midpt, xf)

	delta_y = uf.gen_delta_y(movecar.backaxle_midpt, xf)

	#theta = uf.get_theta(delta_x, turn_radius)

	theta = uf.get_theta_fromarcheight(turn_radius, delta_y)
	
	xm = uf.get_middlept(c1, turn_radius, theta)

	c2 = uf.gen_c2(xm, turn_radius, theta)

	xf = uf.fit_xf(c2, turn_radius, theta, steer_ang)

	arc_height = uf.calc_archeight(turn_radius, theta)
	print uf.check_archeight_biggerthanhalfy(arc_height, delta_y)
	print uf.check_arcs_toobig(delta_y, turn_radius)
	# -----------------------------------------------------------------------------
	[c1x, c1y] = df.sketch_circle(c1, turn_radius)
	plt.plot([c1x],[c1y], "b*")
	[c2x, c2y] = df.sketch_circle(c2, turn_radius)
	plt.plot([c2x],[c2y], "r*")
	plt.plot([c1.x],[c1.y],"b+")
	plt.plot([c2.x],[c2.y], "r+")

	plt.plot([c1.x + turn_radius * (m.cos(theta))],[c1.y + turn_radius * (m.sin(theta))], "g+")
	plt.plot([c1.x + turn_radius * m.cos(theta)],[c1.y + turn_radius * m.sin(-theta)], "r+")
	plt.plot([xm.x],[xm.y], "g+")
	plt.plot([xf.x],[xf.y], "g^")

	[arc1x_vals, arc1y_vals] = df.generate_arc(c1.x, c1.y, theta, turn_radius, 1, dist_bottomcar_to_axlemidpt, steer_ang)
	[arc2x_vals, arc2y_vals] = df.generate_arc(c2.x, c2.y, theta, turn_radius, 2, dist_bottomcar_to_axlemidpt, steer_ang)

	movecar.setFrontAxle(arc2x_vals[0], arc2y_vals[0])
	free_zone = frontcar.b_up.x - arc2x_vals[0] - err_len
	[m_forwardx, m_forwardy] = uf.drive_car_forwards(movecar, free_zone)
	
	#plt.plot([arc1x_vals], [arc1y_vals], "m+")
	#plt.plot([arc2x_vals], [arc2y_vals], "m+")
	#plt.plot([m_forwardx], [m_forwardy], "m+")
	[FINALX_VALS, FINALY_VALS] = df.trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals, m_forwardx, m_forwardy)
	#plt.plot([FINALX_VALS],[FINALY_VALS], "m+")
	total_len = len(arc1x_vals) + len(arc2x_vals) + len(m_forwardx)
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
	df.label_points(ax,c1,c2, xm, xf, xf_backup, Coordinate(FINALX_VALS[0], FINALY_VALS[0]))
	'''
	[fx, fy] = frontcar.genGraphPts()
	[bx, by] = backcar.genGraphPts()
	[move_x, move_y] = movecar.genGraphPts()

	print "FRONT CAR:", move_x, "\t", "BACK CAR:", move_y
	print "INITIAL BACKAXLE MIDPT:(", movecar.backaxle_midpt.x, ", ", movecar.backaxle_midpt.y, ")"
	plt.plot([fx],[fy], "rp")
	plt.plot([bx],[by], "rp")
	plt.plot([move_x],[move_y], "rp")
	'''

	car_angs = uf.gen_angles(FINALX_VALS, FINALY_VALS)
	print "CAR_ANGS(RAD):",car_angs
	patch2 = patches.Rectangle((frontcar.b_down.x, frontcar.b_down.y), movecar.len_car, movecar.width_car, 
		fc='rebeccapurple', alpha = .45)
	patch3 = patches.Rectangle((backcar.b_down.x, backcar.b_down.y), movecar.len_car, movecar.width_car, 
		fc = 'limegreen', alpha = .45)

	curbdanger_zone = Coordinate(0.0, 0.0 + err_len)
	
	df.gen_skeletongraph(ax, frontcar, backcar, movecar,
		FINALX_VALS,
		FINALY_VALS,
		car_angs,
		dist_bottomcar_to_axlemidpt,
		dist_backofcar_tobackaxle,
		curbdanger_zone
		)
	
	
	
	ani = animation.FuncAnimation(fig, update, init_func=init, frames= total_len, fargs = (
		movecar,
		FINALX_VALS,
		FINALY_VALS,
		car_angs,
		dist_bottomcar_to_axlemidpt,
		dist_backofcar_tobackaxle,
		curbdanger_zone
		),
		interval = 100,
		blit=True)
	

	ax.set_aspect(1)
	label_str = "Parallel Parking Map (steer_ang ="
	label_str = label_str + str(steer_ang) + ", d[c] = " + str(len_moveto_fup) + ")"
	plt.title(label_str)
	plt.ylabel("Y")
	plt.xlabel("X")
	plt.show()
	


