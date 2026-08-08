import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()

# 按手机外框 left 切割。外框 div 顺序已知。
# 找每个外框 div 的起始和结束。由于是嵌套绝对定位, 简单按 left 阈值切分整段文本。
bounds = [(100-50, 527.20), (527.20, 954.39), (954.39, 1381.59), (1381.59, 1808.79), (1808.79, 2300)]

# 抓取所有 div style 中的 left 与内部文本。
# Figma 文本模式: <div style="...left:Xpx; top:Ypx;...">SOMETEXT</div>
# 但前面解析 text divs=0, 可能文本在 <div style="..."> 后紧跟 <div ...>文字</div> 这样的嵌套
# 尝试匹配: >([^<]+)</div> 且前驱含 left:
# 用非贪婪提取所有 </div> 前的文本
all_texts = re.findall(r'>\s*([^<>{}]{1,40}?)\s*</div>', html)
print('raw text nodes:', len(all_texts))
# 过滤
real = [t.strip() for t in all_texts if t.strip() and re.search(r'[\w\u4e00-\u9fff]', t)]
print('real text nodes:', len(real))
for t in real[:100]:
    print(repr(t))
