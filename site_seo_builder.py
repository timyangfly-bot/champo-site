import os
import json
from datetime import date

SITE = "https://champoauto.com"
PRODUCTS_DIR = "products"
INDEX_FILE = "index.html"

sitemap_urls = []
home_categories = []

def title_from_slug(slug):
    return slug.replace(".html","").replace("-"," ").title()

for category in os.listdir(PRODUCTS_DIR):

    cat_path = os.path.join(PRODUCTS_DIR, category)

    if not os.path.isdir(cat_path):
        continue

    cat_title = title_from_slug(category)
    cat_url = f"/products/{category}/"

    home_categories.append(
        f'<li><a href="{cat_url}">{cat_title}</a></li>'
    )

    products = []

    for f in os.listdir(cat_path):

        if f.endswith(".html") and f != "index.html":

            name = title_from_slug(f)
            url = f"/products/{category}/{f}"

            products.append({
                "file":f,
                "name":name,
                "url":url
            })

            sitemap_urls.append(SITE + url)

    if not products:
        continue

    # ---------- 生成分类页 ----------

    product_links = "<ul>\n"

    for p in products:
        product_links += f'<li><a href="{p["url"]}">{p["name"]}</a></li>\n'

    product_links += "</ul>"

    category_html = f"""
<!DOCTYPE html>
<html>
<head>

<title>{cat_title} | ChampoAuto</title>

<meta name="description" content="{cat_title} designed for vehicle protection and organization.">

<link rel="canonical" href="{SITE}{cat_url}">

<script type="application/ld+json">
{json.dumps({
"@context":"https://schema.org",
"@type":"BreadcrumbList",
"itemListElement":[
{
"@type":"ListItem",
"position":1,
"name":"Home",
"item":SITE
},
{
"@type":"ListItem",
"position":2,
"name":"Products",
"item":SITE+"/products/"
},
{
"@type":"ListItem",
"position":3,
"name":cat_title,
"item":SITE+cat_url
}
]
},indent=2)}
</script>

</head>

<body>

<h1>{cat_title}</h1>

<p>
Our {cat_title.lower()} help improve vehicle organization and protect car interiors during daily driving and travel.
</p>

<h2>Products</h2>

{product_links}

</body>
</html>
"""

    os.makedirs(cat_path, exist_ok=True)

    with open(os.path.join(cat_path,"index.html"),"w",encoding="utf-8") as f:
        f.write(category_html)

    sitemap_urls.append(SITE + cat_url)

    # ---------- 处理产品页 ----------

    for p in products:

        path = os.path.join(cat_path,p["file"])

        with open(path,"r",encoding="utf-8") as f:
            html = f.read()

        related = "<ul>\n"

        for r in products:
            if r["file"] != p["file"]:
                related += f'<li><a href="{r["url"]}">{r["name"]}</a></li>\n'

        related += "</ul>"

        if "<!--RELATED_PRODUCTS-->" in html:
            html = html.replace("<!--RELATED_PRODUCTS-->",related)

        schema = {
            "@context":"https://schema.org",
            "@type":"Product",
            "name":p["name"],
            "url":SITE+p["url"]
        }

        schema_html = f'<script type="application/ld+json">{json.dumps(schema)}</script>'

        if "</head>" in html:
            html = html.replace("</head>",schema_html+"\n</head>")

        with open(path,"w",encoding="utf-8") as f:
            f.write(html)

# ---------- 首页分类 ----------

if os.path.exists(INDEX_FILE):

    with open(INDEX_FILE,"r",encoding="utf-8") as f:
        html = f.read()

    block = "<ul>\n"+"\n".join(home_categories)+"\n</ul>"

    start = html.find("<!--PRODUCT_CATEGORIES_START-->")
    end = html.find("<!--PRODUCT_CATEGORIES_END-->")

    if start != -1 and end != -1:

        html = html[:start] + "<!--PRODUCT_CATEGORIES_START-->\n" + block + "\n<!--PRODUCT_CATEGORIES_END-->" + html[end+len("<!--PRODUCT_CATEGORIES_END-->"):]

        with open(INDEX_FILE,"w",encoding="utf-8") as f:
            f.write(html)

# ---------- sitemap ----------

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

print("✅ SEO build complete")