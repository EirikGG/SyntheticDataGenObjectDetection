import os, random

import matplotlib.pyplot as plt 

from PIL import Image

# https://matplotlib.org/3.1.1/gallery/widgets/buttons.html
# https://matplotlib.org/examples/pylab_examples/subplots_demo.html#pylab-examples-subplots-demo

def show_images(dirs, n=3):
    '''Displays 3 random images'''
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



if '__main__'==__name__:
    show_images((
        'out\\depth',
        'out\\images',
    ))