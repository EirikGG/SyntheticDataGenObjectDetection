import numpy, stl, pyrender, trimesh

def load_stl(path):
    '''Loads stl model and returns the loaded mesh'''
    try:
        return stl.mesh.Mesh.from_file(path)
    except Exception as e:
        print(e)
        print("Stl model loading failed")

def load_glTF(path):
    '''Loads a glTF file'''
    try:
        scene = trimesh.load(path)
        return pyrender.Mesh.from_trimesh(scene)
    except Exception as e:
        print(e)
        print("glTF model loading failed")

def load_obj(path):
    '''Loads a glTF file'''
    try:
        obj_trimesh = trimesh.load(path)
        return pyrender.Mesh.from_trimesh(obj_trimesh)
    except Exception as e:
        print(e)
        print("obj model loading failed")


if __name__ == "__main__":
    mdl_stl = load_stl('assets/test_model.stl')

    mdl_glb = load_glTF('assets/test.glb')

    print(mdl_glb)