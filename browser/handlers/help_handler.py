from luna_scheme_registry import scheme_registry
from event_bus import events

message = """
LunaExplorer Help Page
----------------------

Supported schemes:
  file://path             Load a local file
  mailto:addr            Show email address
  tel:number             Show phone number
  geo:lat,long           Show Google Maps link
  cmd:command            Run safe commands
  app:name               Launch approved apps
  spotify:...            Show Spotify URI
  calc:expression        Evaluate calculation
  ping:host              Ping host
  note:text              Save text note
  search:keywords        Search DuckDuckGo
  help:                  This page

HTTP/HTTPS as normal.
"""

@scheme_registry.register("help")
def handle_template(url, ctx = None):
    print("[help] Handling help")
    print(message)
