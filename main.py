import os

from dataset_generator import dataset_generator


dataset_generator.generate_dataset(
    n_imgs=11,
    model_name='door_handle',
    model_path=os.path.join(os.getcwd(), 'assets', 'test.obj'),
    output_path='out',
    
    depth_img=True,
    box_label=True,
    mask_label=True,

    show_progress=True,
    enable_print=True,

    img_visualizer=True,
    n_preview_images=3,
)