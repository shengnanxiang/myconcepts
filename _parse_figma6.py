import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 找 5 个手机外框 div 的字符位置
# 外框特征: width: 327.20px; height: 697.45px
import re
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]
print('phone frame positions:', positions)

span_re = re.compile(
    r'<div style="left: ([\d.]+)px; top: ([\d.]+)px; position: absolute; text-align: center">'
    r'<span style="([^"]*)">([^<]+)</span></div>'
)

for idx, pos in enumerate(positions):
    # 取该手机区域: 从 pos 到下一个手机 pos (或文件末尾)
    end = positions[idx+1] if idx+1 < len(positions) else len(html)
    seg = html[pos:end]
    spans = span_re.findall(seg)
    print(f'\n===== SCREEN {idx+1} (chars {pos}-{end}, len {len(seg)}) =====')
    seen = set()
    for x, y, style, txt in spans:
        txt = txt.replace('&nbsp;',' ').strip()
        key = (txt, y)
        if key in seen: continue
        seen.add(key)
        # 提取颜色
        col = 'n/a'
        m = re.search(r'background: (#[0-9A-Fa-f]{3,8})', style)
        if m: col = m.group(1)
        print(f'  top={float(y):6.1f} left={float(x):6.1f}  col={col:10}  {txt[:30]}')
