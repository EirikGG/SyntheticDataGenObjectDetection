import os, humanize, time, pyrender, trimesh

import numpy as np

from dataset_generator.scene import scene_handler
from dataset_generator.tools import loader, saver, visualizer

def generate_dataset(
    n_imgs:int,
    model_path:str,
    output_path:str,
    model_name:str='3d_model',
    depth_img:bool=True,
    box_label:bool=True,
    box_format='yolo',
    mask_label:bool=True,
    bg_method:str='none',
    show_progress:bool=True,
    enable_print:bool=True,
    img_visualizer:bool=False,
    n_preview_images:int=2,
    image_dir:str = 'images',
    depth_dir:str = 'depth',
    box_dir:str = 'labels',
    mask_dir:str = 'mask',
    val_persentage:float=.2,
    train_dir_name:str='train',
    val_dir_name:str='val'):
    '''Loops trough number of images, generates a new image and saves the results.
    n_imgs:             number of images to create
    model_path:         path to main model
    output_path:        Results are written in subfolders of output_path
    model_name:         Name to use in label, default value is 3d_model
    depth_image:        Create depth images
    box_label:          Create box labels
    box_format:         Format for labels (yolo, kitti)
    mask_label:         Create seqmentation labels
    bg_method:          Which method to use when adding background
                        ('none', 'copy_paste', 'black', 'white', 'alpha_blend', 'random')
    show_progress:      Print progress while generating
    enable_print:       Enable disable all prints, overwrites "show progress"
    img_visualizer:     Enable image preview 
    n_preview_images:   Number of images to preview
    image_dir:          Name of output subfolder for images
    depth_dir:          Name of output subfolder for depth images
    box_dir:            Name of output subfolder for box labels
    mask_dir:           Name of output subfolder for mask labels
    
    val_persentage:     Presentage of validation images
    train_dir_name:     Name of training directory
    val_dir_name:       Name of validation directory'''


    if 0 >= n_imgs or not type(n_imgs) == int:                  # Number of images should be int and positive
        raise Exception('Number of images should be greater than zero and an integer, not {}'.format(n_imgs))

    if not os.path.isfile(model_path):                          # Ensures that model path points to file
        raise Exception('Model path dont point to a file: {}'.format(model_path))

    if os.path.isdir(output_path):                              # Ensures that output folder path is folder
        raise Exception('Output folder already exists: {}'.format(output_path))
    else: os.mkdir(output_path)

    print(image_dir, depth_dir, box_dir, mask_dir)

    for parent_dir in train_dir_name, val_dir_name:             # Create train and validation directory
        parent_dir_path = os.path.join(output_path, parent_dir) # Output parent directories
        os.mkdir(parent_dir_path)                               # Create directories

                                                                # Create sub-folder if they are selected
        for sub_dir, b in zip((image_dir, depth_dir, box_dir, mask_dir), (True, depth_img, box_label, mask_label)):
            if b:  
                sub_dir_path = os.path.join(parent_dir_path, sub_dir)
                sub_dir = sub_dir_path
                os.mkdir(sub_dir_path)
    
    print(image_dir, depth_dir, box_dir, mask_dir)

    if enable_print:                                            # Print configuration
        print('\n'.join((
            '\n',
            'Generating dataset with settings:\n',
            'Number of images:              {}'.format(n_imgs),
            'Model path:                    {}'.format(model_path),
            'Output path:                   {}'.format(output_path),
            'Create depth images:           {}'.format(depth_img),
            'Create mask lables:            {}'.format(mask_label),
            'Create box labels:             {}'.format(box_label),
            'Show progress:                 {}'.format(show_progress),
            '\n'
        )))

    sizes = np.array([])                                        # Save filesizes
    times = np.array([])                                        # Save creation time

    model = loader.load_model(                                  # Load model to use
        model_path=model_path
    )                       

    s_handler = scene_handler.Scene_Handler(model)              # Create scene handler object

    for i in range(n_imgs):                                     # Loop and create images
        start_time = time.time()                                # Save start time

        s_handler.generate_new_random_scene()                   # Generate new random scene
        s_handler.create_new_renderer()                         # Creates a new renderer

        parent_output_dir = ''
        if (n_imgs*val_persentage) > i:                         # Create validation set
            parent_output_dir = os.path.join(output_path, val_dir_name)
        else:                                                   # Create training set
            parent_output_dir = os.path.join(output_path, train_dir_name)

        if True:                                                # RGB images
            img = s_handler.get_img(bg_method)
            size = saver.save_pil_img(
                pil_img=img,
                folder=os.path.join(parent_output_dir, image_dir),
                name='image{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)
            
        if depth_img:                                           # Depth images
            img = s_handler.get_depth()
            size = saver.save_pil_img(
                pil_img=img,
                folder=os.path.join(parent_output_dir, depth_dir),
                name='depth{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)

        if box_label:                                           # Box labels
            box = s_handler.get_box(
                class_name=model_name,
                bbox_format=box_format
            )
            size = saver.save_txt(
                dic=box,
                folder=os.path.join(parent_output_dir, box_dir),
                name='image{}.txt'.format(i)
            )
            sizes = np.append(sizes, size)

        if mask_label:                                           # Seqmentation labels
            mask = s_handler.get_mask()
            size = saver.save_pil_img(
                pil_img=mask,
                folder=os.path.join(parent_output_dir, mask_dir),
                name='mask{}.jpg'.format(i)
            )
            sizes = np.append(sizes, size)

        s_handler.remove_renderer()                             # Deletes renderer and frees openGl resources   

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
            )), end='     \r', flush=True)


    if enable_print:                                            # Print ending statement
        working_dir = os.path.abspath(os.getcwd())
        print('\n'.join((
            '\n',
            'Finished in:                   {}s'.format(round(sum(times), 1)),
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
            img_path=os.path.join(parent_output_dir, image_dir),
            depth_path=os.path.join(parent_output_dir, depth_dir) if depth_img else None,

            box_path=os.path.join(parent_output_dir, box_dir) if box_label else None,
            mask_path=os.path.join(parent_output_dir, mask_dir) if mask_label else None,

            n = n_preview_images,

            bbox_format=box_format
        )