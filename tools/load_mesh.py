import numpy, stl


def load_stl(path):
    '''
    Loads stl model and returns the loaded mesh
    '''
    try:
        return stl.mesh.Mesh.from_file(path)
    except Exception as e:
        print(e)
        print("Stl model loading failed")


if __name__ == "__main__":
    model = load_stl('test_file.stl')