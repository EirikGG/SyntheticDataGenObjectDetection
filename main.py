from dataset_generator import dataset_generator

#visualize.show_obj(mesh)

dataset_generator.generate_dataset(
    n_imgs=10, 
    model_path='assets\\test.obj',
    output_path='out',
    rgb_img=True,
    depth_img=True,
    box_label=False,
    seg_label=False,

    show_progress=True,
    enable_print=True
) 