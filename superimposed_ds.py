import os, random, time

import numpy as np

from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS

from dataset_generator.tools import create_bg

folder_path = '/home/eirikgg/Downloads/speaker_img6'

output_path = '/home/eirikgg/msc/yolov5Dir/superimposed_speaker'
#output_path = '/home/eirikgg/msc/3D-model-image-dataset-generation/test'

n_imgs = 10
val_ratio = .166666667

DEBUG = False

images = tuple(filter(lambda x: x.endswith('.jpg'), os.listdir(folder_path)))

t0 = time.time()
for i in range(n_imgs):
    if 0==i%100: print(f'{i} / {n_imgs}')
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
        width, height = img.size
        bg_img = create_bg.get_color_noise(width, height)

    #bg_img = Image.open('/home/eirikgg/msc/3D-model-image-dataset-generation/bg_images/um_000050.png')

    bg_x_size = bg_img.size[0]
    sizex = random.randint(int(bg_x_size*.1), int(bg_x_size*.4))
    img = img.resize((sizex, sizex))
    lbl = lbl.resize((sizex, sizex))

    white_px = np.where(255 == np.array(lbl))
    x0, x1 = min(white_px[1]), max(white_px[1])
    y0, y1 = min(white_px[0]), max(white_px[0])

    width = x1 - x0
    height = y1 - y0

    cropped = img.crop((x0, y0, x1, y1))

    x, y = random.randint(0, bg_img.size[0]-width), random.randint(0, bg_img.size[1]-height)
    bg_img.paste(cropped, (x, y), cropped)

    if DEBUG:
        rect_img = ImageDraw.Draw(bg_img)
        rect_img.rectangle(
            ((x, y), 
            (x+width, y+height)),
            outline='red',
            width=3
        )
        rect_img.point(
            (x+width//2, y+height//2)
        )
        bg_img.show()

    yolo_lbl = (
        '0',
        (x+width//2)/bg_img.size[0],
        (y+height//2)/bg_img.size[1],
        width/bg_img.size[0],
        height/bg_img.size[1]
    )
    
    yolo_lbl = " ".join(map(str, yolo_lbl))

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

print(f'Finished in {time.time() - t0} seconds')