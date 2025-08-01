import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

# Initial points
p1 = np.array([0, 0, 0])
p2 = np.array([1, 0, 0])
p3 = np.array([0, 1, 1])
points = [p1, p2, p3]

# Plot elements
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Update function for animation
def update():
    new_points = [p1, p2, p3]

    # Clear and redraw
    ax.clear()
    xs, ys, zs = zip(*new_points)
    ax.scatter(xs, ys, zs, c='r')

    # Optionally connect them with a plane
    ax.plot_trisurf(xs, ys, zs, alpha=0.5, color='blue')

    ax.set_xlim(-0.05, 0.05)
    ax.set_ylim(-0.05, 0.05)
    ax.set_zlim(0.01, 0.06)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.draw()
    plt.pause(0.01)
