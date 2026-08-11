import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

def dump(idx, n=5000):
    seg = html[positions[idx]:positions[idx+1] if idx+1<len(positions) else len(html)]
    print(f'\n========== SCREEN {idx+1} ==========')
    print(seg[:n])

# Screen 2 (相机-已装卷)
dump(1)
