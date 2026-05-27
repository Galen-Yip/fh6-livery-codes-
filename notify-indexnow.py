#!/usr/bin/env python3
"""notify-indexnow.py  —— 一键通知 Bing / Yandex 收录最新内容

用法：
    python3 notify-indexnow.py                       # 推送默认核心 URL
    python3 notify-indexnow.py /new-page /another    # 推送指定 path（可多个）
"""
import json, sys, urllib.request

HOST = "fh6-livery-codes.vercel.app"
KEY = "641db0ce8ef346df8c70adcc76691748"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

DEFAULT_PATHS = ["/", "/image-to-vinyl-converter", "/sitemap.xml"]

paths = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_PATHS
urls = [f"https://{HOST}{p}" for p in paths]

payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}
print("📤 IndexNow Payload:")
print(json.dumps(payload, indent=2))
print()

def push(name, endpoint):
    print(f"--- → {name} ---")
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            body = r.read().decode(errors="replace")
            print(f"✅ {name}: HTTP {r.status}  body: {body or '(empty)'}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"⚠️  {name}: HTTP {e.code}  body: {body}")
    print()

push("Bing",   "https://api.indexnow.org/IndexNow")
push("Yandex", "https://yandex.com/indexnow")
print("🎉 Done. Bing/Yandex will crawl new URLs in 2-6 hours.")
