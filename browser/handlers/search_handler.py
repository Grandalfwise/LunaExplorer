from luna_scheme_registry import scheme_registry
from event_bus import events

@scheme_registry.register("search")
def handle_search(url, ctx = None):
    print("[search] Handling search")
    link = create_google_link(url.path)
    print(link)


def create_google_link(query):
    base_url = "https://www.google.com/search?q="
    search_link = base_url + query.replace(" ", "+")
    return search_link