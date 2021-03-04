import pyrender, math, trimesh

import numpy as np

from PIL import Image

def get_mask(scene, renderer, model_node):
    '''Creates mask of model from scene
    https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt'''

    cam_node = scene.main_camera_node                           # Main camera in scene
    cam = cam_node.camera                                       # Get camera from node
    
    width=renderer.viewport_width                               # Image width
    height=renderer.viewport_height                             # Image height
    
    projection_mat = cam.get_projection_matrix(                 # Cameras projection matrix (Transposed)
        width,
        height
    ).T
    
    obj_pose = scene.get_pose(model_node)                       # Object world pose
    obj_p = (                                                   # Object center point(column vector)
        obj_pose[0][3],
        obj_pose[1][3],
        obj_pose[2][3]
    )
    
    mask = np.zeros((height, width))                            # Ones image
    for prim in model_node.mesh.primitives:                     # Iterate primitives in object
        for point in prim.positions:                            # Iterate points in primitives
            point = np.append(point.flatten(), 1)               # Row vector with added omega value
            point = np.dot(point, obj_pose.T)                   # Add object rotation/translation to point

            p_2d = np.dot(point, projection_mat)                # Use camera projection matrix to convert to image coordinates

            if 0 < p_2d[-1] and p_2d[-1] < 1:                   # Check w is between zero and one
                p_2d = p_2d / p_2d[-1]                          # Divide the array by w
                x = round(((p_2d[0] + 1.0)/2.0)*width)          # X pixel coodinate                   
                y = round(height - ((p_2d[1] + 1.0)/2.0)*height)# Y pixel coordinate
                
                mask[y][x] = 1                                  # White part in image

    return Image.fromarray(np.uint8(mask*255), 'L')             # Convert from 2d array to pil image