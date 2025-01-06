import argparse
import subprocess
from tools.core import ToolRegistry, Logger, LogLevel

# old implementation, showed help message for all tools
# def getAllHelp(areaFilter="none"):
#       text = "Available tools:\n"
#       data = ToolRegistry.getTools()
#       for area in data:
#         if areaFilter != "none" and area != areaFilter:
#             continue
#         if area == "aliases":
#             continue
#         text += f"\n{area.capitalize()}:\n"
#         text += f"Ussage: pt {area} <tool> [options]\n"
#         text += f"{30*'='}\n"
#         for tool in data[area]:
#             text += f"{tool}\n"
#             if area == "base":
#                 helpOutput = subprocess.run(["pt.bat", f"{tool}", "--help"], capture_output=True).stdout
#             else:
#                 helpOutput = subprocess.run(["pt.bat",f"{area}", f"{tool}", "--help"], capture_output=True).stdout
#             text += str(helpOutput, "utf-8")
#             text += "\n"
#             text += f"{30*'-'}\n"
#         text = text.split("\n")[:-2]
#         cleanedText = []
#         for line in text:
#             if "[WARNING]" in line or "[ERROR]" in line or "[CRITICAL]" in line or "[INFO]" in line:
#                 continue
#             cleanedText.append(line)
#         text = "\n".join(cleanedText)
#       return text

def getAllHelp(areaFilter="none"):
    text = "Available tools:\n"
    data = ToolRegistry.getTools()
    for area in data:
        if areaFilter != "none" and area != areaFilter:
            continue
        if area == "aliases":
            continue
        text += f"\n{area.capitalize()}:\n"
        if area == "base":
            text += f"Ussage: pt <tool> [options]\n"
        else:
            text += f"Ussage: pt {area} <tool> [options]\n"
        text += f"{len(text.splitlines()[-1])*'='}\n"
        for tool in data[area]:
            text += f"{tool} - {ToolRegistry.getToolDescription(tool, area)}"
            aliases = ToolRegistry.getAliases(tool, area)
            if len(aliases) > 0:
                text += f" - [{','.join(aliases)}]"
            text += "\n"
    return text

def getToolList():
    data = ToolRegistry.getTools()
    text = "Available tools:\n"
    for area in data:
        if area == "aliases":
            continue
        text += f"\n{area.capitalize()}:\n"
        for tool in data[area]:
            text += f"{tool}\n"
    return text

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("help", "base")
    )
    parser.add_argument("tool", help="The tool to get help for", nargs="?")
    parser.add_argument("-l", "--list", help="List all available tools", action="store_true")
    parser.add_argument("--area", help="The area to list tools for", default="none")

    parsed_args = parser.parse_args(args)

    if parsed_args.list:
         Logger.log(getToolList(),LogLevel.NONE)
    elif parsed_args.tool is not None:
        if ToolRegistry.doesToolExist(parsed_args.tool):
            helpOutput = subprocess.run(["pt.bat", f"{parsed_args.tool}", "--help"], capture_output=True).stdout
            Logger.log(str(helpOutput, "utf-8"),LogLevel.NONE)
        else:
            Logger.log(f"Tool '{parsed_args.tool}' not found.", LogLevel.ERROR)
    elif parsed_args.area is not None:
        Logger.log(getAllHelp(parsed_args.area),LogLevel.NONE)
    else:
        parser.print_help()
    return

if __name__ == "__main__":
        Logger.log("Cannot run this tool directly", LogLevel.CRITICAL)
