from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("calc")
def handle_calc(url, ctx = None):
    print("[calc] Handling calc")
    print("[calc] In progress")