import argparse, sys, inspect

from dataset_generator.dataset_generator import generate_dataset

parser = argparse.ArgumentParser(description='Create image dataset based on a 3D model. '
                                                'This script calls dataset_generator/dataset_generator.py -> '
                                                'generate_dataset. Docstring: {}'.format(generate_dataset.__doc__))


argspec = inspect.getfullargspec(generate_dataset)      # Get full method spesification
args = argspec.args                                     # Arguments
defaults = list(argspec.defaults)                       # Default values
types = argspec.annotations.values()                    # Required types

while len(args) > len(defaults):                        # Add none when no default value
    defaults.insert(0, None)

for p, v, t in zip(args, defaults, types):              # Pair parameter, values, and types together
    parser.add_argument(    
        '--{}'.format(p),                               # Argument name
        type=t,                                         # Argument type
        default=v if None!=v else None,                 # Default value if spesified in method
        required=False if None!=v else True             # Required flag. True if no default value
    )


parsed_args = parser.parse_args()                       # Parse arguments from user

param_dict = vars(parsed_args)                          # Dictionary with parameters

generate_dataset(**vars(parsed_args))                   # Create dataset