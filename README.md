# fantasyfutopia-archive
Static archive of fantasyfutopia.com (2017–2019): evergreen posts, Glossary and About only. Comments, affiliate links, QR codes, the book, previews and third-party images are removed.
- `build.py` regenerates `docs/` from the WordPress REST dump (`BACKUP` env var). Full backups are offline, not in this repo.
- Old URLs: stub pages (canonical + meta refresh), since GitHub Pages cannot do 301s; `docs/_redirects` is the real 301 map for a host that can.
- `redirects-at-launch.md`: prepared launch-time map (not applied).
- Domain: `www.fantasyfutopia.com` (CNAME); apex redirects to www.
