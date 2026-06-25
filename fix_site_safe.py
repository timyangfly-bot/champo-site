import os

site = r"D:\champo\site"

categories = [
"child-seat-protection-pad",
"pet-seat-cover",
"seat-hanging-bag",
"storage-box",
"tool-kit",
"trunk-mat"
]

for root, dirs, files in os.walk(site):

    for file in files:

        if not file.endswith(".html"):
            continue

        path = os.path.join(root,file)

        with open(path,"r",encoding="utf-8") as f:
            html = f.read()

        # 修复首页CSS
        if "index.html" in path and "products" not in path:

            html = html.replace(
                'href="../../css/style.css"',
                'href="/css/style.css"'
            )

        # 修复分类页CSS
        if "products" in path:

            html = html.replace(
                'href="/css/style.css"',
                'href="../../css/style.css"'
            )

        # 修复分类链接
        for cat in categories:

            html = html.replace(
                f'href="/{cat}/"',
                f'href="/products/{cat}/"'
            )

        with open(path,"w",encoding="utf-8") as f:
            f.write(html)

        print("fixed:",path)

print("site repaired")