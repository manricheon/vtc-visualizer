#!/usr/bin/env python3
"""VTC Visualizer — launcher. (c) mrc

Usage | 사용법:
    python visualizer.py                  # start server + open browser
    python visualizer.py logs/            # autoload csv/json from logs/
    python visualizer.py --port 8765
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
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
OFFLINE = ROOT / "index-offline.html"
DATA_EXTS = {".csv", ".tsv", ".json"}


def build_offline() -> None:
    """index.html의 Plotly CDN <script>를 인라인으로 치환해 index-offline.html 생성."""
    html = INDEX.read_text(encoding="utf-8")
    m = re.search(r'<script src="(https://cdn\.plot\.ly/[^"]+)"[^>]*></script>', html)
    if not m:
        sys.exit("Could not find the Plotly CDN tag in index.html.")
    url = m.group(1)
    print(f"Downloading Plotly… {url}")
    with urllib.request.urlopen(url) as res:
        plotly_js = res.read().decode("utf-8")
    inline = "<script>\n" + plotly_js + "\n</script>"
    out = html.replace(m.group(0), inline, 1)
    out = out.replace("<title>VTC Visualizer</title>",
                      "<title>VTC Visualizer (offline)</title>", 1)
    OFFLINE.write_text(out, encoding="utf-8")
    print(f"Done: {OFFLINE} ({OFFLINE.stat().st_size / 1e6:.1f} MB) — works without internet.")


class Handler(BaseHTTPRequestHandler):
    data_dir = None  # type: Optional[Path]

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
            self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/files":
            files = []
            if self.data_dir:
                files = sorted(p.name for p in self.data_dir.iterdir()
                               if p.is_file() and p.suffix.lower() in DATA_EXTS)
            self._send(200, json.dumps(files).encode(), "application/json")
        elif path == "/api/file":
            name = urllib.parse.parse_qs(parsed.query).get("name", [""])[0]
            target = (self.data_dir / name).resolve() if self.data_dir else None
            # 폴더 밖 경로 접근 차단
            if (not target or not target.is_file()
                    or target.parent != self.data_dir.resolve()
                    or target.suffix.lower() not in DATA_EXTS):
                self._send(404, b"not found", "text/plain")
                return
            self._send(200, target.read_bytes(), "text/plain; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, fmt, *args):  # 요청 로그 간소화
        pass


def serve(data_dir: "Optional[Path]", port: int) -> None:
    Handler.data_dir = data_dir
    server = HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    where = f" (data folder: {data_dir})" if data_dir else ""
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
    args = ap.parse_args()

    if args.target == "build-offline":
        build_offline()
        return

    data_dir = None
    if args.target:
        data_dir = Path(args.target).resolve()
        if not data_dir.is_dir():
            sys.exit(f"Folder not found: {data_dir}")
    serve(data_dir, args.port)


if __name__ == "__main__":
    main()
