# AL MARWA CO SEO and AI Search Launch Checklist

## Source audit — 15 November 2026

- **Local website: 36 public, indexable pages**, plus the custom 404 page.
- Added 12 pages: a shipping-route hub, seven distinct origin-to-Lebanon guides, full truckloads, machinery/large cargo, selected-origin LCL, and worldwide FCL exports from Lebanon.
- Retained `sea-freight-lebanon.html` as the primary worldwide FCL landing page instead of adding a competing page for the same service.
- Connected the new pages through the homepage, services, primary navigation, related-service links, sitemap, and optional `llms.txt` summary.
- Each new page has its own title, description, canonical, social preview, business service data, breadcrumbs, and visible questions matching its FAQ structured data.
- Route-specific quote links carry service, origin, and destination into the existing B2B contact form. The forms still use the existing FormSubmit destination; no test inquiry was sent.
- Checks passed: all 36 public pages, exact sitemap coverage, homepage reachability, section links, local assets, unique metadata, JSON-LD, FAQ visibility, and business identity. Calculator/service logic, JavaScript syntax and quote-context checks also passed.
- Visual browser verification is incomplete because the browser connection is unavailable.

### Further B2B and planning expansion

- Added customer-specific pages for importers/wholesalers, manufacturers/industrial teams, and project/construction teams.
- Added a planning resource hub, a service-scope planner, a packed-cargo volume calculator, and an FCL quote cost guide.
- Added a native Arabic FCL landing page and reciprocal English/German/Arabic sea-freight alternates in page headers and the sitemap.
- Added a downloadable business freight quote checklist and explicit optional cargo-category/container fields in the contact form.
- The calculator supports cm, m, mm and inches, multiple package types, supplied gross weights, a text brief download and an explicit temporary transfer to the quote form. It does not price freight or confirm container fit.
- Planner tests verify that LCL is limited to the seven selected import origins into Lebanon. Exports and other origins do not receive a worldwide LCL recommendation.
- Measurement hooks expose non-personal contact-click events and quote-submission attempts for a future analytics setup. No analytics provider is connected, and a form attempt is not counted as a confirmed received lead.
- Added local logic tests, a source validation workflow and a script that packages only public website files for deployment. The workflow has not run on GitHub because repository access remains unavailable.
- Removed unused hidden homepage example sections and simplified desktop navigation into services, routes, business customers, resources and company information, with language links in the menu.
- No certifications, customer logos, ratings, project outcomes, fixed transit times, freight prices or foreign offices have been invented.

New expansion pages:

- [Commercial imports and wholesale freight](commercial-imports-lebanon.html)
- [Manufacturing and industrial freight](industrial-logistics-lebanon.html)
- [Project cargo](project-cargo-lebanon.html)
- [Planning tools and resources](freight-resources-lebanon.html)
- [Business freight planner](freight-planner-lebanon.html)
- [Cargo volume calculator](cargo-volume-calculator.html)
- [Container quote cost guide](container-shipping-costs-lebanon.html)
- [Native Arabic FCL service page](fcl-shipping-lebanon-ar.html)

### Public-host observations requiring deployment review

Read-only HTTP checks on 15 November 2026 received:

| Public URL | Observed response |
| --- | --- |
| `https://al-marwaco.com/` | HTTP 200, one byte containing a newline; no website content in the response |
| `https://www.al-marwaco.com/` | Resolved to the same homepage response |
| `https://al-marwaco.com/robots.txt` | HTTP 404 |
| `https://al-marwaco.com/sitemap.xml` | HTTP 404 |

The response reported `Server: GitHub.com`. The read-only GitHub Pages settings request for the configured origin repository returned HTTP 404. Subsequent repository metadata checks through both the connected GitHub tool and the existing GitHub CLI session returned HTTP 404 for `Hasfahani/Al-Marwa-co` and `fixwerk/Al-Marwa-co`. The publishing source and settings therefore could not be verified with available access. This does not establish whether the cause is repository access, repository availability, publishing configuration, or deployed content.

The new source has **not been published**. Verify the intended production repository, branch and directory, deploy the complete site, and repeat public checks before treating the site as launched. Missing robots.txt alone is not proof that indexing is blocked; the near-empty homepage response is the more significant content issue.

The owner confirmed that **Hasfahani remains the production repository owner**. The available CLI is authenticated as `fixwerk`; no authenticated Hasfahani CLI account was listed. The installed GitHub connector also returned HTTP 404 for the production repository. Publishing requires a connection with access to `Hasfahani/Al-Marwa-co`; no replacement owner, domain or host was selected.

A verified local deployment archive is prepared at `artifacts/al-marwa-site.zip`, with 147 public files and a SHA-256 release manifest beside it. It contains the complete static site and public assets; Git metadata, internal planning documents and source-generation scripts are excluded. The archive has not been uploaded or deployed.

### Account-side work still outstanding

- Verify the production deployment and inspect the published pages in Google Search Console and Bing Webmaster Tools; submit the sitemap.
- The owner confirmed that no Google Business Profile exists yet and plans to create one later. A factual description and service-list draft is prepared in `business-profile-draft.md`; no profile has been created or claimed.
- Configure the business's chosen analytics and conversion measurement if desired; no account identifiers were supplied or fabricated.
- Monitor qualified B2B inquiries, actual indexed pages and search queries after launch. No crawl, ranking, traffic, AI citation or lead outcome has been verified by these source checks.

### New business service and route pages

- [Shipping route hub](shipping-routes-lebanon.html)
- [China to Lebanon](china-to-lebanon-shipping.html)
- [Turkey to Lebanon](turkey-to-lebanon-shipping.html)
- [UAE to Lebanon](uae-to-lebanon-shipping.html)
- [Jordan to Lebanon](jordan-to-lebanon-shipping.html)
- [Iraq to Lebanon](iraq-to-lebanon-shipping.html)
- [United Kingdom to Lebanon](uk-to-lebanon-shipping.html)
- [Ukraine to Lebanon](ukraine-to-lebanon-shipping.html)
- [Full truckloads](full-truckload-lebanon.html)
- [Machinery and large cargo](heavy-equipment-shipping-lebanon.html)
- [Selected-origin LCL imports](lcl-shipping-lebanon.html)
- [Worldwide FCL exports from Lebanon](export-shipping-lebanon.html)

## Confirmed business focus
- Main audience: importers, exporters, wholesalers, manufacturers, and project teams moving substantial business cargo.
- Primary offer: FCL worldwide, full truckloads on suitable road routes, machinery and large cargo.
- LCL: only from Ukraine, Jordan, Iraq, UAE, Turkey, the United Kingdom, and China into Lebanon.
- Other origins: review large items as FCL shipments; do not advertise worldwide LCL.
- Quote forms collect company, shipment requirement, load size, route, and contact details.

## Implemented in the site
- Connected `LocalBusiness`, `WebSite`, page, service, article, and breadcrumb structured data using stable business identifiers.
- Added visible company facts, local coverage, shipment use cases, contact details, and freight resource links on the homepage.
- Aligned FAQ structured data with the visible questions and answers, including a visible FAQ on the services page.
- Explicitly allowed `OAI-SearchBot`, `PerplexityBot`, and `Claude-SearchBot` in `robots.txt`; general search crawler access remains open.
- Expanded the optional `llms.txt` summary with relevant services, source pages, quote information, and shipment-specific limitations.
- Kept English, Arabic, and German page language annotations and included the English/Arabic Beirut alternates in the sitemap.

These changes are local source changes until deployed to the existing production host.

## 1) Google Search Console
- Add property: https://al-marwaco.com/
- Submit sitemap: https://al-marwaco.com/sitemap.xml
- Request indexing for:
  - https://al-marwaco.com/
  - https://al-marwaco.com/about.html
  - https://al-marwaco.com/services.html
  - https://al-marwaco.com/contact.html
  - https://al-marwaco.com/freight-forwarding-lebanon.html
  - https://al-marwaco.com/spedition-libanon-deutschland.html
  - https://al-marwaco.com/seefracht-deutschland-libanon.html
  - https://al-marwaco.com/luftfracht-deutschland-libanon.html
  - https://al-marwaco.com/freight-forwarding-beirut.html
  - https://al-marwaco.com/freight-forwarding-beirut-ar.html
  - https://al-marwaco.com/beirut-freight-guide.html
  - https://al-marwaco.com/international-shipping.html
- Include the new service, route, customer and resource URLs after they are deployed; the local sitemap contains all 36 indexable pages.
- After deployment, inspect each submitted URL and confirm that Google selected the published canonical.
- Inspect the English and German B2B pages and confirm Google recognizes the reciprocal `en-LB`, `de-DE`, and `x-default` hreflang annotations.
- Review the Core Web Vitals report after enough real-user data is available.

## 2) Google Business Profile (NAP Consistency)
Use this exact business data everywhere:
- Business name: AL MARWA CO
- Category: Freight forwarding service
- Website: https://al-marwaco.com/
- Phone: +961 70 099978
- Email: info@al-marwaco.com
- Address: Khalde Highway, Lebanon
- Service areas: Beirut, Greater Beirut, and Lebanon (only where genuinely served)

Suggested profile description:
AL MARWA CO is a B2B freight forwarding company based in Khalde, Lebanon, since 1997. We specialize in FCL worldwide, full truckloads on suitable road routes, machinery, and large commercial cargo. LCL imports into Lebanon are available from Ukraine, Jordan, Iraq, UAE, Turkey, the United Kingdom, and China, subject to route confirmation. We coordinate FCL exports from Lebanon worldwide.

Profile completion:
- Verify ownership.
- Add accurate business hours and keep holiday hours current.
- Use the primary category that most precisely matches the real business.
- Add original office, team, equipment, and shipment-operation photos.
- Add each genuine service offered; do not add services only to capture keywords.
- Link the website and use the same name, phone, and address shown on the site.
- Ask completed customers for honest Google reviews with the direct review link. Never offer incentives or script the review.
- Reply helpfully to every review without disclosing shipment or customer details.

## 3) Backlink Foundations
Create business profiles on relevant directories and logistics associations using identical NAP details.
Priority profile targets:
- Google Business Profile
- LinkedIn Company Page
- Relevant local business directories in Lebanon
- Logistics and freight industry directories or associations where membership is genuine

Rules:
- Prefer a small number of accurate, reputable listings over bulk directory submissions.
- Do not buy links, trade links at scale, or claim memberships, offices, reviews, or certifications that cannot be verified.
- Correct inconsistent company names, addresses, and phone numbers in existing listings.

## 4) Content Publishing Rhythm
- Publish a page only when it adds first-hand expertise, a genuinely useful guide, or a real service/route that the company supports.
- Interlink each new page from services and homepage.
- Update sitemap.xml whenever a page is added.
- Refresh operational guides when document, route, or service information changes.
- Add real project examples only after removing confidential customer information and confirming the facts.

## 5) KPI Tracking (Monthly)
- Branded clicks
- Non-branded clicks
- Top landing pages by impressions
- Top queries by CTR
- English B2B queries such as FCL shipping Lebanon, full container load Lebanon, full truckload Lebanon, machinery shipping Lebanon, China to Lebanon shipping, and UK to Lebanon FCL
- German B2B queries such as Spedition Libanon, Seefracht Libanon, Luftfracht Libanon, and Transport Deutschland Libanon
- Contact form submissions
- WhatsApp and phone leads attributed to organic search
- Google Business Profile calls, website clicks, and direction requests
- Indexed pages and crawl issues
- Core Web Vitals status

## 6) Important Expectation
No website change can guarantee a number-one ranking. Local visibility is mainly built through relevance, distance, and prominence. The website now improves relevance and technical clarity; the Business Profile, authentic reviews, reputable mentions, and consistent real-world business information build the off-site signals that code cannot create.

## 7) AI assistant discovery after deployment
- Fetch `/robots.txt`, `/sitemap.xml`, `/llms.txt`, and the key landing pages from the public domain and confirm successful responses without login or bot challenges.
- Check hosting/CDN rules and logs for blocked search crawlers. A robots allowance does not override a firewall or CAPTCHA. Verify bot identity using each provider's current guidance before changing firewall rules.
- Submit the sitemap to Bing Webmaster Tools as well as Google Search Console, using the existing verified business accounts.
- Confirm business name, phone, location, and service facts match the genuine Business Profile and other established business listings.
- Publish original project examples with verified route, cargo, scope, and outcome details when the business can supply them and customer confidentiality allows publication.
- Track AI search referrals and qualified inquiries where analytics is available. Record sample questions, dates, citations, and factual accuracy when checking AI answers; answers can vary and a single check does not prove inclusion or exclusion.
- Suggested questions to monitor: “FCL shipping company in Lebanon”, “full truckload freight Lebanon for businesses”, “machinery shipping to Lebanon”, “LCL from China to Lebanon”, and “Spedition Deutschland Libanon für Unternehmen”.
- AI recommendations, citations, crawling, and indexing are not guaranteed. Search access, factual content, and trustworthy external business references support discovery; `llms.txt` is an optional summary, not a ranking or recommendation instruction.
- FAQ markup describes page content. Do not assume a freight company is eligible for Google's FAQ rich results.

## Reference documentation
- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features): ordinary SEO, visible text, internal links, crawl access, and structured data that matches the page remain relevant; special AI files or markup are not required.
- [OpenAI: crawler documentation](https://developers.openai.com/api/docs/bots): `OAI-SearchBot` governs search discovery; `GPTBot` is a separate training crawler.
- [Perplexity: crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers): `PerplexityBot` supports search discovery, with additional hosting/firewall considerations.
- [Anthropic: crawler documentation](https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler): `Claude-SearchBot` supports search indexing.
