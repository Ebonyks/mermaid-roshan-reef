# GIF capabilities and Sky Lagoon output specifications

Checked against the official documentation on 2026-11-05. The native OpenAI animation API, this chat's exposed image tool, and local GIF encoding have different controls. These samples use local source-pixel animation to preserve the original painting and achieve the requested cadence.

## Native OpenAI GIF generation

The current guide documents animated GIF output for GPT Image 2.6 Sunburst and Flare. It describes generation and still-image-guided edit requests. Its GIF controls are 2–16 frames, a default of 9; frame delays 20–2000 ms rounded to 10 ms, default 200 ms; and automatic sizing or positive dimensions divisible by 16. Frame count, dimensions and animation count share model/request pixel budgets. Streaming, partial images, custom compression and prompt rewriting are unavailable for GIF output. [Official image generation guide](https://developers.openai.com/api/docs/guides/image-generation#generate-animated-gif-output).

The API reference additionally requires GIF-preview access for the selected model and excludes masks. It lists a 20 ms minimum but a much larger encoded-delay cap than the guide's 2000 ms request range. Use the narrower guide range until that documentation discrepancy is resolved. The public pages inspected do not provide a single numeric GIF pixel-budget maximum that can safely be promised across accounts/models. [Official generation API reference](https://developers.openai.com/api/reference/resources/images/methods/generate).

This chat exposes an image tool with prompt, reference-image and transparency inputs. It does not expose model selection, `frame_count`, `frame_duration_ms`, output format or seed as structured controls. No native GIF generation call or paid API job was performed for this correction; account preview access and hosted revision were not tested.

## Can native output meet 24–30 fps for 1–3 seconds

The 16-frame ceiling is the limiting factor. One second at 24 fps needs 24 frames; two seconds at 30 fps needs 60. A 16-frame animation at 30 ms delays lasts 0.48 s, while 40 ms delays give 25 fps for 0.64 s. A 1.6-second 16-frame loop at 100 ms is 10 fps. These are arithmetic consequences of the documented controls, not measured native generation results.

Local encoding supports the requested duration and cadence. GIF delay units are hundredths of a second, so exact uniform 33.333 ms or 41.667 ms delays are unavailable. A repeating 30/30/40 ms pattern averages 30 fps; a suitable 40/50 ms pattern averages 24 fps. Actual playback also depends on the viewer and device. [GIF89a specification, graphic control extension](https://www.w3.org/Graphics/GIF/spec-gif89a.txt).

GIF uses indexed colour tables, with at most 256 entries per table, and a transparent palette index rather than smooth RGBA alpha. Small transparent plant edges therefore benefit from lossless PNG/Aseprite sources for game integration. Our preview GIFs use one fixed 256-colour palette per animation and no dithering, to keep stationary scenery from shimmering. GIF is not the editable appearance master. [GIF89a colour tables and transparency](https://www.w3.org/Graphics/GIF/spec-gif89a.txt).

## Delivered study settings

| Setting | This candidate |
|---|---|
| Appearance input | One unchanged 6144×2048 v5 panorama, exact source SHA recorded |
| Targets | Three existing painted flower groups;512×512 context per action |
| Loop |2 seconds,60 timed samples, no duplicated endpoint |
| Distinct RGB poses |59 per source action; GIF palette quantization yields 58/57/58 distinct decoded images. No consecutive padding holds are inserted. |
| GIF timing |30, 30, 40 ms repeated 20 times;2000 ms total,30 fps average |
| Aseprite timing |33, 33, 34 ms repeated 20 times;2000 ms total |
| Individual GIF |512×512, fixed palette, infinite loop, no audio |
| Close-up board |1536×550, three original contexts, fixed composition |
| Panorama GIF |1800×600, fixed camera and original aspect ratio |
| Motion |About 1.3–1.9 native pixels horizontal; zero vertical translation, rigid rotation and scale change |
| Game demo |True Canvas, Godot 4.7.2-stable Mobile; twelve 1024-square background tiles plus three 512-square source/field pairs |
| Runtime canvas |1280×720, canvas_items/expand; original3:1 panorama proportions preserved |
| Native appearance |Lossless RGB/PNG source and editable RGBA Aseprite complete frames; no GIF palette imposed on engine sampling |
| GPU strategy |Three small displacement fields, not 60 full textures per target; target-device performance still required |
| Generation usage |0 calls,$0 paid generation; no new appearance art |

## Inputs for an effective next native trial

Supply an exact crop containing one original flower group, its roots and enough adjacent scenery to show registration. Bind that image as the identity and layout reference. State one small action, a fixed camera and roots, the maximum tip excursion, unchanged flower count/colours, an exact return pose, and no new plants, props, lighting or camera movement. Keep the original uncompressed source and reject any identity, composition or background drift before interpolation.

A bounded native trial could request 16 frames at 100 ms for a 1.6-second loop, using dimensions divisible by 16 and automatic sizing if the model's pixel budget rejects a fixed size. That would be a 10 fps generated study. Re-exporting it as 30 fps does not create 30 distinct authored poses; any interpolation must be declared and visually reviewed. For the present quiet foliage task, the local authored field offers direct source preservation and measured 30 fps sampling.
