# shortlink

Claude Code skill rut gon URL bang [TinyURL API](https://tinyurl.com/app/dev).

## Cai dat

Copy thu muc nay vao `~/.claude/skills/shortlink/`, sau do set API key:

```bash
export TINYURL_API_KEY="<your-tinyurl-api-key>"
```

Lay key tai: https://tinyurl.com/app/settings/api

## Su dung

```bash
# Rut gon 1 URL
python scripts/shortlink.py "https://example.com/duong-dan/rat/dai"

# Custom alias
python scripts/shortlink.py "https://example.com/abc" --alias sale-2026

# Batch (moi dong 1 URL)
python scripts/shortlink.py --batch urls.txt

# Liet ke link da tao
python scripts/shortlink.py --list

# Raw JSON
python scripts/shortlink.py "https://example.com" --json
```

Trong Claude Code, go `/shortlink <url>` de kich hoat skill.

## Bao mat

- KHONG hardcode API key vao code hay commit len repo.
- Luon dung bien moi truong `TINYURL_API_KEY`.
- Neu key bi lo -> revoke va tao lai tren TinyURL dashboard.

## License

MIT
