import os, time, random, pyrender, trimesh, math

import numpy as np

from PIL import Image


def create_img(model):
    '''Times and mesures generated image'''
    t0 = time.time()

    scene = _create_scene(model)
    scene = _add_lighting(scene)
    scene = _add_camera(scene)

    img = _get_img(scene)
    
    #pyrender.Viewer(scene, use_raymond_lighting=False)
    
    return {
        'img': img,
        "time": time.time() - t0
    }

def _create_scene(model):
    '''Creates a scene'''
    scene = pyrender.Scene()
    scene.add(model)
    return scene

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
    r = pyrender.OffscreenRenderer(640, 480)                        # Define image size
    color, depth = r.render(scene)                                  # Get image
    r.delete()                                                      # Remove renderer

    img = Image.fromarray(color.astype('uint8'), 'RGB')             # Convert from point cloud to pil image
    depth_img = Image.fromarray(depth.astype('uint8'), 'L') 

    return img

