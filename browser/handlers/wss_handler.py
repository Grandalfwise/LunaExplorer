from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("wss")
def handle_wss(url, ctx = None):
    print("[wss] Handling wss")
    print("[wss] In progress")