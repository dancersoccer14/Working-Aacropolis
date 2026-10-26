"""Build the static site: python3 tools/build.py (no packages required)."""
from pathlib import Path
import json,html,datetime
ROOT=Path(__file__).resolve().parents[1]
SITE_URL='https://casey-co.github.io/Aacropolis/'
data=json.loads((ROOT/'tools/pages.json').read_text())
E=lambda text:html.escape(str(text),quote=True)

def render(path,page):
    prefix='../' if path.startswith('blog/') else './'
    navigation=''.join('<a href="@@/'+url+'"'+(' aria-current="page"' if path==url else '')+'>'+E(label)+'</a>' for label,url in data['navigation'])
    more=''.join('<a href="@@/'+url+'">'+E(label)+'</a>' for label,url in data['more'])
    map_files='<link rel="stylesheet" href="@@/assets/build-map/leaflet.css"><link rel="stylesheet" href="@@/assets/build-map/map.css"><script src="@@/assets/build-map/leaflet.js" defer></script><script src="@@/assets/build-map/map.js" defer></script>' if path=='communities.html' else ''
    # Keep older shared URLs usable through GitHub Pages' single 404 handler.
    legacy={'about-1':'team.html','general-7':'communities.html','copy-of-home-1':'welcome.html','digitalwelcome':'welcome.html','stef-tester-homepage':'welcome.html','meet-the-team':'team.html','edmonton-communities':'communities.html','copy-of-about':'promotions.html','book-online':'contact.html','copy-of-home':'index.html','home':'index.html'}
    error_script='const root=location.hostname.endsWith(".github.io")?"/"+location.pathname.split("/").filter(Boolean)[0]+"/":"/";const base=document.createElement("base");base.href=root;document.head.append(base);const route=decodeURIComponent(location.pathname.slice(root.length)).replace(/^\\/|\\/$/g,"");const aliases='+json.dumps(legacy)+';const candidate=aliases[route]||(route.startsWith("post/")?"blog/"+route.slice(5)+".html":route+".html");if('+json.dumps(list(data['pages']))+'.includes(candidate))location.replace(root+candidate+location.hash);'
    error_base='<script>'+error_script+'</script>' if path=='404.html' else ''

    document=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8">{error_base}<meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(page['title'])} | Aacropolis Homes</title><meta name="description" content="Custom homes, infills and acreage homes in Edmonton and surrounding communities. Better living starts with us."><meta name="theme-color" content="#59534f"><link rel="stylesheet" href="@@/assets/site.css"><script src="@@/assets/site.js" defer></script>{map_files}</head>
<body class="{E(page.get('kind','standard'))}"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="header-main wrap"><a class="brand" href="@@/index.html" aria-label="Aacropolis Homes – Home"><img src="@@/assets/images/logo.png" alt="Aacropolis Homes" width="185" height="70"></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-navigation">Menu <span aria-hidden="true">☰</span></button><nav id="site-navigation" aria-label="Main navigation">{navigation}<details class="more-nav"><summary>More</summary><div>{more}<a href="@@/site-map.html">All Pages</a></div></details></nav></div><nav class="explore-nav" aria-label="More Aacropolis pages"><a href="@@/team.html">Meet the Team</a><a href="@@/communities.html">Edmonton Communities</a><a href="@@/contact.html">Let’s Talk</a></nav></header>
<main id="main">{page['body']}</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><a class="brand" href="@@/index.html"><img src="@@/assets/images/logo.png" alt="Aacropolis Homes" width="185" height="70" loading="lazy"></a><div><p class="serif">Better living starts with us.</p><a href="mailto:sales@aacropolishomes.com">sales@aacropolishomes.com</a><a href="tel:+18255102298">(825) 510-2298</a></div><div class="footer-links"><a href="@@/site-map.html">All Pages</a><a href="@@/contact.html">Let’s Talk</a><a href="https://www.instagram.com/aacropolishomes/" target="_blank" rel="noopener">Instagram ↗</a><a href="https://www.facebook.com/AacropolisHomes/" target="_blank" rel="noopener">Facebook ↗</a></div></div><p class="copyright">© {datetime.date.today().year} Aacropolis Homes Ltd. · Edmonton, Alberta</p></div></footer>
<dialog id="lightbox" aria-label="Photo viewer"><button id="lightbox-close" aria-label="Close photo viewer">Close ×</button><img id="lightbox-image" alt=""><p id="lightbox-caption"></p></dialog></body></html>'''
    return document.replace('@@/',prefix)

for path,page in data['pages'].items():
    output=ROOT/path
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(render(path,page))
# Preserve the three previously shared hidden-page links without duplicate page copies.
for old,target in {'general-7':'communities.html','about-1':'team.html','copy-of-home-1':'welcome.html'}.items():
    folder=ROOT/old;folder.mkdir(exist_ok=True)
    folder.joinpath('index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Aacropolis Homes</title><script>location.replace("../{target}"+location.hash)</script><meta http-equiv="refresh" content="0;url=../{target}"></head><body><a href="../{target}">Continue to Aacropolis Homes</a></body></html>')
ROOT.joinpath('.nojekyll').write_text('')
ROOT.joinpath('sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE_URL+path+'</loc></url>' for path in data['pages'] if path!='404.html')+'</urlset>')
print('Built',len(data['pages']),'pages and 3 compatibility redirects.')
