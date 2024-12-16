from tools.core.Logging import Logger,LogLevel
import subprocess
from colorama import init

 
class GitClient:
    init(autoreset=True)
    @staticmethod
    def Add(path = ".")->int:
        try:
            result = subprocess.run(
                ["git","add",path], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git add:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode

    def Status()->int:
        try:
            result = subprocess.run(
                ["git","status","-s"], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git status:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def Commit(message:str)->int:
        try:
            result = subprocess.run(
                ["git","commit","-m",message], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git commit:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode

    def Push()->int:
        try:
            result = subprocess.run(
                ["git","push"], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git push:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def getLatestTag()->str:
        try:
            result = subprocess.run(
                ['git', 'tag', '--list', '--sort=-creatordate'], capture_output=True, text=True, check=True
            )
            return result.stdout.splitlines()[0]
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git describe --tags:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
        
    def Tag(tag:str)->int:
        try:
            result = subprocess.run(
                ["git","tag",tag], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git tag:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def PushTag(tag:str)->int:
        try:
            result = subprocess.run(
                ["git","push","origin",tag], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git push origin tag:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def getAllCommitMessageSinceCommit(commit:str)->str:
        try:
            result = subprocess.run(
                ["git","log","--pretty=format:%s",commit], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s -1 {commit}:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""

    def getCommitIdFromTag(tag:str)->str:
        try:
            result = subprocess.run(
                ['git', 'log', tag, '-n', '1', '--pretty=format:%H'], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s -1 {tag}:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
    
    def getCommitsSinceID(commitID:str)->list:
        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%s', f'{commitID}..HEAD'], capture_output=True, text=True, check=True
            )
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git log --pretty=format:%s {commitID}..HEAD:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
        
    def CheckoutBranch(branch:str):
        try:
            result = subprocess.run(
                ["git","checkout",branch], capture_output=True, text=True, check=True
            )
            Logger.log(result.stdout,LogLevel.NONE)
            return result.returncode
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git checkout:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return e.returncode
    
    def getCurrentBranch()->str:
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git branch --show-current:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
    
    def getRemoteUrl()->str:
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            Logger.log(f"Error while executing git config --get remote.origin.url:",LogLevel.ERROR)
            Logger.log(e.stderr,LogLevel.ERROR)
            return ""
    