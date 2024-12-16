import os

class Path:
    CORE_DIR = os.path.dirname(os.path.realpath(__file__))
    TOOLS_DIR = os.path.dirname(CORE_DIR)
    ROOT_DIR = os.path.dirname(TOOLS_DIR)
    CACHE_DIR = os.path.join(ROOT_DIR, "cache")
    CONFIG_DIR = os.path.join(ROOT_DIR, "config")

    def get_dir():
        return os.getcwd()