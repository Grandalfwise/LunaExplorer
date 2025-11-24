from luna_scheme_registry import scheme_registry
from luna_browser_core import http_requester
from event_bus import events

@scheme_registry.register("http")
@scheme_registry.register("https")
def handle_http(url, ctx=None):
    print("[HTTP] Handling HTTP")
    status, headers, body = http_requester.request(url)

    # simple strip-tag renderer
    text = _strip_html_for_console(body)
    print(text)

# Helper copied over; in practice you could import it
import io

def _strip_html_for_console(body: bytes) -> str:
    try:
        s = body.decode("utf8", errors="replace")
    except Exception:
        return "(binary content)"
    out = io.StringIO()
    in_tag = False
    for ch in s:
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif not in_tag:
            out.write(ch)
    return out.getvalue()
