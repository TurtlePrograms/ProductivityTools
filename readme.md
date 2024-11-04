# Productivity Tools

A collection of command-line tools to streamline your daily tasks. This suite of tools is designed to help you manage notes, perform quick Git commits, open project folders, and more.

## Table of Contents

- [Installation](#installation)
- [Usage Overview](#usage-overview)
- [Tools](#tools)
  - [pt-help](#pt-help)
  - [pt-note](#pt-note)
  - [pt-open](#pt-open)
  - [pt-qc](#pt-qc)
  - [pt-run](#pt-run)
  - [pt-search](#pt-search)
  - [pt-update](#pt-update)
- [Requirements](#requirements)
---

## Installation

To install and start using Productivity Tools, follow these steps:

1. Ensure that you have **Python 3.12+** installed.
2. Clone or download this repository.
3. Add the folder containing Productivity Tools to your **PATH** environment variable.

Each command can then be accessed by running the respective `.bat` file, e.g., `pt-help`, from any terminal session.

---

## Usage Overview

Each tool can be accessed with a simple command format, like `pt-help -d`, where `pt-help` runs the main script for that tool with the specified options.

Example commands:
```bash
pt-help -d       # Shows detailed help for all commands
pt-qc "Message"  # Quick commit with a specified message
```
## Tools
### pt-update

Updates the project by pulling the latest changes from the repository.

Usage: ``` pt-update [-h] ```

Options:

    -h, --help : Show help message.

### pt-help

Provides a list of available commands and descriptions, including detailed help for each command.

Usage: ``` pt-help [-h] [-d] [--no-cache] [command] ```

Options:

    command : Specify a command to get detailed help.
    -h, --help : Show help message.
    -d, --detailed : Display detailed help.
    --no-cache : Bypass cache.

### pt-qc

Quickly create a Git commit, with optional push and confirmation bypass.

Usage: ``` pt-qc [-h] [-p] [-y] message ```

Options:

    message : Commit message for the Git commit.
    -h, --help : Show help message.
    -p, --push : Push changes after commit.
    -y, --no-confirm : Skip confirmation prompt.



### pt-run

Runs a preset profile with a list of programs to start.  
running `pt-run` will start the profile `default`, if the profiles.json file does not exist one will be created with an example setup  
the example setup includes a `default` profile, wich run a template called Browser, and opens cmd in this directory then opens vs code  
the template opens a browser (set via params in the profile) and opens a new tab on `google.com`  
the template also includes an example `alias`, called `example` this runs the profile `default`


Usage: ``` pt-run [-h] [-l] [profile] ```

Options:

    profile : Profile to execute.
    -h, --help : Show help message.
    -l, --list : List all profiles.


### pt-open

Opens Visual Studio Code in the Productivity Tools folder.

Usage: ``` pt-open [-h] ```

Options:

    -h, --help : Show help message.


### pt-search

Search for a keyword within a specified directory with recursive options.

Usage: ``` pt-search [-h] [-p PATH] [-r] [-e] [-d RECURSION_DEPTH] [keyword] ```

Options:

    keyword : Keyword to search for.
    -h, --help : Show help message.
    -p PATH, --path PATH : Specify the path for the search.
    -r, --recursive : Enable recursive search.
    -e, --exact : Search for the exact keyword.
    -d RECURSION_DEPTH, --recursion-depth RECURSION_DEPTH : Set recursion depth.

## pt-run: Creating and Customizing Profiles

The pt-run tool allows you to automate workflows by creating profiles that open browsers with preset tabs or start command windows running specific commands. Profiles are defined in a JSON configuration file, and you can list available profiles using the -l option.

Usage: ``` pt-run [-h] [-l] [profile] ```

Example:

bash

pt-run -l        # List available profiles
pt-run default   # Run the 'default' profile

### Profile JSON Structure

Profiles are defined under "profiles" in a JSON file, with each profile containing tasks based on its "type". Here’s an example profile configuration:

```{"templates": {"Browser": {"type": "browser","browser": "$browser","tabs": ["https://www.google.com/"]}},"profiles": {"default": [{"type": "template","name": "Browser","parameters": {"browser": "msedge"}},{"type": "cmd","windows": [{"name": "Productivity Tool","path": "C:\\ProductivityTools","commands": ["code ."]}],"path": "C:\\ProductivityTools"}],"example": {"type": "alias","profile": "default"}}}} ```
Field Descriptions
Profile Types

Each profile item requires a "type" field, which specifies what kind of task it will perform. Currently supported types include:

    browser: Opens a browser with specified tabs.
    cmd: Opens command windows in specified directories, running defined commands.
    alias: References an existing profile to reuse its configuration.
    template: references a template and holds any parameters it should give the template

### Browser Type

The "browser" type allows you to open a specified browser with multiple tabs.

    browser: Defines the executable for the browser to open, e.g., "msedge" for Microsoft Edge or "firefox" for Firefox. Any installed browser executable should work.
    tabs: A list of URLs to open in the browser. There is no hard limit on the number of tabs, but your device’s performance may impact how many can open smoothly.

Example: ``` { "type": "browser", "browser": "msedge", "tabs": [ "https://www.example.com", "https://www.another-example.com" ] } ```
### Cmd Type

The "cmd" type opens one or more command windows and runs specified commands in sequence.

    windows: Defines individual command windows.
        name: The title displayed on the command window.
        path: The directory to set as the starting location for commands.
        commands: A list of commands to execute sequentially. Avoid commands that block, such as powershell, at the start, as they prevent subsequent commands from running. To avoid issues, list non-blocking commands first (e.g., code .), then blocking ones if necessary.

Example: ``` { "type": "cmd", "windows": [ { "name": "Main Development Window", "path": "C:\Development", "commands": [ "code .", "npm start" ] }, { "name": "Monitoring", "path": "C:\Scripts", "commands": [ "python monitor.py" ] } ] } ```

### Alias Type

The "alias" type references another profile by name, allowing you to run configurations from existing profiles without duplicating them. This is useful for quickly reusing complex setups under different profile names.

    profile: The name of the profile to reference. When an alias is run, it will execute the configuration of the referenced profile.

Example: ``` { "type": "alias", "profile": "default" } ```

In this example, "test" is an alias for "default". Running pt-run test will execute the "default" profile.

### Template Type
The "template" type references a template by name, allowing you to create reusable snippets. a template can be any type

### Tips for Profile Management

    Listing Profiles: Use the -l option with pt-run to see a list of all defined profiles.

```bash 
pt-run -l
```

Avoiding Recursive Commands: Avoid calling pt-run within commands or using profiles in a way that might recursively trigger new profiles to run.

Order of Commands: Commands are executed in the order they appear. Be cautious about command blocking; for instance, if you need powershell to be open but also want to run code ., place code . first, followed by powershell.
