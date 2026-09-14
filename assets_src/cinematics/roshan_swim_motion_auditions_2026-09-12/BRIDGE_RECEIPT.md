# Imagine bridge return — 2026-09-13

Topic branch: `grok/imagine-bridge-return-20260913` off `origin/dev`
(`f98ef836`). Do not treat `ca4dd196` as current status.

Filled Codex intake files live next to the packet templates:

- `CAPABILITY_CHECK.json`
- `RETURN_MANIFEST.json`
- this receipt

## What was broken

1. The packet the owner linked was a historical snapshot. Live publication is
   on `dev` with `ARCHIVE_COMPLETE: true` and `GENERATION_READY: false`.
2. Grok chats without video tools substituted still boards. START_HERE now
   forbids that.
3. Imagine cannot be driven from a GitHub tree URL. Images must be hashed,
   downloaded, and attached as IMAGE_1 + IMAGE_2.
4. Native video length is 6 / 10 / 15 seconds, not 8. This return uses 10s
   and labels it honestly.
5. GitHub's text file API cannot store the original MP4s. Hashes below are
   the authority. Playable files live in Reef Imagine Bridge.

## What this session did

- Verified opening SHA-256 values against the immutable ca4dd196 raw URLs.
- Invoked `imagine_reference_to_video` with the named first frame and the
  approved identity painting.
- Returned eight original take-01 MP4s, 1280×720, 24 fps, ~10.04s.
- Reviewed at sampled timestamps. Did not inflate scores. Did not claim
  delivery.

## Bound inputs

| Role | File | SHA-256 |
|---|---|---|
| IMAGE_1 (RSW-01–06) | openings/front-right.png | `cb4f0ccccf31937aabeecc4cba0232d2e50ab37fe0dc97c9b9ac2ef986959bf0` |
| IMAGE_1 (RSW-07–08) | openings/right.png | `5839c5cef6948666984700fb73ed07a77a047f8ad0ae5c75b9e44a465557ae48` |
| IMAGE_2 (all) | references/approved-front.png | `db2d2c13c2ccf9f0727934434adccdbf9d1d127943f743f436a48fff7c62ba3c` |

## Take hashes (binaries not on GitHub)

| Sample | Disposition | SHA-256 |
|---|---|---|
| RSW-01 | comparison_candidate | `a8de1b06b47860894b9d834b897358dfdbadce1a4508a49f95ad927803fe6366` |
| RSW-02 | comparison_candidate | `78c91b17af0a20126ed7c456b8a08970b8b7fde272a1464742a2c2427490cb0a` |
| RSW-03 | comparison_candidate | `96048e0ec855de8d1016c99732afe07f6e026cef1905074441df71d57d0e09cb` |
| RSW-04 | inspiration_only | `e7faf6a569c4c28d8538d67eef6138b35a35ea2995b8e823acfb1496d4fd98eb` |
| RSW-05 | comparison_candidate | `735491d3c33d0261790abf3e73c41e31bc4298a0e2bccb6afe9b36dc87ab909f` |
| RSW-06 | inspiration_only | `f6110264954b243193b4d70ffc046adcb419bfbc801d2f246b5f4be91272b7fa` |
| RSW-07 | inspiration_only | `9df10f68a5e4db29478c4a5c3e3c367cb606579fe573b4fe96ce48247830a39e` |
| RSW-08 | inspiration_only | `51efe2fb3c1d48e7bb4131ef151a63779e9034d700cad0697735c3802efb5c9d` |

Native files: 10.04s, 1280×720, 24 fps, H.264 + unwanted AAC. Requested 8s silent.

## Shortlist (agent only)

1. RSW-03 — curiosity reach.
2. RSW-05 — bored / impatient palm-raise.
3. RSW-01 t2.5–4.0 — quiet diagonal swim.

Owner selection and `DELIVERY_ACCEPTED` stay false. No Aseprite conversion,
no runtime integration, no cinematic acceptance.
