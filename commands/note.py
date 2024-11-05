import os
import argparse
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def getCache() -> dict:
    try:
        with open(f"../pt-cache/notecache.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def saveCache(cache: dict):
    if not os.path.exists(f"../pt-cache"):
        os.makedirs(f"../pt-cache")
    with open(f"../pt-cache/notecache.json", "w") as file:
        json.dump(cache, file)

def addNote(noteName: str, note: str, replace: bool = False):
    cache = getCache() or {}
    name = noteName if noteName else "default"
    if name in cache:
        if replace:
            cache[name] = note
        else:
            cache[name] += f"\\n{note}"
    else:
        cache[name] = note
    saveCache(cache)

def addIndentation(text:str, indentation:int):
    return "\n".join([f"{' '*indentation}{line}" for line in text.split("\\n")])

def listNotes(noteName: str = None):
    cache = getCache()
    if cache:
        if noteName:
            print(f"Note: {noteName}")
            print(addIndentation(str(cache[noteName]), 2))
        else:
            for noteName, note in cache.items():
                print(f"Note: {noteName}")
                print(addIndentation(str(note), 2))
                print()

def run(raw_args):
    parser = argparse.ArgumentParser(
        description="take some simple notes"
    )
    parser.add_argument("-l", "--list", help="list all notes", action="store_true")
    parser.add_argument("-d", "--delete", help="delete a note", type=str)
    parser.add_argument("-r", "--replace", help="replace note", action="store_true")
    parser.add_argument("note", nargs="*", help="note name")
    args = parser.parse_args(raw_args) 

    if len(args.note) == 1 and not args.list and not args.delete:
        listNotes(args.note[0])
    elif args.note:
        addNote(args.note[0], "\\n".join(args.note[1:]), replace=args.replace)
    elif args.list:
        listNotes()
    elif args.delete:
        cache = getCache()
        if cache:
            if args.delete in cache:
                del cache[args.delete]
                saveCache(cache)
            else:
                print(f"Note {args.delete} not found")
        else:
            print("No notes found")
    else:
        listNotes()
    
