#!/usr/bin/env python3
"""VTC Visualizer — launcher. (c) mrc

Usage | 사용법:
    python visualizer.py                  # start server + open browser
    python visualizer.py logs/            # autoload csv/json from logs/
    python visualizer.py --port 8765
    python visualizer.py logs/ --offline  # same, but serve the offline build (no CDN)
    python visualizer.py build-offline    # build index-offline.html with Plotly inlined

Standard library only. index.html also works by simply double-clicking it —
this script is an optional helper for folder autoload and the offline build.
(HTML은 더블클릭만으로도 동작. 이 스크립트는 폴더 자동 로드/오프라인 빌드용 보조 도구.)
"""
import argparse
import json
from typing import Optional
import re
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
OFFLINE = ROOT / "index-offline.html"
DATA_EXTS = {".csv", ".tsv", ".json"}


def build_offline() -> None:
    """index.html의 Plotly CDN <script>를 인라인으로 치환해 index-offline.html 생성."""
    html = INDEX.read_text(encoding="utf-8")
    m = re.search(r'<script\s+[^>]*src="(https://cdn\.plot\.ly/[^"]+)"[^>]*>\s*</script>', html)
    if not m:
        sys.exit("Could not find the Plotly CDN tag in index.html.")
    url = m.group(1)
    print(f"Downloading Plotly… {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            plotly_js = res.read().decode("utf-8")
    except Exception as err:
        sys.exit(f"Failed to download Plotly CDN ({err}). Check your connection.")
    inline = "<script>\n" + plotly_js + "\n</script>"
    out = html.replace(m.group(0), inline, 1)
    out = out.replace("<title>VTC Visualizer</title>",
                      "<title>VTC Visualizer (offline)</title>", 1)
    OFFLINE.write_text(out, encoding="utf-8")
    print(f"Done: {OFFLINE} ({OFFLINE.stat().st_size / 1e6:.1f} MB) — works without internet.")


class Handler(BaseHTTPRequestHandler):
    data_dir = None  # type: Optional[Path]
    use_offline = False

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (http.server convention)
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path in ("/", "/index.html"):
            # --offline이면 인라인 빌드를 서빙 — 폴더 자동 로드와 오프라인을 함께 쓸 수 있다
            page = OFFLINE if (self.use_offline and OFFLINE.exists()) else INDEX
            self._send(200, page.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/files":
            files = []
            if self.data_dir:
                base = self.data_dir.resolve()
                files = sorted(
                    str(p.relative_to(base)).replace("\\", "/")
                    for p in base.rglob("*")
                    if p.is_file() and p.suffix.lower() in DATA_EXTS
                )
            self._send(200, json.dumps(files).encode(), "application/json")
        elif path == "/api/file":
            name = urllib.parse.parse_qs(parsed.query).get("name", [""])[0]
            if self.data_dir and name:
                base = self.data_dir.resolve()
                target = (base / name).resolve()
                try:
                    is_inside = target.is_relative_to(base)
                except AttributeError:
                    is_inside = base in target.parents
                except ValueError:
                    is_inside = False

                if target.is_file() and is_inside and target.suffix.lower() in DATA_EXTS:
                    sfx = target.suffix.lower()
                    ctype = "text/csv; charset=utf-8" if sfx == ".csv" else \
                            "application/json; charset=utf-8" if sfx == ".json" else \
                            "text/plain; charset=utf-8"
                    self._send(200, target.read_bytes(), ctype)
                    return
            self._send(404, b"not found", "text/plain")
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, fmt, *args):  # 요청 로그 간소화
        pass


def serve(data_dir: "Optional[Path]", port: int, host: str = "127.0.0.1", offline: bool = False) -> None:
    Handler.data_dir = data_dir
    Handler.use_offline = offline
    if offline and not OFFLINE.exists():
        sys.exit("index-offline.html not found. Run: python visualizer.py build-offline")
    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}/"
    where = f" (data folder: {data_dir})" if data_dir else ""
    where += " [offline build]" if offline else ""
    print(f"VTC Visualizer — {url}{where}\nStop: Ctrl+C")
    threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBye.")


def main() -> None:
    ap = argparse.ArgumentParser(description="VTC Visualizer launcher")
    ap.add_argument("target", nargs="?", default=None,
                    help="data folder to autoload, or 'build-offline'")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", type=str, default="127.0.0.1",
                    help="host interface to bind (default: 127.0.0.1)")
    ap.add_argument("--offline", action="store_true",
                    help="serve index-offline.html (no CDN) instead of index.html")
    args = ap.parse_args()

    if args.target == "build-offline":
        build_offline()
        return

    data_dir = None
    if args.target:
        data_dir = Path(args.target).resolve()
        if not data_dir.is_dir():
            sys.exit(f"Folder not found: {data_dir}")
    serve(data_dir, args.port, args.host, args.offline)


if __name__ == "__main__":
    main()

