

from tools import load_mesh, visualize_mesh, imgs_generator




if __name__ == "__main__":
    model = load_mesh.load_stl("assets/test_file.stl")
    #visualize_mesh.show_model(model)

    imgs_generator.generate_dataset(n_imgs=100, show_progress=True)

