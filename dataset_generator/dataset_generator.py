import os, humanize, time

import numpy as np

from dataset_generator.scene import scene_handler
from dataset_generator.tools import loader, saver, visualizer

def generate_dataset(n_imgs, model_path, output_path, model_name='3d_model', 
                        depth_img=True, box_label=True, seg_label=True, show_progress=True, 
                        enable_print=True, img_visualizer=False, n_preview_images=2):
    '''Loops trough number of images, generates a new image and saves the results.
    n_imgs:             number of images to create
    model_path:         path to main model
    output_path:        Results are written in subfolders of output_path
    rgb:                Create rgb images
    depth_image:        Create depth images
    box_label:          Create box labels
    seg_label:          Create seqmentation labels
    show_progress:      Print progress while generating
    enable_print:       Enable disable all prints, overwrites "show progress"
    img_visualizer:     Enable image preview 
    n_preview_images:   Number of images to previou'''


    if 0 >= n_imgs or not type(n_imgs) == int:                  # Number of images should be int and positive
        raise Exception('Number of images should be greater than zero and an integer, not {}'.format(n_imgs))

    if not os.path.isfile(model_path):                          # Ensures that model path points to file
        raise Exception('Model path dont point to a file: {}'.format(path))

    if not os.path.isdir(output_path):                          # Ensures that output folder path is folder
        raise Exception('Output path is not a directory: {}'.format(output_path))

    image_dir = 'images'                                        # Ensure image folder exists
    if not os.path.isdir(os.path.join(output_path, image_dir)):
        raise Exception('Missing "{}" output folder'.format(image_dir))

    depth_dir = 'depth'                                         # Ensure depth image folder exists
    if depth_img and not os.path.isdir(os.path.join(output_path, depth_dir)):
        raise Exception('Missing "{}" output folder'.format(depth_dir))

    box_dir = 'box'                                             # Ensure box label folder exists
    if box_label and not os.path.isdir(os.path.join(output_path, box_dir)):
        raise Exception('Missing "{}" output folder'.format(box_dir))
    
    seg_dir = 'seg'                                             # Ensure depth image folder exists
    if seg_label and not os.path.isdir(os.path.join(output_path, seg_dir)):
        raise Exception('Missing "{}" output folder'.format(seg_dir))

    if enable_print:                                            # Print configuration
        print('\n'.join((
            '\n',
            'Generating dataset with settings:\n',
            'Number of images:              {}'.format(n_imgs),
            'Model path:                    {}'.format(model_path),
            'Output path:                   {}'.format(output_path),
            'Create depth images:           {}'.format(depth_img),
            'Create segmentation lables:    {}'.format(seg_label),
            'Create box labels:             {}'.format(box_label),
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

        if True:                                                # RGB images
            img = s_handler.get_img()
            size = saver.save_pil_img(
                pil_img=img,
                folder=os.path.join(output_path, image_dir),
                name='image{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)
            
        if depth_img:                                           # Depth images
            img = s_handler.get_depth()
            size = saver.save_pil_img(
                pil_img=img,
                folder=os.path.join(output_path, depth_dir),
                name='depth{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)

        if box_label:                                           # Box labels
            box = s_handler.get_box(
                class_name=model_name
            )
            size = saver.save_json(
                dic=box,
                folder=os.path.join(output_path, box_dir),
                name='box{}.txt'.format(i)
            )
            sizes = np.append(sizes, size)

        if seg_label:                                           # Seqmentation labels
            pass

        times = np.append(times, time.time() - start_time)      # Save used time

        if show_progress and enable_print:                      # Print update
            loading_bar_size = 50
            avg_time = round(np.mean(times), 3)
            step_norm = round(((i+1)/n_imgs)*loading_bar_size)
            print(', '.join((
                '[{}{}]'.format(
                    ''.join(["#" for _ in range(step_norm)]), 
                    ''.join(["-" for _ in range(step_norm, loading_bar_size)])
                ),
                'Step {} / {}'.format(i+1, n_imgs),
                'Average time: {}s'.format(avg_time),
                'Remaining time: {}s'.format(round(avg_time * (n_imgs - i - 1), 3)),
                'Folder size: {}'.format(humanize.naturalsize(sum(sizes))),
            )), end='{}{}'.format(''.join([' 'for _ in range(10)]), '\r'))


    if enable_print:                                            # Print ending statement
        working_dir = os.path.abspath(os.getcwd())
        print('\n'.join((
            '\n',
            'Finished in:                   {}s'.format(round(sum(times))),
            'Dataset size:                  {}'.format(humanize.naturalsize(sum(sizes))),
            'Saved to folder:               {}'.format(os.path.join(working_dir, output_path)),
            '',
        ))) 


    user_conf = True                                            # User confirmation flag
    if 5 < n_preview_images:
        while True:                                             # Warn user that each preview image opens a window
            user_msg = input(('Are you sure you want to display {} images,' 
                            ' this would open {} separate windows.'
                            ' (yes/no): ').format(
                n_preview_images,
                n_preview_images
            ))
            if user_msg in ('yes', 'y'):
                break
            elif user_msg in ('no', 'n'):
                user_conf = False
                break

    if img_visualizer and user_conf:                            # Show random selection of images

        print('Starting image preview of {} image(s):'.format(n_preview_images))
        visualizer.show_images(
            img_path=os.path.join(output_path, image_dir),
            depth_path=os.path.join(output_path, depth_dir) if depth_img else None,

            box_path=os.path.join(output_path, box_dir) if box_label else None,
            seg_path=os.path.join(output_path, seg_dir) if seg_label else None,

            n = n_preview_images
        )