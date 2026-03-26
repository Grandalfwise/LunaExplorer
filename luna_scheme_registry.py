from typing import Any
from event_bus import events

"""Configuration: known schemes"""
SCHEMES_WITH_SLASHES = {
    "http", "https", "file", "wss"
}

SCHEMES_SIMPLE = {
    "mailto", "tel",
    "cmd", "spotify", "app",
    "calc", "ping",
    "note", "search", "help"
}

TEMPLATE_SCHEME = {
    "template"
}

ALL_SCHEMES = SCHEMES_WITH_SLASHES | SCHEMES_SIMPLE | TEMPLATE_SCHEME

""" Scheme handler registry / plugin system"""
class SchemeHandlerRegistry:
    def __init__(self):
        self._handlers = {}

    def register(self, scheme: str):
        if scheme not in ALL_SCHEMES:
            raise ValueError(f"Unknown scheme: {scheme}")

        def decorator(func):
            if scheme in self._handlers:
                print(f"Warning: overriding handler for '{scheme}'")
            print(f"[REGISTRY] Registered handler for '{scheme}' -> {func.__name__}")
            self._handlers[scheme] = func
            return func
        return decorator

    def handle(self, url, context: Any = None):
        handler = self._handlers.get(url.scheme)
        if not handler:
            events.emit("scheme.missing", url.scheme, url)
            raise NotImplementedError(f"No handler registered for scheme: {url.scheme}")

        #events.emit("scheme.before", url.scheme, url)
        result = handler(url, context)
        print("RESULT: " + result)
        #events.emit("scheme.after", url.scheme, url, result)
        return result
scheme_registry = SchemeHandlerRegistry()