import os
import re
from bs4 import BeautifulSoup

DOMAIN = "https://champoauto.com"
ROOT = "."

pages = 0
fixed_alt = 0
fixed_desc = 0

urls = []

def make_alt(src):
    name = os.path.basename(src)
    name = name.replace(".webp","")
    name = name.replace(".jpg","")
    name = name.replace(".png","")
    name = name.replace("-"," ")
    name = name.replace("_"," ")
    return name

def make_description(title):
    if not title:
        return "High quality automotive accessories from Champo."
    return f"{title} - premium automotive accessories from Champo."

for root, dirs, files in os.walk(ROOT):

    for f in files:

        if f.endswith(".html"):

            path = os.path.join(root,f)
            pages += 1

            with open(path,"r",encoding="utf8",errors="ignore") as file:
                soup = BeautifulSoup(file,"html.parser")

            title = None
            if soup.title:
                title = soup.title.text.strip()

            if not soup.find("meta",attrs={"name":"description"}):

                desc = make_description(title)

                tag = soup.new_tag("meta")
                tag.attrs["name"] = "description"
                tag.attrs["content"] = desc

                if soup.head:
                    soup.head.append(tag)

                fixed_desc += 1

            for img in soup.find_all("img"):

                src = img.get("src")

                if src:

                    src = re.sub(r'\.jpg','.webp',src)
                    src = re.sub(r'\.png','.webp',src)

                    img["src"] = src

                    if not img.get("alt"):

                        img["alt"] = make_alt(src)
                        fixed_alt += 1

            with open(path,"w",encoding="utf8",errors="ignore") as file:
                file.write(str(soup))

            url = path.replace("\\","/").replace("./","")
            urls.append(url)

            print("processed:",path)

print("generate sitemap")

with open("sitemap.xml","w",encoding="utf8") as f:

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    for u in urls:

        f.write("<url>\n")
        f.write(f"<loc>{DOMAIN}/{u}</loc>\n")
        f.write("</url>\n")

    f.write("</urlset>")

print("\nSEO REPORT")
print("pages:",pages)
print("alt added:",fixed_alt)
print("meta description added:",fixed_desc)
print("sitemap pages:",len(urls))