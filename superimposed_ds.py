import os, random

import numpy as np

from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS

from dataset_generator.tools import create_bg

folder_path = 'N:\\TestObjects\\Meshroom-2021.1.0-win64\\speaker\\speaker_img6'

output_path = 'C:\\Users\\Eirik\\OneDrive\\school\\Simulation and Visualization\\4.semester\\Master_project\\s1_generate_dataset\\code\\test'


n_imgs = 10
val_ratio = .2

DEBUG = True

images = tuple(filter(lambda x: x.endswith('.jpg'), os.listdir(folder_path)))

for i in range(10):
    basename = random.choice(images).split(".")[:-1]

    img = Image.open(os.path.join(folder_path, f'{"".join(basename)}{".jpg"}'))
    lbl = Image.open(os.path.join(folder_path, f'{"".join(basename)}{"_mask.png"}')).convert('L')

    img.putalpha(lbl)

    bg_img = None
    method = random.choice((1, 2, 3))

    if 1 == method:
        bg_img = create_bg.get_rand_img('bg_images')
    elif 2 == method:
        bg_img = create_bg.get_color_img(img.size)
    elif 3 == method:
        bg_img = create_bg.get_color_noise(img.size)


    size = random.randint(100, 500)
    img = img.resize((size, size))
    lbl = lbl.resize((size, size))

    white_px = np.where(255 == np.array(lbl))
    x0, x1 = min(white_px[1]), max(white_px[1])
    y0, y1 = min(white_px[0]), max(white_px[0])

    cropped = img.crop((x0, y0, x1, y1))

    x, y = random.randint(0, bg_img.size[0]-(x1-x0)), random.randint(0, bg_img.size[1]-(y1-y0))
    bg_img.paste(
        cropped, 
        (x, y), 
        cropped)

    if DEBUG:
        rect_img = ImageDraw.Draw(bg_img)
        rect_img.rectangle(
            ((x, y), 
            (x+cropped.size[0], y+cropped.size[1])),
            outline='red',
            width=3
        )
        rect_img.point(
            (x+cropped.size[0]//2, y+cropped.size[1]//2)
        )
        bg_img.show()

    yolo_lbl = f'{"0"} {x+cropped.size[0]//2} {y+cropped.size[1]//2} {x1-x0} {y1-y0}'


    out = ''
    if i < n_imgs*val_ratio:
        out = os.path.join(output_path, 'val')
    else: 
        out = os.path.join(output_path, 'train')

    img_out = os.path.join(out, 'images')
    val_out = os.path.join(out, 'labels')

    if not os.path.isdir(img_out): os.makedirs(img_out)
    if not os.path.isdir(val_out): os.makedirs(val_out)

    bg_img.save(os.path.join(img_out, f'image{i}.jpg'))

    with open(os.path.join(val_out, f'image{i}.txt'), 'w') as f: f.writelines(yolo_lbl)