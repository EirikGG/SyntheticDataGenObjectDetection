import os, time, numpy, statistics, humanize

from PIL import Image
from tools import img_generator, url

def _save_pil_img(pil_img, folder, name):
    '''Save PIL image to path'''
    file_path = '\\'.join((folder, name))
    pil_img.save(file_path)
    return os.stat(file_path).st_size


def _print_progress(step, max_steps, avg_time, size, newline=False, loading_bar_size=50):
    '''
    Takes a step and maximum number of steps and show the progress
    '''

    # Normalizes the steps
    step_norm = round((step/max_steps)*loading_bar_size)

    # Formates and prints the loading bar
    print('[{}{}] {} Avg time: {}s, Folder size: {}{}'.format( 
        ''.join(["#" for _ in range(step_norm)]), 
        ''.join(["-" for _ in range(step_norm, loading_bar_size)]),
        'Step {} / {}'.format(step, max_steps),
        avg_time,
        size,
        '                                                 '
    ), end='\n' if newline else '\r')


def generate_dataset(n_imgs, model, output_path='', show_progress=True, enable_print=True):
    while not url.validate(output_path):
        output_path = url.create_abs(input('Path: \n{}\nis invalid, input new output path: '.format(output_path)))

    # Opening print
    if enable_print:
        print("\n\nCreating dataset of {} images\n".format(n_imgs))

    info = {"times": [], "sizes":[]}

    for i in range(n_imgs):
        # Generate image
        result = img_generator.create_img(model)
        size = _save_pil_img(result['img'], output_path, ''.join(('image', str(i), '.jpg')))

        # Update general information
        info["sizes"].append(size)
        info["times"].append(result["time"])

        # Display progress
        if show_progress and enable_print:
            _print_progress(
                i+1, 
                n_imgs, 
                avg_time=round(numpy.mean(info["times"]), 3),
                size=humanize.naturalsize(sum(info["sizes"]), 3)
            )
    
    # Ending print
    if enable_print:
        print('\n'.join((
            '\n',
            'Completed dataset generation',
            'N images:  {}'.format(n_imgs),
            'Size:      {}'.format(humanize.naturalsize(sum(info["sizes"]), 3)),
            'Time:      {}s'.format(round(sum(info["times"]), 3)),
            '\n'
        )))