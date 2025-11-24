from event_bus import events

@events.on("scheme.before")
def log_before(scheme, url):
    print(f"[EVENT] Scheme '{scheme}' is about to handle: {url}")

@events.on("scheme.after")
def log_after(scheme, url, result):
    print(f"[EVENT] Scheme '{scheme}' finished handling.")