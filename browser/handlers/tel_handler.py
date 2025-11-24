import os
import subprocess
import sys
import urllib.parse

from luna_scheme_registry import scheme_registry

@scheme_registry.register("tel")
def handle_tel(url, ctx = None):
    number = url.scheme + ":" + url.path

    print("[tel] Handling tel")
    open_tel_raw(number)

def open_tel_raw(number: str):
    if sys.platform.startswith("win"):
        # Windows: use start
        subprocess.run(["powershell", "-Command", f"start '{number}'"], shell=True)

    elif sys.platform == "darwin":
        # macOS: use open
        subprocess.run(["open", number])

    else:
        # Linux / BSD: use xdg-open
        subprocess.run(["xdg-open", number])