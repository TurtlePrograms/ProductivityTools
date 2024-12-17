# tree

# Description

create a folder tree

## Usage
```
usage: pt tree [-h] [-p PATH] [-o OUTPUT] [-f] [--no-print] [-r RECRUSION_LIMIT] [-d] [--no-color]

create a folder tree

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The root directory to start the tree from (default: current directory)
  -o OUTPUT, --output OUTPUT
                        Output file to write the tree to (optional)
  -f, --map-files       Include files in the tree
  --no-print            Do not print the tree
  -r RECRUSION_LIMIT, --recrusion-limit RECRUSION_LIMIT
                        The maximum depth of the tree
  -d, --debug           Print debug information
  --no-color            Disable colored output
```