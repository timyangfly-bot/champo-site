import os

categories = [
"child-seat-protection-pad",
"pet-seat-cover",
"seat-hanging-bag",
"storage-box",
"tool-kit",
"trunk-mat"
]

html_block = """

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
For internal support boards, common options include cardboard, PE board and 
MDF board. Different materials offer different advantages in durability, 
weight and cost.
</p>

<p>
Product sizes can be modified based on customer requirements, and completely 
new designs can also be developed.
</p>

<p>
Logo customization methods include embroidery, silk screen printing, 
heat transfer printing and PVC rubber logo patches.
</p>

<p>
Different packaging options are available such as header card, color box 
and wrap card packaging to meet different market needs.
</p>

"""

for cat in categories:

    path = f"products/{cat}/index.html"

    if not os.path.exists(path):
        print("skip:",path)
        continue

    with open(path,"r",encoding="utf-8") as f:
        html = f.read()

    if "Customization Service" in html:
        print("already exists:",cat)
        continue

    html = html.replace("</body>", html_block + "\n</body>")

    with open(path,"w",encoding="utf-8") as f:
        f.write(html)

    print("added to:",cat)

print("✅ customization section added")