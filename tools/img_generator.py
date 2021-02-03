import os, time, random, pyrender, trimesh, math

import numpy as np

from PIL import Image


def create_img(model):
    '''Takes a model and generates a scene using the model,
    scene is buildt with random lighting and random orientations.
    Also times and mesures generated image'''
    t0 = time.time()

    scene, model_node = _create_scene(model)                        # Create scene and add
    scene = _add_lighting(scene)                                    # Add lighting
    scene = _add_camera(scene)                                      # Add camera to scene

    img = _get_img(scene)                                           # Take image
    
    pyrender.Viewer(scene, use_raymond_lighting=False)
    _add_rotation(scene, model_node, 180.0*math.pi/180.0, 'x')
    pyrender.Viewer(scene, use_raymond_lighting=False)
    
    return {                                                        # Return new image and time to create
        'img': img,
        "time": time.time() - t0
    }

def _create_scene(model):
    '''Creates a scene'''
    scene = pyrender.Scene()                                        # Creates a scene
    model_node = scene.add(model)                                   # Adds model and saves node
    return scene, model_node

def _add_lighting(scene, r_dir=(0, 2), r_p=(1, 4)):
    '''Takes scene and adds random amout of lighting.
    r_dir:   Range to pick number of directional lights from.
    r_p:     Range to pick number of point lights from.'''
    n_dir = random.randrange(r_dir[0], r_dir[1])                    # Number of directional lights
    n_p = random.randrange(r_p[0], r_p[1])                          # Number of point lights

    for _ in range(n_dir):                                          # Add directional lights
        d = pyrender.DirectionalLight(color=[1.0,1.0,1.0], intensity=2.0)
        scene.add(d)

    for _ in range(n_p):                                            # Add point lights
        p = pyrender.PointLight(color=[1.0,1.0,1.0], intensity=2.0)
        scene.add(p)

    return scene

def _add_camera(scene):
    '''Adds a camera to the scene'''
    cam = pyrender.PerspectiveCamera(yfov=np.pi/3.0)                # Create perspective camera
    s = np.sqrt(2)/2
    mat = np.array([                                                # Perspective matrix
        [0.0, -s, s, 0.3],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, s, s, 0.35],
        [0.0, 0.0, 0.0, 1.0]
    ])

    scene.add(cam, pose=mat)                                        # Add camera to scene
    return scene

def _get_img(scene):
    '''Takes a rendered image from the scene'''
    r = pyrender.OffscreenRenderer(640, 480)                        # Define image size
    color, depth = r.render(scene)                                  # Get image
    r.delete()                                                      # Remove renderer

    img = Image.fromarray(color.astype('uint8'), 'RGB')             # Convert from point cloud to pil image
    depth_img = Image.fromarray(depth.astype('uint8'), 'L') 

    return img

def _add_rotation(scene, model, angle, axis):
    '''Applies a rotation matrix to the model'''
    mat = None
    if 'x'==axis:
        mat = np.array([                                            # Rotation matrix for x axis
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    elif 'y'==axis:
        mat = np.array([                                            # Rotation matrix for y axis
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    elif 'z'==axis:
        mat = np.array([                                            # Rotation matrix for z axis
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1] 
        ])
    scene.set_pose(model, pose=mat)
    return scene

def _add_translation(scene, model, x=0, y=0, z=0):
    '''Applies a translation matrix to the model'''
    mat = np.array([                                                # Translation matrix
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0]
    ])
    scene.set_pose(model, pose=mat)
    return scene