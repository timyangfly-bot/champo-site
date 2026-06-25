import os
import re
from datetime import date

SITE = "https://champoauto.com"
ROOT = "."

pages = []
sitemap_urls = []

def title_from_path(path):

    name = os.path.basename(path)

    name = name.replace(".html","").replace("-"," ")

    return name.title()

for root,dirs,files in os.walk(ROOT):

    for f in files:

        if f.endswith(".html"):

            path = os.path.join(root,f)

            pages.append(path)

for file in pages:

    with open(file,"r",encoding="utf-8") as f:
        html = f.read()

    title = title_from_path(file)

    # 自动 description
    if 'name="description"' not in html:

        desc = f'<meta name="description" content="{title} automotive accessory manufactured by CHAMPO. Durable car storage and protection solution.">'

        html = html.replace("</head>",desc+"\n</head>")

    # 自动 canonical
    if 'rel="canonical"' not in html:

        url = file.replace("\\","/")

        url = url.replace("./","")

        url = url.replace("index.html","")

        canonical = f'<link rel="canonical" href="{SITE}/{url}">'

        html = html.replace("</head>",canonical+"\n</head>")

    # 图片 alt
    imgs = re.findall(r'<img[^>]+>',html)

    for img in imgs:

        if "alt=" not in img:

            src = re.search(r'src="([^"]+)"',img)

            if src:

                alt = src.group(1).split("/")[-1].replace(".jpg","").replace("-"," ")

                new_img = img.replace(">",f' alt="{alt}">')

                html = html.replace(img,new_img)

    with open(file,"w",encoding="utf-8") as f:
        f.write(html)

    url = file.replace("\\","/")

    url = url.replace("./","")

    sitemap_urls.append(SITE+"/"+url)

print("✅ SEO fixes applied")

# 生成 sitemap

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'

xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in sitemap_urls:

    xml += f"""
<url>
<loc>{url}</loc>
<lastmod>{date.today()}</lastmod>
<changefreq>monthly</changefreq>
<priority>0.8</priority>
</url>
"""

xml += "</urlset>"

with open("sitemap.xml","w",encoding="utf-8") as f:
    f.write(xml)

print("✅ sitemap.xml generated")

print("Total pages:",len(pages))