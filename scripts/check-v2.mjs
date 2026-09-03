import fs from "node:fs/promises";
import path from "node:path";
const root=path.resolve(import.meta.dirname,"..","dist");
const html=[];async function walk(p){for(const e of await fs.readdir(p,{withFileTypes:true})){const f=path.join(p,e.name);if(e.isDirectory())await walk(f);else if(e.name.endsWith('.html'))html.push(f)}}await walk(root);
const broken=[];let placeholders=0;for(const file of html){const s=await fs.readFile(file,'utf8');placeholders+=(s.match(/8613800000000|href=["']#["']|�/g)||[]).length;for(const m of s.matchAll(/(?:href|src)=["'](\/[^"][^"']*)["']/g)){const u=m[1].split('#')[0].split('?')[0];if(!u)continue;let target=path.join(root,decodeURIComponent(u));try{const st=await fs.stat(target);if(st.isDirectory())target=path.join(target,'index.html');await fs.access(target)}catch{broken.push({file:path.relative(root,file),url:u})}}}
console.log(JSON.stringify({htmlPages:html.length,brokenLinks:broken.length,placeholders},null,2));if(broken.length){console.log(broken.slice(0,30));process.exitCode=1}
