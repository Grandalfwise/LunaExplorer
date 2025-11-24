import os
import subprocess
import sys
import urllib.parse

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("mailto")
def handle_mailto(url, ctx = None):
    link = url.scheme + ":" + url.path

    print("[mailto] Handling mailto")
    open_mailto_raw(link)

def open_mailto_raw(link: str):
    if sys.platform.startswith("win"):
        # Windows: use start
        subprocess.run(["powershell", "-Command", f"start '{link}'"], shell=True)

    elif sys.platform == "darwin":
        # macOS: use open
        subprocess.run(["open", link])

    else:
        # Linux / BSD: use xdg-open
        subprocess.run(["xdg-open", link])