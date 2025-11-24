from luna_scheme_registry import scheme_registry
from event_bus import events
from datetime import datetime

@scheme_registry.register("note")
def handle_note(url, ctx = None):
    print("[note] Handling note")
    payload = url.path
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # Save notes in a notes file
    with open("assets/notes.txt", "a", encoding="utf8") as f:
        f.write(timestamp + " " + payload + "\n")
    print("Saved note.")