import pyrender


def get_box(scene, renderer, model):
    '''Takes a rendered image from the scene'''
    color, _ = renderer.render(scene)                               # Get image
    return color