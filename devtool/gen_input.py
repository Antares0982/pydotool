import re


def read_definitions(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = re.compile(r'#define\s+(\w+)\s+(\w+)')
    definitions = pattern.findall(content)

    return definitions


# change this path to your own path
file_path = "/usr/include/linux/input-event-codes.h"
definitions = read_definitions(file_path)

for name, value in definitions:
    print(f'{name} = {value}')
