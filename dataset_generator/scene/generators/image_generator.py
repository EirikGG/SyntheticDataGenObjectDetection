import pyrender, os, random

import numpy as np

from PIL import Image
from dataset_generator.tools import create_bg

def _create_img(scene, renderer, bg_color, mode='RGB'):
    scene.bg_color = bg_color
    color, depth = renderer.render(                                         # Get image
        scene,
        pyrender.RenderFlags.RGBA if 'RGBA'==mode else pyrender.RenderFlags.NONE
    )
    return Image.fromarray(color, mode) # Convert from point cloud to pil image.astype('uint8'), mode

def get_img(scene, renderer, bg_method:str, bg_images:str='bg_images'):
    '''Takes a rendered image from the scene'''
    img = None

    if 'random_mix' == bg_method: 
        bg_method = random.choice((
            f'color:{random.randrange(255)},{random.randrange(255)},{random.randrange(255)}',
            'random',
            'alpha_blend',
            'copy_paste'
        ))

    if 'color' in bg_method:
        try:
            col_str = bg_method.split(':')[1]
            col_arr = list(map(int, col_str.split(',')))

            img, _ = _create_img(scene, renderer, col_arr)
        except:     # No color specified, use random color
            col_arr = np.random.randint(low = 0, high = 255, size=3)
            img = _create_img(scene, renderer, col_arr)
    
    elif 'random'==bg_method:
        scene_img = _create_img(scene, renderer, (0, 0, 0, 0)).convert('RGB')

        rand_img = create_bg.get_color_noise((*scene_img.size, 3))

        # https://stackoverflow.com/questions/56942102/how-to-generate-a-mask-using-pillows-image-load-function
        scene_arr = np.array(scene_img)
        mask_arr = scene_arr[:,:,2] > 0
        mask_img = Image.fromarray((mask_arr*255).astype(np.uint8)).convert('L')
        img = Image.composite(scene_img, rand_img, mask_img)                # Combine images

    elif 'alpha_blend'in bg_method:
        bg_img = create_bg.get_rand_img(bg_images)


        renderer.viewport_height = bg_img.size[1]                           # Match height dimension
        renderer.viewport_width = bg_img.size[0]                            # Match width dimension
        scene_img = _create_img(scene, renderer, (255//2,255//2,255//2,0))  # Create image of model
                                                                            # Get alpha value from input, else random
        alpha = int(bg_method.split(':')[-1]) if ':' in bg_method else .2
        try: img = Image.blend(scene_img, bg_img, alpha=alpha)
        except Exception as e:
            print('\n\n')
            print(bg_img.mode)
            print(scene_img.mode)
            print('\n\n')

            bg_img.show()
            scene_img.show()

            raise e

    elif 'copy_paste'==bg_method:
        bg_img = create_bg.get_rand_img(bg_images)                          # Get random background image

        renderer.viewport_height = bg_img.size[1]                           # Match height dimension
        renderer.viewport_width = bg_img.size[0]                            # Match width dimension
        scene_img = _create_img(                                            # Get scene image
            scene,
            renderer,
            bg_color=(0, 0, 0, 0),
            mode='RGBA'
        )
        
        img = Image.alpha_composite(bg_img.convert("RGBA"), scene_img)      # Combine images

        img = img.convert("RGB")

    else:
        raise('Bacground method not recognized', bg_method)


    return img