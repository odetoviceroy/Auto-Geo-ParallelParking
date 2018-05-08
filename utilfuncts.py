import math as m
from ppobjs import Car
from ppobjs import Coordinate

def dist_twopoints(p1,p2):
	res = (p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y)
	res = m.sqrt(res)
	print "DISTANCE BETWEEN TWO GIVEN POINTS: ", res
	return res

def get_parkspace_len(frontcar, backcar):
	res = frontcar.b_up.x - backcar.f_up.x
	print "PARKSPACE LEN:", res
	return res

def get_turn_radius(axle_len, steer_ang):
	res = axle_len / m.tan(steer_ang) # this is in radians
	print "STEER_ANG:", steer_ang, "\nTURN RADIUS:", res
	return res

def gen_xf(backcar, err_len, dist_backofcar_tobackaxle, axle_len):
	resx = backcar.f_up.x + err_len + dist_backofcar_tobackaxle + axle_len
	resy = err_len + (backcar.width_car / 10.0)
	print "XF Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx,resy)

def gen_delta_x(backaxle_midpt, xf):
	res = backaxle_midpt.x - xf.x
	print "DELTA X:", res
	return res

def gen_delta_y(backaxle_midpt, xf):
	res = backaxle_midpt.y - xf.y
	print "DELTA Y:", res
	return res

def gen_c1(frontcar, frontaxle_midpt, turn_radius):
	resx = frontaxle_midpt.x
	resy = frontaxle_midpt.y - turn_radius
	print "C1 Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx, resy)

def gen_c2(xm, turn_radius, theta):
	resx = xm.x + turn_radius * m.cos(m.pi/2 + theta)
	resy = xm.y + turn_radius * m.sin(m.pi/2 + theta)
	'''
	resx = xf.x
	resy = xf.y + turn_radius
	'''
	print "C2 Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx, resy)

def get_theta(delta_x, turn_radius):
	res = m.asin(delta_x/ (2 * turn_radius))
	print "THETA:", res
	return res

def get_middlept(c1, turn_radius, theta): 
	resx = c1.x + turn_radius * m.cos(m.pi/2 + theta)
	resy = c1.y + turn_radius * m.sin(m.pi/2 + theta)
	print "INITIAL XM Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx, resy)

def check_arcs_toobig(delta_y, turn_radius):
	return delta_y > (2 * turn_radius)

def calc_archeight(turn_radius, theta):
	res = turn_radius - (1 - m.cos(theta / 2.0))
	print "ARC HEIGHT:", res
	return res

def check_archeight_biggerthanhalfy(arc_height, delta_y):
	return arc_height <= (.5 * delta_y)

def gen_angles(FINALX_VALS, FINALY_VALS):
	car_angs = []
	car_angs.append(0.0)
	for i in range(0, len(FINALX_VALS) - 1):
		rise = m.fabs(FINALY_VALS[i+1] - FINALY_VALS[i])
		run = m.fabs(FINALX_VALS[i+1] - FINALX_VALS[i])
		if run == 0:
			car_angs.append(car_angs[i-1])
		else:
			car_angs.append(m.atan(rise / run))
	print "CAR ANGS LENGTH: ", len(car_angs)
	return car_angs

def get_theta_fromarcheight(turn_radius, delta_y):
	# The paper states that the height of both arcs must be fitted to 1/2 * delta_y each
	# So we can therefore use this to figure out theta for drawing these arcs and therefore getting xm
	res = 1 - ((delta_y / 2.0) / turn_radius) 
	print "RES: ", res
	res = m.acos(res) 
	print "THETA: ", res
	return res

def fit_xf(c2, turn_radius, theta, steer_ang):
	resx = c2.x + turn_radius * m.cos(-1 * (m.pi - (theta + m.pi/2)) - theta + (steer_ang/1.5))
	resy = c2.y + turn_radius * m.sin(-1 * (m.pi - (theta + m.pi/2)) - theta + (steer_ang/1.5))
	print "FITTED XF COORDINATE:(", resx, ",", resy, ")"
	return Coordinate(resx,resy)

def gen_end_effector(lamb_da, curr_car_angs, FINALX_VAL, FINALY_VAL, 
	dist_bottomcar_to_axlemidpt, dist_backofcar_tofrontaxle):

	lamb_da = curr_car_angs
	phi1 = lamb_da - m.pi/2
	phi2 = lamb_da - m.pi

	first_joint = Coordinate(FINALX_VAL, FINALY_VAL)
	second_joint = Coordinate(
		first_joint.x + dist_bottomcar_to_axlemidpt * m.cos(phi1),
		first_joint.y + dist_bottomcar_to_axlemidpt * m.sin(phi1),
		)
	return Coordinate(
		second_joint.x + dist_backofcar_tofrontaxle * m.cos(phi2),
		second_joint.y + dist_backofcar_tofrontaxle * m.sin(phi2)

		)

def drive_car_forwards(movecar, err_len):
	x_vals = []
	y_vals = []
	for i in range(0, 20):
		movecar.setFrontAxle(movecar.frontaxle_midpt.x + (err_len / 20.0), movecar.frontaxle_midpt.y)
		x_vals.append(movecar.frontaxle_midpt.x)
		y_vals.append(movecar.frontaxle_midpt.y)
	return [x_vals, y_vals]

