# Foleno product website

Bilingual product, support and privacy pages for Foleno, a CAJ and PDF research reader for Apple devices.

- Chinese: https://szlab-ai.github.io/foleno-site/zh/
- English: https://szlab-ai.github.io/foleno-site/en/
- Support: `/zh/support/` and `/en/support/`
- Privacy: `/zh/privacy/` and `/en/privacy/`

## Build and check

Python 3.10+; no third-party build dependencies.

```sh
python3 scripts/build.py
python3 scripts/check.py
```

The build outputs `dist/`. For a local preview that preserves the Pages project prefix:

```sh
mkdir -p .preview
ln -s ../dist .preview/foleno-site
python3 -m http.server 4321 --directory .preview
```

Open http://localhost:4321/foleno-site/zh/ . Do not commit `.preview/` or `dist/`.

Push to `main` runs `.github/workflows/deploy.yml`, builds and checks the site, then publishes `dist/` through GitHub Actions to GitHub Pages. Pages source must be GitHub Actions. This follows the publication method of the other SZLab product sites.

## Source structure

- `src/content.py`: both languages, feature descriptions, support and privacy policy.
- `scripts/build.py`: shared page shell, sections, SEO metadata, canonical and alternate-language routes.
- `public/assets/site.css`: responsive paper-and-ink visual system.
- `public/assets/site.js`: progressive screenshot tabs with keyboard support; no analytics or storage.
- `public/assets/`: Foleno's existing app icon and actual app screenshots with original demonstration papers.
- `scripts/check.py`: checks the built pages, local links, asset paths, fragments, metadata, localization and public content boundaries.

## Content boundaries

CAJ support is a subset. Do not claim universal compatibility, encryption bypass, paper downloads or database access. AI uses the user's configured service and API key; Foleno does not include hosted models or quotas. iCloud sync supports iPhone, iPad and Mac, subject to Apple Account, connectivity, storage and scheduling.

The public beta is currently offered through the existing TestFlight invitation. The public beta is available on iPhone, iPad and Mac. The site deliberately has no App Store download badge until the listing is live; do not invent ratings, customers, price offers or download numbers. Do not promise a permanent pricing or monetization model.

Update both languages when functionality or data processing changes. Screenshots currently show Chinese UI on both languages, with an explicit caption. See `ASSET-RIGHTS.md`.

No third-party analytics, external fonts, document upload forms, API-key inputs or browser storage are used. GitHub's hosting logs and optional external Apple/model services are described in the privacy policy.
