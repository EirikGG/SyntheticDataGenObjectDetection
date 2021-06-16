import os

from dataset_generator import dataset_generator

models = (
    dict(
        model_name = 'musicAngle3',
        cls = '0'
    ),
    dict(
        model_name = 'test_object_rect_100_50_20',
        cls = '1'
    ),
    dict(
        model_name = 'green_rect',
        cls = '2'
    )
)

models = [models[-1]]

for model in models:
    model_path = os.path.join(os.getcwd(), 'assets', f'{model["model_name"]}.obj')

    dataset_generator.generate_dataset(
        n_imgs=10,
        model_path=model_path,
        output_path=f'out_{model["model_name"]}',
        model_name=model['cls'],
     
        image_dir='images',       
        depth_img=False,
        box_label=True,
        box_format='yolo',
        box_dir='labels',
        mask_label=False,
        
        bg_method='copy_paste',
        
        show_progress=True,
        enable_print=True,
        
        img_visualizer=True,
        n_preview_images=3,

        val_persentage=.2
    )