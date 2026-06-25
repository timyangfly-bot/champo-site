import os

ROOT="."

sections={
    "Home":[],
    "Categories":[],
    "Products":[],
    "Blog":[],
    "Custom":[],
    "Other":[]
}

for root,dirs,files in os.walk(ROOT):

    for f in files:

        if f.endswith(".html"):

            path=os.path.join(root,f)
            url=path.replace("\\","/").replace("./","")

            if url=="index.html":
                sections["Home"].append(url)

            elif url.startswith("categories/"):
                sections["Categories"].append(url)

            elif url.startswith("products/"):
                sections["Products"].append(url)

            elif url.startswith("blog/"):
                sections["Blog"].append(url)

            elif url.startswith("custom/"):
                sections["Custom"].append(url)

            else:
                sections["Other"].append(url)


with open("SITE_MAP.md","w",encoding="utf8") as f:

    f.write("# SITE MAP\n\n")

    for k,v in sections.items():

        if not v:
            continue

        f.write("## "+k+"\n\n")

        for item in sorted(v):
            f.write("- "+item+"\n")

        f.write("\n")


print("SITE_MAP.md generated")