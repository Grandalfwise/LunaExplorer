import shlex
import subprocess

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("cmd")
def handle_cmd(url, ctx = None):
    """run a shell command -- BE CAREFUL: this executes arbitrary commands"""
    print("[cmd] Handling cmd")

    cmd = url.path
    try:
        parts = shlex.split(cmd)
    except Exception:
        parts = [cmd]
        print(f"Running command: {cmd}")
    try:
        res = subprocess.run(parts, capture_output=True, text=True, timeout=5)
        print("STDOUT:\n", res.stdout)
        print("STDERR:\n", res.stderr)
    except Exception as e:
        print("Command failed:", e)