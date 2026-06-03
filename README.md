# OBS Shaders

Custom shaders for the [OBS ShaderFilter](https://github.com/exeldro/obs-shader-filter) plugin.
Written in HLSL-style `.effect` format.

## Structure

```
shaders/
└── <shader-name>/
    ├── <shader-name>.effect          # base / default version
    ├── <shader-name>-<variant>.effect # tweaked variants
    └── media/
        ├── preview.gif               # static or animated preview
        └── demo.mp4                  # full demo (tracked via Git LFS)
```

Each shader lives in its own folder so all variants and assets stay together.

## Shaders

| Shader | Description |
|--------|-------------|
| [lens-dirt](shaders/lens-dirt/) | Procedural noise-based sensor dust/smudge overlay |

## Usage

1. In OBS, add a **Filter** to a source → **Shader Filter**
2. Browse to the `.effect` file
3. Adjust the exposed uniforms in the filter panel

## Media files

Large media (`.mp4`, `.mov`, `.gif`, etc.) are tracked with **Git LFS**.
Run `git lfs install` once before cloning or pulling assets.
