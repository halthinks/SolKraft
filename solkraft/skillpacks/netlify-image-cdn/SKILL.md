---
name: netlify-image-cdn
description: Guide for using Netlify Image CDN for image optimization and transformation. Use when serving optimized images, creating responsive image markup, setting up user-uploaded image pipelines, or configuring image transformations. Covers the /.netlify/images endpoint, query parameters, remote image allowlisting, clean URL rewrites, and composing uploads with Functions + Blobs.
---

<!-- solkraft-doc-sync: contract-aware-v1 | semantic-proof-373k | 2026-10 -->

# Netlify Image CDN

Every Netlify site has a built-in `/.netlify/images` endpoint for on-the-fly image transformation. No configuration required for local images.

## Basic Usage

```html
<img src="/.netlify/images?url=/photo.jpg&w=800&h=600&fit=cover&q=80" />
```

## Query Parameters

| Param | Description | Values |
|---|---|---|
| `url` | Source image path (required) | Relative path or absolute URL |
| `w` | Width in pixels | Any positive integer |
| `h` | Height in pixels | Any positive integer |
| `fit` | Resize behavior | `contain` (default), `cover`, `fill` |
| `position` | Crop alignment (with `cover`) | `center` (default), `top`, `bottom`, `left`, `right` |
| `fm` | Output format | `avif`, `webp`, `jpg`, `png`, `gif`, `blurhash` |
| `q` | Quality (lossy formats) | 1-100 (default: 75) |

When `fm` is omitted, Netlify auto-negotiates the best format based on browser support (preferring `webp`, then `avif`).

## Remote Image Allowlisting

External images must be explicitly allowed in `netlify.toml`:

```toml
[images]
remote_images = ["https://example\\.com/.*", "https://cdn\\.images\\.com/.*"]
```

Values are regex patterns.

## Clean URL Rewrites

Create user-friendly image URLs with redirects:

```toml
# Basic optimization
[[redirects]]
from = "/img/*"
to = "/.netlify/images?url=/:splat"
status = 200

# Preset: thumbnail
[[redirects]]
from = "/img/thumb/:key"
to = "/.netlify/images?url=/uploads/:key&w=150&h=150&fit=cover"
status = 200

# Preset: hero
[[redirects]]
from = "/img/hero/:key"
to = "/.netlify/images?url=/uploads/:key&w=1200&h=675&fit=cover"
status = 200
```

## Caching

- Transformed images are cached at the CDN edge automatically
- Cache invalidates on new deploys
- Set cache headers on source images to control caching:

```toml
[[headers]]
for = "/uploads/*"
[headers.values]
Cache-Control = "public, max-age=31536000, immutable"
```

## User-Uploaded Images

Combine **Netlify Functions** (upload handler) + **Netlify Blobs** (storage) + **Image CDN** (serving/transforming) to build a complete user-uploaded image pipeline. See [references/user-uploads.md](references/user-uploads.md) for the full pattern.

## Bundled References (Load As Needed)

- [User uploads pipeline](references/user-uploads.md)

<!-- BEGIN SOLKRAFT SKILL INTEGRATION -->
## SolKraft integration

- This procedure is selected by SolKraft's contract-aware router; selection does not authorize execution.
- Public routing defaults to hardened policy; opaque or contract-inadmissible capabilities fail closed.
- When `contract.yaml` exists, compact metadata is evaluated before this full instruction body is loaded.
- Runtime authority stays with the host; SolKraft keeps `execution_authorized: false`.
- See repository `VALIDATION.md` and `docs/SEMANTIC_ROUTER_PROOF.md` for current executed results, source identity, precision limits, and rerun instructions. Do not infer perfect matching or execution from a selected route.

<!-- END SOLKRAFT SKILL INTEGRATION -->
