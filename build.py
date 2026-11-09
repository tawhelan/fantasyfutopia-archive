#!/usr/bin/env python3
"""Build the static FantasyFutopia archive from the REST dump (BACKUP env var)."""
import json, glob, os, re, shutil, subprocess, html, sys
from bs4 import BeautifulSoup
BK = os.environ.get('BACKUP', os.path.expanduser('~/backup/fantasyfutopia_2026-11-05'))
OUT = 'docs'; HOST = 'https://www.fantasyfutopia.com'
BANNER = 'This site is archived (2017–2019). Something new is coming.'
EVERGREEN = ['how-to-play-daily-fantasy-football','per-90-stats-explained','understanding-pick-players-draftkings',
 'set-pieces-daily-fantasy-football','january-transfers-fantasy-perspective','understanding-how-to-pick-yahoo-players',
 'common-cognitive-biases-in-daily-fantasy-football']
def load(t):
    r=[]
    for f in sorted(glob.glob(f'{BK}/rest/{t}.p*.json')): r+=json.load(open(f))
    return r
posts, pages, media = load('posts'), load('pages'), load('media')
keep_slugs = set(EVERGREEN) | {p['slug'] for p in posts if p['slug'].startswith('python-for-fantasy-football')} | {'glossary','about'}
items = [p for p in posts+pages if p['slug'] in keep_slugs]
path = lambda u: re.sub(r'^https?://[^/]+','',u)
kept_paths = {path(p['link']) for p in items}
BAD_IMG = re.compile(r'giphy|bookbanner|QR|^YH-|^DK-|Lineup-Example|Heskey|Age-of-Arsenal|prizepool|^comment\.|inspect_element|banner',re.I)
BAD_LINK = re.compile(r'draftkings|fantasybet|adsrv|amazon\.|sumo|t\.co|twitter\.com|yahoo\.com|facebook\.com|youtu',re.I)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f'{OUT}/img')
def get_img(src):
    base = os.path.basename(src.split('?')[0]); orig = re.sub(r'-\d+x\d+(\.\w+)$',r'\1',base)
    rel = re.sub(r'^https?://[^/]+/','',os.path.dirname(src))
    for b in (orig, base):
        for cand in (f'{BK}/uploads/{rel}/{b}',):
            if os.path.exists(cand) and os.path.getsize(cand)>0: return cand, b
    for b in (orig, base):
        u = f'{HOST}/{rel}/{b}'; tmp=f'{OUT}/.dl'
        if subprocess.run(['curl','-sf','-m','60','-o',tmp,u]).returncode==0: return tmp, b
    return None, None
CSS = """:root{--bg:#fff;--fg:#1c1c1c;--mu:#666;--ac:#0b5cad;--bd:#ddd;--cb:#f5f5f5;--bn:#fff3cd}
@media(prefers-color-scheme:dark){:root{--bg:#161616;--fg:#e8e8e8;--mu:#999;--ac:#7db7ff;--bd:#333;--cb:#222;--bn:#3a3217}}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 Georgia,serif}
.banner{background:var(--bn);padding:.7rem 16px;text-align:center;font:600 15px system-ui,sans-serif}
main,header.s{max-width:760px;margin:0 auto;padding:0 16px}header.s{padding-top:1rem;font:15px system-ui,sans-serif}
a{color:var(--ac)}h1{line-height:1.25}.meta{color:var(--mu);font:14px system-ui,sans-serif}
img{max-width:100%;height:auto}pre{background:var(--cb);padding:12px;overflow-x:auto;font-size:14px;line-height:1.45}
table{border-collapse:collapse;display:block;overflow-x:auto}td,th{border:1px solid var(--bd);padding:4px 8px}
footer{max-width:760px;margin:3rem auto;padding:0 16px;color:var(--mu);font:14px system-ui,sans-serif}"""
def page(title, body, canon, meta=''):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} – FantasyFutopia (archive)</title><meta name="google-site-verification" content="-HsE7dGj4Tcs1q-zUxB7MEG7T3r_L9hL3H33froGLTc"><link rel="canonical" href="{HOST}{canon}"><link rel="stylesheet" href="/style.css"></head>
<body><div class="banner">{BANNER}</div><header class="s"><a href="/">FantasyFutopia</a></header><main>{meta}{body}</main>
<footer>FantasyFutopia, 2017–2019. Archived; no comments, forms or affiliate links.</footer></body></html>"""
PROMO = re.compile(r'QR code|scan the|preview of my book|out now on Amazon|my book|on Amazon|Amazon Kindle|New players currently earn|sign-up (?:bonus|offer)|referral|promo code|click here to (?:sign|join|play)|not a DraftKings member|To sign up for an account',re.I)
def clean(h):
    s = BeautifulSoup(h,'lxml')
    for t in s(['script','iframe','style','noscript','video','form']): t.decompose()
    for t in s.select('blockquote.twitter-tweet, .sharedaddy, .wp-caption-text'): t.decompose()
    for img in s('img'):
        src = img.get('src','')
        if BAD_IMG.search(os.path.basename(src)): 
            tgt = img.find_parent(['figure','a']) or img
            tgt.decompose() if tgt else None; continue
        f,b = get_img(src)
        if not f: img.decompose(); continue
        name = b; shutil.copyfile(f, f'{OUT}/img/{name}')
        for a in ('srcset','sizes','class','width','height','data-attachment-id'): img.attrs.pop(a,None)
        img['src']='/img/'+name; img['loading']='lazy'; img.attrs.setdefault('alt','')
    for a in s('a'):
        h = a.get('href','')
        if a.find('img') and re.search(r'/wp-content/uploads/|attachment',h): a.unwrap(); continue
        if re.match(r'https?://(www\.)?fantasyfutopia\.com',h):
            p = path(h).split('#')[0]
            if p in kept_paths: a['href']=p
            else: a.unwrap()
        elif BAD_LINK.search(h): a.unwrap()
    for f in s('figure'):
        if not f.find('img'): f.decompose()
    for t in s.find_all(['p','div','figure']):
        if not t.get_text(strip=True) and not t.find(['img','pre','table']): t.decompose()
    for p in s.find_all(['p','li']):
        tx = p.get_text(' ',strip=True)
        if PROMO.search(tx): p.decompose()
    body = s.body.decode_contents() if s.body else str(s)
    body = body.replace('which is available now on Amazon Kindle','which is no longer in print')
    return re.sub(r'\[/?(?:caption|python|code)[^\]]*\]','',body)
os.makedirs(OUT,exist_ok=True)
for p in items:
    title = html.unescape(p['title']['rendered']); c = path(p['link'])
    meta = f'<p class="meta">{p["date"][:10]}</p>' if p['type']=='post' else ''
    body = f'<h1>{html.escape(title)}</h1>{meta}{clean(p["content"]["rendered"])}'
    os.makedirs(OUT+c,exist_ok=True); open(OUT+c+'index.html','w').write(page(title,body,c))
if os.path.exists(f'{OUT}/.dl'): os.remove(f'{OUT}/.dl')
# home
byslug = {p['slug']:p for p in items}
def li(slugs): return '<ul>'+''.join(f'<li><a href="{path(byslug[s]["link"])}">{html.unescape(byslug[s]["title"]["rendered"])}</a></li>' for s in slugs)+'</ul>'
py = sorted([s for s in byslug if s.startswith('python-for')], key=lambda s: byslug[s]['date'])
home = f"""<h1>FantasyFutopia</h1><p>Daily fantasy football analysis, 2017–2019, kept online as a reference.</p>
<h2>Guides and stats</h2>{li(EVERGREEN)}<h2>Python for Fantasy Football</h2>{li(py)}<h2>Reference</h2>{li(['glossary','about'])}"""
open(f'{OUT}/index.html','w').write(page('Home',home,'/'))
open(f'{OUT}/style.css','w').write(CSS); open(f'{OUT}/CNAME','w').write('www.fantasyfutopia.com\n')
open(f'{OUT}/.nojekyll','w').write('')
# redirects: stubs for every known old URL that is not kept
def stub(target, canon_path):
    t = target
    return f'<!doctype html><meta charset="utf-8"><title>Redirecting</title><link rel="canonical" href="{HOST}{t}"><meta http-equiv="refresh" content="0;url={t}"><meta name="robots" content="noindex"><script>location.replace("{t}")</script><p>Moved to <a href="{t}">{t}</a>.</p>'
id2link = {p['id']:path(p['link']) for p in posts+pages}
rmap = {}
for p in posts+pages:
    c = path(p['link'])
    if c not in kept_paths and c!='/': rmap[c]='/'
for m in media:
    c = path(m['link']); par = id2link.get(m['post'],'/')
    rmap[c] = par if par in kept_paths else '/'
for c,t in rmap.items():
    d = OUT+c; os.makedirs(d,exist_ok=True)
    if not os.path.exists(d+'index.html'): open(d+'index.html','w').write(stub(t,c))
open(f'{OUT}/404.html','w').write('<!doctype html><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex"><script>location.replace("/")</script><p>This page is gone. <a href="/">FantasyFutopia home</a>.</p>')
with open(f'{OUT}/_redirects','w') as f:
    for c,t in sorted(rmap.items(), key=lambda x:(x[1]!='/',x[0])): f.write(f'{c} {t} 301\n')
print(len(items),'pages;',len(rmap),'redirects;',len(os.listdir(f'{OUT}/img')),'images')
# sitemap + robots so Search Console can recrawl the kept pages
with open(f'{OUT}/sitemap.xml','w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for c in ['/']+sorted(kept_paths): f.write(f'<url><loc>{HOST}{c}</loc></url>\n')
    f.write('</urlset>\n')
open(f'{OUT}/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {HOST}/sitemap.xml\n')
