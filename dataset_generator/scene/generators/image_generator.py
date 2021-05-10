import pyrender, os, random

import numpy as np

from PIL import Image

def _create_img(scene, renderer, bg_color):
    scene.bg_color = bg_color
    color, _ = renderer.render(                                             # Get image
        scene,
    )                                       
    return Image.fromarray(color.astype('uint8'), 'RGB')                    # Convert from point cloud to pil image

def _get_rand_img(folder):
    '''Returns random image from folder path'''
    bg_path = os.path.join(os.getcwd(), folder)                             # Get full folder path
    images_filtered = list(filter(lambda x: x.endswith((                    # Filter images
        '.jpg',
        '.png',
        '.jpeg'
    )), os.listdir(bg_path)))

    bg_img_name = random.choice(images_filtered)                            # List images in directory
    return Image.open(os.path.join(bg_path, bg_img_name))                   # Open random image


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

            img = _create_img(scene, renderer, col_arr)
        except:
            raise Exception('Color not formated correctly (color: r,g,b), ex: "color:255,255,255"')

    
    elif 'random'==bg_method:
        scene_img = _create_img(scene, renderer, (0, 0, 0, 0)).convert('RGB')

        # https://stackoverflow.com/questions/59056216/how-do-you-generate-an-image-where-each-pixel-is-a-random-color-in-python
        w,h = scene_img.size
        rand_arr = np.random.randint(low = 0, high = 255, size=(h, w, 3))
        rand_img = Image.fromarray(rand_arr.astype('uint8')).convert('RGB') # Create image of rnadom color

        # https://stackoverflow.com/questions/56942102/how-to-generate-a-mask-using-pillows-image-load-function
        scene_arr = np.array(scene_img)
        mask_arr = scene_arr[:,:,2] > 0
        mask_img = Image.fromarray((mask_arr*255).astype(np.uint8)).convert('L')
        img = Image.composite(scene_img, rand_img, mask_img)                # Combine images

    elif 'alpha_blend'in bg_method:
        bg_img = _get_rand_img(bg_images)

        renderer.viewport_height = bg_img.size[1]                           # Match height dimension
        renderer.viewport_width = bg_img.size[0]                            # Match width dimension
        scene_img = _create_img(scene, renderer, (255//2,255//2,255//2,0))  # Create image of model


        alpha = int(bg_method.split(':')[-1]) if ':' in bg_method else .2    # Get alpha value from input
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
        bg_img = _get_rand_img(bg_images)                                   # Get random background image

        renderer.viewport_height = bg_img.size[1]                           # Match height dimension
        renderer.viewport_width = bg_img.size[0]                            # Match width dimension
        scene_img = _create_img(scene, renderer, (255, 255, 255))           # Get scene image
        
        # https://stackoverflow.com/questions/56942102/how-to-generate-a-mask-using-pillows-image-load-function
        scene_arr = np.array(scene_img)
        mask_arr = scene_arr[:,:,2] < 255
        mask_img = Image.fromarray((mask_arr*255).astype(np.uint8)).convert('L')
        
        img = Image.composite(scene_img, bg_img, mask_img)                  # Combine images

    else:
        raise('Bacground method not recognized', bg_method)


    return img