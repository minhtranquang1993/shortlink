---
name: shortlink
description: >
  Rut gon URL bang TinyURL API. Trigger khi user go "/shortlink <url>", "rut gon link nay",
  "tao short link", "shorten url", hoac gui 1 URL dai kem yeu cau rut gon. Ho tro custom alias,
  batch nhieu URL, va liet ke link da tao.
argument-hint: "<url> [--alias ten-tuy-chinh] | --batch <file> | --list"
---

# /shortlink — TinyURL Shortener

Rut gon URL nhanh bang [TinyURL API](https://tinyurl.com/app/dev).

## When to Use

- `/shortlink <url>` — rut gon 1 URL, tra ve link ngan
- `/shortlink <url> --alias ten-rieng` — tao link voi alias tuy chinh
- `/shortlink --batch urls.txt` — rut gon nhieu URL (file, moi dong 1 URL)
- `/shortlink --list` — liet ke cac link da tao truoc do
- Khi user gui 1 URL dai kem y "rut gon giup", "lam link ngan"

## Setup (bat buoc 1 lan)

Skill doc API key tu bien moi truong `TINYURL_API_KEY`:

```bash
export TINYURL_API_KEY="<your-tinyurl-api-key>"
```

Lay key tai: https://tinyurl.com/app/settings/api

> **Bao mat:** KHONG hardcode API key vao code hay commit len repo public.
> Luon dung bien moi truong. Neu key bi lo, revoke va tao lai tren TinyURL dashboard.

## How to Run

Tu thu muc skill:

```bash
# Rut gon 1 URL
python scripts/shortlink.py "https://example.com/duong-dan/rat/dai"

# Custom alias
python scripts/shortlink.py "https://example.com/abc" --alias sale-2026

# Batch tu file (moi dong 1 URL)
python scripts/shortlink.py --batch urls.txt

# Liet ke link da tao
python scripts/shortlink.py --list

# Output raw JSON (de parse tiep)
python scripts/shortlink.py "https://example.com" --json
```

## Workflow cho Agent

Khi user yeu cau rut gon link:

1. Xac dinh URL can rut gon (tu prompt hoac file). Neu chua co URL -> hoi.
2. Kiem tra `TINYURL_API_KEY` da set chua. Neu chua -> nhac user set (xem Setup).
3. Chay `python scripts/shortlink.py "<url>"` (them `--alias` neu user muon ten rieng).
4. Tra ve link ngan cho user. Neu batch -> tra bang mapping `short <- long`.
5. Loi thuong gap:
   - `HTTP 422` alias da ton tai -> goi y user doi alias khac.
   - `HTTP 401` -> API key sai/het han, nhac user kiem tra key.

## API Reference

- Endpoint: `POST https://api.tinyurl.com/create`
- Auth: header `Authorization: Bearer <API_KEY>`
- Body: `{"url": "...", "alias": "...", "domain": "tinyurl.com"}`
- List: `GET https://api.tinyurl.com/urls?type=all`

Chi tiet: https://tinyurl.com/app/dev
