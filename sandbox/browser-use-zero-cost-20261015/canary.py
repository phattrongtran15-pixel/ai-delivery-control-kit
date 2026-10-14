"""Browser Use open-source zero-cost CDP canary; no credentials or paid model."""
import asyncio
import json
import os
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen

MARKER = "browser-use-open-source-canary-20261015"
EVENT = {"clicked": False, "marker": MARKER}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format_, *args):
        return

    def do_GET(self):
        if self.path == "/":
            body = ("<!doctype html><title>Browser Use Canary</title>"
                    "<button id='canary-action' onclick=\"fetch('/event', {method:'POST',body:'"
                    + MARKER + "'})\">Run test</button>").encode()
            kind = "text/html; charset=utf-8"
        elif self.path == "/receipt":
            body = json.dumps(EVENT, sort_keys=True).encode()
            kind = "application/json"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/event":
            self.send_error(404)
            return
        payload = self.rfile.read(int(self.headers.get("Content-Length", "0"))).decode()
        if payload != MARKER:
            self.send_error(400)
            return
        EVENT["clicked"] = True
        self.send_response(204)
        self.end_headers()


def independent_receipt(port):
    with urlopen(f"http://127.0.0.1:{port}/receipt", timeout=4) as response:
        return json.loads(response.read())


async def main():
    for key in ("OPENAI_API_KEY", "BROWSER_USE_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"):
        assert not os.environ.get(key), f"PROTECTED: {key} must be unavailable"
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_port
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        before = independent_receipt(port)
        assert before == {"clicked": False, "marker": MARKER}, before
        print("NEGATIVE_CANARY_PASS: no-click not accepted", flush=True)
        from browser_use import Browser
        browser = Browser(headless=True)
        try:
            await browser.start()
            page = await browser.new_page(f"http://127.0.0.1:{port}/")
            assert await page.get_title() == "Browser Use Canary"
            elements = await page.get_elements_by_css_selector("#canary-action")
            assert len(elements) == 1, len(elements)
            await elements[0].click()
            receipt = None
            for _ in range(30):
                receipt = await asyncio.to_thread(independent_receipt, port)
                if receipt["clicked"]:
                    break
                await asyncio.sleep(0.2)
            assert receipt == {"clicked": True, "marker": MARKER}, receipt
            print("BROWSER_USE_CDP_CANARY_PASS: Browser Use clicked button", flush=True)
            print("INDEPENDENT_HTTP_RECEIPT_PASS: " + json.dumps(receipt, sort_keys=True), flush=True)
        finally:
            await browser.kill()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    asyncio.run(main())
