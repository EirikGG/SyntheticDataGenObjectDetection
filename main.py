from dataset_generator import dataset_generator

dataset_generator.generate_dataset(
    n_imgs=10000, 
    model_path='assets\\test.obj',
    output_path='out',
    rgb_img=True,
    depth_img=True,
    box_label=True,
    seg_label=False,

    show_progress=True,
    enable_print=True,

    img_visualizer=True,
    n_preview_images=2,
) 