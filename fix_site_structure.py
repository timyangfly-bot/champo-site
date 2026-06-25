import os
import re

SITE = "https://champoauto.com"
ROOT = "."

categories = [
"child-seat-protection-pad",
"pet-seat-cover",
"seat-hanging-bag",
"storage-box",
"tool-kit",
"trunk-mat"
]

def fix_index():

    path = os.path.join(ROOT,"index.html")

    if not os.path.exists(path):
        return

    with open(path,"r",encoding="utf-8") as f:
        html = f.read()

    # 修复 canonical
    html = html.replace(
    "https://champoauto.com/index.html",
    "https://champoauto.com/"
    )

    # 修复 categories 链接
    html = re.sub(
    r'categories/(.*?).html',
    r'/products/\1/',
    html
    )

    # 卡片变成链接
    for c in categories:

        title = c.replace("-"," ").title()

        html = html.replace(
        f'<div class="card">{title}</div>',
        f'<a href="/products/{c}/" class="card">{title}</a>'
        )

    with open(path,"w",encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html fixed")

def create_products_index():

    os.makedirs("products",exist_ok=True)

    html = """
<!DOCTYPE html>
<html>
<head>

<title>Products | CHAMPO</title>

<meta name="description" content="Automotive accessories including pet seat covers, trunk organizers and car storage solutions.">

<link rel="canonical" href="https://champoauto.com/products/">

</head>

<body>

<h1>Product Categories</h1>

<ul>
"""

    for c in categories:

        title = c.replace("-"," ").title()

        html += f'<li><a href="/products/{c}/">{title}</a></li>\n'

    html += """
</ul>

</body>
</html>
"""

    with open("products/index.html","w",encoding="utf-8") as f:
        f.write(html)

    print("✅ products/index.html created")

def scan_html():

    for root,dirs,files in os.walk("."):

        for file in files:

            if file.endswith(".html"):

                path = os.path.join(root,file)

                with open(path,"r",encoding="utf-8") as f:
                    html = f.read()

                html = re.sub(
                r'categories/(.*?).html',
                r'/products/\1/',
                html
                )

                with open(path,"w",encoding="utf-8") as f:
                    f.write(html)

    print("✅ all links updated")

fix_index()
create_products_index()
scan_html()

print("🎉 site structure fixed")