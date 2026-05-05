import re, base64, os

html_path = '/home/user/laft/Index-New.html'
img_dir   = '/home/user/laft/images'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Match src="data:image/TYPE;base64,DATA" or background:url('data:...')
pattern = re.compile(r'data:(image/(png|jpeg|jpg|svg\+xml|gif|webp));base64,([A-Za-z0-9+/=]+)')

counter = {}
replacements = {}

for m in pattern.finditer(html):
    full   = m.group(0)
    mime   = m.group(2).replace('+xml', '')   # svg+xml → svg
    ext    = 'svg' if 'svg' in mime else mime
    data   = m.group(3)

    if full in replacements:
        continue  # already processed (duplicate)

    counter[ext] = counter.get(ext, 0) + 1
    filename = f'img-{ext}-{counter[ext]:02d}.{ext}'
    filepath = os.path.join(img_dir, filename)

    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(data))

    replacements[full] = f'images/{filename}'
    print(f'Extracted → {filename}  ({len(data)*3//4//1024}KB)')

# Replace in HTML
for b64, path in replacements.items():
    html = html.replace(b64, path)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone. {len(replacements)} images extracted.')
