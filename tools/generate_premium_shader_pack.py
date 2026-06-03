#!/usr/bin/env python3
"""Generate the original OBS Shaderfilter premium numbered pack.

The output files are intentionally self-contained .effect shaders. The
generator exists to keep the OBS boilerplate consistent across 150 shaders
while each shader receives its own metadata, defaults, and visual recipe.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "shaders" / "premium-pack"


PACKS = [
    ("Confidential / privacy pack", [
        "Strong confidential blur",
        "Pixelated privacy shield",
        "Frosted glass confidential screen",
        "Adaptive text destroying blur",
        "Redacted document look",
        "Security blackout pulse",
        "Privacy noise glass",
        "Corporate presentation blur",
        "Password manager destroyer",
        "Emergency privacy wipe",
    ]),
    ("Webcam motion pack", [
        "Subtle breathing rotation",
        "Floating webcam drift",
        "Handheld micro sway",
        "Paranormal twitch",
        "VHS frame instability",
        "Slow cinematic zoom",
        "Pendulum camera swing",
        "Dream camera drift",
        "Earthquake shake",
        "Security camera motor pan",
    ]),
    ("Cinematic camera pack", [
        "Teal and orange",
        "Bleach bypass",
        "Cold moonlight",
        "Supernatural green blue",
        "Rainy noir",
        "Horror red shadows",
        "Desert dust grade",
        "Golden hour",
        "Apocalyptic gray",
        "Documentary handheld look",
    ]),
    ("Retro analog pack", [
        "Old black and white film",
        "Silent movie projector",
        "Sepia damaged film",
        "CRT scanlines",
        "VHS tracking damage",
        "NTSC color bleed",
        "PAL phase shift",
        "Interlaced jitter",
        "Tape wrinkle",
        "Burned film edges",
    ]),
    ("Horror / supernatural pack", [
        "Haunted green shadows",
        "Ghost double exposure",
        "Possession pulse",
        "Demonic red contrast",
        "Foggy cemetery",
        "Sleep paralysis edges",
        "Cursed VHS",
        "Blood moon grade",
        "Ritual vignette",
        "Spirit camera distortion",
    ]),
    ("Cyberpunk / glitch pack", [
        "RGB split glitch",
        "Datamosh block shift",
        "Digital tearing",
        "Broken signal",
        "Cyberpunk neon boost",
        "Matrix terminal green",
        "Hologram flicker",
        "Robot vision",
        "Scanner sweep",
        "Corrupted codec",
    ]),
    ("Lens / distortion pack", [
        "Fisheye",
        "Barrel distortion",
        "Pincushion",
        "Chromatic aberration",
        "Fake 3D anaglyph",
        "Heat haze",
        "Water ripple",
        "Shockwave ring",
        "Tunnel warp",
        "Broken glass approximation",
    ]),
    ("Streamer branding pack", [
        "Rounded corners",
        "Animated neon border",
        "Soft drop shadow",
        "Glass webcam frame",
        "Polaroid webcam",
        "Cyberpunk panel",
        "Circular crop",
        "Hexagon crop",
        "Torn paper mask",
        "Security camera overlay",
    ]),
    ("Experimental art pack", [
        "Kaleidoscope",
        "Spiral warp",
        "Pixel melt",
        "Liquid metal",
        "Posterize",
        "Comic halftone",
        "Pencil sketch",
        "Ink outline",
        "Oil paint approximation",
        "Watercolor wash",
    ]),
    ("Weather / atmosphere pack", [
        "Rain on glass",
        "Snow overlay",
        "Smoke drift",
        "Ash particles",
        "Lightning flash",
        "Frosted lens",
        "Wet lens streaks",
        "Sandstorm",
        "Cloud shadow",
        "Sun flare approximation",
    ]),
    ("VJ / music video expansion", [
        "Beat pulse tunnel",
        "Neon kaleido wash",
        "Prism trail split",
        "Laser grid sweep",
        "Strobe smear",
        "Bass glow throb",
        "Spectral color split",
        "Liquid club wash",
        "Mirror stage flip",
        "Rave posterize",
    ]),
    ("Screen capture utility expansion", [
        "Focus spotlight",
        "Edge readability boost",
        "Dashboard glass dim",
        "Terminal phosphor glow",
        "Browser privacy haze",
        "Presentation spotlight",
        "Code rain overlay",
        "Document scanner pass",
        "Window focus vignette",
        "Cursor area magnifier",
    ]),
    ("Portrait / beauty expansion", [
        "Soft skin bloom",
        "Warm portrait lift",
        "Cool studio webcam",
        "Beauty vignette",
        "TikTok soft glam",
        "Instagram peach fade",
        "Smartphone HDR selfie",
        "Old laptop webcam",
        "News anchor clarity",
        "Low light webcam rescue",
    ]),
    ("Sci-fi / fantasy expansion", [
        "Arcane mana shimmer",
        "Portal edge glow",
        "Dragon fire heat",
        "Ice magic border",
        "Poison curse green",
        "Holy light rays",
        "Shadow realm wash",
        "Space monitor tint",
        "Alien scanner bands",
        "Forcefield ripple",
    ]),
    ("Extreme / transition expansion", [
        "Fullscreen melt",
        "RGB explosion",
        "Whiteout flash",
        "Blackout pulse",
        "Negative inversion",
        "Solarize threshold",
        "Thermal false color",
        "Deep fried meme",
        "JPEG artifact approximation",
        "Corrupted codec blocks",
    ]),
]


PRINCIPLES = {
    "privacy": (
        "large-kernel signal destruction with pixel quantization and procedural privacy noise",
        "it hides readable details but leaves the audience aware that real content exists underneath",
    ),
    "motion": (
        "animated UV camera transforms around a stable center point",
        "it makes a static source feel physically alive without moving the OBS source transform",
    ),
    "grade": (
        "luminance-aware color remapping, contrast shaping, vignette, and animated grain",
        "it gives ordinary footage a clear emotional direction in one pass",
    ),
    "analog": (
        "scanlines, field jitter, chroma drift, and time-varying tape damage",
        "it sells nostalgic hardware instability with cheap procedural math",
    ),
    "horror": (
        "crushed shadows, color-biased darkness, pulse timing, and unstable edges",
        "it adds dread by making the frame feel reactive and contaminated",
    ),
    "glitch": (
        "channel separation, block displacement, horizontal tears, and quantized corruption",
        "it creates readable digital failure while keeping the source recognizable",
    ),
    "distort": (
        "radial or directional UV warping with small compensating zoom",
        "it bends the camera feed like a lens or energy field while preserving the source",
    ),
    "mask": (
        "alpha-safe geometric masking, decorative frames, and procedural edge treatment",
        "it turns a plain source into a branded layout element",
    ),
    "art": (
        "stylized color quantization, edge emphasis, pattern overlays, and painterly sampling",
        "it makes live footage look intentionally illustrated instead of merely filtered",
    ),
    "weather": (
        "procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses",
        "it adds environmental storytelling without external image textures",
    ),
    "hud": (
        "synthetic graphics drawn in UV space over the live source",
        "it instantly reframes the source as tactical, technical, or broadcast media",
    ),
    "beauty": (
        "small-radius softening, tonal lift, flattering contrast, and gentle vignette",
        "it improves webcam polish while staying light enough for live streaming",
    ),
    "extreme": (
        "aggressive remapping, block damage, inversion, and transition-style pulses",
        "it is visually loud and useful for stingers, alerts, and music-video moments",
    ),
}

BEST_FOR = {
    "privacy": "screen capture, browser source, IDEs, dashboards, documents",
    "motion": "webcam camera source, image source, video source",
    "grade": "webcam, game capture, video source, cinematic scenes",
    "analog": "game capture, retro scenes, video source, screen capture",
    "horror": "webcam, horror games, video source, dramatic scenes",
    "glitch": "screen capture, game capture, music visuals, alerts",
    "distort": "webcam, game capture, image source, video source",
    "mask": "webcam camera source, streamer layouts, browser source",
    "art": "webcam, image source, video source, VJ visuals",
    "weather": "webcam, game capture, video source, image source",
    "hud": "game capture, webcam, screen capture, surveillance scenes",
    "beauty": "webcam camera source, smartphone camera, portrait video",
    "extreme": "alerts, transitions, music visuals, game capture",
}

CHAINS = {
    "privacy": "soft vignette -> this shader -> subtle noise or scanline overlay",
    "motion": "this shader -> soft drop shadow -> color grade",
    "grade": "exposure controls -> this shader -> film grain",
    "analog": "this shader -> chromatic aberration -> vignette",
    "horror": "this shader -> ghost double image -> dark vignette",
    "glitch": "this shader -> RGB split -> digital noise",
    "distort": "this shader -> chromatic aberration -> bloom",
    "mask": "this shader -> soft drop shadow -> animated border",
    "art": "this shader -> posterize or halftone -> light vignette",
    "weather": "this shader -> cinematic grade -> lens dirt",
    "hud": "this shader -> scanlines -> slight chromatic aberration",
    "beauty": "low-light correction -> this shader -> warm grade",
    "extreme": "this shader -> RGB split -> blackout/whiteout pulse",
}


def slugify(name: str) -> str:
    slug = name.lower().replace("3d", "3d")
    slug = re.sub(r"[^a-z0-9]+", "_", slug).strip("_")
    return slug


def classify(category: str, name: str) -> str:
    text = f"{category} {name}".lower()
    if "privacy" in text or "confidential" in text or "password" in text or "redacted" in text or "blackout" in text:
        return "privacy"
    if "motion" in text or "drift" in text or "sway" in text or "shake" in text or "swing" in text or "zoom" in text or "pan" in text or "twitch" in text or "instability" in text:
        return "motion"
    if "cinematic" in text or "teal" in text or "bleach" in text or "moonlight" in text or "noir" in text or "golden" in text or "documentary" in text or "gray" in text or "desert" in text:
        return "grade"
    if "retro" in text or "film" in text or "crt" in text or "vhs" in text or "ntsc" in text or "pal" in text or "interlaced" in text or "tape" in text:
        return "analog"
    if "horror" in text or "haunted" in text or "ghost" in text or "demonic" in text or "foggy" in text or "sleep" in text or "cursed" in text or "blood" in text or "ritual" in text or "spirit" in text:
        return "horror"
    if "glitch" in text or "datamosh" in text or "tearing" in text or "broken" in text or "hologram" in text or "robot" in text or "scanner" in text or "codec" in text or "matrix" in text:
        return "glitch"
    if "fisheye" in text or "barrel" in text or "pincushion" in text or "aberration" in text or "anaglyph" in text or "haze" in text or "ripple" in text or "shockwave" in text or "tunnel" in text or "glass" in text or "forcefield" in text:
        return "distort"
    if "branding" in text or "corner" in text or "border" in text or "shadow" in text or "frame" in text or "crop" in text or "mask" in text or "overlay" in text or "polaroid" in text or "panel" in text:
        return "mask"
    if "art" in text or "kaleidoscope" in text or "spiral" in text or "melt" in text or "liquid" in text or "posterize" in text or "halftone" in text or "sketch" in text or "ink" in text or "paint" in text or "watercolor" in text:
        return "art"
    if "weather" in text or "rain" in text or "snow" in text or "smoke" in text or "ash" in text or "lightning" in text or "frost" in text or "wet" in text or "sandstorm" in text or "cloud" in text or "sun" in text:
        return "weather"
    if "utility" in text or "spotlight" in text or "dashboard" in text or "terminal" in text or "browser" in text or "presentation" in text or "document" in text or "cursor" in text:
        return "hud"
    if "portrait" in text or "beauty" in text or "selfie" in text or "webcam" in text or "studio" in text or "glam" in text or "laptop" in text or "low light" in text:
        return "beauty"
    return "extreme"


def color_for(index: int, kind: str) -> tuple[float, float, float]:
    palettes = {
        "privacy": [(0.62, 0.76, 0.86), (0.08, 0.10, 0.12), (0.85, 0.88, 0.90)],
        "motion": [(1.0, 1.0, 1.0), (0.85, 0.92, 1.0), (1.0, 0.92, 0.82)],
        "grade": [(0.10, 0.50, 0.62), (1.0, 0.58, 0.25), (0.48, 0.62, 0.92)],
        "analog": [(0.95, 0.88, 0.72), (0.55, 0.70, 0.95), (0.90, 0.20, 0.18)],
        "horror": [(0.15, 0.38, 0.22), (0.85, 0.05, 0.04), (0.08, 0.02, 0.12)],
        "glitch": [(0.0, 0.9, 1.0), (1.0, 0.0, 0.55), (0.15, 1.0, 0.35)],
        "distort": [(0.55, 0.85, 1.0), (1.0, 0.35, 0.12), (0.35, 0.95, 0.65)],
        "mask": [(0.05, 0.85, 1.0), (1.0, 0.25, 0.75), (1.0, 0.88, 0.58)],
        "art": [(1.0, 0.70, 0.20), (0.20, 0.65, 1.0), (0.85, 0.30, 1.0)],
        "weather": [(0.70, 0.82, 1.0), (0.95, 0.93, 0.86), (0.65, 0.55, 0.35)],
        "hud": [(0.1, 1.0, 0.45), (0.1, 0.85, 1.0), (1.0, 0.22, 0.12)],
        "beauty": [(1.0, 0.72, 0.58), (0.84, 0.92, 1.0), (1.0, 0.82, 0.92)],
        "extreme": [(1.0, 0.15, 0.05), (0.05, 0.95, 1.0), (1.0, 0.95, 0.10)],
    }
    return palettes[kind][index % len(palettes[kind])]


def hlsl_common_header(filename, category, effect, kind, perf, alpha_safe, idx, suggested):
    principle, cool = PRINCIPLES[kind]
    chains = CHAINS[kind]
    return f"""// Filename: {filename}
// Category: {category}
// Effect: {effect}
// Visual principle: {principle}.
// What makes it cool: {cool}.
// Suggested source type: {suggested}
// Suggested shader-chain combinations: {chains}
// Performance cost: {perf}
// Alpha safe: {"yes" if alpha_safe else "no"}
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = {1.0 + (idx % 3) * 0.15:.2f};
uniform float amount = {0.85 + (idx % 5) * 0.08:.2f};
uniform float speed = {0.65 + (idx % 7) * 0.18:.2f};
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = {"true" if alpha_safe else "false"};

sampler_state textureSampler {{
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
}};

struct VertData {{
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
}};

VertData VSDefault(VertData v_in)
{{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}}

float hash12(float2 p)
{{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}}

float luma3(float3 c)
{{
    return dot(c, float3(0.299, 0.587, 0.114));
}}

float2 rotate2d(float2 p, float a)
{{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}}

float alphaOut(float sampled_alpha)
{{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {{
        a = 1.0;
    }}
    return a * saturate(opacity);
}}

"""


def body_privacy(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 pixels = max(float2(1.0, 1.0), uv_size);
    float block = lerp(12.0, 42.0, saturate(amount * 0.7));
    float2 cells = max(float2(1.0, 1.0), pixels / block);
    float2 puv = (floor(uv * cells) + 0.5) / cells;
    float2 px = uv_pixel_interval * (8.0 + amount * 24.0);
    float4 blur = image.Sample(textureSampler, puv) * 0.36;
    blur += image.Sample(textureSampler, clamp(puv + float2(px.x, 0.0), 0.0, 1.0)) * 0.16;
    blur += image.Sample(textureSampler, clamp(puv - float2(px.x, 0.0), 0.0, 1.0)) * 0.16;
    blur += image.Sample(textureSampler, clamp(puv + float2(0.0, px.y), 0.0, 1.0)) * 0.16;
    blur += image.Sample(textureSampler, clamp(puv - float2(0.0, px.y), 0.0, 1.0)) * 0.16;
    float grain = hash12(floor(uv * pixels / max(2.0, block * 0.35)) + floor(elapsed_time * speed * 12.0));
    float gray = luma3(blur.rgb);
    float3 tint = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_motion(idx, color):
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * {0.7 + idx % 4 * 0.17:.2f}) + sin(t * 0.37 + {idx % 9}.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + {idx}.0), cos(t * 0.73 + {idx % 11}.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}}
"""


def body_grade(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 warm = float3(1.05, 0.88 + {idx % 4} * 0.03, 0.72);
    float3 cool = float3(0.70, 0.88, 1.12);
    float vignette = smoothstep(0.88, 0.18, length((uv - float2(center_x, center_y)) * float2(1.15, 1.0)));
    float grain = hash12(floor(uv * max(uv_size, float2(1.0, 1.0)) * 0.55) + floor(elapsed_time * speed * 18.0)) - 0.5;
    float3 graded = lerp(color.rgb, float3(gray, gray, gray), 0.12 + 0.18 * amount);
    graded = (graded - 0.5) * (1.0 + 0.45 * intensity) + 0.5;
    graded *= lerp(cool, warm, saturate(tint.r + 0.25));
    graded = lerp(graded, tint * (0.25 + gray * 0.95), 0.20 * intensity);
    graded *= 0.72 + vignette * 0.38;
    graded += grain * 0.045 * intensity;
    return float4(saturate(graded), alphaOut(color.a));
}}
"""


def body_analog(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float scan = 0.72 + 0.28 * sin(uv.y * uv_size.y * 3.14159);
    float field = step(0.5, frac(uv.y * uv_size.y * 0.5 + floor(t * 6.0)));
    float band = sin(uv.y * 42.0 + t * 5.0) * 0.006 * amount;
    float tear = (hash12(float2(floor(uv.y * 18.0), floor(t * 3.0))) - 0.5) * 0.020 * amount;
    float2 uv_r = clamp(uv + float2( band + tear, 0.0), 0.0, 1.0);
    float2 uv_g = clamp(uv + float2(-band * 0.35, field * uv_pixel_interval.y * 1.5), 0.0, 1.0);
    float2 uv_b = clamp(uv + float2(-band - tear * 0.5, 0.0), 0.0, 1.0);
    float rch = image.Sample(textureSampler, uv_r).r;
    float gch = image.Sample(textureSampler, uv_g).g;
    float bch = image.Sample(textureSampler, uv_b).b;
    float noise = hash12(floor(uv * uv_size / 3.0) + floor(t * 20.0)) - 0.5;
    float3 tint = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_horror(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_glitch(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float row = floor(uv.y * (24.0 + amount * 28.0));
    float gate = step(0.68, hash12(float2(row, floor(t * 8.0))));
    float shift = (hash12(float2(row * 3.1, floor(t * 6.0))) - 0.5) * 0.075 * amount * gate;
    float block = floor(uv.x * 18.0) + floor(uv.y * 10.0) * 31.0;
    float block_gate = step(0.78, hash12(float2(block, floor(t * 4.0))));
    float2 duv = float2(shift + block_gate * 0.025 * sin(t + block), 0.0);
    float spread = 0.006 * intensity + abs(shift) * 0.25;
    float rch = image.Sample(textureSampler, clamp(uv + duv + float2(spread, 0.0), 0.0, 1.0)).r;
    float gch = image.Sample(textureSampler, clamp(uv + duv, 0.0, 1.0)).g;
    float bch = image.Sample(textureSampler, clamp(uv + duv - float2(spread, 0.0), 0.0, 1.0)).b;
    float3 accent = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_distort(idx, color):
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * {18 + idx % 12}.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + {idx % 5}.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}}
"""


def body_mask(idx, color):
    r, g, b = color
    shape = idx % 5
    shape_expr = {
        0: "length(p) - 0.46",
        1: "max(abs(p.x) * 0.86 + abs(p.y) * 0.50, abs(p.y)) - 0.43",
        2: "abs(p.x) + abs(p.y) - 0.58",
        3: "max(abs(p.x) - 0.43, abs(p.y) - 0.39)",
        4: "length(p * float2(1.08, 0.92)) - 0.47 + jag * 0.035",
    }[shape]
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = {shape_expr};
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3({r:.3f}, {g:.3f}, {b:.3f}) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {{
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }}
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}}
"""


def body_art(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 px = uv_pixel_interval * (1.0 + amount * 2.0);
    float4 c = color;
    float4 cx = image.Sample(textureSampler, clamp(uv + float2(px.x, 0.0), 0.0, 1.0));
    float4 cy = image.Sample(textureSampler, clamp(uv + float2(0.0, px.y), 0.0, 1.0));
    float edge = length(c.rgb - cx.rgb) + length(c.rgb - cy.rgb);
    float levels = 4.0 + floor(amount * 5.0);
    float3 quant = floor(c.rgb * levels) / levels;
    float dots = step(0.48, frac((uv.x + uv.y + sin(elapsed_time * speed) * 0.03) * uv_size.x / (10.0 + amount * 10.0)));
    float gray = luma3(quant);
    float3 ink = lerp(quant, float3({r:.3f}, {g:.3f}, {b:.3f}) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}}
"""


def body_weather(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_hud(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float t = elapsed_time * speed;
    float ring = 1.0 - smoothstep(0.004, 0.018, abs(length(p) - (0.18 + 0.06 * sin(t))));
    float cross = 1.0 - smoothstep(0.0, 0.004 + amount * 0.003, min(abs(p.x), abs(p.y)));
    float grid = step(0.985, max(frac(uv.x * 12.0), frac(uv.y * 12.0)));
    float2 sweep_dir = float2(cos(t * 1.2), sin(t * 1.2));
    float sweep = smoothstep(0.965, 1.0, dot(normalize(p + float2(0.0001, 0.0002)), sweep_dir));
    sweep *= smoothstep(0.02, 0.45, length(p));
    float scan = ring + cross * 0.6 + grid * 0.25 + sweep * 0.35;
    float3 hud = float3({r:.3f}, {g:.3f}, {b:.3f}) * scan * intensity;
    float3 out_rgb = color.rgb * (0.82 + 0.18 * sin(uv.y * uv_size.y * 3.14159)) + hud;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


def body_beauty(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 px = uv_pixel_interval * (2.0 + amount * 3.0);
    float4 src = color;
    float4 soft = color * 0.40;
    soft += image.Sample(textureSampler, clamp(uv + float2(px.x, 0.0), 0.0, 1.0)) * 0.15;
    soft += image.Sample(textureSampler, clamp(uv - float2(px.x, 0.0), 0.0, 1.0)) * 0.15;
    soft += image.Sample(textureSampler, clamp(uv + float2(0.0, px.y), 0.0, 1.0)) * 0.15;
    soft += image.Sample(textureSampler, clamp(uv - float2(0.0, px.y), 0.0, 1.0)) * 0.15;
    float gray = luma3(src.rgb);
    float vignette = smoothstep(0.90, 0.20, length((uv - float2(center_x, center_y)) * float2(1.05, 1.0)));
    float3 tint = float3({r:.3f}, {g:.3f}, {b:.3f});
    float3 out_rgb = lerp(src.rgb, soft.rgb, 0.32 * intensity);
    out_rgb = lerp(out_rgb, tint * (0.35 + gray * 0.9), 0.16 * amount);
    out_rgb += 0.05 * intensity;
    out_rgb *= 0.82 + vignette * 0.22;
    return float4(saturate(out_rgb), alphaOut(src.a));
}}
"""


def body_extreme(idx, color):
    r, g, b = color
    return f"""float4 mainImage(VertData v_in) : TARGET
{{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 pixels = max(uv_size, float2(1.0, 1.0));
    float block_size = 8.0 + amount * 28.0;
    float2 cell = floor(uv * pixels / block_size);
    float corrupt = step(0.62, hash12(cell + floor(t * 5.0)));
    float2 shift = (float2(hash12(cell), hash12(cell + 13.7)) - 0.5) * 0.12 * corrupt * amount;
    float pulse = 0.5 + 0.5 * sin(t * 4.0);
    float4 src = image.Sample(textureSampler, clamp(uv + shift, 0.0, 1.0));
    float gray = luma3(src.rgb);
    float3 false_color = lerp(float3(0.02, 0.04, 0.08), float3({r:.3f}, {g:.3f}, {b:.3f}), smoothstep(0.15, 0.95, gray));
    float3 inverted = 1.0 - src.rgb;
    float3 out_rgb = lerp(src.rgb, false_color, 0.45 * intensity);
    out_rgb = lerp(out_rgb, inverted, corrupt * 0.35 * amount);
    out_rgb += pulse * corrupt * float3({r:.3f}, {g:.3f}, {b:.3f}) * 0.25;
    return float4(saturate(out_rgb), alphaOut(color.a));
}}
"""


BODY_BY_KIND = {
    "privacy": body_privacy,
    "motion": body_motion,
    "grade": body_grade,
    "analog": body_analog,
    "horror": body_horror,
    "glitch": body_glitch,
    "distort": body_distort,
    "mask": body_mask,
    "art": body_art,
    "weather": body_weather,
    "hud": body_hud,
    "beauty": body_beauty,
    "extreme": body_extreme,
}


def performance(kind: str) -> str:
    if kind in {"privacy", "analog", "glitch", "beauty", "art"}:
        return "medium"
    return "low"


def shader_code(idx: int, category: str, effect: str) -> tuple[str, str, str, str, bool]:
    kind = classify(category, effect)
    slug = slugify(effect)
    filename = f"shader_{idx:03d}_{slug}.effect"
    alpha_safe = kind in {"mask", "motion", "beauty", "distort", "art", "weather"} or "webcam" in effect.lower()
    color = color_for(idx, kind)
    perf = performance(kind)
    suggested = BEST_FOR[kind]
    header = hlsl_common_header(filename, category, effect, kind, perf, alpha_safe, idx, suggested)
    body = BODY_BY_KIND[kind](idx, color)
    code = header + body + """
technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
"""
    return filename, code, kind, perf, alpha_safe


def checklist(start: int, end: int) -> str:
    return f"""
### Compile-test checklist: shaders {start:03d}-{end:03d}

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    idx = 1
    for category, effects in PACKS:
        for effect in effects:
            filename, code, kind, perf, alpha_safe = shader_code(idx, category, effect)
            (OUT / filename).write_text(code, encoding="utf-8")
            principle, cool = PRINCIPLES[kind]
            entries.append((idx, filename, category, effect, kind, perf, alpha_safe, principle, cool, code))
            idx += 1

    lines = [
        "# Premium OBS Shaderfilter Pack",
        "",
        "Original single-pass `.effect` shaders for OBS Studio + obs-shaderfilter.",
        "No third-party shader code is copied; these are fresh implementations based on visual principles.",
        "",
        "Research anchors used for principles: OBS Shaderfilter user-defined shader examples, Libretro CRT/Slang shader documentation, and general HLSL-style single-pass shader practice.",
        "",
    ]
    for entry in entries:
        idx, filename, category, effect, kind, perf, alpha_safe, principle, cool, code = entry
        lines.extend([
            f"## {filename}",
            "",
            f"Category: {category}",
            f"Effect: {effect}",
            f"Best for: {BEST_FOR[kind]}",
            f"Visual inspiration: {principle}",
            f"What makes it cool: {cool}",
            "Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha",
            f"Performance: {perf}",
            f"Alpha safe: {'yes' if alpha_safe else 'no'}",
            "Code:",
            "",
            "```hlsl",
            code.rstrip(),
            "```",
            "",
        ])
        if idx % 25 == 0:
            lines.append(checklist(idx - 24, idx))

    lines.extend([
        "## Final Known OBS Shaderfilter Pitfalls",
        "",
        "- Use `.effect` files for this pack and load them through the Shaderfilter user-defined shader UI.",
        "- Keep `image.Sample(textureSampler, uv)` syntax; `texture2D`, `sampler2D`, `iChannel`, `iResolution`, and `gl_FragCoord` are intentionally absent.",
        "- OBS exposes uniforms as controls, but unsupported uniform types or typoed names can silently produce confusing UI.",
        "- Multi-pass CRT and bloom references from other ecosystems are simplified here because Shaderfilter user shaders are usually single-pass source filters.",
        "- Clamp or compensate UV warps with zoom to avoid black corners; these shaders clamp sampler addressing and most warps add zoom internally.",
        "- Alpha masks should be tested on transparent webcam/browser sources and on full-screen captures because alpha behavior depends on the OBS source chain.",
        "- If a shader appears unchanged, raise `intensity` and `amount`, then confirm `elapsed_time` is updating by adjusting `speed`.",
        "- Heavy chains of multiple medium-cost shaders can cost more than one complex shader; profile the final OBS scene at the target canvas resolution.",
    ])
    (OUT / "PREMIUM_SHADER_PACK.md").write_text("\n".join(lines), encoding="utf-8")

    index_lines = [
        "# Premium Shader Pack Index",
        "",
        "Compact index for the 150 numbered OBS Shaderfilter shaders.",
        "Open `PREMIUM_SHADER_PACK.md` for full descriptions, controls, performance notes, limitations, and copy-paste code.",
        "",
    ]
    current_category = ""
    for entry in entries:
        idx, filename, category, effect, kind, perf, alpha_safe, _principle, _cool, _code = entry
        if category != current_category:
            if current_category:
                index_lines.append("")
            index_lines.append(f"## {category}")
            index_lines.append("")
            current_category = category
        index_lines.append(
            f"- `{filename}` - {effect}; best for {BEST_FOR[kind]}; performance {perf}; alpha safe {'yes' if alpha_safe else 'no'}"
        )
    (OUT / "PACK_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
