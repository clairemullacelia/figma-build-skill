#!/usr/bin/env python3
"""
shot.py: full-page screenshots and DOM probes over the Chrome DevTools
Protocol, with a REAL viewport.

WHY THIS EXISTS
    `--headless --screenshot --window-size=1440,15000` looks like a
    full-page capture and is not: `vh` units resolve against that
    15000px window, so `min-height: 100vh` heroes inflate to fifteen
    screens and every measurement taken from the image is wrong. This
    keeps the viewport at a real size and asks Chrome to capture beyond
    it, which is what `captureBeyondViewport` is for.

    It also answers the other recurring question, "what is actually
    painting that black box?", with `--eval`, so layout bugs get
    measured instead of guessed at.

USAGE
    python3 scripts/shot.py URL out.png [--width 1440] [--height 900] [--clip-sel "#id"]
    python3 scripts/shot.py URL --eval "document.title"

    --clip-sel captures just that element's box, which is usually what
    you want when reviewing one section of a long page.

No third-party packages: the WebSocket frame handling is inline below.
"""
import atexit
import os
import shutil
import signal
import sys
import argparse, base64, json, os, socket, struct, sys, subprocess, time, urllib.request, uuid

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


class WS:
    """The smallest WebSocket client that can speak CDP."""

    def __init__(self, url):
        _, rest = url.split("://", 1)
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n".encode()
        )
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.n = 0

    def _read(self, k):
        while len(self.buf) < k:
            chunk = self.s.recv(65536)
            if not chunk:
                raise IOError("socket closed")
            self.buf += chunk
        out, self.buf = self.buf[:k], self.buf[k:]
        return out

    def send(self, method, **params):
        self.n += 1
        payload = json.dumps({"id": self.n, "method": method, "params": params}).encode()
        header = b"\x81"
        L = len(payload)
        if L < 126:
            header += bytes([0x80 | L])
        elif L < 65536:
            header += bytes([0x80 | 126]) + struct.pack(">H", L)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", L)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.s.sendall(header + mask + masked)
        return self.n

    def wait(self, want):
        while True:
            b0, b1 = self._read(2)
            L = b1 & 0x7F
            if L == 126:
                L = struct.unpack(">H", self._read(2))[0]
            elif L == 127:
                L = struct.unpack(">Q", self._read(8))[0]
            data = self._read(L)
            if (b0 & 0x0F) not in (1, 2):   # ignore pings/closes
                continue
            msg = json.loads(data)
            if msg.get("id") == want:
                return msg


# ⚠️ A HIDDEN CHROME LEFT RUNNING BREAKS YOUR LINKS. One copy from an earlier
# run once stayed alive for 43 hours, and while it was, no link from the
# terminal reached the real browser. macOS hands web links to
# "Google Chrome", and a headless copy is still Google Chrome. So every exit
# path closes it: a slow start, an error, Ctrl-C, a timeout's SIGTERM. And each
# run first sweeps orphans (parent pid 1) that an older, killed run left.
def sweep_orphans():
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,command="],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) == 3 and parts[1] == "1" and "--user-data-dir=/tmp/shot-" in parts[2] \
                and "--headless" in parts[2]:
            try:
                os.kill(int(parts[0]), signal.SIGKILL)
            except OSError:
                pass


def close(p, profile):
    if p.poll() is None:
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    shutil.rmtree(profile, ignore_errors=True)


def launch(port):
    profile = f"/tmp/shot-{uuid.uuid4().hex[:8]}"
    p = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--remote-debugging-port={port}",
         f"--user-data-dir={profile}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(close, p, profile)
    for _ in range(100):
        try:
            j = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
            for t in j:
                if t.get("type") == "page":
                    return p, t["webSocketDebuggerUrl"], profile
        except Exception:
            time.sleep(0.1)
    close(p, profile)
    raise RuntimeError("chrome did not come up")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=float, default=1)
    ap.add_argument("--clip-sel")
    ap.add_argument("--eval")
    ap.add_argument("--css", help="inject a stylesheet before capturing, for "
                                  "trying a treatment without editing the project")
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--wait", type=float, default=1.2)
    a = ap.parse_args()

    sweep_orphans()
    # SIGTERM (a timeout) and SIGHUP (a closed terminal) skip `finally`
    # unless they are turned into a normal exit first.
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, lambda *_: sys.exit(1))
    proc, wsurl, profile = launch(a.port)
    try:
        ws = WS(wsurl)
        ws.wait(ws.send("Page.enable"))
        ws.wait(ws.send("Emulation.setDeviceMetricsOverride", width=a.width,
                        height=a.height, deviceScaleFactor=a.scale, mobile=False))
        ws.wait(ws.send("Page.navigate", url=a.url))
        time.sleep(a.wait)

        if a.css:
            ws.wait(ws.send("Runtime.evaluate", expression=(
                "(()=>{const s=document.createElement('style');"
                f"s.textContent={__import__('json').dumps(a.css)};"
                "document.head.appendChild(s);return 1})()"), returnByValue=True))
            time.sleep(0.25)

        if a.eval:
            # awaitPromise lets --eval test anything that needs a tick to
            # settle: a click that opens the lightbox, a React state update.
            # Harmless on a plain value: CDP only waits when one is returned.
            r = ws.wait(ws.send("Runtime.evaluate", expression=a.eval,
                                returnByValue=True, awaitPromise=True))
            print(json.dumps(r["result"].get("result", {}).get("value"), indent=1))
            # With an output path as well, --eval becomes a SETUP step and the
            # shot is taken of whatever state it left behind, which is the
            # only way to photograph something that needs a click first, such
            # as the lightbox.
            if not a.out:
                return

        params = {"format": "png", "captureBeyondViewport": True}
        if a.clip_sel:
            js = (f"(()=>{{const e=document.querySelector({json.dumps(a.clip_sel)});"
                  "if(!e)return null;const r=e.getBoundingClientRect();"
                  "return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height};})()")
            r = ws.wait(ws.send("Runtime.evaluate", expression=js, returnByValue=True))
            box = r["result"]["result"].get("value")
            if not box:
                sys.exit(f"selector not found: {a.clip_sel}")
            # ⚠️ NOT a.scale. deviceScaleFactor above already downscales the
            # capture; CDP multiplies the clip's own scale on top of it, so
            # passing a.scale here squares it: --scale 0.3 rendered at 0.09
            # and a 1261px section came out 113px wide.
            box["scale"] = 1
            params["clip"] = box
        r = ws.wait(ws.send("Page.captureScreenshot", **params))
        open(a.out, "wb").write(base64.b64decode(r["result"]["data"]))
        print(f"  ✓  {a.out}")
    finally:
        close(proc, profile)


if __name__ == "__main__":
    main()
