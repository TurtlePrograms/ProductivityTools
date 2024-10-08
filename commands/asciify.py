import json
import argparse
import time
import os

localDir = os.path.dirname(os.path.abspath(__file__))

characters = json.load(open(localDir + '\\ascii.json'))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert an text to big ASCII text.')
    parser.add_argument('-f', '--text-file', type=str, default=None, help='The file to convert to ASCII text')
    parser.add_argument('-t', '--text', type=str, default=None, help='The text to convert to ASCII text')
    parser.add_argument('-s', '--size', type=int, default=5, help='The size of the ASCII text (5 or 7)(default 5)')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file to write the ASCII text to (optional)')
    parser.add_argument('--no-print', action='store_true', help='Do not print the ASCII text')
    return parser.parse_args()

args = parse_arguments()

def asciify(text: list[str], size):
    asciiFied = []
    for textRow in text:
        textRow = list(textRow)
        for row in range(size):
            line = []
            for char in textRow:
                try:
                    line.append(characters[char][row])
                except KeyError:
                    line.append(characters["NF"][row])
            asciiFied.append(' '.join(line))
        asciiFied.append('')
    return '\n'.join(asciiFied)

def main():
    if args.text_file:
        with open(args.text_file, 'r') as file:
            text = file.read().splitlines()
    elif args.text:
        text = args.text.splitlines()
    else:
        print('No text provided')
        return

    asciified = asciify([line.upper() for line in text], args.size)
    if not args.no_print:
        print(asciified)
    
    if args.output:
        with open(args.output, 'w') as file:
            file.write(asciified)

if __name__ == "__main__":
    sTime = time.time()
    main()
    eTime = time.time()
    if eTime >= 60:
        print(f"Time taken: {round(eTime - sTime)} seconds")