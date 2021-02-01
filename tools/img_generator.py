import time, random, pyrender, trimesh

def create_img(model, output_path):
    '''Times and mesures generated image'''
    t0 = time.time()
    time.sleep(random.uniform(.05, 1))
    create_scene(model)
    return {
        "size": random.uniform(1, 3),
        "time": time.time() - t0
    }

def create_scene(model):
    '''Creates a scene'''
    scene = pyrender.Scene()
    scene.add(model)
