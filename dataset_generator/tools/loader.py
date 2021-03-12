import os, pyrender, trimesh

def load_model(model_path):
    suffix = model_path.split('.')[-1]                      # Get model suffix

    if suffix in ('obj', 'stl'):
        return load_obj(model_path)

    else:
        raise Exception('Model extension not recognised')


def load_obj(path):
    '''Loads a object file'''
    obj_trimesh = trimesh.load(path)                        # Load mesh from path
    
    return pyrender.Mesh.from_trimesh(obj_trimesh)