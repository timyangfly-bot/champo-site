import pandas as pd
import os
from datetime import date
import subprocess

site_root = r"D:\champo\site"
excel = os.path.join(site_root,"product.xlsx")

products_dir = os.path.join(site_root,"products")
images_dir = os.path.join(products_dir,"images")

rules = {
"tk":"tool-kit",
"tm":"trunk-mat",
"sc":"pet-seat-cover",
"sb":"storage-box",
"sh":"seat-hanging-bag",
"cs":"child-seat-protection-pad"
}

categories = {
"tool-kit":"Tool Kit",
"trunk-mat":"Trunk Mat",
"pet-seat-cover":"Pet Seat Cover",
"storage-box":"Storage Box",
"seat-hanging-bag":"Seat Hanging Bag",
"child-seat-protection-pad":"Child Seat Protection Pad"
}

df = pd.read_excel(excel)

product_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{model} | CHAMPO</title>
<meta name="description" content="{model} automotive accessory manufactured by CHAMPO.">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>

<div class="container">

<h1>{model}</h1>

<div class="product-page">

<div class="product-image">
<img src="/products/images/{image}" alt="{model}">
</div>

<div class="product-info">

<h2>Product Information</h2>

<table class="spec-table">

<tr><td>Model</td><td>{model}</td></tr>
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

cards = {k:"" for k in categories.keys()}
urls = []

for i,row in df.iterrows():

    model = str(row["Item No."]).strip().lower()
    prefix = model.split("-")[0]

    if prefix not in rules:
        continue

    category = rules[prefix]
    category_dir = os.path.join(products_dir,category)

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

    html = product_template.format(
        model=model.upper(),
        dimension=dimension,
        packing=packing,
        weight=weight,
        moq=moq,
        color=color,
        features=features,
        image=image
    )

    product_path = os.path.join(category_dir,model+".html")

    with open(product_path,"w",encoding="utf-8") as f:
        f.write(html)

    print("product created:",product_path)

    cards[category] += f"""
<div class="product-card">
<img src="/products/images/{image}">
<h3>{model.upper()}</h3>
<a class="btn" href="/products/{category}/{model}.html">View Details</a>
</div>
"""

    urls.append(f"https://champoauto.com/products/{category}/{model}.html")

for category,title in categories.items():

    category_dir = os.path.join(products_dir,category)
    os.makedirs(category_dir,exist_ok=True)

    index_html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>{title} | CHAMPO</title>

<meta name="description" content="{title} manufacturer and supplier.">

<link rel="stylesheet" href="/css/style.css">

</head>

<body>

<h1>{title}</h1>

<div class="category-layout">

<aside class="category-sidebar">

<h3>Product Categories</h3>

<ul class="category-menu">
"""

    for c,t in categories.items():
        active = "class='active'" if c==category else ""
        index_html += f"<li {active}><a href='/products/{c}/'>{t}</a></li>"

    index_html += """
</ul>

</aside>

<main class="product-grid">
"""

    index_html += cards[category]

    index_html += """
</main>

</div>

</body>
</html>
"""

    with open(os.path.join(category_dir,"index.html"),"w",encoding="utf-8") as f:
        f.write(index_html)

    print("category updated:",category)

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    sitemap += f"""
<url>
<loc>{url}</loc>
<lastmod>{date.today()}</lastmod>
<changefreq>monthly</changefreq>
<priority>0.8</priority>
</url>
"""

sitemap += "</urlset>"

with open(os.path.join(site_root,"sitemap_products.xml"),"w",encoding="utf-8") as f:
    f.write(sitemap)

print("sitemap updated")

try:
    subprocess.run(["git","add","."],cwd=site_root)
    subprocess.run(["git","commit","-m","auto update products"],cwd=site_root)
    subprocess.run(["git","push"],cwd=site_root)
    print("git deployed")
except:
    print("git push skipped")