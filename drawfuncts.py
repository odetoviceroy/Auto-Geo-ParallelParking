import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

from ppobjs import Coordinate
from ppobjs import Car
import utilfuncts as uf


def gen_circle(c, r):
	theta = np.linspace(0, 2 * np.pi, 100)
	# theta goes from 0 to 2pi
	# the radius of the circle
	# compute x1 and y1
	x1 = c.x + r*np.cos(theta)
	y1 = c.y + r*np.sin(theta)
	return [x1,y1]
	
def generate_arc(cx, cy, theta, r, cflag, axle_len, steer_ang):
	if(cflag == 1):
		theta = np.linspace(
			np.pi / 2, 
			(np.pi/2) + theta, 
			25
			)
		#r = r - (axle_len)
	else:
		theta = np.linspace(
			2 * np.pi - (np.pi - (theta + np.pi/2)) - theta + (steer_ang / 1.5), 
			2 * np.pi - (np.pi - (theta + np.pi/2)), 
			25
			)
		#r = r + (axle_len)

	x1 = cx + (r *np.cos(theta))
	y1 = cy + (r *np.sin(theta))
	return [x1,y1]

def trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals, m_forwardx, m_forwardy):
	FINALX_VALS = []
	FINALY_VALS = []
	for point in arc1x_vals:
		FINALX_VALS.append(point)
	for point in arc1y_vals:
		FINALY_VALS.append(point)
	for i in range(len(arc2x_vals) - 1, -1, -1):
		FINALX_VALS.append(arc2x_vals[i])
		FINALY_VALS.append(arc2y_vals[i])
	for p in m_forwardx:
		FINALX_VALS.append(p)
	for p in m_forwardy:
		FINALY_VALS.append(p)
	return [FINALX_VALS, FINALY_VALS]


def sketch_circle(c, turn_radius):
	[cx, cy] = gen_circle(c, turn_radius)
	return [cx, cy]

def label_points(ax,c1,c2,xm,xf, xf_backup, x0):
	txt = ax.annotate('C1',xy=(c1.x,c1.y),fontsize=10,\
	xytext=(c1.x + .2,c1.y - .2),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))
	txt = ax.annotate('C2',xy=(c2.x,c2.y),fontsize=10,\
	xytext=(c2.x - .2,c2.y - .2),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))
	txt = ax.annotate('XM',xy=(xm.x,xm.y),fontsize=10,\
	xytext=(xm.x + .3,xm.y + .4),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))
	txt = ax.annotate('FITTED XF',xy=(xf.x,xf.y),fontsize=10,\
	xytext=(xf.x - .4,xf.y - .4),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))
	txt = ax.annotate('ORIGINAL XF',xy=(xf_backup.x,xf_backup.y),fontsize=10,\
	xytext=(xf_backup.x + .1,xf_backup.y - .4),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))
	txt = ax.annotate('X0',xy=(x0.x,x0.y),fontsize=10,\
	xytext=(x0.x + .2,x0.y + .2),arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=-.2"))

def gen_skeletongraph(ax, frontcar, backcar, movecar,
		FINALX_VALS,
		FINALY_VALS,
		car_angs,
		dist_bottomcar_to_axlemidpt,
		dist_backofcar_tofrontaxle,
		):

	patch2 = patches.Rectangle((frontcar.b_down.x, frontcar.b_down.y), movecar.len_car, movecar.width_car, 
		fc='rebeccapurple', alpha = .45)
	ax.add_patch(patch2)
	patch3 = patches.Rectangle((backcar.b_down.x, backcar.b_down.y), movecar.len_car, movecar.width_car, 
		fc = 'limegreen', alpha = .45)
	ax.add_patch(patch3)

	for i in range(0, len(FINALX_VALS) - 1, 2):
		lamb_da = car_angs[i]
		patch = patches.Rectangle((FINALX_VALS[i], FINALY_VALS[i]), movecar.len_car, movecar.width_car, 
		fc = 'none', alpha = .45, edgecolor = 'rebeccapurple', ls = 'solid', lw = 1.0)
		end_effector = uf.gen_end_effector(lamb_da, car_angs[i], FINALX_VALS[i], FINALY_VALS[i], 
		dist_bottomcar_to_axlemidpt, dist_backofcar_tofrontaxle)
		t2 = mpl.transforms.Affine2D().rotate_deg_around(end_effector.x, end_effector.y, np.rad2deg(lamb_da)) + ax.transData
		patch.set_transform(t2)
		patch.set_xy((end_effector.x, end_effector.y))
		ax.add_patch(patch)

	return 0
	

