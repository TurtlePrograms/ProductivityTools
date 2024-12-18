from tools.core.Path import Path
import os
import json
from typing import Tuple

class Cache:

    AVAILABLE_CACHES = {
        "tool_registry": "tool_registry.json",
        "config": "config.json",
        "IgnoreFolders": "IgnoreFolders.json",	
        "notes": "notes.json",
    }

    def getCache(cache_name:str)->dict:
        try:
            if not os.path.exists(Path.CACHE_DIR):
                os.makedirs(Path.CACHE_DIR)
        
            path = os.path.join(Path.CACHE_DIR, Cache.AVAILABLE_CACHES[cache_name])
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except KeyError:
            raise ValueError(f"Cache '{cache_name}' not found")
        except json.JSONDecodeError:
            return {}
        except PermissionError:
            return {}
        except Exception as e:
            raise e
    
    def saveCache(cache_name:str, cache:json)->bool:
        try:
            if not os.path.exists(Path.CACHE_DIR):
                os.makedirs(Path.CACHE_DIR)
        
            path = os.path.join(Path.CACHE_DIR, Cache.AVAILABLE_CACHES[cache_name])
            with open(path, "w") as file:
                json.dump(cache, file, indent=4)
            return True
        except FileNotFoundError:
            return False
        except KeyError:
            raise ValueError(f"Cache '{cache_name}' not found")
        except json.JSONDecodeError:
            return False
        except PermissionError:
            return False
        except Exception as e:
            raise e

class ToolRegistry:
    
    @staticmethod
    def getScript(command:str,section:str)->str:
        try:
            ToolRegistry.getToolInfo(command,section)
            return ToolRegistry.getToolInfo(command,section)["script"]
        except Exception as e:
            raise e
    
    @staticmethod

    def getToolInfo(command:str,section:str)->Tuple[dict, str]:
        try:
            tool_registry = Cache.getCache("tool_registry")
            if section is None or tool_registry.get(section) is None:
                return None
            tool_registry = tool_registry[section]
            return [tool_registry[command],section]
        except KeyError:
            alliases = Cache.getCache("tool_registry").get("aliases", [])
            for alias in alliases:
                if alias == command:
                    return ToolRegistry.getToolInfo(alliases[alias]['tool'],alliases[alias]['section'])
    
    @staticmethod
    def getTools()->dict:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry
        except Exception as e:
            raise e
    
    @staticmethod
    def getAllCommandsAndAliases()->list:
        try:
            tool_registry = Cache.getCache("tool_registry")
            commands = []
            for key in tool_registry.keys():
                for command in tool_registry[key]:
                    commands.append(command)
            return commands
        except Exception as e:
            raise e
    
    @staticmethod
    def getAllCommandsInSectionAndAliases(section:str)->list:
        try:
            tool_registry = Cache.getCache("tool_registry")
            commands = []
            for key in tool_registry[section].keys():
                commands.append(key)
            for alias in tool_registry['aliases']:
                commands.append(alias)
            return commands
        except Exception as e:
            raise e

    @staticmethod
    def doesToolExist(command:str,section:str)->bool:
        try:
            return command in ToolRegistry.getAllCommandsInSectionAndAliases(section)
        except Exception as e:
            raise e
    
    @staticmethod
    def setToolValue(section:str, tool_name:str, key:str, value:str)->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            tool_registry[section][tool_name][key] = value
            Cache.saveCache("tool_registry", tool_registry)
        except Exception as e:
            raise e

    @staticmethod
    def registerTool(name:str, description:str,section:str, aliases:list=[])->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            if ToolRegistry.doesToolExist(name,section):
                return False
            tool_registry[section][name] = {
                "description": description,
                "script": name,
                "isExperimental": True,
            }
            for alias in aliases:
                if not ToolRegistry.doesToolExist(alias,section):
                    tool_registry['aliases'][alias] = {
                        "tool": name,
                        "section": section
                    }

            Cache.saveCache("tool_registry", tool_registry)

            Documentation.createDocumentation(name, description,section)

            return True
        except Exception as e:
            raise e
        
    @staticmethod
    def getToolDescription(command:str,section:str="base")->str:
        try:
            info = ToolRegistry.getToolInfo(command,section)[0]
            return info["description"]
        except Exception as e:
            raise e

class Documentation:
    @staticmethod
    def createDocumentation(tool_name:str, description:str,section:str):
        try:
            doc_dir = os.path.join(Path.ROOT_DIR, "Docs", "tools")
            if section != "base":
                doc_dir = os.path.join(doc_dir, section)
            if not os.path.exists(doc_dir):
                os.makedirs(doc_dir)
            
            doc_path = os.path.join(doc_dir,f"{tool_name}.md")
            with open(doc_path, "w") as file:
                file.write(f"# {tool_name}\n\n")
                file.write(f"# Description\n\n")
                file.write(f"{description}\n\n")
                file.write("## Usage\n")
                if section != "base":
                    file.write(f"```\nUsage: pt {section} {tool_name} [arguments]\n```\n\n")
                else:
                    file.write(f"```\nUsage: pt {tool_name} [arguments]\n```\n\n")
        except Exception as e:
            raise e
        finally:
            relative_doc_path = os.path.relpath(doc_path, Path.ROOT_DIR)
            ToolRegistry.setToolValue(section, tool_name, "documentation", relative_doc_path)


