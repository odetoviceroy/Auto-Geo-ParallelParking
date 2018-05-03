import math as m
from ppobjs import Car
from ppobjs import Coordinate

def get_parkspace_len(frontcar, backcar):
	res = frontcar.b_up.x - backcar.f_up.x
	print "PARKSPACE LEN:", res
	return res

def get_turn_radius(axle_len, steer_ang):
	res = axle_len / m.tan(steer_ang) # this is in radians
	print "TURN RADIUS:", res
	return res

def gen_xf(backcar, err_len, dist_backofcar_tobackaxle, width_car, axle_len):
	resx = backcar.f_up.x + err_len + dist_backofcar_tobackaxle + axle_len
	resy = err_len + (width_car / 2.0)
	print "XF Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx,resy)

def gen_delta_x(xf_x, parkspace_len, err_len, dist_backofcar_tobackaxle, axle_len):
	res = xf_x + (parkspace_len - err_len) + dist_backofcar_tobackaxle + axle_len
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

def gen_c2(backcar, err_len, dist_backofcar_tobackaxle, xf, turn_radius, axle_len):
	resx = backcar.f_up.x + err_len + dist_backofcar_tobackaxle - axle_len
	resy = xf.y + turn_radius
	print "C2 Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx, resy)

def get_theta(delta_x, turn_radius):
	res = m.asin(delta_x/ (2 * turn_radius))
	print "THETA:", res
	return res

def get_middlept(c1, c2): 
	resx = (c1.x + c2.x) /2
	resy = (c1.y + c2.y) / 2
	print "INITIAL XM Coordinate (", resx, ",", resy, ")"
	return Coordinate(resx, resy)

def check_arcs_toobig(delta_y, turn_radius):
	return delta_y > (2 * turn_radius)


def gen_angles(movecar):
	return 0