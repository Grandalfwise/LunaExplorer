"""
LunaExplorer - Core browser module
Single-file implementation containing:
- URL parser (supports scheme:// and scheme: formats)
- HTTP/HTTPS requester (socket + optional TLS)
- Scheme handler registry / plugin system
- Simple EventEmitter for logging / UI hooks
- Built-in example handlers for mailto, cmd, ping, note
"""

import re
import socket
import ssl

from typing import Dict, Tuple, Any

from luna_scheme_registry import scheme_registry
import browser.handlers  # <-- THIS LOADS ALL HANDLER PLUGINS

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

ALL_SCHEMES = SCHEMES_WITH_SLASHES | SCHEMES_SIMPLE

# Regex to match scheme at start: captures scheme and separator (':' or '://')
SCHEME_REGEX = re.compile(r"^([a-zA-Z][a-zA-Z0-9+\-.]*)(://|:)")

class URL:
    """Parse a URL from a string. Supports both "scheme://host/..." and
    opaque "scheme:payload" forms. Validates scheme against ALL_SCHEMES.

    Attributes:
    scheme: str
    sep: str # either ':' or '://'
    host: Optional[str]
    port: Optional[int]
    path: str # for scheme:// this is path including leading '/'; for opaque its payload
    """

    def __init__(self, url):
        m = SCHEME_REGEX.match(url)
        if not m:
            self.scheme = None
            sep = None
        else:
            self.scheme = m.group(1)
            if self.scheme not in ALL_SCHEMES:
                self.scheme = None
                sep = None
            else:
                sep = m.group(2)

        if sep:
            after = url[len(self.scheme + sep):]
        else:
            after = url

        # HANDLE scheme:// (has host)
        if self.scheme in SCHEMES_WITH_SLASHES:
            # For file:///absolute paths, after may start with an extra '/'
            if "/" not in after:
                after += "/"
            host, rest = after.split("/", 1)
            self.host = host
            self.path = "/" + rest

            # default ports
            if self.scheme == "https":
                self.port = 443
            elif self.scheme == "http":
                self.port = 80
            else:
                self.port = None

            # support host:port
            if self.scheme == "http" or self.scheme == "https":
                if self.host and ":" in self.host:
                    h, p = self.host.split(":", 1)
                    self.host = h
                    try:
                        self.port = int(p)
                    except ValueError:
                        raise ValueError("Invalid port")

        # HANDLE scheme: (no host)
        else:
            # opaque form: payload stored in path
            self.host = None
            self.port = None
            self.path = after

#"""HTTP/HTTPS requester"""
class HTTPRequester:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def request(self, url: URL) -> Tuple[int, Dict[str, str], bytes]:

        if url.scheme not in ("http", "https"):
            raise ValueError("HTTPRequester supports only http/https schemes")

        port = url.port or (443 if url.scheme == "https" else 80)

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.settimeout(self.timeout)

        try:
            s.connect((url.host, port))
            if url.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=url.host)

            # simple HTTP/1.0 request
            request = "GET {} HTTP/1.0\r\n".format(url.path)
            request += "Host: {}\r\n".format(url.host)
            request += "User-Agent: LunaExplorer/1.0\r\n"
            request += "Accept-Encoding: identity\r\n Connection: close\r\n"
            request += "\r\n"
            s.send(request.encode("utf8"))

            fp = s.makefile("rb")
            statusline = fp.readline().decode("utf8", errors="replace").strip()
            if not statusline:
                raise ConnectionError("No response")
            parts = statusline.split(" ", 2)
            version = parts[0]
            status = int(parts[1]) if len(parts) > 1 else 0

            response_headers: Dict[str, str] = {}
            while True:
                line = fp.readline().decode("utf8", errors="replace")
                if line in ("\r\n", "\n", ""):
                    break
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                response_headers[k.strip().lower()] = v.strip()

            if "transfer-encoding" in response_headers:
                raise NotImplementedError("Chunked transfer-encoding not supported")
            if "content-encoding" in response_headers:
                raise NotImplementedError("Content encoding not supported")

            # read remaining bytes
            body_bytes = fp.read()
            fp.close()
            return status, response_headers, body_bytes
        finally:
            try:
                s.close()
            except Exception:
                pass

# default handler fallback for HTTP/HTTPS: perform request with HTTPRequester
http_requester = HTTPRequester()

# -----------------------------
# Public API convenience functions
# -----------------------------

def load_url(url_str: str, context: Any = None):
    """Parse the url string, emit events and route to the appropriate handler."""
    url = URL(url_str)
    context = url.scheme
    if url.scheme in ("http", "https"):
        # For HTTP, we call the registry handler which uses HTTPRequester by default
        return scheme_registry.handle(url, context)
    else:
        return scheme_registry.handle(url, context)


if __name__ == "__main__":
    print("Luna Browser — Interactive Mode")
    print("Type something or a URL (http://example.com). Type 'exit' or Ctrl+C to quit.\n")

    try:
        while True:
            raw = input("URL> ").strip()

            if not raw:
                continue  # ignore blank lines

            if raw.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            try:
                load_url(raw)
            except Exception as e:
                print("[ERROR]:", e, "\n")

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")