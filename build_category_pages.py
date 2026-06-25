import os

categories = [
("child-seat-protection-pad","Child Seat Protection Pad"),
("pet-seat-cover","Pet Seat Cover"),
("seat-hanging-bag","Seat Hanging Bag"),
("storage-box","Storage Box"),
("tool-kit","Tool Kit"),
("trunk-mat","Trunk Mat")
]

def sidebar(current):

    html = '<aside class="category-sidebar">'
    html += '<h3>Product Categories</h3>'
    html += '<ul class="category-menu">'

    for slug,name in categories:

        if slug == current:
            html += f'<li class="active"><a href="/products/{slug}/">{name}</a></li>'
        else:
            html += f'<li><a href="/products/{slug}/">{name}</a></li>'

    html += "</ul></aside>"

    return html


def product_grid(folder):

    html = '<main class="product-grid">'

    for file in os.listdir(folder):

        if file.endswith(".webp") or file.endswith(".jpg"):

            name = file.replace(".webp","").replace(".jpg","").upper()

            html += f'''
<div class="product-card">

<img src="/products/{os.path.basename(folder)}/{file}" alt="{name}">

<h3>{name}</h3>

<a class="btn" href="/contact/">Get Quote</a>

</div>
'''

    html += "</main>"

    return html


for slug,title in categories:

    folder = f"products/{slug}"

    if not os.path.exists(folder):
        continue

    sidebar_html = sidebar(slug)

    products_html = product_grid(folder)

    page = f'''
<!DOCTYPE html>
<html>
<head>

<title>{title} | CHAMPO</title>

<meta name="description" content="{title} manufacturer and supplier. OEM customization available.">

<link rel="stylesheet" href="/css/style.css">

</head>

<body>

<section class="category-header">

<h1>{title}</h1>

<p>
Professional manufacturer of {title.lower()} with OEM and ODM customization service.
</p>

</section>

<div class="category-layout">

{sidebar_html}

{products_html}

</div>

</body>
</html>
'''

    with open(f"{folder}/index.html","w",encoding="utf-8") as f:
        f.write(page)

    print("built:",slug)

print("✅ category pages built")