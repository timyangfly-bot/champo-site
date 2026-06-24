import os
from bs4 import BeautifulSoup

ROOT="."
IMG_DIR="images"

html_files=[]
used_images=set()
all_images=set()

print("STEP1 scan images")

for root,dirs,files in os.walk(IMG_DIR):
    for f in files:
        if f.lower().endswith((".jpg",".jpeg",".png",".webp",".svg")):
            p=os.path.join(root,f).replace("\\","/")
            all_images.add(p)

print("total images:",len(all_images))


print("STEP2 scan html")

for root,dirs,files in os.walk(ROOT):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root,f))


missing_images=[]
no_alt=[]
no_title=[]
no_desc=[]

for path in html_files:

    with open(path,"r",encoding="utf8",errors="ignore") as f:
        soup=BeautifulSoup(f,"html.parser")

    # title
    if not soup.title:
        no_title.append(path)

    # description
    if not soup.find("meta",attrs={"name":"description"}):
        no_desc.append(path)

    # images
    for img in soup.find_all("img"):

        src=img.get("src")

        if src:

            p=src.lstrip("/")

            used_images.add(p)

            if not os.path.exists(p):
                missing_images.append((path,src))

        if not img.get("alt"):
            no_alt.append((path,src))


print("\nMISSING IMAGES")
for m in missing_images:
    print(m)

print("\nIMAGES WITHOUT ALT")
for a in no_alt:
    print(a)

print("\nPAGES WITHOUT TITLE")
for t in no_title:
    print(t)

print("\nPAGES WITHOUT META DESCRIPTION")
for d in no_desc:
    print(d)

print("\nUNUSED IMAGES")

unused=all_images-used_images

for u in unused:
    print(u)

print("\nSUMMARY")
print("pages:",len(html_files))
print("images:",len(all_images))
print("missing images:",len(missing_images))
print("no alt:",len(no_alt))
print("unused images:",len(unused))