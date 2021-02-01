import os

def path_from_relative(relative, show_output=False):
    relative = relative.replace('/', '\\')
    dir_path = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[0:-1])
    total = os.path.join(dir_path, relative)

    if show_output:
        print('\n'.join((
            'Relative path:     {}'.format(relative),
            'Working dir path:  {}'.format(dir_path),
            'Total system path: {}'.format(total),
        )))

    return total
