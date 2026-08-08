import re
html = open('.codebuddy/figma/255_3135/figma.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'width: 327\.20px; height: 697\.45px', html)]

seg3 = html[positions[2]:positions[3]]
print("===== SCREEN 3 (camera full) =====")
print(seg3[:4500])

seg5 = html[positions[4]:]
print("\n\n===== SCREEN 5 (dark room) =====")
print(seg5[:6000])
