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

Each folder under `shaders/` is one effect. `shaders/premium-pack/` holds 150 numbered effects. `shaders/_helpers/helpers.effect` is a paste reference. The plugin does not include it.

## Usage

1. In OBS, add a **Filter** to a source, then **User-defined shader**.
2. Load the `.effect` file from disk.
3. Leave **Override entire effect** on. A `.effect` path turns it on. The file must contain `technique Draw`.
4. Adjust the exposed uniforms in the filter panel.

A file with no `technique Draw` draws nothing.

## Media files

Large media (`.mp4`, `.mov`, `.gif`, etc.) are tracked with **Git LFS**.
Run `git lfs install` once before cloning or pulling assets.
