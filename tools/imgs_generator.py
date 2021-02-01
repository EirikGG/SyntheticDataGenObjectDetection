import time, numpy, statistics

from tools import img_generator

def print_progress(step, max_steps, avg_time, size, newline=False, loading_bar_size=50):
    '''
    Takes a step and maximum number of steps and show the progress
    '''

    # Normalizes the steps
    step_norm = round((step/max_steps)*loading_bar_size)

    # Formates and prints the loading bar
    print('[{}{}] {} Avg time: {}s, Folder size: {}MB'.format( 
        ''.join(["#" for _ in range(step_norm)]), 
        ''.join(["-" for _ in range(step_norm, loading_bar_size)]),
        'Step {} / {}'.format(step, max_steps),
        avg_time,
        size
    ), end='\n' if newline else '\r')


def generate_dataset(n_imgs, model, output_path='', show_progress=True, enable_print=True):
    # Opening print
    if enable_print:
        print("\n\nCreating dataset of {} images\n".format(
            n_imgs
        ))

    info = {
        "times": [],
        "sizes":[]
    }

    for i in range(n_imgs):
        # Generate image
        result = img_generator.create_img(model, output_path)

        # Update general information
        info["sizes"].append(result["size"])
        info["times"].append(result["time"])

        # Display progress
        if show_progress and enable_print:
            print_progress(
                i+1, 
                n_imgs, 
                avg_time=round(numpy.mean(info["times"]), 3),
                size=round(sum(info["sizes"]), 3)
            )
    
    # Ending print
    if enable_print:
        print('\n'.join((
            '\n',
            'Completed dataset generation',
            'N images:  {}'.format(n_imgs),
            'Size:      {}MB'.format(round(sum(info["sizes"]), 3)),
            'Time:      {}s'.format(round(sum(info["times"]), 3)),
            '\n'
        )))