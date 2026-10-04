<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Repository readiness

## Portability

- Use standard Git-flavored Markdown.
- Prefer relative repository links.
- Do not require JavaScript, custom CSS, external fonts, or proprietary expanders.
- Keep Mermaid optional: pair every diagram with a short prose explanation.
- Give images meaningful alt text and avoid text-only information encoded in color.

## Commands

- Copy commands from source-backed installation or development evidence.
- Keep each command block executable from the stated directory and shell.
- State prerequisites before commands.
- Reject placeholders such as `<your-token>` from an accepted quick start.
- Never execute arbitrary source commands merely to validate syntax. Run commands only when the user authorized repository execution and the command is safe.

## Truth and maturity

- Distinguish released, experimental, planned, unavailable, and host-dependent capabilities.
- Do not use badges without a real target and current evidence.
- Match capability and tool names to the live registry.
- Keep security and authority boundaries visible in the root README even when details move to `/docs`.

## Existing repositories

Preserve unrelated README content, legal notices, attribution, badges, and user changes. When replacing an existing README, present a semantic diff and record where each removed section moved or why it was omitted.

The bundled transformer is intentionally create-only: it validates the complete package before writing and refuses any existing target file. For an existing repository, compile and validate the candidate, inspect the current files, apply a semantic patch under the accepted plan, and preserve all unrelated content. Never use a force-overwrite switch.
