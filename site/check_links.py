#!/usr/bin/env python3
"""Controlla i collegamenti locali e gli ancoraggi del sito statico."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.srcs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.srcs.append(values["src"])
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("name"):
            self.ids.add(values["name"])


def local_target(source, href):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith("//"):
        return None, parsed.fragment
    fragment = parsed.fragment
    path = parsed.path
    if not path:
        target = source
    else:
        target = (source.parent / path).resolve()
    return target, fragment


def main():
    errors = []
    html_files = sorted(ROOT.rglob("*.html"))
    parsed_files = {}
    for source in html_files:
        parser = Links()
        parser.feed(source.read_text(encoding="utf-8"))
        parsed_files[source] = parser

    for source, parser in parsed_files.items():
        for href in parser.hrefs:
            if href.startswith(("mailto:", "javascript:")):
                continue
            target, fragment = local_target(source, href)
            if target is None:
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{source.relative_to(ROOT)} -> {href} (file non trovato)")
                continue
            if fragment:
                if target not in parsed_files:
                    target_parser = Links()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    parsed_files[target] = target_parser
                if fragment not in parsed_files[target].ids:
                    errors.append(f"{source.relative_to(ROOT)} -> {href} (ancora non trovata)")
        for src in parser.srcs:
            target, _ = local_target(source, src)
            if target is not None and not target.is_file():
                errors.append(f"{source.relative_to(ROOT)} -> {src} (asset non trovato)")

    if errors:
        print("Link locali non validi:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Link check OK: {len(html_files)} pagine HTML controllate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
