import pyrender

import numpy as np

def get_box(scene, renderer, model_node):
    '''Creates box label of model from scene'''

    cam_node = scene.main_camera_node                           # Main camera in scene
    cam = cam_node.camera                                       # Get camera from node
    
    width=renderer.viewport_width                               # Image width
    height=renderer.viewport_height                             # Image height
    
    projection_mat = cam.get_projection_matrix(                 # Cameras projection matrix
        width,
        height
    ).T


    obj_pose = scene.get_pose(model_node)                       # Object world pose
    obj_p = np.array(((                                         # Object point(column vector)
        obj_pose[0][3],
        obj_pose[1][3],
        obj_pose[2][3],
        1
    )))


    p1 = np.dot(obj_p, projection_mat)

    p1 = p1 / p1[-2]

    dim = model_node.mesh.extents

    result = {
        'x': ((p1[0] + 1)/2)*width,
        'y': height - ((p1[1] + 1)/2)*height,
        'h': 50,
        'w': 50,
    }

    return result