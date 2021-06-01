import os

from dataset_generator import dataset_generator

models = (
    dict(
        model_name='musicAngle3',
        cls = '0'
        ),
    dict(
        model_name='test_object_rect_100_50_20',
        cls = '1'
    )
)

for model in models:
    model_path = os.path.join(os.getcwd(), 'assets', f'{model["model_name"]}.obj')

    dataset_generator.generate_dataset(
        n_imgs=10000,
        model_path=model_path,
        output_path=f'out_{model["model_name"]}',
        model_name=model['cls'],
     
        image_dir='images',       
        depth_img=False,
        box_label=True,
        box_format='yolo',
        box_dir='labels',
        mask_label=False,
        
        bg_method='random_mix',
        
        show_progress=True,
        enable_print=True,
        
        img_visualizer=False,
        n_preview_images=5,

        val_persentage=.2
    )