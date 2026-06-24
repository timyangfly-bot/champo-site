import os
import re
from PIL import Image

ROOT_IMG = "images"
ROOT_SITE = "."
QUALITY = 80

sizes = {
    "": 1200,
    "_thumb": 400,
    "_mini": 150
}

print("Scanning images...")

for root, dirs, files in os.walk(ROOT_IMG):
    for file in files:

        if file.lower().endswith((".jpg",".jpeg",".png")):

            path = os.path.join(root,file)
            name = os.path.splitext(file)[0]

            try:
                img = Image.open(path)
                img = img.convert("RGB")

                for suffix,width in sizes.items():

                    im = img.copy()
                    im.thumbnail((width,width))

                    out = os.path.join(root,f"{name}{suffix}.webp")

                    im.save(out,"WEBP",quality=80)

                print("optimized:",path)

            except:
                print("skip:",path)

print("Images done")

print("Updating HTML...")

for root, dirs, files in os.walk(ROOT_SITE):
    for file in files:

        if file.endswith(".html"):

            path = os.path.join(root,file)

            with open(path,"r",encoding="utf8") as f:
                html = f.read()

            html = re.sub(r'\.jpg','.webp',html)
            html = re.sub(r'\.png','.webp',html)

            with open(path,"w",encoding="utf8") as f:
                f.write(html)

            print("updated:",path)

print("HTML done")