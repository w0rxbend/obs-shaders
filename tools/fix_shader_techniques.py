#!/usr/bin/env python3
"""Fix .effect technique blocks that accidentally use mainImage as vertex shader."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SHADERS = ROOT / "shaders"

VIEWPROJ = "uniform float4x4 ViewProj;"
VSDEFAULT = """VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv  = v_in.uv;
    return vert_out;
}

"""


def add_viewproj(text: str) -> str:
    if VIEWPROJ in text:
        return text
    match = re.search(r"^uniform\s+", text, re.MULTILINE)
    if not match:
        return VIEWPROJ + "\n" + text
    return text[:match.start()] + VIEWPROJ + "\n" + text[match.start():]


def add_vsdefault(text: str) -> str:
    if "VertData VSDefault(VertData v_in)" in text:
        return text
    match = re.search(
        r"struct\s+VertData\s*\{[^{}]*\}\s*;\s*\n",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("missing simple VertData struct")
    return text[:match.end()] + "\n" + VSDEFAULT + text[match.end():]


def main() -> None:
    changed = []
    for path in sorted(SHADERS.glob("**/*.effect")):
        text = path.read_text(encoding="utf-8")
        uses_bad_main_vertex = "vertex_shader = mainImage(v_in);" in text
        uses_vsdefault = "vertex_shader = VSDefault(v_in);" in text
        if not uses_bad_main_vertex and not uses_vsdefault:
            continue

        new_text = text.replace("vertex_shader = mainImage(v_in);", "vertex_shader = VSDefault(v_in);")
        new_text = add_viewproj(new_text)
        new_text = add_vsdefault(new_text)

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    print(f"Fixed technique vertex shaders: {len(changed)}")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
