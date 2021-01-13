import time, numpy, statistics

from tools import img_generator

def print_progress(step, max_steps, avg_time, newline=False, loading_bar_size=50):
    '''
    Takes a step and maximum number of steps and show the progress
    '''

                                    # Normalizes the steps
    step_norm = round((step/max_steps)*loading_bar_size)
    
    print('[{}{}] {} {}'.format(       # Formates and prints the loading bar
        ''.join(["#" for _ in range(step_norm)]), 
        ''.join(["-" for _ in range(step_norm, loading_bar_size)]),
        'Step {} / {}'.format(step, max_steps),
        'Average time per image: {}'.format(avg_time)
    ), end='\n' if newline else '\r')


def generate_dataset(n_imgs, model, output_path='', show_progress=True):
    img_generation_times = []
    for i in range(n_imgs):
        # Generate image and time the process
        t0 = time.time()
        
        img_generator.create_img(model, output_path)

        img_generation_times.append(time.time()-t0)

        # Display progress
        if show_progress:
            print_progress(i+1, n_imgs, avg_time=round(numpy.mean(img_generation_times), 3))
    
    print("\nCreated {} images in {} seconds".format(n_imgs, round(sum(img_generation_times), 3)))