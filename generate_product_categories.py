import os
import json
from datetime import date

SITE = "https://champoauto.com"
OUT = "products"

os.makedirs(OUT, exist_ok=True)

categories = [

{
"slug":"child-seat-protection-pad",
"title":"Child Seat Protection Pads for Cars",
"keywords":"car seat protector, child seat protection pad, baby car seat protector, waterproof seat protector mat"
},

{
"slug":"pet-seat-cover",
"title":"Pet Car Seat Covers",
"keywords":"pet seat cover, dog car seat cover, waterproof dog seat cover, dog hammock car seat cover"
},

{
"slug":"seat-hanging-bag",
"title":"Back Seat Hanging Organizers",
"keywords":"car seat organizer, seat hanging organizer, back seat organizer, car seat storage bag"
},

{
"slug":"storage-box",
"title":"Car Trunk Storage Boxes",
"keywords":"car trunk organizer, trunk storage box, foldable trunk organizer, collapsible trunk organizer"
},

{
"slug":"tool-kit",
"title":"Vehicle Emergency Tool Kits",
"keywords":"car emergency kit, vehicle emergency tool kit, roadside emergency kit, car repair tool kit"
},

{
"slug":"trunk-mat",
"title":"Waterproof Car Trunk Mats",
"keywords":"car trunk mat, trunk liner, waterproof trunk mat, cargo liner, SUV trunk liner"
}

]

template = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<title>{title} | ChampoAuto</title>

<meta name="description" content="High quality {title}. Durable materials designed to protect and organize your car interior for everyday travel.">

<meta name="keywords" content="{keywords}">

<link rel="canonical" href="{site}/products/{slug}/">

<script type="application/ld+json">
{breadcrumb_schema}
</script>

<script type="application/ld+json">
{faq_schema}
</script>

</head>

<body>

<h1>{title}</h1>

<p>
Our {title_lower} are designed to improve vehicle organization and protect important areas of your car interior. 
Made from durable materials and practical designs, these products provide reliable protection and storage solutions 
for daily driving, family trips, and long-distance travel.
</p>

<h2>Featured Products</h2>

<p>
Explore our premium {title_lower} designed for durability, convenience, and everyday vehicle use.
</p>

<h2>Frequently Asked Questions</h2>

<h3>Why use {title_lower}?</h3>

<p>
They help protect your vehicle interior from scratches, dirt, and wear while improving storage convenience.
</p>

<h3>Will these products fit most vehicles?</h3>

<p>
Yes. Most products are designed to fit sedans, SUVs, and trucks.
</p>

</body>

</html>
"""

sitemap_urls = []

for c in categories:

    slug = c["slug"]
    title = c["title"]
    keywords = c["keywords"]

    breadcrumb = {
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
        "item":f"{SITE}/products/"
        },
        {
        "@type":"ListItem",
        "position":3,
        "name":title,
        "item":f"{SITE}/products/{slug}/"
        }
        ]
    }

    faq = {
        "@context":"https://schema.org",
        "@type":"FAQPage",
        "mainEntity":[
        {
        "@type":"Question",
        "name":f"What are {title.lower()}?",
        "acceptedAnswer":{
        "@type":"Answer",
        "text":f"{title} are designed to protect and organize your car interior during daily travel."
        }
        },
        {
        "@type":"Question",
        "name":"Are these products easy to install?",
        "acceptedAnswer":{
        "@type":"Answer",
        "text":"Yes. Most products can be installed quickly without tools."
        }
        }
        ]
    }

    html = template.format(
        title=title,
        title_lower=title.lower(),
        slug=slug,
        keywords=keywords,
        site=SITE,
        breadcrumb_schema=json.dumps(breadcrumb,indent=2),
        faq_schema=json.dumps(faq,indent=2)
    )

    folder = f"{OUT}/{slug}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/index.html"

    with open(path,"w",encoding="utf-8") as f:
        f.write(html)

    sitemap_urls.append(f"{SITE}/products/{slug}/")

    print("Generated:", path)

# 生成 sitemap

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in sitemap_urls:

    sitemap += f"""
<url>
<loc>{url}</loc>
<lastmod>{date.today()}</lastmod>
<changefreq>weekly</changefreq>
<priority>0.8</priority>
</url>
"""

sitemap += "</urlset>"

with open("sitemap_products.xml","w",encoding="utf-8") as f:
    f.write(sitemap)

print("Sitemap generated: sitemap_products.xml")