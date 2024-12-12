import argparse
from tools.core import GitClient, ToolRegistry, Logger, LogLevel,Cache
from tools import semver


import re

def validate_documentation(content):
    """
    Validate if the content meets the minimum documentation criteria:
    1. A title (first non-empty line starting with #).
    2. A description (at least one non-empty line after the title).
    3. A usage block (contains 'usage:' and command-line style syntax).

    :param content: String, the content of the documentation.
    :return: Dictionary with validation results.
    """
    result = {
        "title": False,
        "description": False,
        "usage_block": False
    }

    lines = content.splitlines()

    # Check for title
    for line in lines:
        if line.strip().startswith("#"):
            result["title"] = True
            break

    # Check for description (non-empty line after the title)
    if result["title"]:
        title_index = next(i for i, line in enumerate(lines) if line.strip().startswith("#"))
        description_lines = [line for line in lines[title_index + 1:] if line.strip()]
        if description_lines and not description_lines[0].strip().startswith("usage:"):
            result["description"] = True

    # Check for usage block
    usage_pattern = re.compile(r"usage:\.*")
    for line in lines:
        if usage_pattern.search(line):
            result["usage_block"] = True
            break

    return result

def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("publish")
    )
    parsed_args = parser.parse_args(args)

    (isTagUpdated,newTag,LatestTag,updateLevel) = semver.run([])
    if (isTagUpdated is False):
        Logger.log("No changes to publish",LogLevel.WARNING)
        return
    Logger.log(f"Publishing changes to {newTag}",LogLevel.INFO)
    Logger.log(f"Changes since {LatestTag} are {updateLevel}",LogLevel.INFO)

    ## check if changelog exists for the new tag
    with open('Docs/Changelogs.md','r') as f:
        changelogs = f.readlines()
    
    isNewTagPresent = False
    for line in changelogs:
        if line.startswith(f"## {newTag}"):
            Logger.log(f"Changelog for {newTag} already exists",LogLevel.INFO)
            isNewTagPresent = True
            break
    
    if isNewTagPresent is False:
        Logger.log(f"Changelog for {newTag} not found",LogLevel.WARNING)
        return

    ## check if every tool has a documentation
    tools = ToolRegistry.getTools()
    for tool in tools:
        if tools[tool]['documentation'] == "":
            Logger.log(f"Documentation for {tool} not found",LogLevel.WARNING)
            return
        try:
            with open(tools[tool]['documentation'],'r') as f:
                content = f.read()
                validation = validate_documentation(content)
                for key in validation:
                    if not validation[key]:
                        Logger.log(f"Documentation for {tool} is missing {key}",LogLevel.WARNING)
                if not all(validation.values()):
                    Logger.log(f"Documentation for {tool} is incomplete",LogLevel.WARNING)
                    return
                
        except FileNotFoundError:
            Logger.log(f"Documentation for {tool} not found",LogLevel.WARNING)
            return
    Logger.log("All tools have documentation",LogLevel.INFO)

    ## make a commit with the new tag on the release branch
    currentBranch = GitClient.getCurrentBranch()
    GitClient.CheckoutBranch("release")
    GitClient.Commit(f"Release {newTag}")
    GitClient.Tag(newTag)
    GitClient.Push()  
    GitClient.CheckoutBranch(currentBranch)

    return

if __name__ == "__main__":
    run()
