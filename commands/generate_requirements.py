import os
import sys
import argparse

STANDARD_LIBRARIES = set(sys.builtin_module_names)  # Built-in modules

def parse_imports(file_path):
    """
    Extracts imported modules from a Python file.
    """
    imports = set()
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    parts = line.split()
                    if parts[0] == "import":
                        imports.add(parts[1].split('.')[0])  # Handle `import module.submodule`
                    elif parts[0] == "from":
                        imports.add(parts[1].split('.')[0])  # Handle `from module import something`
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return imports

def filter_third_party(imports):
    """
    Filters third-party libraries from a set of imports.
    """
    third_party = set()
    for module in imports:
        if module not in STANDARD_LIBRARIES:
            try:
                __import__(module)  # Check if it's installed
            except ImportError:
                third_party.add(module)
    return third_party

def run(args):
    parser = argparse.ArgumentParser(
        description="Generate requirements.txt by analyzing Python scripts in a folder."
    )
    parser.add_argument("folder", help="Path to the folder containing Python scripts.")
    parsed_args = parser.parse_args(args)

    folder = parsed_args.folder
    if not os.path.isdir(folder):
        print(f"The path '{folder}' is not a valid directory.")
        return

    all_third_party = set()

    # Iterate through Python files in the folder
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}...")
                imports = parse_imports(file_path)
                third_party = filter_third_party(imports)
                all_third_party.update(third_party)

    # Write to requirements.txt
    requirements_path = os.path.join(folder, "requirements.txt")
    try:
        with open(requirements_path, "w") as f:
            for library in sorted(all_third_party):
                f.write(f"{library}\n")
        print(f"requirements.txt created at {requirements_path}")
    except Exception as e:
        print(f"Error writing requirements.txt: {e}")
