import numpy as np
import matplotlib.pyplot as plt

from ppobjs import Coordinate
from ppobjs import Car


def gen_circle(c, r):

	theta = np.linspace(0, 2 * np.pi, 100)
	# theta goes from 0 to 2pi
	# the radius of the circle
	# compute x1 and y1
	x1 = c.x + r*np.cos(theta)
	y1 = c.y + r*np.sin(theta)
	return [x1,y1]
	'''
	# create the figure
	fig, ax = plt.subplots(1)
	ax.plot(x1, x2)
	ax.set_aspect(1)
	plt.show()
	'''
def generate_arc(cx, cy, theta, r, cflag):
	if(cflag == 1):
		theta = np.linspace(np.pi / 2, (np.pi/2) + theta, 50)
	else:
		theta = np.linspace((2 * np.pi) - theta, ((2 * np.pi) - theta) + np.pi/6, 50)
	x1 = cx + r*np.cos(theta)
	y1 = cy + r*np.sin(theta)
	return [x1,y1]

def trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals):
	FINALX_VALS = []
	FINALY_VALS = []
	for point in arc1x_vals:
		FINALX_VALS.append(point)
	for point in arc1y_vals:
		FINALY_VALS.append(point)
	for i in range(len(arc2x_vals) - 1, -1, -1):
		FINALX_VALS.append(arc2x_vals[i])
		FINALY_VALS.append(arc2y_vals[i])
	return [FINALX_VALS, FINALY_VALS]


def sketch_circle(c, turn_radius):
	[cx, cy] = gen_circle(c, turn_radius)
	return [cx, cy]