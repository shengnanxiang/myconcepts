import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

# 抓取所有 "left: Xpx; top: Ypx; position: absolute" 块内的文本 (span 或纯文本)
# 模式1: <div style="...left/top...text-align: center"><span style=...>TXT</span></div>
# 模式2: <div style="...left/top...text-align: center">TXT</div>
block_re = re.compile(
    r'<div style="left: ([\d.]+)px; top: ([\d.]+)px; position: absolute; text-align: center">(.*?)</div>'
)

for idx, pos in enumerate(positions):
    end = positions[idx+1] if idx+1 < len(positions) else len(html)
    seg = html[pos:end]
    blocks = block_re.findall(seg)
    print(f'\n===== SCREEN {idx+1} : {len(blocks)} text blocks =====')
    seen = set()
    rows = []
    for x, y, inner in blocks:
        # 提取颜色
        col = 'n/a'
        m = re.search(r'(?:background|color): (#[0-9A-Fa-f]{3,8})', inner)
        if m: col = m.group(1)
        fs = re.search(r'font-size: ([\d.]+)px', inner)
        bold = 'B' if ('font-weight: 700' in inner or 'font-weight: bold' in inner) else ''
        # 提取文字 (去掉 span 标签)
        txt = re.sub(r'<[^>]+>', '', inner).replace('&nbsp;',' ').strip()
        if not txt: continue
        key = (txt, round(float(y),1))
        if key in seen: continue
        seen.add(key)
        rows.append((float(y), float(x), txt, col, fs.group(1) if fs else '?', bold))
    rows.sort()
    for y, x, txt, col, fs, bold in rows:
        print(f'  y={y:6.1f} x={x:6.1f} fs={fs:>4} {bold} col={col:9} {txt[:40]}')
