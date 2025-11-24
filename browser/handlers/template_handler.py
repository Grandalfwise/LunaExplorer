from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("template")
def handle_template(url, ctx = None):
    print("[template] Handling template")