import os, pyrender, trimesh

def load_model(model_path):
    suffix = model_path.split('.')[-1]                      # Get model suffix

    if 'obj'==suffix:
        return load_obj(model_path)

    else:
        raise Exception('Model extension not recognised')


def load_obj(path):
    '''Loads a object file'''
    obj_trimesh = trimesh.load(path)
    return pyrender.Mesh.from_trimesh(obj_trimesh)