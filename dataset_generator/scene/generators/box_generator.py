import pyrender, math, trimesh

import numpy as np

def get_box(scene, renderer, model_node, class_name):
    '''Creates box label of model from scene and returns label str in kitti format
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
    
    l, r, t, b = math.inf, -math.inf, math.inf, -math.inf
    for prim in model_node.mesh.primitives:                     # Iterate primitives in object
        for point in prim.positions:                            # Iterate points in primitives
            point = np.append(point.flatten(), 1)               # Row vector with added omega value
            point = np.dot(point, obj_pose.T)                   # Add object rotation/translation to point

            p_2d = np.dot(point, projection_mat)                # Use camera projection matrix to convert to image coordinates

            if 0 < p_2d[-1] and p_2d[-1] < 1:                   # Check w is between zero and one
                p_2d = p_2d / p_2d[-1]                          # Divide the array by w
                
                x = round(((p_2d[0] + 1.0)/2.0)*width)          # X pixel coodinate
                if l > x:
                    l = x
                if r < x:
                    r = x

                                                                # Y pixel coordinate
                y = round(height - ((p_2d[1] + 1.0)/2.0)*height)
                if t > y:
                    t = y
                if b < y:
                    b = y

    

    kitti_str = ' '.join((
        class_name,                                             # Object name
        str(0),                                                 # Truncated float from 0 to 1
        str(3),                                                 # Occlusion int 0 to 3
        str(math.pi),                                           # Observation angle -pi to pi
        str(l),                                                 # BBOX: Left
        str(t),                                                 # BBOX: Top
        str(r),                                                 # BBOX: Right
        str(b),                                                 # BBOX: Bottom
        str(1),                                                 # DIM: Height
        str(1),                                                 # DIM: Width
        str(1),                                                 # DIM: Length
        str(1),                                                 # Location: x
        str(1),                                                 # Location: y
        str(1),                                                 # Location: z
        str(1),                                                 # Rotation: y
        str(-1),                                                # Score (used for submission)
    ))

    return kitti_str