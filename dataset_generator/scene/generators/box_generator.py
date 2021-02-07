import pyrender, math

import numpy as np

def get_box(scene, renderer, model_node, class_name):
    '''Creates box label of model from scene and returns label str in kitti format
    https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt'''

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

    # https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt
    kitti_str = ' '.join((
        class_name,                                             # Object name
        str(0),                                                 # Truncated float from 0 to 1
        str(3),                                                 # Occlusion int 0 to 3
        str(math.pi),                                           # Observation angle -pi to pi
        str(1),                                                 # BBOX: Left
        str(1),                                                 # BBOX: Top
        str(1),                                                 # BBOX: Right
        str(1),                                                 # BBOX: Bottom
        str(1),                                                 # DIM: Height
        str(1),                                                 # DIM: Width
        str(1),                                                 # DIM: Length
        str(1),                                                 # Location: x
        str(1),                                                 # Location: y
        str(1),                                                 # Location: z
        str(1),                                                 # Rotation: y
        str(1),                                                 # Score
    ))

    print(kitti_str)

    result = {
        'x': ((p1[0] + 1)/2)*width,
        'y': height - ((p1[1] + 1)/2)*height,
        'h': 50,
        'w': 50,
    }

    return result