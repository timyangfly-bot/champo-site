import os
from PIL import Image

site = r"D:\champo\site"
img_source = os.path.join(site,"images","products")

css = """
*{margin:0;padding:0;box-sizing:border-box;}

body{
font-family:Arial, Helvetica, sans-serif;
background:#f7f7f7;
color:#333;
}

.container{
width:1200px;
margin:auto;
padding:40px 20px;
}

h1{font-size:32px;margin-bottom:20px;}
h2{font-size:24px;margin-top:40px;margin-bottom:20px;}

.btn{
display:inline-block;
background:#111;
color:#fff;
padding:10px 18px;
text-decoration:none;
border-radius:3px;
}

.category-layout{
display:flex;
gap:40px;
margin-top:30px;
}

.category-sidebar{
width:260px;
background:#fff;
border:1px solid #eee;
padding:20px;
}

.category-menu{
list-style:none;
}

.category-menu li{
border-bottom:1px solid #eee;
}

.category-menu a{
display:block;
padding:10px;
text-decoration:none;
color:#333;
}

.product-grid{
flex:1;
display:grid;
grid-template-columns:repeat(3,1fr);
gap:30px;
}

.product-card{
background:#fff;
border:1px solid #eee;
padding:15px;
text-align:center;
}

.product-card img{
width:100%;
height:220px;
object-fit:cover;
margin-bottom:10px;
}

.product-page{
display:flex;
gap:40px;
margin-top:30px;
}

.product-image{
width:400px;
}

.product-image img{
width:100%;
border:1px solid #eee;
}

.spec-table{
width:100%;
border-collapse:collapse;
margin-top:15px;
}

.spec-table td{
border:1px solid #eee;
padding:10px;
}

@media (max-width:900px){

.category-layout{
flex-direction:column;
}

.product-grid{
grid-template-columns:repeat(2,1fr);
}

.product-page{
flex-direction:column;
}

}

@media (max-width:600px){

.product-grid{
grid-template-columns:1fr;
}

}
"""

css_path = os.path.join(site,"css","style.css")

with open(css_path,"w",encoding="utf-8") as f:
    f.write(css)

print("✅ CSS rebuilt")


for root,dirs,files in os.walk(site):

    for file in files:

        if not file.endswith(".html"):
            continue

        path = os.path.join(root,file)

        with open(path,"r",encoding="utf-8") as f:
            html = f.read()

        html = html.replace(
        'href="/css/style.css"',
        'href="../../css/style.css"'
        )

        html = html.replace(
        'src="/products/images/',
        'src="../../images/products/'
        )

        html = html.replace(
        'href="/products/',
        'href="../'
        )

        with open(path,"w",encoding="utf-8") as f:
            f.write(html)

print("✅ HTML paths fixed")


thumb_dir = os.path.join(img_source,"thumb")

os.makedirs(thumb_dir,exist_ok=True)

for img in os.listdir(img_source):

    if not img.lower().endswith(("jpg","jpeg","png")):
        continue

    path = os.path.join(img_source,img)

    im = Image.open(path)

    webp_name = img.split(".")[0] + ".webp"

    webp_path = os.path.join(img_source,webp_name)

    im.save(webp_path,"WEBP",quality=85)

    thumb = im.copy()
    thumb.thumbnail((400,400))

    thumb_path = os.path.join(thumb_dir,webp_name)

    thumb.save(thumb_path,"WEBP",quality=80)

    print("image optimized:",img)

print("✅ images optimized")