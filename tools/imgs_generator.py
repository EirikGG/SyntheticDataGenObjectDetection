import time

from tools import img_generator, label_generator




def show_loading(step, max_steps, newline=False, loading_bar_size=50):
    '''
    Takes a step and maximum number of steps and show the progress
    If step is greater than maximum number of steps it raises an exeption
    '''
    if step > max_steps:            # Raises exception if step is larger than max_steps
        raise Exception("Step value is greater than maximum steps")

                                    # Normalizes the steps
    step_norm = round((step/max_steps)*loading_bar_size)
    
    print('[{}{}] {}'.format(       # Formates and prints the loading bar
        ''.join(["#" for _ in range(step_norm)]), 
        ''.join(["-" for _ in range(step_norm, loading_bar_size)]),
        'Step {} / {}'.format(step, max_steps)
    ), end='\n' if newline else '\r')


def generate_dataset(n_imgs, show_progress):

    for i in range(n_imgs):
        if show_progress:
            show_loading(i+1, n_imgs)
        time.sleep(.05)