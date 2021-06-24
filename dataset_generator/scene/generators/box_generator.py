import pyrender, math, trimesh

import numpy as np

def get_box(scene, renderer, model_node, class_name, bbox_format):
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
    prims = 0
    pots = 0
    for prim in model_node.mesh.primitives:                     # Iterate primitives in object
        for point in prim.positions:                            # Iterate points in primitives
            point = np.append(point.flatten(), 1)               # Row vector with added omega value
            point = np.dot(point, obj_pose.T)                   # Add object rotation/translation to point
            p_2d = np.dot(point, projection_mat)                # Use camera projection matrix to convert to image coordinates

            #if 0 < p_2d[-1] and p_2d[-1] < 2:                  # Check w is between zero and one
            p_2d = p_2d / p_2d[-1]                              # Divide the array by w
            
            x = round(((p_2d[0] + 1.0)/2.0)*width)              # X pixel coodinate
            if 0 < x and x < width:
                if l > x:
                    l = x
                if r < x:
                    r = x

                                                                # Y pixel coordinate
            y = round(height - ((p_2d[1] + 1.0)/2.0)*height)
            if 0 < y and y < height:
                if t > y:
                    t = y
                if b < y:
                    b = y

    res = ''

    if 'kitti' == bbox_format:
        res = ' '.join((
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
    elif 'yolo' == bbox_format:
        x = (l + (r-l)/2) / width
        y = (t + (b-t)/2) / height
        x_span = (r-l) / width
        y_span = (b-t) / height

        
        if 0 < x + x_span/4 and x - x_span/4 < width:
            if  0 < y + y_span/4 and y - y_span/4 < height:
        
                vs = ( x, y, x_span, y_span)                        # Coordinates in yolo format: class x_center y_center width height

                vs = [                                              # Add class name and map values from 0 - 1
                    class_name, 
                    *map(str, vs)
                ]
                
                res = ' '.join(map(str, vs))
        
    else: raise Exception(f'Invalid bbox format {bbox_format}')

    return res