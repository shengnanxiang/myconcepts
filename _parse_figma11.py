import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

# Screen 1: 提取每个胶片卡: 名字(含<br/>行) + 颜色 + 它的 chips
seg1 = html[positions[0]:positions[1]]

# 胶片名 = font-size:20 bold 的 span (可能是单行或两行)
film_block = re.findall(
    r"background: (#[0-9A-Fa-f]{6}); color: transparent; background-clip: text; font-size: 20px; font-family: Space Mono; font-weight: 700; word-wrap: break-word\">([^<]*)(?:<br/>([^<]*))?</span>",
    seg1)
print("=== Screen 1 Film Cards ===")
for col, l1, l2 in film_block:
    name = (l1 + ((' ' + l2) if l2 else '')).strip()
    print(f"  {name:20} color={col}")

# Select a style 标题 颜色
print("\n=== Headers / buttons Screen1 ===")
for m in re.finditer(r"background: (#[0-9A-Fa-f]{6}); color: transparent; background-clip: text; font-size: (\d+)px; font-family: Space Mono; font-weight: 700[^>]*>([^<]*)<", seg1):
    print(f"  fs={m.group(2)} col={m.group(1)} text={m.group(3)}")

# 提取 "Select" (筛选条) 和 顶部 tab: all/b&w/warm/cold/style
filters = re.findall(r"background: (white|#A39C91); color: transparent; background-clip: text; font-size: 10px; font-family: Space Mono; font-weight: 400; letter-spacing: 1px[^>]*>([^<]*)<", seg1)
print("\n=== Filters ===")
for col, t in filters:
    print(f"  {t} (col={col})")

# 提取 "SELECT A STYLE" 标题
title = re.findall(r"font-size: 12px; font-family: Space Mono; font-weight: 400[^>]*>([^<]*)<", seg1)
print("\n=== Title-ish (fs12) ===", title)
