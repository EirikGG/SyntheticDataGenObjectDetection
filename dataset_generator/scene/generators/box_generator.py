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
    obj_p = np.array(((                                         # Object center point(column vector)
        obj_pose[0][3],
        obj_pose[1][3],
        obj_pose[2][3],
        0
    )))

    b = model_node.mesh.bounds                                  # Bounds on local coordinates

    p1 = np.append(b[0], 0) + obj_p                             # 8 corners in bounding box
    p2 = p1 + (abs(b[0][0]) + abs(b[1][0]), 0, 0, 0)
    p3 = p1 + (0, abs(b[0][1]) + abs(b[1][1]), 0, 0)
    p4 = p1 + (0, 0, abs(b[0][2]) + abs(b[1][2]), 0)
    p5 = p4 + (abs(b[0][0]) + abs(b[1][0]), 0, 0, 0)
    p6 = p4 + (0, abs(b[0][1]) + abs(b[1][1]), 0, 0)
    p7 = p4 + (0, 0, abs(b[0][2]) + abs(b[1][2]), 0)

    l, r, t, b = math.inf, -math.inf, math.inf, -math.inf
    for p in (p1, p2, p3, p4, p5, p6, p7):                      # Find outer points
        p_2d = np.dot(p, projection_mat)
        print(p_2d)
        p_2d = p_2d / p_2d[-2]
        print(p_2d)

        x = round(((p_2d[0] + 1)/2)*width)
        if l > x:
            l = x
        if r < x:
            r = x

        y = round(height - ((p_2d[1] + 1)/2)*height)
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
        str(-1),                                                # Score
    ))

    return kitti_str