import subprocess
from AppOpener import open

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("app")
def handle_app(url, ctx = None):
    """
    Handle app:* URIs.
    This is for launching local apps by name.
    Use app:LS for listing app names
    """
    print("[app] Handling app")

    app_name = url.path  # e.g., calculator, discord, notepad

    try:
        open(app_name)
        print(f"Started {app_name} (if installed)")
    except Exception as e:
        print(f"APP handler error: {e}")