import argparse
from enum import Enum
from tools.core import ToolRegistry, Logger, LogLevel,GitClient

class ChangeLevel(Enum):
    NONE = 0
    PATCH = 1
    MINOR = 2
    MAJOR = 3

class Prefix(Enum):
    FIX = ChangeLevel.PATCH
    FEAT = ChangeLevel.MINOR

class Semver:
    patch = 0
    minor = 0
    major = 0

    def __init__(self, patch:int, minor:int, major:int):
        self.patch = patch
        self.minor = minor
        self.major = major
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
    
    def patchUpdate(self):
        self.patch += 1
        return self
    
    def minorUpdate(self):
        self.minor += 1
        self.patch = 0
        return self
    
    def majorUpdate(self):
        self.major += 1
        self.minor = 0
        self.patch = 0
        return self
    


def run(args):
    parser = argparse.ArgumentParser(
        description=ToolRegistry.getToolDescription("semver")
    )
    parsed_args = parser.parse_args(args)
    
    latestTagString = GitClient.getLatestTag()
    major,minor,patch = latestTagString.split('.')
    latestTag = Semver(int(patch),int(minor),int(major))
    newTag = Semver(latestTag.patch,latestTag.minor,latestTag.major)
    isTagUpdated = latestTag != newTag
    commitID = GitClient.getCommitIdFromTag(latestTagString)
    commits = GitClient.getCommitsSinceID(commitID)
    
    currentLevel = ChangeLevel.NONE

    for commit in commits:
        for prefix in Prefix:
            if commit.startswith(prefix.name.lower()):
                if prefix.value.value > currentLevel.value:
                    currentLevel = prefix.value
                break

    if currentLevel == ChangeLevel.NONE:
        pass
    elif currentLevel == ChangeLevel.PATCH:
        newTag = newTag.patchUpdate()
    elif currentLevel == ChangeLevel.MINOR:
        newTag = newTag.minorUpdate()
    elif currentLevel == ChangeLevel.MAJOR:
        newTag = newTag.majorUpdate()

    isTagUpdated = latestTag != newTag
    Logger.log(f"Latest tag: {latestTag}",LogLevel.NONE)
    Logger.log(f"New tag: {newTag}",LogLevel.NONE)
    Logger.log(f"Change level: {currentLevel.name}",LogLevel.NONE)
    Logger.log(f"Is tag updated: {isTagUpdated}",LogLevel.NONE)

    return (isTagUpdated,str(newTag),str(latestTag),currentLevel.name)

if __name__ == "__main__":
    run()
