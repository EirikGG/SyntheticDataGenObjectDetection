import os, time, random, pyrender, trimesh, math

import numpy as np

from PIL import Image


def create_img(model):
    '''Takes a model and generates a scene using the model,
    scene is buildt with random lighting and random orientations.
    Also times and mesures generated image'''
    t0 = time.time()

    scene, model_node = _create_scene(model)                        # Create scene and adds model to it
    scene = _add_lighting(scene)                                    # Add lighting
    scene = _add_camera(scene)                                      # Add camera to scene
    
    for axis in ['x', 'y', 'z']:
        angle = random.uniform(0, 2*math.pi)                        # Find random angle and convert to radians
        scene = _add_rotation(scene, model_node, angle, axis)

    img, depth = _get_img(scene)                                    # Take image
    
    return {                                                        # Return new image and time to create
        'img': img,
        'depth': depth,
        "time": time.time() - t0
    }

def _create_scene(model):
    '''Creates a scene'''
    scene = pyrender.Scene()                                        # Creates a scene
    model_node = scene.add(model, pose=np.eye(4))                   # Adds model and saves node
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
    r = pyrender.OffscreenRenderer(                                 # Define image size
        viewport_height=random.randint(400, 1080),
        viewport_width=random.randint(400, 1920)
    )                       
    color, depth = r.render(scene)                                  # Get image
    r.delete()                                                      # Remove renderer

    img = Image.fromarray(color.astype('uint8'), 'RGB')             # Convert from point cloud to pil image
    depth_img = Image.fromarray(np.uint8(depth*255), 'L')           # Convert from 2d array to pil image

    return img, depth_img

def _add_rotation(scene, model, angle, axis):
    '''Applies a rotation matrix to the model'''
    mat = np.eye(4)
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
    scene = _change_model(scene, model, mat)
    return scene

def _add_translation(scene, model, x=0, y=0, z=0):
    '''Applies a translation matrix to the model'''
    mat = np.array([                                                # Translation matrix
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0]
    ])
    scene = _change_model(scene, model, mat)
    return scene

def _change_model(scene, model, mat):
    '''Transposes matrix and applies it to the  model.
    Using method to avoid transposing multiple places 
    in the script.'''
    mat = np.matrix.transpose(mat)
    scene.set_pose(model, pose=mat)
    return scene
