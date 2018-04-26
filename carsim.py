import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# What we are given: center point of the back axle of the moving car: movecar_axlept
# D = length of the parking space: parkspace_len
# 4 coordinates of the two cars we want to park between: frontcar_up, frontcar_down, backcar_up, backcar_down
# Steering angle: steer_ang

# X0 = position of movecar_axlept when the back of the cars are aligned
# X1 = position of movecar_axlept when the back axle and the back of the front car are aligned

def get_turn_radius(steer_ang):


def get_theta(parkspace_len, turn_radius):
    return m.pi + m.asin(parkspace_len / (2 * turn_radius))


def get_middlept(parkspace_len, turn_radius, c1, theta):
    print "PARK SPACE LEN: ", parkspace_len, "\nTURN RADIUS: ", turn_radius, "\nTHETA: ", theta, "\nEND COORDINATE OF C1 (", c1.x, ",", c1.y, ")"
    xm = Coordinate(c1.x + (turn_radius * m.cos(theta)), c1.y + (turn_radius * m.sin(theta)))
    print "END COORDINATE OF XM: (", xm.x, ", ", xm.y, " )"
    return xm


def plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down, c1):
    x = [movecar_axlept.x, frontcar_up.x, frontcar_down.x, backcar_up.x, backcar_down.x, c1.x]
    y = [movecar_axlept.y, frontcar_up.y, frontcar_down.y, backcar_up.y, backcar_down.x, c1.y]
    plt.plot(x, y, 'ro')
    plt.autoscale()


def robot_draw_circle(radius, center, theta):
    time = [x * 0.2 for x in range(0, 100)]
    theta_list = []
    for t in time:
        theta_list.append(t * (theta) / 12)
    return theta_list


def gen_xy_vals(center, center_flag, theta, turn_radius):
    theta_list = robot_draw_circle(turn_radius, center, theta)
    x_vals = []
    y_vals = []
    if center_flag == 1:
        for i in range(0, len(theta_list)):
            if theta_list[i] <= theta and theta_list[i] >= m.pi / 2:
                x_vals.append(center.x + turn_radius * m.cos(theta_list[i]))
                y_vals.append(center.y + turn_radius * m.sin(theta_list[i]))
    if center_flag == 2:
        for i in range(0, len(theta_list)):
            if theta_list[i] >= theta + m.pi / 3 and theta_list[i] <= 2 * m.pi:
                x_vals.append(center.x + turn_radius * m.cos(theta_list[i]))
                y_vals.append(center.y + turn_radius * m.sin(theta_list[i]))
    return [x_vals, y_vals]


def get_c2(turn_radius, xm, xf):
    radsq = turn_radius * turn_radius
    q_x = m.sqrt(((xf.x - xm.x) * (xf.x - xm.x)) + ((xf.y - xm.y) * (xf.y - xm.y)))
    q_y = m.sqrt(((xf.x - xm.x) * (xf.x - xm.x)) + ((xf.y - xm.y) * (xf.y - xm.y)))
    x3 = (xf.x + xm.x) / 2
    y3 = (xf.y + xm.y) / 2
    return Coordinate(x3 - m.sqrt(radsq - ((q_x / 2) * (q_x / 2))) * ((xm.y - xf.y) / q_x),
                      y3 - m.sqrt(radsq - ((q_y / 2) * (q_y / 2))) * ((xf.x - xm.x) / q_y))


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


fig = plt.figure()
ax = plt.axes(xlim=(-8, 8), ylim=(-8, 8))
N = 2
points = ax.plot(*([[], []] * N), color='green', linestyle='--', marker='o')
patch = patches.Rectangle((0, 0), 0, 0, fc='y')


def init():
    ax.add_patch(patch)
    return patch,


def animate(i, FINALX_VALS, FINALY_VALS, theta):
    patch.set_width(3.0)
    patch.set_height(4.0)
    patch.set_xy([FINALX_VALS[i], FINALY_VALS[i]])
    patch._angle = -np.rad2deg(theta)
    return patch,


if __name__ == "__main__":  # main function
    turn_radius = get_turn_radius(m.pi / 9)
    movecar_axlept = Coordinate(4, 10)
    frontcar_up = Coordinate(4, 5)
    frontcar_down = Coordinate(4, .1)
    backcar_up = Coordinate(0, 5)
    backcar_down = Coordinate(0, .1)
    parkspace_len = frontcar_up.x - backcar_up.x

    c1 = Coordinate(movecar_axlept.x, movecar_axlept.y - turn_radius)
    theta = get_theta(parkspace_len, turn_radius)
    xm = get_middlept(parkspace_len, turn_radius, c1, theta)
    xf = Coordinate(0, (backcar_up.y - backcar_down.y + 0.5) / 2)
    c2 = get_c2(turn_radius, xm, xf)
    plot_graph(movecar_axlept, frontcar_up, frontcar_down, backcar_up, backcar_down, c1)

    [arc1x_vals, arc1y_vals] = gen_xy_vals(c1, 1, theta, turn_radius)
    [arc2x_vals, arc2y_vals] = gen_xy_vals(c2, 2, theta, turn_radius)
    [FINALX_VALS, FINALY_VALS] = trace_path(arc1x_vals, arc1y_vals, arc2x_vals, arc2y_vals)

    plt.plot([xm.x], [xm.y], "ko")
    plt.plot([xf.x], [xf.y], "ko")
    plt.plot([c1.x], [c1.y], "mo")
    plt.plot([c2.x], [c2.y], "mo")
    plt.plot([FINALX_VALS], [FINALY_VALS], "m+")
    plt.xlabel('X')
    plt.ylabel('Y')

    total_len = len(arc1x_vals) + len(arc2x_vals)
    print "LEN(ARC1X_VALS)", len(arc1x_vals), "\nLEN(ARC2X_VALS):", len(arc2x_vals)

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=total_len, fargs=(
        FINALX_VALS,
        FINALY_VALS,
        theta,
    ), interval=100, blit=True)
    plt.show()
