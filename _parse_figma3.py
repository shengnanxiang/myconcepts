import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 5 个手机屏幕的 left 起点 (外框)
starts = [100, 527.20, 954.39, 1381.59, 1808.79]
# 内屏 left 偏移 ~ +10 (外框 left + 6.67 内框 + ...), 用 100~527 区间判断
bounds = [(100, 527.20), (527.20, 954.39), (954.39, 1381.59), (1381.59, 1808.79), (1808.79, 2236)]

# 抓取所有块: <div style=...>TEXT</div> 或半结构
# 由于单行, 用正则分块较困难。改为按 img 的 left 坐标分组
imgs = re.findall(r"<div data-svg-wrapper style=\"left: ([\d.]+)px; top: ([\d.]+)px; position: absolute\"><img src='([^']+)'", html)
print('SVG wrappers:', len(imgs))

# 文字: 找到所有 '>TEXT</div>' 模式, 取前一个 div 的 left
# 用更宽正则捕获 style 和文本
pattern = re.compile(r'<div style="([^"]*?)">([^<]{1,40})</div>')
matches = pattern.findall(html)
print('text divs:', len(matches))

for bi, (lo, hi) in enumerate(bounds):
    texts = []
    for s, txt in matches:
        l = re.search(r'left: ([\d.]+)px', s)
        if not l: continue
        x = float(l.group(1))
        if lo - 10 <= x < hi:
            t = txt.strip()
            if t and re.search(r'[\w\u4e00-\u9fff]', t):
                texts.append((x, t))
    texts.sort()
    print(f'\n===== SCREEN {bi+1} (left {lo:.0f}) =====')
    for x, t in texts[:60]:
        print(f'  x={x:6.1f}  {t[:35]}')
