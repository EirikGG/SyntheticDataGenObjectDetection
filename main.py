import os

from dataset_generator import dataset_generator

models = ('test_object_rect_100_50_20', )
models = ('musicAngle3', )

for model in models:
    model_path = os.path.join(os.getcwd(), 'assets', f'{model}.obj')

    dataset_generator.generate_dataset(
        n_imgs=100,
        model_path=model_path,
        output_path=f'out_{model}',
        model_name='1',
     
        image_dir='images',       
        depth_img=False,
        box_label=True,
        box_format='yolo',
        box_dir='labels',
        mask_label=False,
        
        bg_method='color',
        
        show_progress=True,
        enable_print=True,
        
        img_visualizer=True,
        n_preview_images=3,

        val_persentage=.1
    )