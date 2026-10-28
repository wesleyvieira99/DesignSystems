import {createServer} from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
const root=resolve(import.meta.dirname,'../dist'),port=Number(process.env.PORT||4173);
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon'};
createServer(async(req,res)=>{try{const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);let file=resolve(root,'.'+pathname);if(file!==root&&!file.startsWith(root+sep)){res.writeHead(403).end();return;}if((await stat(file)).isDirectory())file=resolve(file,'index.html');res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});res.end(await readFile(file));}catch{res.writeHead(404).end('Not found');}}).listen(port,'127.0.0.1',()=>console.log(`Atlas: http://127.0.0.1:${port}`));
