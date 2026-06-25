import os

site = r"D:\champo\site\products"

categories = {

"tool-kit":{
"title":"Car Emergency Tool Kits",
"desc":"Professional manufacturer of vehicle emergency tool kits designed for roadside emergencies and vehicle safety."
},

"trunk-mat":{
"title":"Waterproof Car Trunk Mats",
"desc":"Durable waterproof trunk mats designed to protect cargo areas from dirt, water and scratches."
},

"pet-seat-cover":{
"title":"Pet Car Seat Covers",
"desc":"Waterproof dog car seat covers designed to protect car seats from pet hair, scratches and dirt."
},

"storage-box":{
"title":"Car Trunk Storage Boxes",
"desc":"Foldable trunk storage boxes designed to organize tools, groceries and travel gear."
},

"seat-hanging-bag":{
"title":"Car Seat Hanging Organizers",
"desc":"Back seat hanging organizers with multiple storage pockets for tablets, drinks and travel accessories."
},

"child-seat-protection-pad":{
"title":"Child Seat Protection Pads",
"desc":"Car seat protection pads designed to protect vehicle seats from child seat pressure and scratches."
}

}

sidebar = """
<aside class="category-sidebar">

<h3>Product Categories</h3>

<ul class="category-menu">

<li><a href="/products/child-seat-protection-pad/">Child Seat Protection Pad</a></li>
<li><a href="/products/pet-seat-cover/">Pet Seat Cover</a></li>
<li><a href="/products/seat-hanging-bag/">Seat Hanging Bag</a></li>
<li><a href="/products/storage-box/">Storage Box</a></li>
<li><a href="/products/tool-kit/">Tool Kit</a></li>
<li><a href="/products/trunk-mat/">Trunk Mat</a></li>

</ul>

</aside>
"""

customization = """
<h2>Customization Service</h2>

<p>
All CHAMPO automotive accessories support OEM and ODM customization.
Size, materials, internal boards, plastic accessories, logos and packaging
can be customized according to customer requirements.
</p>

<p>
Common fabric options include leather and Oxford fabric. Special requirements
such as waterproof, flame‑retardant and environmentally friendly materials
can also be customized.
</p>

<p>
For internal support boards, common options include cardboard, PE board and MDF board.
Different materials offer different advantages in durability, weight and cost.
</p>

<p>
Product sizes can be modified based on customer requirements and new designs can also be developed.
Logo customization methods include embroidery, silk screen printing,
heat transfer printing and PVC rubber logo patches.
</p>
"""

faq = """
<h2>Frequently Asked Questions</h2>

<h3>Can you customize the product size?</h3>
<p>Yes. Product dimensions can be customized according to customer requirements.</p>

<h3>What materials are available?</h3>
<p>Common materials include leather and Oxford fabric with optional waterproof
and flame‑retardant features.</p>

<h3>What logo customization options are available?</h3>
<p>Logo options include embroidery, silk screen printing,
heat transfer printing and PVC rubber patches.</p>
"""

for slug,data in categories.items():

    folder = os.path.join(site,slug)

    os.makedirs(folder,exist_ok=True)

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>{data['title']} | CHAMPO</title>

<meta name="description" content="{data['desc']}">

<link rel="stylesheet" href="/css/style.css">

</head>

<body>

<div class="container">

<h1>{data['title']}</h1>

<p>{data['desc']}</p>

<div class="category-layout">

{sidebar}

<main class="product-grid">

<!-- PRODUCT CARDS AUTO GENERATED -->

</main>

</div>

{customization}

{faq}

</div>

</body>

</html>
"""

    file = os.path.join(folder,"index.html")

    with open(file,"w",encoding="utf-8") as f:
        f.write(html)

    print("category page created:",slug)

print("✅ category templates generated")