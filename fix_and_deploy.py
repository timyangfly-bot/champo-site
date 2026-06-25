import os
import subprocess

site = r"D:\champo\site"

categories = [
"child-seat-protection-pad",
"pet-seat-cover",
"seat-hanging-bag",
"storage-box",
"tool-kit",
"trunk-mat"
]

print("---- Fixing HTML links ----")

for root, dirs, files in os.walk(site):

    for file in files:

        if not file.endswith(".html"):
            continue

        path = os.path.join(root,file)

        with open(path,"r",encoding="utf-8") as f:
            html = f.read()

        # 修复分类路径
        for cat in categories:

            html = html.replace(
                f'href="/{cat}/"',
                f'href="/products/{cat}/"'
            )

            html = html.replace(
                f'href="{cat}/"',
                f'href="/products/{cat}/"'
            )

        # 修复 CSS 路径
        html = html.replace(
            'href="/css/style.css"',
            'href="../../css/style.css"'
        )

        # 修复图片路径
        html = html.replace(
            'src="/products/images/',
            'src="../../images/products/'
        )

        with open(path,"w",encoding="utf-8") as f:
            f.write(html)

        print("fixed:",path)

print("✅ HTML fixed")


print("---- Git Deploy ----")

try:

    subprocess.run(["git","add","."],cwd=site)

    subprocess.run(["git","commit","-m","auto fix links and layout"],cwd=site)

    subprocess.run(["git","push"],cwd=site)

    print("✅ pushed to github")

except:

    print("⚠ git push failed")


print("Done")