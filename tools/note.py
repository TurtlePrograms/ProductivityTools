import argparse
from tools.core import ToolRegistry, Logger, LogLevel, Cache,UserInput

def addNote(noteName: str, note: str, replace: bool = False):
    cache = Cache.getCache("notes") or {}
    name = noteName if noteName else "default"
    if name in cache:
        if replace:
            cache[name] = note
        else:
            cache[name] += f"\\n{note}"
    else:
        cache[name] = note
    Cache.saveCache("notes",cache)

def addIndentation(text:str, indentation:int):
    return "\n".join([f"{' '*indentation}{line}" for line in text.split("\\n")])

def listNotes(noteName: str = None):
    cache = Cache.getCache("notes")
    if cache:
        if noteName and noteName in cache:
            Logger.log(f"Note: {noteName}", LogLevel.NONE)
            Logger.log(addIndentation(str(cache[noteName]), 0), LogLevel.NONE)
            Logger.log("", LogLevel.NONE)
        elif noteName and noteName not in cache:
            Logger.log(f"Note \"{noteName}\" not found", LogLevel.ERROR)
        else:
            for noteName, note in cache.items():
                Logger.log(f"Note: {noteName}", LogLevel.NONE)
                Logger.log(addIndentation(str(note), 2), LogLevel.NONE)
                Logger.log("", LogLevel.NONE)


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("note")
    )
    parser.add_argument("-l", "--list", help="list all notes", action="store_true")
    parser.add_argument("-d", "--delete", help="delete a note", type=str)
    parser.add_argument("-r", "--replace", help="replace note", action="store_true")
    parser.add_argument("note", nargs="*", help="note name")

    parsed_args = parser.parse_args(args)

    if len(parsed_args.note) == 1 and not parsed_args.list and not parsed_args.delete:
        listNotes(parsed_args.note[0])
    elif parsed_args.note:
        addNote(parsed_args.note[0], "\\n".join(parsed_args.note[1:]), replace=parsed_args.replace)
    elif parsed_args.list:
        listNotes()
    elif parsed_args.delete:
        cache = Cache.getCache("notes")
        if cache:
            if parsed_args.delete in cache:
                if (UserInput.confirm(f"Are you sure you want to delete note \"{parsed_args.delete}\"?")):
                    del cache[parsed_args.delete]
                    Cache.saveCache("notes", cache)
                    Logger.log(f"Note \"{parsed_args.delete}\" deleted", LogLevel.INFO)
                else:
                    Logger.log(f"Note \"{parsed_args.delete}\" not deleted", LogLevel.INFO)
            else:
                Logger.log(f"Note \"{parsed_args.delete}\" not found", LogLevel.ERROR)
        else:
            Logger.log("No notes found", LogLevel.ERROR)
    else:
        listNotes()
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
