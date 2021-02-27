import os
import subprocess

from bubbles.config import PluginManager, COMMAND_PREFIXES


def deploy_to_staging(payload):
    options = ["alexandria", "zenodotus"]
    args = payload.get("text").split()
    say = payload['extras']['say']

    if len(args) > 1:
        if args[0] in COMMAND_PREFIXES:
            args.pop(0)

    if len(args) == 1:
        say(
            "Need a service to deploy to staging. Usage: @bubbles deploy [service]"
            " -- example: `@bubbles deploy alexandria`"
        )
        return

    location = args[1].lower().strip()
    if location not in options:
        say(f"Received a request to deploy {args[1]}, but I'm not sure what that is.")
        return

    say(f"Deploying {location} to staging. This may take a moment...")
    os.chdir(f"/data/{location}")

    git_response = (
        subprocess.check_output(["git", "pull", "origin", "master"]).decode().strip()
    )
    say(f"Git:\n```\n{git_response}```")

    say("Installing dependencies...")
    poetry_response = (
        subprocess.check_output(
            ["/data/pyenv/shims/poetry", "install"]
        )
            .decode()
            .strip()
    )
    say(f"Poetry:\n```\n{poetry_response}```")

    PYTHON = f"/data/{location}/.venv/bin/python"

    say("Running `./manage.py migrate`...")
    say(f'```{subprocess.check_output([PYTHON, "manage.py", "migrate"]).decode().strip()}```')

    say("Running `./manage.py collectstatic --noinput`...")
    say(f'```{subprocess.check_output([PYTHON, "manage.py", "collectstatic", "--noinput"]).decode().strip()}```')

    say(f"Restarting service for {location}...")
    systemctl_response = subprocess.check_output(
        ["sudo", "systemctl", "restart", location]
    )
    if systemctl_response.decode().strip() == '':
        say("Restarted successfully!")
    else:
        say(f"systemctl:\n```\n{systemctl_response}```")

    # reset back to our primary directory
    os.chdir("/data/bubbles")


PluginManager.register_plugin(
    deploy_to_staging, r"deploy ?(.+)",
    help="!deploy [alexandria, zenodotus] - deploys the code currently on github to the staging server."
)
