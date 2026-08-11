import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 找 5 个手机外框 div 的字符位置
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

# 更宽正则: 抓所有带 left/top + span 文本
span_re = re.compile(
    r'<div style="left: ([\d.]+)px; top: ([\d.]+)px; position: absolute; text-align: center">'
    r'<span style="([^"]*)">([^<]+)</span></div>'
)

for idx, pos in enumerate(positions):
    end = positions[idx+1] if idx+1 < len(positions) else len(html)
    seg = html[pos:end]
    spans = span_re.findall(seg)
    print(f'\n===== SCREEN {idx+1} =====')
    seen = set()
    rows = []
    for x, y, style, txt in spans:
        txt = txt.replace('&nbsp;',' ').strip()
        if not txt: continue
        key = (txt, round(float(y),1))
        if key in seen: continue
        seen.add(key)
        col = 'n/a'
        m = re.search(r'(?:background|color): (#[0-9A-Fa-f]{3,8})', style)
        if m: col = m.group(1)
        fs = re.search(r'font-size: ([\d.]+)px', style)
        bold = 'bold' if 'font-weight: 700' in style or 'font-weight: bold' in style else ''
        rows.append((float(y), float(x), txt, col, fs.group(1) if fs else '?', bold))
    rows.sort()
    for y, x, txt, col, fs, bold in rows:
        print(f'  y={y:6.1f} x={x:6.1f} fs={fs:>4} {bold:4} col={col:9} {txt[:35]}')
