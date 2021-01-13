from tools import load_model, visualize

model = load_model.load_stl("assets/test_file.stl")
visualize.show_model(model)