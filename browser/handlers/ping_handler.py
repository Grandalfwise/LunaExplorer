import subprocess
import sys
import re

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("ping")
def handle_ping(url, ctx = None):
    print("[ping] Handling ping")
    target = url.path
    if not target:
        print("ping: no host specified")
        return
    # Use system ping as a convenience (platform differences apply)
    try:
        print(ping(target))
    except Exception as e:
        print("Ping failed:", e)


def ping(host):
    # Pick correct command for OS
    cmd = ["ping", "-n", "4", host] if sys.platform.startswith("win") else ["ping", "-c", "4", host]

    raw = subprocess.run(cmd, capture_output=True, text=True).stdout
    lines = raw.splitlines()

    sent = received = lost = None
    min_ms = max_ms = avg_ms = None

    for line in lines:

        # ------------------------------
        # WINDOWS PACKET STATISTICS
        # ------------------------------
        if sys.platform.startswith("win"):
            m = re.search(r"Sent = (\d+), Received = (\d+), Lost = (\d+)", line)
            if m:
                sent = int(m.group(1))
                received = int(m.group(2))
                lost = int(m.group(3))

            m = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", line)
            if m:
                min_ms = int(m.group(1))
                max_ms = int(m.group(2))
                avg_ms = int(m.group(3))

        # ------------------------------
        # LINUX / MAC PACKET STATISTICS
        # ------------------------------
        else:
            m = re.search(r"(\d+) packets transmitted, (\d+) received", line)
            if m:
                sent = int(m.group(1))
                received = int(m.group(2))
                lost = sent - received

            m = re.search(r"rtt min/avg/max/[^\s]+ = ([\d.]+)/([\d.]+)/([\d.]+)/", line)
            if m:
                min_ms = float(m.group(1))
                avg_ms = float(m.group(2))
                max_ms = float(m.group(3))

    if sent is None:
        return f"The host '{host}' cannot be found."

    info = {
        "sent": sent,
        "received": received,
        "lost": lost,
        "min": min_ms,
        "max": max_ms,
        "avg": avg_ms
    }

    return info