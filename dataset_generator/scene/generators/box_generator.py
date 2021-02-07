import pyrender

import numpy as np

def get_box(scene, camera, renderer, model_node):
    '''Creates box label from scene'''
    #cam = camera.camera                                         # Get camera object

    cam_node = scene.main_camera_node
    cam = cam_node.camera
    
    width=renderer.viewport_width
    height=renderer.viewport_height
    
    projection_mat = cam.get_projection_matrix(                 # Cameras projection matrix
        width,
        height
    ).T

    '''
    bounds = model_node.mesh.centroid
    bound = np.append(bounds, 1)'''
    obj = scene.get_pose(model_node)
    obj_p = np.array(((
        obj[0][3],
        obj[1][3],
        obj[2][3],
        1
    )))


    p1 = np.dot(obj_p, projection_mat)

    p1 = p1 / p1[-2]

    dim = model_node.mesh.extents

    result = {
        'x': ((p1[0] + 1)/2)*width,
        'y': height - ((p1[1] + 1)/2)*height,
        'h': 1,
        'w': 1,
    }

    return result