# CHAMPO V2

The V2 site is generated from `src/data/products.json`.

Run `npm run build` to generate the deployable site in `dist/`. Run `npm run preview` to preview it at `http://127.0.0.1:4173`.

Product URLs follow `/products/{category}/{sku}/`. The build also creates `products.json`, `robots.txt`, and `sitemap.xml`. Sitemap `lastmod` values are derived from the modification date of `src/data/products.json`, so rebuild after approved catalog changes.
