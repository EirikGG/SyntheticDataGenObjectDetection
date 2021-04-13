import os, random, json

import matplotlib.pyplot as plt 
import matplotlib.patches as patches

from PIL import Image


def get_full_path(p):
    return os.path.join(os.getcwd(), p)

def get_coord(bbox, bbox_format, img_dim):
    '''Takes bbox information and returns coordinates, (left, top, width, height)'''
    if 'kitti' == bbox_format:
        return int(bbox[4]),  int(bbox[5]), int(bbox[6]) - int(bbox[4]), int(bbox[7]) - int(bbox[5])

    image_w, image_h = img_dim[1], img_dim[0]
    if 'yolo' == bbox_format:
        x = int(float(bbox[1])*image_w)
        y = int(float(bbox[2])*image_h)
        w = int(float(bbox[3])*image_w)
        h = int(float(bbox[4])*image_h)
        
        return x-w/2, y-h/2, w, h

def show_images(img_path, depth_path=None, box_path=None, mask_path=None, n=3, bbox_format='kitti'):
    '''Displays n random images'''
    row, col = 2, 2 
    
    imgs_path = get_full_path(img_path)                             # Full path to image directory
    imgs = sorted(os.listdir(imgs_path))                            # List images in directory

    if len(imgs) < n:                                               # Adjust n images to max number 
        n = len(imgs)

    for i in random.sample(range(len(imgs)), k=n):                  # Loop trough n random picked image indecies

        f, axarr = plt.subplots(                                    # Create empty figure
            row, 
            col,
            figsize=(15, 10)
        )
        
        img = imgs[i]                                               # Picked image

        img_arr = plt.imread(os.path.join(img_path, img))

        axarr[0, 0].imshow(img_arr)                                 # Add image to first subplot
        axarr[0, 0].title.set_text('Image: {}'.format(img))         # Add title to subplot

        if box_path:
            axarr[1, 0].imshow(plt.imread(os.path.join(img_path, img)))

            bp = get_full_path(box_path)                            # Path to box dir
            
            box = sorted(os.listdir(bp))[i]                         # Pick same box as image
            with open(os.path.join(bp, box)) as f:                  # Read file
                bbox = f.read().split()                             # Load text
            
            x, y, w, h = get_coord(bbox, bbox_format, img_arr.shape)

            rect = patches.Rectangle(                               # Create new rectangle
                (x, y),
                w,                                                  # Width
                h,                                                  # Height
                linewidth=1,
                edgecolor='r',
                facecolor='none'
            )
            axarr[1, 0].add_patch(rect)                             # Add rectangle to subplot
            axarr[1, 0].title.set_text('Box label: {}'.format(box)) # Add title to subplot

        if depth_path:                                              # Print deph image
            dp = get_full_path(depth_path)                          # Depth image folder
            depth_img = sorted(os.listdir(dp))[i]                   # Pick image
            axarr[0, 1].imshow(                                     # Add to subplot
                plt.imread(os.path.join(dp, depth_img)),
                cmap='gray',
                vmin=0,
                vmax=255
            )                                                       # Add title to subplot
            axarr[0, 1].title.set_text('Depth image: {}'.format(depth_img))

        if mask_path:                                               # Print mask image
            mp = get_full_path(mask_path)                           # Depth image folder
            mask_img = sorted(os.listdir(mp))[i]                    # Pick image
            axarr[1, 1].imshow(                                     # Add to subplot
                plt.imread(os.path.join(mp, mask_img)),
                cmap='gray',
                vmin=0,
                vmax=255
            )                                                       # Add title to subplot
            axarr[1, 1].title.set_text('Mask image: {}'.format(mask_img))
            
    plt.show()                                                      # Show figure
    


if '__main__'==__name__:
    show_images(img_path='out\\images', depth_path='out\\depth', box_path='out\\box', mask_path=None, n=3)