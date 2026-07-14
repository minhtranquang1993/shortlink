# -*- coding: utf-8 -*-
"""
Shortlink - TinyURL API client
===============================
Rut gon URL bang TinyURL API (https://tinyurl.com/app/dev).

Usage:
  python shortlink.py <url>                       # rut gon 1 URL
  python shortlink.py <url> --alias my-custom      # custom alias
  python shortlink.py <url> --domain tinyurl.com   # chon domain
  python shortlink.py --batch urls.txt             # rut gon nhieu URL (moi dong 1 URL)
  python shortlink.py --list                        # liet ke cac link da tao
  python shortlink.py --json <url>                 # output raw JSON

API key doc theo thu tu uu tien:
  1. --api-key <key>
  2. bien moi truong TINYURL_API_KEY
"""

import sys
import io
import os
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

# Fix encoding
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass

API_BASE = "https://api.tinyurl.com"


def get_api_key(cli_key=None):
    key = cli_key or os.environ.get("TINYURL_API_KEY")
    if not key:
        sys.stderr.write(
            "ERROR: Thieu API key. Dat bien moi truong TINYURL_API_KEY "
            "hoac truyen --api-key.\n"
        )
        sys.exit(2)
    return key


def _request(method, path, api_key, payload=None, query=None):
    url = API_BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(body)
            errs = parsed.get("errors") or [body]
            msg = "; ".join(str(x) for x in errs)
        except Exception:
            msg = body
        sys.stderr.write("HTTP {}: {}\n".format(e.code, msg))
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write("Network error: {}\n".format(e.reason))
        sys.exit(1)


def create_link(api_key, long_url, alias=None, domain=None):
    payload = {"url": long_url}
    if alias:
        payload["alias"] = alias
    if domain:
        payload["domain"] = domain
    return _request("POST", "/create", api_key, payload=payload)


def list_links(api_key):
    return _request("GET", "/urls", api_key, query={"type": "all"})


def main():
    p = argparse.ArgumentParser(description="Rut gon URL bang TinyURL API")
    p.add_argument("url", nargs="?", help="URL can rut gon")
    p.add_argument("--alias", help="Custom alias (chi ky tu chu-so-gach)")
    p.add_argument("--domain", help="Domain (mac dinh tinyurl.com)")
    p.add_argument("--batch", help="File chua danh sach URL, moi dong 1 URL")
    p.add_argument("--list", action="store_true", help="Liet ke link da tao")
    p.add_argument("--api-key", help="TinyURL API key")
    p.add_argument("--json", action="store_true", help="In raw JSON")
    args = p.parse_args()

    api_key = get_api_key(args.api_key)

    if args.list:
        res = list_links(api_key)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            for item in res.get("data", []):
                print("{}  <-  {}".format(item.get("tiny_url"), item.get("url")))
        return

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            urls = [ln.strip() for ln in f if ln.strip()]
        results = []
        for u in urls:
            res = create_link(api_key, u, domain=args.domain)
            data = res.get("data", {})
            tiny = data.get("tiny_url", "")
            results.append({"url": u, "tiny_url": tiny})
            if not args.json:
                print("{}  <-  {}".format(tiny, u))
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if not args.url:
        p.error("Can 1 URL, hoac dung --batch / --list")

    res = create_link(api_key, args.url, alias=args.alias, domain=args.domain)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(res.get("data", {}).get("tiny_url", ""))


if __name__ == "__main__":
    main()
