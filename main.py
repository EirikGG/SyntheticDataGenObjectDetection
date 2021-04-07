import os

from dataset_generator import dataset_generator

models = ('cube_red', )

for model in models:
    model_path = os.path.join(os.getcwd(), 'assets', f'{model}.obj')

    dataset_generator.generate_dataset(
        n_imgs=1000,
        model_name=model,
        model_path=model_path,
        output_path=model,
        
        depth_img=True,
        box_label=True,
        mask_label=True,
        
        bg_method='color:0,0,0',
        
        show_progress=True,
        enable_print=True,
        
        img_visualizer=True,
        n_preview_images=3,
    )