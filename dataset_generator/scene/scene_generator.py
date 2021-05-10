import pyrender, trimesh, random, math

import numpy as np

def generate_random_scene(model):
    scene = pyrender.Scene(                                     # Create new scene
        ambient_light=[int(random.uniform(.3, .7)*255) for _ in range(3)]
    )

    scene, model_node = _add_model(scene, model)                # Add model to scene

    scene, cam = _add_camera(scene)                             # Add camera


    for l_type in ('directional_lights', 'point_lights'):       # Adds light to the scene
        scene = _add_lighting(scene, light_type=l_type)
    '''
    scene.add(
        pyrender.DirectionalLight(
            color=np.ones(3),
            intensity=10.0,
        ), pose = scene.get_pose(scene.main_camera_node)
    )
    '''

    return scene, model_node, cam

def _add_model(scene, model, pose=np.eye(4)):
    '''Adds a model to the scene, default position is origin.
    Returns scene and models node.'''
    node = scene.add(model, pose=pose)

    a_x = random.uniform(-math.pi, math.pi)                     # Random x angle
    a_y = random.uniform(-math.pi, math.pi)                     # Random y angle

    scene = _add_rotation(scene, node, a_y, 'y')                # Add rotation
    scene = _add_rotation(scene, node, a_x, 'x')

    t_z = random.uniform(5, 12)                                 # Random translation
    t_x = random.uniform(-4, 4)
    t_y = random.uniform(-4, 4)

    # Multiply variables with model size to scale it
    try: t_x, t_y, t_z = [v1*v2 for v1, v2 in zip((t_x, t_y, t_z), node.mesh.extents)]
    except Exception as e: pass # Model is light and dont have mesh.extent

    scene = _add_translation(                                   # Add translation
        scene,
        node,
        x=t_x,
        y=t_y,
        z=-t_z
    )
    return scene, node

def _add_lighting(scene, light_type, random_range=(1, 4)):
    '''Takes scene and adds random amout of lighting.
    random_range:   Range to pick number of lights from.'''
    n = random.randrange(                                       # Number of lights
        random_range[0],
        random_range[1]
    )                    

    for _ in range(n):                                          # Add directional lights
        d = None
        if 'directional_lights'==light_type:
            d = pyrender.DirectionalLight(color=[1.0,1.0,1.0], intensity=2)
        elif 'point_lights'==light_type:
            d = pyrender.PointLight(color=[1.0,1.0,1.0], intensity=2)
        else:
            raise Exception('Light type not recognized, should be \"direction_lights\" or \"point_lights\", not {}'.format(light_type))

        _add_model(scene, d)

    return scene


def _add_camera(scene):
    '''Adds a camera to the scene'''
    cam = pyrender.PerspectiveCamera(                           # Create perspective camera
        yfov=np.pi/3.0,
        znear = 0.05,
        zfar=100
    )

    cam = scene.add(cam)                                        # Add camera to scene

    return scene, cam

def _add_rotation(scene, model, angle, axis):
    '''Applies a rotation matrix to the model'''
    mat = np.eye(4)
    if 'x'==axis:
        mat = np.array([                                        # Rotation matrix for x axis
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    elif 'y'==axis:
        mat = np.array([                                        # Rotation matrix for y axis
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    elif 'z'==axis:
        mat = np.array([                                        # Rotation matrix for z axis
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1] 
        ])
    scene = _update_model(scene, model, mat)
    return scene


def _add_translation(scene, model, x=0, y=0, z=0):
    '''Applies a translation matrix to the model'''
    mat = np.array([                                            # Translation matrix
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])
    scene = _update_model(scene, model, mat)
    return scene

def _update_model(scene, model, mat):
    '''Transposes matrix and applies it to the  model.
    Using method to avoid transposing multiple places 
    in the script.'''
    old = scene.get_pose(model)
    scene.set_pose(model, pose=np.matmul(mat, old))
    return scene