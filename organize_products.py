import os
import shutil

site = r"D:\champo\site\products"
generated = os.path.join(site,"generated")

# 产品分类规则
rules = {
"tk":"tool-kit",
"tm":"trunk-mat",
"sc":"pet-seat-cover",
"sb":"storage-box",
"sh":"seat-hanging-bag",
"cs":"child-seat-protection-pad"
}

# 移动产品页面
for file in os.listdir(generated):

    if not file.endswith(".html"):
        continue

    prefix = file.split("-")[0]

    if prefix not in rules:
        print("skip:",file)
        continue

    category = rules[prefix]

    target_dir = os.path.join(site,category)

    os.makedirs(target_dir,exist_ok=True)

    src = os.path.join(generated,file)
    dst = os.path.join(target_dir,file)

    shutil.move(src,dst)

    print("moved:",file,"→",category)


# 生成分类产品列表
for category in rules.values():

    folder = os.path.join(site,category)

    if not os.path.exists(folder):
        continue

    cards = ""

    for file in os.listdir(folder):

        if not file.endswith(".html"):
            continue

        model = file.replace(".html","").upper()

        cards += f"""
<div class="product-card">

<img src="/products/images/{model.lower()}.webp">

<h3>{model}</h3>

<a class="btn" href="/products/{category}/{file}">
View Details
</a>

</div>
"""

    index_file = os.path.join(folder,"product-list.html")

    with open(index_file,"w",encoding="utf-8") as f:
        f.write(cards)

    print("list created:",category)

print("✅ products organized")