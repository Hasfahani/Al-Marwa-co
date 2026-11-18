# Deploy AL MARWA CO on Cloudflare Pages

Prepared for the existing production domain **https://al-marwaco.com/**. These files do not create a Cloudflare project, change DNS, or deploy the website.

## Ready-to-upload package

Use `artifacts/al-marwa-cloudflare.zip`, or upload the **contents** of `dist/` as your Pages assets. `index.html`, `_headers`, `_redirects`, `robots.txt`, `sitemap.xml` and `404.html` must be at the upload root. Do not upload the repository root or wrap `dist/` inside another directory.

The old download name `artifacts/al-marwa-site.zip` is an identical copy of the new Cloudflare package. Earlier packages are superseded.

Rebuild and check with:

```text
python scripts/package_site.py
python scripts/test_cloudflare.py
```

The package includes referenced public assets and licenses. Unrelated documents in `videos/`, internal scripts, Git metadata and planning documents are excluded. Local originals are untouched.

## Cloudflare Pages settings

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command, for a Git-connected Pages project | `python3 scripts/build_cloudflare.py` |
| Build output directory | `dist` |
| Direct Upload | Upload `al-marwa-cloudflare.zip` or the contents of `dist/` |
| Production custom domain | `al-marwaco.com` |

Choose Git integration if you want Cloudflare to rebuild automatically from the production repository. Direct Upload accepts the prepared ZIP. Cloudflare documents that a Direct Upload project cannot later be converted to Git integration; that would require a new project.

## Custom domain and canonical host

1. Add `al-marwaco.com` under the Pages project's **Custom domains** and complete Cloudflare's DNS/domain activation steps.
2. Enable **Always Use HTTPS** for the production zone.
3. Configure a Cloudflare **Bulk Redirect** from `www.al-marwaco.com` to `https://al-marwaco.com`, status **301**, with **Preserve query string**, **Subpath matching**, and **Preserve path suffix** enabled. Complete the `www` DNS setup described in Cloudflare's guide.

The www-to-apex redirect is an account/zone setting; Pages `_redirects` does not implement domain-level redirects. Do not assume uploading the ZIP configures it.

## What the build already handles

- Published canonicals, internal links, language alternates, structured-data URLs, social URLs, AI summary links and sitemap URLs use extensionless paths, such as `/contact` and `/sea-freight-lebanon`.
- Old `.html` URLs and known trailing-slash aliases redirect permanently to those canonical paths. Quote query parameters are preserved.
- CSS, scripts, fonts, images and videos have content hashes in their filenames, allowing long browser caching without making the next release stale.
- HTML retains Pages' revalidation behavior. Leave whole-site custom cache rules off; fingerprinted assets already carry immutable caching headers.
- Pages aliases and branch previews receive `X-Robots-Tag: noindex`; production content remains indexable.
- The custom `404.html` is included. Unknown paths return a real 404 instead of the homepage, with root-relative assets that work at nested URLs.
- Response headers include content-type protection, referrer policy, frame restrictions and a policy that permits the existing FormSubmit form action. Inline site scripts and styles remain supported.
- Existing small PNG favicons are used instead of redundant full-size JPEG icons. Service footage is loaded only when a visitor chooses to play it.

The editable source keeps `.html` links for normal file-based previews. The Cloudflare build produces the clean published URLs; upload the built output.

## Local Pages runtime check

In one terminal:

```text
npx wrangler@4.163.0 pages dev dist --ip 127.0.0.1 --port 8788 --compatibility-date=2026-11-16 --show-interactive-dev-session=false
```

In another:

```text
python scripts/test_cloudflare.py --base-url http://127.0.0.1:8788
```

This checks every canonical page, old-page redirects, retained quote parameters, missing-page status, cache/security headers and preview noindex behavior. It does not submit a quote.

## After deployment

Run:

```text
python scripts/test_cloudflare.py --base-url https://al-marwaco.com --check-hosts
```

Optionally add `--pages-url https://YOUR-ACTUAL-PROJECT.pages.dev` to check that the actual Pages alias stays out of search. Replace the placeholder with the project's real URL; no project name has been assumed.

Then inspect the homepage and representative English/Arabic pages in a mobile browser, measure performance/Core Web Vitals on the live deployment, and submit `https://al-marwaco.com/sitemap.xml` through the business's verified search accounts. Confirm one real form submission is received by the company before treating email delivery as verified. No form was submitted during this work.

## Official Cloudflare references

- [Static HTML deployment](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/)
- [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Serving pages and clean URLs](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- [Headers](https://developers.cloudflare.com/pages/configuration/headers/)
- [Redirects](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Redirect www to the apex domain](https://developers.cloudflare.com/pages/how-to/www-redirect/)
