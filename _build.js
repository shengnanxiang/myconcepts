// 生成 minigame.html 的脚本
const fs = require('fs');
const p = 'c:/Users/Nan/Documents/GitHub/myconcepts/';

// 读取模板部分
const css = fs.readFileSync(p + '_part_css.html', 'utf8');
const js = fs.readFileSync(p + '_part_js.js', 'utf8');

const html = css + '\n<script>\n' + js + '\n</script>\n</body>\n</html>\n';

fs.writeFileSync(p + 'minigame.html', html);
console.log('Done. Size:', (fs.statSync(p + 'minigame.html').size / 1024).toFixed(1) + 'KB');
