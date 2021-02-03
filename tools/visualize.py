import pyrender

from matplotlib import pyplot
from mpl_toolkits import mplot3d

def show_mesh(mesh):
    '''Takes a mesh and vizualises it using matplotlib'''
    fig = pyplot.figure() 
    axes = mplot3d.Axes3D(fig)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))

    scale = mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    pyplot.show()


def show_obj(mesh):
    scene = pyrender.Scene()
    scene.add(mesh)
    pyrender.Viewer(scene, use_raymond_lighting=True)