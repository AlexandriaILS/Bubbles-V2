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

    def saycode(command):
        say(f'```{command.decode().strip()}```')

    def migrate():
        say("Migrating models...")
        saycode(subprocess.check_output([PYTHON, "manage.py", "migrate"]))

    def pull_from_git(branch: str="master"):
        say("Pulling latest code...")
        saycode(subprocess.check_output(["git", "pull", "origin", branch]))

    def install_deps():
        say("Installing dependencies...")
        saycode(subprocess.check_output(["/data/pyenv/shims/poetry", "install"]))

    def flush_db():
        say("Nuking DB...")
        # there's no return, so there's nothing to say
        subprocess.check_output([PYTHON, "manage.py", "flush", "--noinput"])

    def bootstrap_types():
        say("Re-adding default information...")
        saycode(subprocess.check_output([PYTHON, "manage.py", "bootstrap_types"]))

    def import_from_z():
        say("Importing data from Zenodotus. This will take a minute.")
        subprocess.check_output([PYTHON, "manage.py", "import_from_z"])
        say("Import complete.")

    def collect_static():
        say("Gathering staticfiles...")
        saycode(subprocess.check_output([PYTHON, "manage.py", "collectstatic", "--noinput"]))

    def restart_service(loc):
        say(f"Restarting service for {loc}...")
        systemctl_response = subprocess.check_output(
            ["sudo", "systemctl", "restart", loc]
        )
        if systemctl_response.decode().strip() == '':
            say("Restarted successfully!")
        else:
            say("Something went wrong and could not restart.")
            saycode(systemctl_response)

    pull_from_git()
    install_deps()

    PYTHON = f"/data/{location}/.venv/bin/python"

    if location == 'alexandria':
        say("Running commands specific to Alexandria.\n")
        flush_db()
        migrate()
        bootstrap_types()
        import_from_z()
    else:
        migrate()

    collect_static()

    restart_service(location)

    # reset back to our primary directory
    os.chdir("/data/bubbles")


PluginManager.register_plugin(
    deploy_to_staging, r"deploy ?(.+)",
    help="!deploy [alexandria, zenodotus] - deploys the code currently on github to the staging server."
)
