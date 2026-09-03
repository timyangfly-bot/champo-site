import http from "node:http";
import fs from "node:fs";
import path from "node:path";
const root=path.resolve(import.meta.dirname,"..","dist");
const types={".html":"text/html; charset=utf-8",".css":"text/css",".js":"text/javascript",".json":"application/json",".xml":"application/xml",".webp":"image/webp",".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png"};
http.createServer((req,res)=>{let file=path.join(root,decodeURIComponent(req.url.split("?")[0]));if(req.url.endsWith("/"))file=path.join(file,"index.html");fs.stat(file,(e,s)=>{if(e||!s.isFile()){res.writeHead(404);return res.end("Not found")}res.writeHead(200,{"Content-Type":types[path.extname(file).toLowerCase()]||"application/octet-stream"});fs.createReadStream(file).pipe(res)})}).listen(4173,"127.0.0.1",()=>console.log("CHAMPO V2 http://127.0.0.1:4173"));
