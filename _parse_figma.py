import re
from collections import Counter

html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
tags = re.findall(r'<([a-zA-Z0-9]+)(?:\s|>)', html)
c = Counter(tags)
print('TAG COUNTS:', c.most_common(20))

imgs = re.findall(r"src='([^']+)'", html)
print('IMG COUNT:', len(imgs))
for i in imgs[:12]:
    print(i[-45:])

# 文字节点: figm 导出常见 <div style=...>TEXT</div> 或 <span>
# 尝试找包含中文/英文单词的纯文本节点
texts = re.findall(r'>([^<>{}]{1,60})<', html)
seen = set()
out = []
for t in texts:
    t = t.strip()
    if t and t not in seen and re.search(r'[\u4e00-\u9fffA-Za-z]', t):
        seen.add(t)
        out.append(t)
print('TEXT-LIKE NODES:', len(out))
for t in out[:120]:
    print(repr(t))
