import os

categories = [
"child-seat-protection-pad",
"pet-seat-cover",
"seat-hanging-bag",
"storage-box",
"tool-kit",
"trunk-mat"
]

faq_html = """

<h2>Frequently Asked Questions</h2>

<h3>Can you customize the product size?</h3>
<p>
Yes. Product dimensions can be customized according to customer requirements. 
Our engineering team can also help redesign the product if needed.
</p>

<h3>What materials are available?</h3>
<p>
Common materials include leather and Oxford fabric. Special requirements such 
as waterproof, flame‑retardant and environmentally friendly materials can also 
be customized.
</p>

<h3>What logo customization options are available?</h3>
<p>
We support embroidery, silk screen printing, heat transfer printing and PVC 
rubber logo patches according to your branding requirements.
</p>

<script type="application/ld+json">
{
"@context":"https://schema.org",
"@type":"FAQPage",
"mainEntity":[
{
"@type":"Question",
"name":"Can you customize the product size?",
"acceptedAnswer":{
"@type":"Answer",
"text":"Yes. Product dimensions can be customized according to customer requirements."
}
},
{
"@type":"Question",
"name":"What materials are available?",
"acceptedAnswer":{
"@type":"Answer",
"text":"Common materials include leather and Oxford fabric with optional waterproof or flame retardant features."
}
},
{
"@type":"Question",
"name":"What logo customization options are available?",
"acceptedAnswer":{
"@type":"Answer",
"text":"Logo options include embroidery, silk screen printing, heat transfer printing and PVC rubber patches."
}
}
]
}
</script>

"""

for cat in categories:

    path = f"products/{cat}/index.html"

    if not os.path.exists(path):
        print("skip:",cat)
        continue

    with open(path,"r",encoding="utf-8") as f:
        html = f.read()

    if "Frequently Asked Questions" in html:
        print("already exists:",cat)
        continue

    html = html.replace("</body>", faq_html + "\n</body>")

    with open(path,"w",encoding="utf-8") as f:
        f.write(html)

    print("FAQ added:",cat)

print("✅ FAQ SEO added")