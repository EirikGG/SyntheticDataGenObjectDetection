import pyrender, math, trimesh

import numpy as np

from PIL import Image

def get_mask(scene, renderer, model_node):
    '''Creates mask of model from scene.'''
    _, depth = renderer.render(scene)                               # Get image
    
    mask = np.where(0<depth, 1, 0)                                  # Filter values to create mask

    return Image.fromarray(np.uint8(mask*255), 'L')                 # Convert from 2d array to pil image