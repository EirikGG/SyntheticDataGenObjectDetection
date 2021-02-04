import os, humanize, time

import numpy as np

from dataset_generator.scene import scene_handler
from dataset_generator.tools import loader, saver

def generate_dataset(n_imgs, model_path, output_path, rgb_img=True, depth_img=True, box_label=True, seg_label=True, show_progress=True, enable_print=True):
    '''Loops trough number of images, generates a new image and saves the results.
    n_imgs: number of images to create
    model_path: path to model
    output_path: Results are written in subfolders
    rgb: Create rgb images
    depth_image: Create depth images
    show_progress: Print progress while generating
    enable_print: Enable disable all prints, overwrites "show progress"'''
    if not os.path.isfile(model_path):                          # Ensures that model path points to file
        raise Exception("Model path dont point to a file: {}".format(path))

    if not os.path.isdir(output_path):                          # Ensures that output folder path is folder
        raise Exception("Output path is not a directory:\n{}".format(output_path))

    if enable_print:                                            # Print configuration
        print('\n'.join((
            '\n',
            'Generating dataset with settings:\n',
            'Number of images:              {}'.format(n_imgs),
            'Model path:                    {}'.format(model_path),
            'Output path:                   {}'.format(output_path),
            'Create rgb images:             {}'.format(rgb_img),
            'Create depth images:           {}'.format(depth_img),
            'Create segmentation lables:    {}'.format(box_label),
            'Create box labels:             {}'.format(seg_label),
            'Show progress:                 {}'.format(show_progress),
            '\n'
        )))

    sizes = np.array([])                                        # Save filesizes
    times = np.array([])                                        # Save creation time

    model = loader.load_model(model_path)                       # Load model to use

    s_handler = scene_handler.Scene_Handler(model)              # Create scene handler object


    for i in range(n_imgs):                                     # Loop and create images
        start_time = time.time()                                # Save start time

        s_handler.generate_new_random_scene()                   # Generate new random scene

        if rgb_img:                                             # RGB images
            img = s_handler.get_img()
            size = saver._save_pil_img(
                pil_img=img,
                folder=os.path.join(output_path, 'images'),
                name='image{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)
            
        if depth_img:                                           # Depth images
            img = s_handler.get_depth()
            size = saver._save_pil_img(
                pil_img=img,
                folder=os.path.join(output_path, 'depth'),
                name='depth{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)

        if box_label:                                           # Box labels
            pass

        if seg_label:                                           # Seqmentation labels
            pass

        times = np.append(times, time.time() - start_time)      # Save used time

        if show_progress and enable_print:                      # Print update
            loading_bar_size = 50
            step_norm = round(((i+1)/n_imgs)*loading_bar_size)
            print(', '.join((
                '[{}{}]'.format(
                    ''.join(["#" for _ in range(step_norm)]), 
                    ''.join(["-" for _ in range(step_norm, loading_bar_size)])
                ),
                'Step {} / {}'.format(i+1, n_imgs),
                'Average time: {}s'.format(round(np.mean(times),3)),
                'Folder size: {}'.format(humanize.naturalsize(sum(sizes)))
            )), end='\r')
    print('\n')                                                 # Add newline after loop


    if enable_print:                                            # Print ending statement
        working_dir = os.path.abspath(os.getcwd())
        print('Dataset saved to folder: {}'.format(os.path.join(working_dir, output_path)))


