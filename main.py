from dataset_generator import dataset_generator

dataset_generator.generate_dataset(
    n_imgs=10,
    model_name='door_handle',
    model_path='assets\\test.obj',
    output_path='out',
    
    depth_img=True,
    box_label=True,
    mask_label=True,

    show_progress=True,
    enable_print=True,

    img_visualizer=True,
    n_preview_images=3,
)