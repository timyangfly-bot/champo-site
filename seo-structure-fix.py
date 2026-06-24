import os
from bs4 import BeautifulSoup

DOMAIN="https://champoauto.com"

print("Fix robots.txt")

robots="""User-agent: *
Allow: /

Sitemap: {}/sitemap.xml
""".format(DOMAIN)

with open("robots.txt","w",encoding="utf8") as f:
    f.write(robots)

print("robots.txt updated")


for root,dirs,files in os.walk("."):

    for file in files:

        if file.endswith(".html"):

            path=os.path.join(root,file)

            url=path.replace("\\","/").replace("./","")

            with open(path,"r",encoding="utf8",errors="ignore") as f:
                soup=BeautifulSoup(f,"html.parser")


            # canonical
            canonical=soup.new_tag("link")
            canonical.attrs["rel"]="canonical"
            canonical.attrs["href"]=DOMAIN+"/"+url

            if soup.head:
                soup.head.append(canonical)


            # breadcrumb schema
            breadcrumb=f"""
<script type="application/ld+json">
{{
 "@context":"https://schema.org",
 "@type":"BreadcrumbList",
 "itemListElement":[
  {{
   "@type":"ListItem",
   "position":1,
   "name":"Home",
   "item":"{DOMAIN}"
  }},
  {{
   "@type":"ListItem",
   "position":2,
   "name":"Page",
   "item":"{DOMAIN}/{url}"
  }}
 ]
}}
</script>
"""

            soup.head.append(BeautifulSoup(breadcrumb,"html.parser"))


            # FAQ schema only for products
            if "products" in path:

                faq=f"""
<script type="application/ld+json">
{{
 "@context":"https://schema.org",
 "@type":"FAQPage",
 "mainEntity":[
  {{
   "@type":"Question",
   "name":"Do you support OEM?",
   "acceptedAnswer":{{
    "@type":"Answer",
    "text":"Yes, we provide OEM and ODM manufacturing services."
   }}
  }},
  {{
   "@type":"Question",
   "name":"What is your MOQ?",
   "acceptedAnswer":{{
    "@type":"Answer",
    "text":"MOQ depends on the product model. Please contact us for details."
   }}
  }}
 ]
}}
</script>
"""

                soup.body.append(BeautifulSoup(faq,"html.parser"))


            with open(path,"w",encoding="utf8") as f:
                f.write(str(soup))

            print("updated:",path)

print("SEO structure done")