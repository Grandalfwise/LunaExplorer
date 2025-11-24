# SPOTIFY handler
# Example: spotify:track:4uLU6hMCjMI75M1A2tKUQC
# Example: spotify:album:1ATL5GLyefJaxhQzSPVrLX

# This handler prints parsed data and simulates launching Spotify.
# Later you can integrate Spotify's Web API or URI launcher.

from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("spotify")
def handle_spotify(url, ctx = None):
    """
    Handle spotify:* URIs.
    Spotify URIs can be nested like spotify:track:ID or spotify:playlist:ID.
    url.host = first part (e.g., 'track')
    url.path = '/ID' or '/subtype/ID' depending on format
    """
    print("[spotify] Handling spotify")

    parts = [url.scheme, url.host] + [p for p in url.path.split('/') if p]

    print("--- SPOTIFY HANDLER ---")
    print("Parsed Spotify URI parts:")
    for p in parts:
        print(f" - {p}")

    print("Simulating Spotify launch…")
    print("(Integrate API or system launcher here)")
    print("---------------------------")