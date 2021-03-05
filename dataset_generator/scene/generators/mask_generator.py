import pyrender, trimesh

import numpy as np

from PIL import Image

def get_mask(scene, renderer, model_node):
    '''Creates mask of model from scene by using depth information.'''
    main_camera = scene.main_camera_node                            # Get main camera

    new_scene = pyrender.Scene()                                    # Create empty scene

    new_scene.add_node(main_camera)                                 # Add camera to new scene
    new_scene.add_node(model_node)                                  # Add main model to scene

    _, depth = renderer.render(new_scene)                           # Get image

    mask = np.where(0<depth, 1, 0)                                  # Filter values to create mask

    return Image.fromarray(np.uint8(mask*255), 'L')                 # Convert from 2d array to pil image