from interpreter import converter
from pathlib import Path

def convert_all(directory, target):
    for file in Path(directory).glob('*.flon'):
        converter.convert(str(file), target)

convert_all('./configs', 'json')