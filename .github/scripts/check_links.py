#!/usr/bin/env python3
"""docs の相対リンク切れ検査（issue #6）。

リポジトリ内の .html / .md を走査し、相対リンク（href/src、Markdown の
[..](..)）が指すローカルファイル/ディレクトリが実在するかを検査する。
外部 URL・アンカーのみ(#..)・mailto 等・Jinja 式({{..}}) はスキップする。
壊れたリンクが1件でもあれば exit 1。

標準ライブラリのみ。ローカルでも `python .github/scripts/check_links.py` で実行可。
"""
import os
import re
import sys
from urllib.parse import unquote, urldefrag

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
SCAN_EXT = (".html", ".md")

# href="..." / src="..." / href='...'
RE_ATTR = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
# Markdown インラインリンク/画像 [text](target) ![alt](target)
RE_MD = re.compile(r"""!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+["'][^"']*["'])?\s*\)""")

EXTERNAL_PREFIX = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")


def is_checkable(link: str) -> bool:
    if not link:
        return False
    if link.startswith("#"):
        return False  # 同一ページ内アンカーは対象外
    if link.lower().startswith(EXTERNAL_PREFIX):
        return False  # 外部リンクは対象外（CI で叩くと不安定なため）
    if "{{" in link or "{%" in link:
        return False  # Jinja テンプレート式
    return True


def resolve(src_file: str, link: str) -> str:
    link, _frag = urldefrag(link)  # #fragment を除去
    link = link.split("?", 1)[0]   # ?query を除去
    link = unquote(link)
    if not link:
        return ""  # フラグメントのみだった
    if link.startswith("/"):
        return os.path.normpath(os.path.join(ROOT, link.lstrip("/")))
    return os.path.normpath(os.path.join(os.path.dirname(src_file), link))


def main() -> int:
    broken = []
    n_files = 0
    n_links = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(SCAN_EXT):
                continue
            path = os.path.join(dirpath, fn)
            n_files += 1
            text = open(path, encoding="utf-8", errors="replace").read()
            links = RE_ATTR.findall(text)
            if fn.endswith(".md"):
                links += RE_MD.findall(text)
            for link in links:
                if not is_checkable(link):
                    continue
                target = resolve(path, link)
                if not target:
                    continue
                n_links += 1
                if not os.path.exists(target):
                    broken.append((os.path.relpath(path, ROOT), link))

    print(f"走査: {n_files} ファイル / 検査した相対リンク: {n_links} 件")
    if broken:
        print(f"\n❌ リンク切れ {len(broken)} 件:")
        for src, link in broken:
            print(f"  {src}  ->  {link}")
        return 1
    print("✅ リンク切れなし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
