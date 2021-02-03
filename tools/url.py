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

def validate(path) -> bool:
    return os.path.exists(path)

def create_abs(path):
    is_abs = os.path.isabs(path)
    if is_abs:
        return path
    else:
        return path_from_relative(path, show_output=False)


if '__main__'==__name__:
    print(validate('assets/test.glb'))