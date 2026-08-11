import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

img_re = re.compile(r"<img src='([^']+)' style='width: ([\d.]+)px; height: ([\d.]+)px'>")
for idx, pos in enumerate(positions):
    end = positions[idx+1] if idx+1 < len(positions) else len(html)
    seg = html[pos:end]
    imgs = img_re.findall(seg)
    print(f'\n===== SCREEN {idx+1} : {len(imgs)} images =====')
    for src, w, h in imgs:
        print(f'  {w}x{h}  ...{src[-40:]}')
