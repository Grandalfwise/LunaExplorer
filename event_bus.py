from collections import defaultdict
from typing import Callable, Dict, List, Any

# -----------------------------
# Event emitter (simple)
# -----------------------------
class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

    def on(self, event_name: str):
        """Decorator: @events.on("event_name")"""
        def decorator(func: Callable):
            self._listeners[event_name].append(func)
            print(f"[EVENTS] Registered listener for '{event_name}': {func.__name__}")
            return func
        return decorator

    def emit(self, event_name: str, *args, **kwargs):
        """Emit an event: calls all listeners for this event."""
        listeners = self._listeners.get(event_name, [])
        print(f"[EVENTS] Emitting '{event_name}' → {len(listeners)} listeners")
        for fn in listeners:
            fn(*args, **kwargs)

# Global event bus instance
events = EventBus()