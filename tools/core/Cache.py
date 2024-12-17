from tools.core.Path import Path
import os
import json

class Cache:

    AVAILABLE_CACHES = {
        "tool_registry": "tool_registry.json",
        "config": "config.json",
        "IgnoreFolders": "IgnoreFolders.json",	
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
    def getScript(command:str)->str:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry[command]["script"]
        except KeyError:
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                if command in aliases:
                    return tool_registry[key]["script"]
            return None
        except Exception as e:
            raise e
    
    @staticmethod
    def getToolInfo(command:str)->dict:
        try:
            tool_registry = Cache.getCache("tool_registry")
            return tool_registry[command]
        except KeyError:
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                if command in aliases:
                    return tool_registry[key]
            return None
    
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
            commands = list(tool_registry.keys())
            for key in tool_registry.keys():
                aliases = tool_registry[key].get("aliases", [])
                commands += aliases
            return commands
        except Exception as e:
            raise e
    
    @staticmethod
    def doesToolExist(command:str)->bool:
        try:
            return command in ToolRegistry.getAllCommandsAndAliases()
        except Exception as e:
            raise e
    
    @staticmethod
    def setToolValue(tool_name:str, key:str, value:str)->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            tool_registry[tool_name][key] = value
            Cache.saveCache("tool_registry", tool_registry)
        except Exception as e:
            raise e

    @staticmethod
    def registerTool(name:str, description:str, aliases:list=[])->bool:
        try:
            tool_registry = Cache.getCache("tool_registry")
            if ToolRegistry.doesToolExist(name):
                return False
            tool_registry[name] = {
                "description": description,
                "script": name,
                "script": name,
                "aliases": [],
                "isExperimental": True,
            }
            for alias in aliases:
                if not ToolRegistry.doesToolExist(alias):
                    tool_registry[name]["aliases"].append(alias)

            Cache.saveCache("tool_registry", tool_registry)

            Documentation.createDocumentation(name, description)

            return True
        except Exception as e:
            raise e
        
    @staticmethod
    def getToolDescription(command:str)->str:
        try:
            info = ToolRegistry.getToolInfo(command)
            return info["description"]
        except Exception as e:
            raise e

class Documentation:
    @staticmethod
    def createDocumentation(tool_name:str, description:str):
        try:
            doc_dir = os.path.join(Path.ROOT_DIR, "Docs")
            if not os.path.exists(doc_dir):
                os.makedirs(doc_dir)
            
            doc_path = os.path.join(doc_dir,"tools", f"{tool_name}.md")
            with open(doc_path, "w") as file:
                file.write(f"# {tool_name}\n\n")
                file.write(f"# Description\n\n")
                file.write(f"{description}\n\n")
                file.write("## Usage\n")
                file.write(f"```\nUsage: pt {tool_name} [arguments]\n```\n\n")
        except Exception as e:
            raise e
        finally:
            relative_doc_path = os.path.relpath(doc_path, Path.ROOT_DIR)
            ToolRegistry.setToolValue(tool_name, "documentation", relative_doc_path)


