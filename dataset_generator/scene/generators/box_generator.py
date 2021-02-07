import pyrender

import numpy as np

def get_box(scene, camera, renderer, model_node):
    '''Creates box label from scene'''
    #cam = camera.camera                                         # Get camera object

    cam_node = scene.main_camera_node
    cam = cam_node.camera
    
    width=renderer.viewport_width
    height=renderer.viewport_height

    print('\n'.join((
        'w: {}'.format(width),
        'h: {}'.format(height)
    )))
    
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
    
    #print(projection_mat)
    #print('Point: {}'.format(obj_p))


    p1 = np.dot(obj_p, projection_mat)

    #print('Point: {}'.format(p1))
    p1 = p1 / p1[-2]
    #print('Point: {}'.format(p1))
    
    #print('x: {}, y: {}'.format((p1[0]+(width/2))/width, (p1[1]+(height/2))/height))
    #print('x: {}, y: {}'.format(((p1[0] + 1)/2)*width, ((p1[1] + 1)/2)*height))

    dim = model_node.mesh.extents
    print(dim)

    result = {
        'x': ((p1[0] + 1)/2)*width,
        'y': height - ((p1[1] + 1)/2)*height,
        'h': 1,
        'w': 1,
    }

    return result