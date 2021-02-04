from tools import load_model, visualize, imgs_generator, url


path = url.path_from_relative('assets/test.obj')

mesh = load_model.load_obj(path)

#visualize.show_obj(mesh)

imgs_generator.generate_dataset(
    n_imgs=100, 
    model=mesh, 
    output_path='out', 
    show_progress=True,
    enable_print=True
) 