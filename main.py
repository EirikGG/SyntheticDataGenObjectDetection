from tools import load_mesh, visualize_mesh, imgs_generator


mesh = load_mesh.load_stl("assets/test_model.stl")
#visualize_mesh.show_model(model)

imgs_generator.generate_dataset(n_imgs=1, model=mesh, output_path='')

