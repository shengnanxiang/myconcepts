const fs = require('fs');
const content = fs.readFileSync('c:/Users/Nan/Documents/GitHub/myconcepts/minigame.html', 'utf8');
// Extract from start to <script>
const scriptStart = content.indexOf('<script>');
if (scriptStart !== -1) {
  let html = content.substring(0, scriptStart);
  // Replace base64 data URIs with placeholder
  html = html.replace(/data:image\/jpeg;base64,[A-Za-z0-9+/=]+/g, 'BASE64_DATA_URI');
  fs.writeFileSync('c:/Users/Nan/Documents/GitHub/myconcepts/_html_extract.txt', html);
  console.log('HTML extracted (base64 stripped), length:', html.length, 'chars');
}
