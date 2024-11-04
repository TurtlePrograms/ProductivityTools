import os
import argparse
import subprocess

valid_choices = {
    "platform": r"C:\Users\DavidvanHoek\source\Twintos\Platform",
    "p": r"C:\Users\DavidvanHoek\source\Twintos\Platform",
    "platform_provisioning": r"C:\Users\DavidvanHoek\source\Twintos\Platform_Provisioning",
    "pp": r"C:\Users\DavidvanHoek\source\Twintos\Platform_Provisioning"
}

def clone(url, path):
    os.chdir(path)

    clone_result = subprocess.run(
        ["git", "clone", url], check=True, capture_output=True, text=True
    )
    print(clone_result.stdout)

    repo_name = url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(path, repo_name)

    os.chdir(repo_path)

    fetch_result = subprocess.run(
        ["git", "fetch", "--all", "--tags"], check=True, capture_output=True, text=True
    )
    print(fetch_result.stdout)


def run(args):
    def lowercase_choice(value):
        value = value.lower()
        if value not in valid_choices:
            raise argparse.ArgumentTypeError(f"Invalid choice: '{value}'. Choose from {list(valid_choices.keys())}.")
        return value

    parser = argparse.ArgumentParser(description="Clones the given repo")
    parser.add_argument("https_url", help="The HTTPS URL of the repository to clone")
    parser.add_argument("platform", type=lowercase_choice, help=f"Specify platform as one of: {list(valid_choices.keys())}")
    parsed_args = parser.parse_args(args)

    platform_path = valid_choices[parsed_args.platform]
    print(platform_path,parsed_args.platform)
    clone(parsed_args.https_url,platform_path)
