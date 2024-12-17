# file-count

# Description

Recursively counts files matching a pattern in a directory

## Usage
```
usage: main.py [-h] [-p PATH] [-r RECRUSION_LIMIT] [-f] [-d] [-l] [pattern]

Recursively counts files matching a pattern in a directory

positional arguments:
  pattern               Pattern to match files and folders (default: "*")

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The directory to search from (default: current directory)
  -r RECRUSION_LIMIT, --recrusion-limit RECRUSION_LIMIT
                        The maximum recursion depth
  -f, --include-folders
                        Include folders in the count
  -d, --debug           Print debug information
  -l, --count-lines     Count lines in files
```

