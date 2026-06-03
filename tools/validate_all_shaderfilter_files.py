#!/usr/bin/env python3
"""Static audit for all OBS Shaderfilter .effect files in this repo."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SHADERS = ROOT / "shaders"

REFERENCE_ONLY = {
    "shaders/_helpers/helpers.effect",
}

FORBIDDEN_PATTERNS = [
    ("GLSL texture2D", re.compile(r"\btexture2D\b")),
    ("GLSL sampler2D", re.compile(r"\bsampler2D\b")),
    ("Shadertoy iChannel", re.compile(r"\biChannel\d*\b")),
    ("Shadertoy iResolution", re.compile(r"\biResolution\b")),
    ("GLSL gl_FragCoord", re.compile(r"\bgl_FragCoord\b")),
    ("GLSL gl_FragColor", re.compile(r"\bgl_FragColor\b")),
    ("Shadertoy fragCoord", re.compile(r"\bfragCoord\b")),
    ("GLSL mix", re.compile(r"\bmix\s*\(")),
    ("GLSL fract", re.compile(r"\bfract\s*\(")),
    ("repeated component .xxx swizzle", re.compile(r"\.xxx\b")),
    ("repeated component .yyy swizzle", re.compile(r"\.yyy\b")),
    ("repeated component .zzz swizzle", re.compile(r"\.zzz\b")),
    ("repeated component .www swizzle", re.compile(r"\.www\b")),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def strip_line_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if "//" in line:
            line = line.split("//", 1)[0]
        lines.append(line)
    return "\n".join(lines)


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def delimiter_errors(path_rel: str, code: str) -> list[str]:
    errors = []
    stack: list[tuple[str, int]] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    opens = set(pairs.values())
    closes = set(pairs)

    for index, ch in enumerate(code):
        if ch in opens:
            stack.append((ch, line_number(code, index)))
        elif ch in closes:
            if not stack or stack[-1][0] != pairs[ch]:
                errors.append(f"{path_rel}:{line_number(code, index)}: unmatched closing delimiter {ch}")
            else:
                stack.pop()

    for ch, line in stack:
        errors.append(f"{path_rel}:{line}: unmatched opening delimiter {ch}")

    return errors


def main() -> int:
    verbose = "--verbose" in sys.argv
    files = sorted(SHADERS.glob("**/*.effect"))
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []

    if not files:
        errors.append("No .effect files found under shaders/")

    for path in files:
        path_rel = rel(path)
        text = path.read_text(encoding="utf-8")
        code = strip_line_comments(text)
        reference_only = path_rel in REFERENCE_ONLY
        file_errors: list[str] = []
        file_warnings: list[str] = []

        file_errors.extend(delimiter_errors(path_rel, code))

        for label, pattern in FORBIDDEN_PATTERNS:
            match = pattern.search(code)
            if match:
                file_errors.append(f"{path_rel}:{line_number(code, match.start())}: forbidden {label}")

        if not reference_only:
            if "float4 mainImage(VertData v_in) : TARGET" not in code:
                file_errors.append(f"{path_rel}: missing exact OBS entry point mainImage(VertData v_in) : TARGET")

            if "image.Sample(textureSampler" not in code:
                file_errors.append(f"{path_rel}: missing image.Sample(textureSampler, ...) source sampling")

            if "uniform texture2d image" not in code:
                file_errors.append(f"{path_rel}: missing uniform texture2d image declaration")

            if "sampler_state textureSampler" not in code:
                file_errors.append(f"{path_rel}: missing sampler_state textureSampler declaration")

            if not re.search(r"struct\s+VertData\s*\{", code):
                file_errors.append(f"{path_rel}: missing VertData input struct")

            if not re.search(r"\breturn\s+[^;]+;", code):
                file_errors.append(f"{path_rel}: no obvious pixel return statement")

            if re.search(r"vertex_shader\s*=\s*mainImage\s*\(", code):
                file_errors.append(f"{path_rel}: technique binds pixel shader mainImage as vertex shader")

            if re.search(r"pixel_shader\s*=\s*VSDefault\s*\(", code):
                file_errors.append(f"{path_rel}: technique binds vertex shader VSDefault as pixel shader")

            if re.search(r"vertex_shader\s*=\s*VSDefault\s*\(", code):
                if "VertData VSDefault(VertData v_in)" not in code:
                    file_errors.append(f"{path_rel}: technique uses VSDefault but the function is missing")
                if "uniform float4x4 ViewProj" not in code:
                    file_errors.append(f"{path_rel}: VSDefault requires uniform float4x4 ViewProj")

            if "technique Draw" in code:
                if not re.search(r"pixel_shader\s*=\s*mainImage\s*\(", code):
                    file_errors.append(f"{path_rel}: technique Draw missing pixel_shader = mainImage(v_in)")
                if not re.search(r"vertex_shader\s*=\s*[A-Za-z_]\w*\s*\(", code):
                    file_errors.append(f"{path_rel}: technique Draw missing vertex_shader binding")

        sample_count = code.count("image.Sample(textureSampler")
        if not reference_only:
            if sample_count > 18:
                file_warnings.append(f"{path_rel}: high static texture sample count ({sample_count})")

            const_like_names = set(
                re.findall(r"\b(?:static\s+const\s+int|const\s+int|int)\s+([A-Za-z_]\w*)\s*=\s*[-+]?\d+\s*;", code)
            )
            nonliteral_bounds = re.findall(
                r"for\s*\([^;]+;\s*[^;]*(?:<=|<)\s*([A-Za-z_]\w*)\s*;",
                code,
            )
            risky_bounds = [name for name in nonliteral_bounds if name not in const_like_names]
            if risky_bounds:
                file_warnings.append(
                    f"{path_rel}: loop has non-literal upper bound(s) {', '.join(sorted(set(risky_bounds)))}; consider unrolling for OBS portability"
                )

            loop_count = len(re.findall(r"\bfor\s*\(", code))
            if loop_count > 2 and sample_count > 5:
                file_warnings.append(f"{path_rel}: multiple loops ({loop_count}) with texture sampling; check live performance")

            if re.search(r"\bfloat[234]?\s+\w+\s*\[\s*\d+\s*\]\s*=", code):
                file_warnings.append(f"{path_rel}: local array initializer; valid HLSL on many setups but worth OBS compile-testing")

        if file_errors:
            errors.extend(file_errors)
        else:
            passed.append(path_rel)
        warnings.extend(file_warnings)

    print(f"Shaderfilter audit: {len(files)} .effect files checked")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Files passing static OBS checks: {len(passed)}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if verbose:
        print("\nPer-file static result:")
        failed_files = {item.split(":", 1)[0] for item in errors}
        warned_files = {item.split(":", 1)[0] for item in warnings}
        for path in sorted(rel(path) for path in files):
            if path in failed_files:
                status = "FAIL"
            elif path in warned_files:
                status = "WARN"
            else:
                status = "PASS"
            print(f"{status} {path}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
