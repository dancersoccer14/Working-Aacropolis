"""Check every generated page for missing links, assets, and document structure."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.h1=0;self.viewport=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.h1+=1
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        for key in ['href','src','poster']:
            if a.get(key):self.refs.append(a[key])
errors=[];pages=json.loads((ROOT/'tools/pages.json').read_text())['pages']
for path in pages:
    file=ROOT/path;text=file.read_text();p=Page();p.feed(text)
    if p.h1!=1 or not p.viewport:errors.append(path+': invalid heading or viewport')
    if '@@/' in text:errors.append(path+': unresolved path')
    for ref in p.refs+re.findall(r"url\(['\"]?([^)'\"]+)",text):
        if ref.startswith(('https:','http:','mailto:','tel:','#','data:')):continue
        target=(file.parent/ref.split('#')[0].split('?')[0]).resolve()
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(path+': missing '+ref)
if (ROOT/'process.html').read_text().count('<li>')!=9:errors.append('Process: expected 9 steps')
if 'chatgpt.site' in (ROOT/'communities.html').read_text():errors.append('Map must run natively')
print('Checked',len(pages),'pages;',len(errors),'errors.')
for error in errors:print(error)
raise SystemExit(bool(errors))
