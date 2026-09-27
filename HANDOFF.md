# CHAMPO Website Handoff

## Project location and Git state

- Code root: `C:\Users\timya\Documents\Codex\2026-09-03\new-chat-2\work\champo-v2`
- Current branch: `redesign/v2` (tracks `origin/redesign/v2`)
- Checked on: 2026-09-26 (Asia/Shanghai)
- Git status at handoff: clean (`git status --short --branch` reported `## redesign/v2...origin/redesign/v2`).
- Latest commit observed: `c92fe22` — `Enrich product sourcing content and schema`.

## Project goal

Build and maintain CHAMPO's English B2B automotive accessories website, covering product catalogs and detail pages, OEM/ODM and factory information, buyer inquiry paths, SEO landing pages, analytics, and deployable static files for `https://www.champoauto.com/`.

## Completed work verified in the current project files

- `src/data/products.json` is the product data source; `scripts/build-v2.mjs` generates the deployable static site under `dist/`.
- The homepage, product/category pages, company and capability content, and supporting buyer information are present in the generator and build output.
- Three product-line manufacturer landing pages are included in the generated-site configuration and current sitemap:
  - `/pet-seat-cover-manufacturer/`
  - `/car-trunk-organizer-manufacturer/`
  - `/automotive-tool-bag-manufacturer/`
- The manufacturer pages contain product-specific capabilities and stated daily capacities: pet seat covers 1,000 sets/day, trunk organizers 1,000 pcs/day, and automotive tool bags 3,000 pcs/day. These are website claims sourced from project content, not independently audited production figures.
- The site generator includes GA4 measurement ID `G-7S6Z52Q2XQ`, GTM container `GTM-TCTPFSLG`, and floating WhatsApp/WeChat contact UI. The contact values are read from `src/data/products.json`.
- Generated `dist/index.html` visibly contains both analytics tags and the contact UI. `dist/robots.txt` points crawlers to the sitemap.
- Generated `dist/sitemap.xml` includes the homepage, three manufacturer landing pages, three buyer guides, three primary product category URLs, and product detail URLs. Its `<lastmod>` values are derived from the modification date of `src/data/products.json` during each build.
- Three B2B buyer guides were added to the generator and sitemap: `/choose-car-trunk-organizer-manufacturer/`, `/oem-pet-car-seat-cover-specification-checklist/`, and `/private-label-automotive-tool-bags-production-guide/`. They link to the relevant manufacturer programs and include Article schema.
- `README-V2.md` documents the basic build and preview commands.

## Work recorded in prior session, with verification limits

The current Search Console session confirmed that `https://www.champoauto.com/sitemap.xml` is successful, was read on 2026-09-26, and contains 80 discovered pages. The overview currently shows 31 indexed pages and 285 not indexed pages.

URL Inspection was rechecked for all three manufacturer landing pages. Each is currently “Discovered – currently not indexed” and references the current sitemap. An indexing request was attempted for the pet-seat-cover page, but Google returned “There was a problem submitting your indexing request. Please try again later” and displayed reCAPTCHA protection. The remaining two requests were not submitted after the same temporary failure appeared.

The Search Console action is incomplete because Google requires an interactive reCAPTCHA/temporary retry. Do not treat the failed request as evidence that the pages are blocked from crawling.

## Outstanding items

- After several hours or the next day, retry one manufacturer URL at a time in URL Inspection. If Google shows reCAPTCHA, complete it manually in the browser before clicking the request button. Record the exact result; do not repeatedly submit all three URLs in one session.
- Deployed the new buyer-guide pages to `origin/main` at commit `d9f5816`; live browser verification confirmed all three guide URLs return their intended pages. Reopen Search Console sitemap reporting to confirm Google has reread the new 84-URL sitemap.
- Confirmed on 2026-09-26 that the live homepage and all three manufacturer landing pages serve the current V2 content: 68 catalog products, current manufacturer copy/capacity claims, navigation links and GA4 measurement ID `G-7S6Z52Q2XQ`. Direct browser access to `robots.txt` and `sitemap.xml` was blocked by the browser client, but Search Console successfully read the live sitemap and reported 80 discovered pages.
- FormSubmit delivery and GA4 `generate_lead` tracking were verified in an earlier session according to the user; do not repeat unless a deployment changes the form or analytics code.
- Rebuild after approved catalog changes so sitemap `<lastmod>` values reflect the current `src/data/products.json` modification date.
- `robots.txt.txt` exists in the source root while the build generates the deployable `dist/robots.txt`; ensure deployments publish `dist/robots.txt`, not the oddly named source file.

## Important decisions and conventions

- Treat `work/champo-v2` as the active V2 source project. `work/champo-deploy` is a separate deploy/output snapshot and should not be assumed to be the source of truth.
- Product records live in `src/data/products.json`; modify source data/templates and rebuild rather than hand-editing generated pages under `dist/`.
- Static site output is `dist/`; product routes use `/products/{category}/{sku}/`.
- Preserve anonymous descriptions of retail/customer relationships; do not identify named retailers in public case studies without explicit approval.
- The website is English-facing. Factory and capacity details are marketing claims that should be kept consistent with current approved company information.

## Start, build, and validation commands

Run these from the code root:

```powershell
npm run build
npm run preview
```

The preview server listens at `http://127.0.0.1:4173` and serves `dist/`.

The repository also contains a link/placeholder checker:

```powershell
node scripts/check-v2.mjs
```

Validation status for this handoff: direct Node execution of `scripts/build-v2.mjs` completed successfully; `scripts/check-v2.mjs` reported 86 HTML pages, 0 broken links and 0 placeholders. The `npm` command was unavailable on the current PATH, and the preview server was not started in this task.

## Known issues / cautions

- Sitemap dates follow the product-source file modification date; rebuild after catalog edits before deployment.
- Search Console's indexing-request interface returned a temporary submission error and reCAPTCHA during the 2026-09-26 retry. Sitemap discovery is successful, but an indexing request is not a guarantee of indexing.
- Analytics tags being present in HTML does not establish that GA4 is receiving data or that GTM tags are published/configured correctly.
- The local preview server only serves generated `dist/`; rebuild after source edits before expecting preview changes.
- This handoff does not assert that current local output exactly matches the live deployment.

## Conversation handoff and next task

- The current Codex task is named `网站开发` and remains the main conversation for overall CHAMPO website development, deployment and release coordination.
- SEO planning and future SEO automation should be handled in a separate child task/worktree when created; do not rename or repurpose this main website-development task.
- The next isolated SEO implementation task is to create `scripts/seo-audit.mjs` and an `npm run seo:audit` command. It should audit generated HTML metadata, internal links, sitemap and robots.txt without deploying or submitting indexing requests.
- This main task is being archived after this handoff; resume the SEO implementation from the separate child task when available.
