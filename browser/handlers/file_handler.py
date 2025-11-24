import os.path

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("file")
def handle_file(url, ctx = None):
    """
    Handle file:// URLs by reading the file from local disk.
    """
    print("[file] Handling file")
    path = url.host
    print("Path =", path)

    if not os.path.exists(path):
        print(f"[file] File not found: {path}")
        return

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        body = f.read()

    print(body)