"""Keep Skilleo renderer source intact; mirror its exact Outfit font in the build.

The headless browser cannot reach the Google font CDN on this host. Embed the
same downloaded bytes into the installed Google Fonts package's URL table.
Only node_modules changes. The native slide layout and animation are untouched.
"""
import sys,base64
from pathlib import Path
from urllib.request import urlopen
R=Path(__file__).resolve().parent
url='https://fonts.gstatic.com/s/outfit/v15/QGYvz_MVcBeNP4NJtEtq.woff2'
font=R/'assets/fonts/Outfit-latin.woff2';font.parent.mkdir(exist_ok=True)
if not font.exists():font.write_bytes(urlopen(url,timeout=30).read())
data='data:font/woff2;base64,'+base64.b64encode(font.read_bytes()).decode()
package=Path(sys.argv[1])/'node_modules/@remotion/google-fonts/dist'
count=0
for path in package.rglob('Outfit.*'):
 if path.suffix not in ('.js','.mjs'):continue
 text=path.read_text()
 if url in text:path.write_text(text.replace(url,data));count+=1
print('Mirrored identical font bytes in',count,'build modules')
license=R/'assets/fonts/OFL-Outfit.txt'
if not license.exists():license.write_bytes(urlopen('https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/OFL.txt',timeout=30).read())
