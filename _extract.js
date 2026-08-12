const fs = require('fs');
const content = fs.readFileSync('c:/Users/Nan/Documents/GitHub/myconcepts/minigame.html', 'utf8');
const start = content.indexOf('<script>');
const end = content.indexOf('</script>');
if (start !== -1 && end !== -1) {
  let js = content.substring(start + 8, end);
  // Replace base64 data URIs with placeholder
  js = js.replace(/data:image\/jpeg;base64,[A-Za-z0-9+/=]+/g, 'BASE64_DATA_URI');
  fs.writeFileSync('c:/Users/Nan/Documents/GitHub/myconcepts/_js_extract.txt', js);
  console.log('JS extracted (base64 stripped), length:', js.length, 'chars');
} else {
  console.log('Script tags not found');
}
