import pyrender, trimesh, random

from dataset_generator.scene import scene_generator
from dataset_generator.scene.generators import image_generator, depth_generator, box_generator, seg_generator

class Scene_Handler():
    _model = None
    _model_node = None
    _scene = None
    _renderer = None
    _camera = None
    

    def __init__(self, model):
        '''Loads model and generates a random scene'''
        self._model = model

    def generate_new_random_scene(self):
        '''Generates a new random scene and adds it to object field''' 
        self._scene, self._model_node, self._camera = scene_generator.generate_random_scene(self._model)
        self._generate_new_renderer()

    def _generate_new_renderer(self):
        '''Deletes previous renderer and creates a new one with random 
        height and width'''
        if self._renderer:                                              # Delete previous renderer
            self._renderer.delete()
        self._renderer = pyrender.OffscreenRenderer(                    # Define image size
            viewport_height=random.randint(400, 1080),
            viewport_width=random.randint(400, 1920)
        )    

    def get_img(self):
        '''Returns an image'''
        return image_generator.get_img(self._scene, self._renderer)

    def get_depth(self):
        '''Returns an image'''
        return depth_generator.get_depth(self._scene, self._renderer)

    def get_box(self):
        '''Returns a box label of object'''
        return box_generator.get_box(self._scene, self._renderer, self._model_node)

    
