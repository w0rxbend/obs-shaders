#!/usr/bin/env python3
"""Static checks for the generated premium OBS Shaderfilter pack."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "shaders" / "premium-pack"
CATALOG = PACK / "PREMIUM_SHADER_PACK.md"

FORBIDDEN = [
    "texture2D",
    "sampler2D",
    "iChannel",
    "iResolution",
    "gl_FragCoord",
    "gl_FragColor",
    "fragCoord",
    ".xxx",
    ".yyy",
    ".zzz",
    ".www",
    "mix(",
    "fract(",
    "atan2",
]

REQUIRED_SNIPPETS = [
    "uniform texture2d image;",
    "uniform float elapsed_time;",
    "float4 mainImage(VertData v_in) : TARGET",
    "image.Sample(textureSampler",
    "v_in.uv * uv_scale + uv_offset",
    "return float4",
    "technique Draw",
]


def strip_line_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    files = sorted(PACK.glob("shader_*.effect"))
    if len(files) != 150:
        fail(f"expected 150 premium shaders, found {len(files)}")

    expected = [f"shader_{i:03d}_" for i in range(1, 151)]
    for prefix, path in zip(expected, files):
        if not path.name.startswith(prefix):
            fail(f"expected filename prefix {prefix}, found {path.name}")

    for path in files:
        text = strip_line_comments(path.read_text(encoding="utf-8"))

        for snippet in REQUIRED_SNIPPETS:
            if snippet not in text:
                fail(f"{path.name} missing required snippet: {snippet}")

        for token in FORBIDDEN:
            if token in text:
                fail(f"{path.name} contains forbidden token: {token}")

        sample_count = text.count("image.Sample(textureSampler")
        if sample_count > 9:
            fail(f"{path.name} has {sample_count} texture samples; max allowed is 9")

        if re.search(r"\bfloat\s+\w+\s*=.*;\s*\n\s*float3\(\s*\w+\.xxx", text):
            fail(f"{path.name} appears to use scalar swizzle expansion")

    if not CATALOG.exists():
        fail("missing PREMIUM_SHADER_PACK.md")

    catalog = CATALOG.read_text(encoding="utf-8")
    section_count = len(re.findall(r"^## shader_\d{3}_.*\.effect$", catalog, re.MULTILINE))
    if section_count != 150:
        fail(f"catalog has {section_count} shader sections; expected 150")

    for start in range(1, 151, 25):
        end = start + 24
        marker = f"Compile-test checklist: shaders {start:03d}-{end:03d}"
        if marker not in catalog:
            fail(f"catalog missing checkpoint: {marker}")

    if "Final Known OBS Shaderfilter Pitfalls" not in catalog:
        fail("catalog missing final OBS pitfalls section")

    print("PASS: premium shader pack static validation succeeded")
    print(f"Shaders checked: {len(files)}")
    print(f"Catalog sections checked: {section_count}")


if __name__ == "__main__":
    main()
