import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 5 个手机外框 left (外框 left 值)
phone_lefts = [100, 527.20, 954.39, 1381.59, 1808.79]
# 内屏 left 偏移: 外框 left + 6.67(内框) ... 实际内容用相对内屏坐标
# 但 Figma 导出是相对画布绝对坐标。每个手机内元素 left 在 [phone_left, phone_left+327]
# 切块
bounds = []
for i, L in enumerate(phone_lefts):
    nxt = phone_lefts[i+1] if i+1 < len(phone_lefts) else 2236
    bounds.append((L, nxt))

# 提取 span 文本 (含坐标和颜色)
span_re = re.compile(
    r'<div style="left: ([\d.]+)px; top: ([\d.]+)px; position: absolute; text-align: center">'
    r'<span style="([^"]*)">([^<]+)</span></div>'
)
spans = span_re.findall(html)
print('SPAN TEXT NODES:', len(spans))

for bi, (lo, hi) in enumerate(bounds):
    items = []
    for x, y, style, txt in spans:
        xf = float(x); yf = float(y)
        # span 的 left 是相对父 div, 父 div 的绝对 left 需加。简化: 用 top 分组 + 大致区间
        # 这里 x 已经是相对内屏? 实测 'all' 在 left:1 top:0, 父 div left:? 
        # 用 top 判断手机: 每个手机 top 都在 100~800 (画布坐标)
        # 但 span 的 top 是相对父, 父的绝对 top 才是关键。我们改用父 div 绝对 top。
        # 退而求其次: 统计每个屏幕 top 范围
        items.append((yf, xf, txt, style[:40]))
    # 需要父级坐标。改为解析带 absolute + left/top 的 div 父级
    print(f'\n===== SCREEN {bi+1} =====')
    # 仅打印前若干
    for yf, xf, txt, st in sorted(items)[:50]:
        print(f'  top={yf:6.1f} left={xf:6.1f}  {txt[:25]}')
