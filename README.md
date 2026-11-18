# AL MARWA CO business freight website

Static website for the freight business based on Khalde Highway, Lebanon, since 1997.

## Commercial scope

- Main audience: importers, exporters, wholesalers, manufacturers and project teams moving substantial business loads.
- Primary services: worldwide FCL, full truckloads (FTL) between Lebanon and Ukraine, Jordan, Iraq, the UAE, Turkey, the United Kingdom and China (mainly imports), machinery and large commercial cargo.
- Not offered: parcels, courier, household moves or personal effects.
- LCL: only from Ukraine, Jordan, Iraq, UAE, Turkey, the United Kingdom and China into Lebanon, subject to shipment acceptance and route confirmation.
- No invented rates, transit guarantees, reviews, certifications, foreign offices or project results.

## Preview

Serve the repository root using `python -m http.server 8765 --bind 127.0.0.1`, then open `http://127.0.0.1:8765/`. No Node dependency installation or framework build is required.

## Update content

Existing core pages are edited directly. Arabic route pages live in `scripts/routes_ar.py`. The route, service, industry and planning pages use content from `scripts/build_freight_pages.py` and `scripts/business_content.py`. Shared navigation is defined in `scripts/site_navigation.py`.

After changing those sources, run:

```text
python scripts/sync_site.py
```

This renders the dependent pages and updates the shared navigation, discovery links, Arabic FCL language alternates, sitemap and optional AI-readable summary. Edit the generator content instead of editing a generated page alone.

## Validate

```text
python scripts/test_site.py
node scripts/test_freight_tools.js
node scripts/test_quote_context.js
node --check assets/js/freight-tools.js
node --check assets/js/main.js
```

The checks cover metadata, business identity, schema, visible FAQ answers, local assets, sitemap coverage, language alternates, internal links, page reachability, calculator units and weights, LCL scope, and temporary quote context.

## Prepare deployment

The production target is now **Cloudflare Pages**. Run `python scripts/package_site.py`, then `python scripts/test_cloudflare.py`.

Upload `artifacts/al-marwa-cloudflare.zip` or the contents of `dist/`. The old `al-marwa-site.zip` download name is updated to the identical Cloudflare package. The referenced-files build excludes unrelated PDFs, Git metadata, source scripts, internal documents and GitHub-specific hosting files. Original local files are untouched.

For Git-connected Cloudflare Pages, use framework preset **None**, build command `python3 scripts/build_cloudflare.py`, and output directory **dist**. The build transforms published page links and SEO URLs to Cloudflare's extensionless paths, fingerprints referenced assets, and includes permanent path redirects, response headers, preview noindex rules and a true custom 404.

See [the Cloudflare deployment guide](cloudflare/DEPLOY.md) for custom-domain activation, HTTPS, the account-level www redirect, local runtime checks and post-deployment verification. No Cloudflare account settings or live website have been changed. The prepared CI workflow checks and packages changes; it does not deploy them.

## Tools, forms and measurement

- The freight planner uses the published service scope; it does not check live carrier availability.
- The cargo calculator calculates external packed volume and supplied gross weights, not container fit or freight prices.
- Calculator details transfer to the quote form only after the visitor chooses that action, using a temporary session draft consumed on the contact page. Drafts older than 30 minutes are ignored.
- Forms continue to submit through FormSubmit to the existing company email. Email activation/delivery must be checked by the business; no test inquiry was sent.
- `almarwa:lead` browser events and an existing `dataLayer`, if one is configured later, receive `freight_contact_click` and `freight_quote_submission_attempt`. Payloads contain the public page path, contact method and service category; they contain no name, email, phone, cargo dimensions or message. A submission attempt is not a confirmed received lead.
- No analytics provider or invented measurement account ID has been added. Follow the chosen provider's setup before claiming that conversion tracking is active.

## Search and AI discovery

The website supplies useful visible content, crawlable links, stable business facts, page/service/article/tool schema, reciprocal language alternates and an XML sitemap. `llms.txt` is an optional factual summary, not an instruction to rank or recommend the company. Search indexing, AI citations and rankings are not guaranteed.

No Google Business Profile exists yet, as confirmed by the owner. `business-profile-draft.md` contains a factual setup draft for later use. Creating the profile, verifying ownership and publishing reviews or other external business information remain separate account tasks.

## Credits

The original template is Forty by HTML5 UP. Preserve the attribution and licensing terms in `README.txt` and `LICENSE.txt`; font licenses are included under `assets/webfonts/`.
