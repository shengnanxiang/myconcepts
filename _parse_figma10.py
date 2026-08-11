import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

# 提取所有胶片名 (红/彩色 big text) + EXP + chips + tab 标签
# 胶片名: background:#E53935 或其他色, font-size:20 bold
film_re = re.compile(r"background: (#[0-9A-Fa-f]{6}); color: transparent; background-clip: text; font-size: 20px; font-family: Space Mono; font-weight: 700[^>]*>([^<]+)<br/>([^<]+)")
exp_re = re.compile(r"background: #A39C91[^>]*>(\d+&nbsp;EXP)</span>")
chip_re = re.compile(r"background: #E6DFD3[^>]*>([^<]+)</span>")
tab_re = re.compile(r"background: #A39C91[^>]*>([^<]+)</span>")
# 大按钮文字
btn_re = re.compile(r"font-weight: 700[^>]*>([^<]+)</span>")

for idx, pos in enumerate(positions):
    end = positions[idx+1] if idx+1 < len(positions) else len(html)
    seg = html[pos:end]
    print(f'\n===== SCREEN {idx+1} =====')
    films = film_re.findall(seg)
    for col, l1, l2 in films:
        print(f'  FILM: {l1} {l2}  (color {col})')
    exps = exp_re.findall(seg)
    for e in exps: print(f'  EXP: {e}')
    chips = chip_re.findall(seg)
    for c in chips: print(f'  CHIP: {c}')
