import os
import subprocess

from bubbles.config import PluginManager
from bubbles.helpers import fire_and_forget


def update(data) -> None:
    def trigger_update():
        subprocess.run(os.path.join(os.getcwd(), "update.py"))

    print(os.getcwd())
    fire_and_forget(trigger_update)

PluginManager.register_plugin(update, r"update$", help="!update - pull changes from github and restart!")
