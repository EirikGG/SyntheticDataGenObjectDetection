import os, random, json

import matplotlib.pyplot as plt 
import matplotlib.patches as patches

from PIL import Image

# https://matplotlib.org/3.1.1/gallery/widgets/buttons.html
# https://matplotlib.org/examples/pylab_examples/subplots_demo.html#pylab-examples-subplots-demo

def get_full_path(p):
    return os.path.join(os.getcwd(), p)

def show_images(img_path=None, depth_path=None, box_path=None, seg_path=None, n=3):
    '''Displays n random images'''
    row, col = 1, 2
    f, axarr = plt.subplots(row, col)

    if img_path:
        path = get_full_path(img_path)
        img = os.listdir(path)[0]
        axarr[0].imshow(plt.imread(os.path.join(path, img)))
        if box_path:
            box_p = get_full_path(box_path)
            box = os.listdir(box_p)[0]
            with open(os.path.join(box_p, box)) as f:
                data = dict(json.load(f))
                print(data)
            
            rect = patches.Rectangle((data['x'], data['y']), 100,100,linewidth=1,edgecolor='r',facecolor='none')
            axarr[0].add_patch(rect)

    if depth_path:
        dept = get_full_path(depth_path)
        img = os.listdir(dept)[0]
        axarr[1].imshow(plt.imread(os.path.join(dept, img)))


    plt.show()
    '''
    for imgs in random.choices(list(zip(*map(os.listdir, dirs))), k=n):
        f, axarr = plt.subplots(1, len(imgs))
        for i, img in enumerate(imgs):
            path = os.path.join(
                os.path.abspath(
                    os.getcwd()),
                    os.path.join(dirs[i],
                    img
                )
            )
            axarr[i].imshow(plt.imread(path))
        plt.show()
    '''


if '__main__'==__name__:
    show_images(img_path='out\\images', depth_path='out\\depth', box_path='out\\box', seg_path=None, n=3)