import os

from tools import load_model, visualize_mesh, imgs_generator, url

path = url.path_from_relative('assets/test.obj')

mesh = load_model.load_obj(path)

visualize_mesh.show_obj(mesh)

imgs_generator.generate_dataset(
    n_imgs=5, 
    model=mesh, 
    output_path='', 
    show_progress=True,
    enable_print=True
)
