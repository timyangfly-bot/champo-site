import pandas as pd
import os

# Excel路径
excel = r"D:\champo\site\product.xlsx"

# 网站products目录
site_products = r"D:\champo\site\products"

df = pd.read_excel(excel)

template = """
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>{model} | CHAMPO</title>

<meta name="description" content="{model} automotive accessory manufactured by CHAMPO. OEM customization available.">

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

<tr>
<td>Model</td>
<td>{model}</td>
</tr>

<tr>
<td>Dimension</td>
<td>{dimension}</td>
</tr>

<tr>
<td>Packing Size</td>
<td>{packing}</td>
</tr>

<tr>
<td>Net Weight</td>
<td>{weight}</td>
</tr>

<tr>
<td>MOQ</td>
<td>{moq}</td>
</tr>

<tr>
<td>Color</td>
<td>{color}</td>
</tr>

</table>

<h3>Features</h3>

<ul>
{features}
</ul>

<a class="btn" href="/#contact">Get Quote</a>

</div>

</div>

<h2>Customization Service</h2>

<p>
Size, materials, internal boards, plastic parts, logo and packaging can be customized.
Leather and Oxford fabrics are available with waterproof or flame‑retardant options.
</p>

</div>

</body>
</html>
"""

output_folder = os.path.join(site_products,"generated")

os.makedirs(output_folder,exist_ok=True)

for i,row in df.iterrows():

    model = str(row["Item No."]).strip()

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

    image = model.lower() + ".webp"

    html = template.format(
        model=model,
        dimension=dimension,
        packing=packing,
        weight=weight,
        moq=moq,
        color=color,
        features=features,
        image=image
    )

    file_path = os.path.join(output_folder,model.lower()+".html")

    with open(file_path,"w",encoding="utf-8") as f:
        f.write(html)

    print("created:",file_path)

print("✅ All product pages generated")