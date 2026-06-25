import os
import re

ROOT = "."
SITE = "https://champoauto.com"

html_files = []
links = []
images = []

missing_title = []
missing_desc = []
missing_canonical = []
missing_alt = []
broken_links = []
missing_images = []

def scan_files():

    for root,dirs,files in os.walk(ROOT):

        for file in files:

            if file.endswith(".html"):

                html_files.append(os.path.join(root,file))

scan_files()

for file in html_files:

    with open(file,"r",encoding="utf-8") as f:
        html = f.read()

    # title
    if "<title>" not in html:
        missing_title.append(file)

    # description
    if 'name="description"' not in html:
        missing_desc.append(file)

    # canonical
    if 'rel="canonical"' not in html:
        missing_canonical.append(file)

    # images
    imgs = re.findall(r'<img[^>]+>',html)

    for img in imgs:

        src = re.search(r'src="([^"]+)"',img)
        alt = re.search(r'alt="([^"]*)"',img)

        if src:
            images.append(src.group(1))

            path = src.group(1).replace("/","")

            if not os.path.exists(path):
                missing_images.append((file,src.group(1)))

        if not alt:
            missing_alt.append((file,img))

    # links
    hrefs = re.findall(r'href="([^"]+)"',html)

    for href in hrefs:

        if href.startswith("http"):
            continue

        if href.startswith("#"):
            continue

        links.append((file,href))

        path = href.lstrip("/")

        if not os.path.exists(path) and not os.path.exists(path+"index.html"):

            broken_links.append((file,href))

print("\n==== SITE AUDIT ====\n")

print("Total HTML pages:",len(html_files))

print("\nMissing title:")
for i in missing_title:
    print(i)

print("\nMissing description:")
for i in missing_desc:
    print(i)

print("\nMissing canonical:")
for i in missing_canonical:
    print(i)

print("\nImages without alt:")
for i in missing_alt[:20]:
    print(i)

print("\nMissing image files:")
for i in missing_images[:20]:
    print(i)

print("\nBroken links:")
for i in broken_links[:20]:
    print(i)

print("\nAudit finished")