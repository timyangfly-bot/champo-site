import pandas as pd
import os
from datetime import date
import subprocess

site = r"D:\champo\site"
excel = os.path.join(site,"product.xlsx")
products = os.path.join(site,"products")

rules = {
"tk":"tool-kit",
"tm":"trunk-mat",
"sc":"pet-seat-cover",
"sb":"storage-box",
"sh":"seat-hanging-bag",
"cs":"child-seat-protection-pad"
}

df = pd.read_excel(excel)

cards = {}

for cat in rules.values():
    cards[cat] = ""

for i,row in df.iterrows():

    model = str(row["Item No."]).strip().lower()
    prefix = model.split("-")[0]

    if prefix not in rules:
        continue

    category = rules[prefix]

    category_dir = os.path.join(products,category)

    os.makedirs(category_dir,exist_ok=True)

    dimension = str(row["Dimension(cm)"])
    packing = str(row["Packing Data(cm)"])
    weight = str(row["Net weight(kg)"])
    moq = str(row["MOQ"])
    color = str(row["color"])
    desc = str(row["Discription"])

    features = ""
    for line in desc.split("\n"):
        if line.strip():
            features += f"<li>{line.strip()}</li>"

    image = model + ".webp"

    product_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{model.upper()} | CHAMPO</title>
<meta name="description" content="{model.upper()} automotive accessory manufactured by CHAMPO.">
<link rel="stylesheet" href="/css/style.css">
</head>

<body>

<div class="container">

<h1>{model.upper()}</h1>

<div class="product-page">

<div class="product-image">
<img src="/products/images/{image}">
</div>

<div class="product-info">

<h2>Product Information</h2>

<table class="spec-table">

<tr><td>Model</td><td>{model.upper()}</td></tr>
<tr><td>Dimension</td><td>{dimension}</td></tr>
<tr><td>Packing Size</td><td>{packing}</td></tr>
<tr><td>Net Weight</td><td>{weight}</td></tr>
<tr><td>MOQ</td><td>{moq}</td></tr>
<tr><td>Color</td><td>{color}</td></tr>

</table>

<h3>Features</h3>

<ul>
{features}
</ul>

<a class="btn" href="/#contact">Get Quote</a>

</div>
</div>

</div>

</body>
</html>
"""

    product_file = os.path.join(category_dir,model+".html")

    with open(product_file,"w",encoding="utf-8") as f:
        f.write(product_html)

    print("product created:",model)

    cards[category] += f"""

<div class="product-card">

<img src="/products/images/{image}">

<h3>{model.upper()}</h3>

<a class="btn" href="/products/{category}/{model}.html">
View Details
</a>

</div>
"""

for category in cards:

    index_file = os.path.join(products,category,"index.html")

    if not os.path.exists(index_file):
        continue

    with open(index_file,"r",encoding="utf-8") as f:
        html = f.read()

    start = html.find("<main class=\"product-grid\">")
    end = html.find("</main>")

    if start == -1:
        continue

    new_html = html[:start] + '<main class="product-grid">' + cards[category] + "</main>" + html[end+7:]

    with open(index_file,"w",encoding="utf-8") as f:
        f.write(new_html)

    print("category updated:",category)

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for category in cards:
    folder = os.path.join(products,category)

    for file in os.listdir(folder):

        if file.endswith(".html") and file != "index.html":

            url = f"https://champoauto.com/products/{category}/{file}"

            sitemap += f"""
<url>
<loc>{url}</loc>
<lastmod>{date.today()}</lastmod>
<changefreq>monthly</changefreq>
<priority>0.8</priority>
</url>
"""

sitemap += "</urlset>"

with open(os.path.join(site,"sitemap_products.xml"),"w",encoding="utf-8") as f:
    f.write(sitemap)

print("sitemap updated")

try:
    subprocess.run(["git","add","."],cwd=site)
    subprocess.run(["git","commit","-m","auto update products"],cwd=site)
    subprocess.run(["git","push"],cwd=site)
    print("git deployed")
except:
    print("git push skipped")
