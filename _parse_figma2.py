import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 找顶层 frame: 大尺寸绝对定位 div (手机外框)
# 外框特征: width~327 height~697 且带 box-shadow
frames = re.findall(r'<div style="([^"]*?)">', html)
print('TOTAL styled divs:', len(frames))

# 筛选可能的手机外框 (width 接近 327)
phone_frames = []
for i, s in enumerate(frames):
    if 'width: 327' in s and 'height: 697' in s:
        phone_frames.append((i, s))
print('PHONE FRAMES FOUND:', len(phone_frames))
for i, s in phone_frames:
    # 提取 left/top
    lt = re.search(r'left: ([\d.]+)px; top: ([\d.]+)px', s)
    print(f'  idx={i} pos={lt.group(0) if lt else "?"}')

# 统计每个手机屏幕内的文字, 通过 left 坐标分组
# 提取所有带 left/top 的 div 块及其文本
blocks = re.findall(r'<div style="([^"]*?)">([^<]*)</div>', html)
# 重新抓: 包含 text 的 div
print('\n--- sample screen text positions ---')
for s, txt in blocks:
    if txt.strip() and ('left:' in s) and ('top:' in s):
        l = re.search(r'left: ([\d.]+)px', s)
        t = re.search(r'top: ([\d.]+)px', s)
        if l and t:
            # 只打印 top 在 100-800 范围 (手机内)
            top = float(t.group(1))
            if 100 <= top <= 800:
                print(f'top={top:6.1f} left={l.group(1):6.1f}  {txt.strip()[:30]}')
