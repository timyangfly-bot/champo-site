import os
import re
from PIL import Image
from bs4 import BeautifulSoup

ROOT = "."
IMG_DIR = "images"

sizes = {
    "":1200,
    "_thumb":400,
    "_mini":150
}

print("STEP 1: optimize images")

for root, dirs, files in os.walk(IMG_DIR):

    for file in files:

        if file.lower().endswith((".jpg",".jpeg",".png")):

            path=os.path.join(root,file)
            name=os.path.splitext(file)[0]

            try:

                img=Image.open(path).convert("RGB")

                for suffix,w in sizes.items():

                    im=img.copy()
                    im.thumbnail((w,w))

                    out=os.path.join(root,f"{name}{suffix}.webp")

                    im.save(out,"WEBP",quality=80)

                print("image ok:",path)

            except:
                print("skip:",path)


print("STEP 2: update html image paths")

html_files=[]

for root,dirs,files in os.walk(ROOT):

    for f in files:

        if f.endswith(".html"):
            html_files.append(os.path.join(root,f))


for path in html_files:

    with open(path,"r",encoding="utf8") as f:
        html=f.read()

    html=re.sub(r'\.jpg','.webp',html)
    html=re.sub(r'\.png','.webp',html)

    with open(path,"w",encoding="utf8") as f:
        f.write(html)

    print("html updated:",path)


print("STEP 3: scan missing images")

missing=[]

for path in html_files:

    with open(path,"r",encoding="utf8") as f:
        soup=BeautifulSoup(f,"html.parser")

    for img in soup.find_all("img"):

        src=img.get("src")

        if src:

            p=src.lstrip("/")

            if not os.path.exists(p):
                missing.append((path,src))


for m in missing:
    print("MISSING:",m)


print("STEP 4: generate sitemap")

urls=[]

for root,dirs,files in os.walk(ROOT):

    for f in files:

        if f.endswith(".html"):

            p=os.path.join(root,f)

            url=p.replace("\\","/").replace("./","")

            urls.append(url)


with open("sitemap.xml","w",encoding="utf8") as f:

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    for u in urls:

        f.write("<url>\n")
        f.write(f"<loc>https://yourdomain.com/{u}</loc>\n")
        f.write("</url>\n")

    f.write("</urlset>")

print("sitemap generated")