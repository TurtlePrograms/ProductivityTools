import sys
import importlib


def main():
    if len(sys.argv) < 2:
        print("Error: No command provided.")
        return

    # First argument is the command, rest are passed along
    command = sys.argv[1]
    command_args = sys.argv[2:]  # All remaining arguments

    try:
        # Dynamically import the appropriate module based on the command
        module = importlib.import_module(f"commands.{command}")

        # Call the 'run' function of the module, passing all other args
        module.run(command_args)
    except ModuleNotFoundError as e:
        print(f"Error: Command '{command}' not found.")
        print(f"Details: {e}")
    except AttributeError as e:
        print(f"Error: Command '{command}' is missing a 'run' function.")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()
