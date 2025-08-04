import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys

# Set up 3D PyQtGraph window
app = pg.mkQApp("3D Point Viewer")
w = gl.GLViewWidget()
w.setWindowTitle('Live 3D Points')
w.setGeometry(0, 0, 800, 600)
w.show()

# Create a 3D scatter plot item
sp = gl.GLScatterPlotItem()
sp.setGLOptions('opaque')
w.addItem(sp)

# Optionally, create a plane by connecting the 3 points with triangles (GLMeshItem)
mesh = gl.GLMeshItem()
mesh.setGLOptions('opaque')
w.addItem(mesh)

def update(p1, p2, p3):
    points = np.vstack([p1, p2, p3])
    points = points * 30

    # Update scatter plot
    sp.setData(pos=points, color=(1, 0, 0, 1), size=10)

    # Update mesh (triangle)
    faces = np.array([[0, 1, 2]])
    mesh.setMeshData(vertexes=points, faces=faces, smooth=False, drawEdges=True, edgeColor=(1, 1, 1, 1))

    pg.QtGui.QGuiApplication.processEvents()



# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# from matplotlib.animation import FuncAnimation
# 
# # Initial points
# p1 = np.array([0, 0, 0])
# p2 = np.array([1, 0, 0])
# p3 = np.array([0, 1, 1])
# points = [p1, p2, p3]
# 
# # Plot elements
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# 
# # Update function for animation
# def update():
#     new_points = [p1, p2, p3]
# 
#     # Clear and redraw
#     ax.clear()
#     xs, ys, zs = zip(*new_points)
#     ax.scatter(xs, ys, zs, c='r')
# 
#     # Optionally connect them with a plane
#     ax.plot_trisurf(xs, ys, zs, alpha=0.5, color='blue')
# 
#     ax.set_xlim(-0.05, 0.05)
#     ax.set_ylim(-0.05, 0.05)
#     ax.set_zlim(0.01, 0.06)
#     ax.set_xlabel("X")
#     ax.set_ylabel("Y")
#     ax.set_zlabel("Z")
#     plt.draw()
#     plt.pause(0.01)
