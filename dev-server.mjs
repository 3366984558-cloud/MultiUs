import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, sep } from 'node:path';

const args = process.argv.slice(2);
function arg(name, dflt){ const i = args.indexOf('--' + name); return i > -1 ? args[i+1] : dflt; }
const port = +(arg('port', process.env.PORT || 7100));
const host = arg('host', '127.0.0.1');
const root = process.cwd();
const MIME = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.css':'text/css', '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml', '.ico':'image/x-icon' };

http.createServer(async (req, res) => {
  try{
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if(p === '/') p = '/index.html';
    const file = normalize(join(root, p));
    if(!file.startsWith(root + sep) && file !== root){ res.writeHead(403); return res.end(); }
    const data = await readFile(file);
    res.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream' });
    res.end(data);
  }catch{ res.writeHead(404); res.end('not found'); }
}).listen(port, host, () => console.log(`MultiUs dev server -> http://${host}:${port}/`));
