import os

site = r"D:\champo\site"
products = os.path.join(site,"products")

# 读取首页
with open(os.path.join(site,"index.html"),"r",encoding="utf-8") as f:
    home = f.read()

header = home.split("<header")[1].split("</header>")[0]
header = "<header" + header + "</header>"

footer = home.split("<footer")[1].split("</footer>")[0]
footer = "<footer" + footer + "</footer>"

for root, dirs, files in os.walk(products):

    for file in files:

        if file != "index.html":
            continue

        path = os.path.join(root,file)

        with open(path,"r",encoding="utf-8") as f:
            html = f.read()

        # 提取主体内容
        if "<body>" in html:
            content = html.split("<body>")[1].split("</body>")[0]
        else:
            content = html

        new_html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">
<link rel="stylesheet" href="/css/style.css">

</head>

<body>

{header}

<div class="container">

{content}

</div>

{footer}

</body>
</html>
"""

        with open(path,"w",encoding="utf-8") as f:
            f.write(new_html)

        print("repaired:",path)

print("✅ category pages rebuilt")