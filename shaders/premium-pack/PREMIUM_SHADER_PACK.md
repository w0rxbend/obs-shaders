# Premium OBS Shaderfilter Pack

Original single-pass `.effect` shaders for OBS Studio + obs-shaderfilter.
No third-party shader code is copied; these are fresh implementations based on visual principles.

Research anchors used for principles: OBS Shaderfilter user-defined shader examples, Libretro CRT/Slang shader documentation, and general HLSL-style single-pass shader practice.

## shader_001_strong_confidential_blur.effect

Category: Confidential / privacy pack
Effect: Strong confidential blur
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_001_strong_confidential_blur.effect
// Category: Confidential / privacy pack
// Effect: Strong confidential blur
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.080, 0.100, 0.120);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_002_pixelated_privacy_shield.effect

Category: Confidential / privacy pack
Effect: Pixelated privacy shield
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_002_pixelated_privacy_shield.effect
// Category: Confidential / privacy pack
// Effect: Pixelated privacy shield
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.850, 0.880, 0.900);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_003_frosted_glass_confidential_screen.effect

Category: Confidential / privacy pack
Effect: Frosted glass confidential screen
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_003_frosted_glass_confidential_screen.effect
// Category: Confidential / privacy pack
// Effect: Frosted glass confidential screen
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.620, 0.760, 0.860);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_004_adaptive_text_destroying_blur.effect

Category: Confidential / privacy pack
Effect: Adaptive text destroying blur
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_004_adaptive_text_destroying_blur.effect
// Category: Confidential / privacy pack
// Effect: Adaptive text destroying blur
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.080, 0.100, 0.120);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_005_redacted_document_look.effect

Category: Confidential / privacy pack
Effect: Redacted document look
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_005_redacted_document_look.effect
// Category: Confidential / privacy pack
// Effect: Redacted document look
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.850, 0.880, 0.900);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_006_security_blackout_pulse.effect

Category: Confidential / privacy pack
Effect: Security blackout pulse
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_006_security_blackout_pulse.effect
// Category: Confidential / privacy pack
// Effect: Security blackout pulse
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.620, 0.760, 0.860);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_007_privacy_noise_glass.effect

Category: Confidential / privacy pack
Effect: Privacy noise glass
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_007_privacy_noise_glass.effect
// Category: Confidential / privacy pack
// Effect: Privacy noise glass
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.080, 0.100, 0.120);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_008_corporate_presentation_blur.effect

Category: Confidential / privacy pack
Effect: Corporate presentation blur
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_008_corporate_presentation_blur.effect
// Category: Confidential / privacy pack
// Effect: Corporate presentation blur
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.850, 0.880, 0.900);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_009_password_manager_destroyer.effect

Category: Confidential / privacy pack
Effect: Password manager destroyer
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_009_password_manager_destroyer.effect
// Category: Confidential / privacy pack
// Effect: Password manager destroyer
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.620, 0.760, 0.860);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_010_emergency_privacy_wipe.effect

Category: Confidential / privacy pack
Effect: Emergency privacy wipe
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_010_emergency_privacy_wipe.effect
// Category: Confidential / privacy pack
// Effect: Emergency privacy wipe
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.080, 0.100, 0.120);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_011_subtle_breathing_rotation.effect

Category: Webcam motion pack
Effect: Subtle breathing rotation
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_011_subtle_breathing_rotation.effect
// Category: Webcam motion pack
// Effect: Subtle breathing rotation
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 11.0), cos(t * 0.73 + 0.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_012_floating_webcam_drift.effect

Category: Webcam motion pack
Effect: Floating webcam drift
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_012_floating_webcam_drift.effect
// Category: Webcam motion pack
// Effect: Floating webcam drift
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 12.0), cos(t * 0.73 + 1.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_013_handheld_micro_sway.effect

Category: Webcam motion pack
Effect: Handheld micro sway
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_013_handheld_micro_sway.effect
// Category: Webcam motion pack
// Effect: Handheld micro sway
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 13.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_014_paranormal_twitch.effect

Category: Webcam motion pack
Effect: Paranormal twitch
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_014_paranormal_twitch.effect
// Category: Webcam motion pack
// Effect: Paranormal twitch
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 14.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_015_vhs_frame_instability.effect

Category: Webcam motion pack
Effect: VHS frame instability
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_015_vhs_frame_instability.effect
// Category: Webcam motion pack
// Effect: VHS frame instability
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 15.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_016_slow_cinematic_zoom.effect

Category: Webcam motion pack
Effect: Slow cinematic zoom
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_016_slow_cinematic_zoom.effect
// Category: Webcam motion pack
// Effect: Slow cinematic zoom
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 7.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 16.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_017_pendulum_camera_swing.effect

Category: Webcam motion pack
Effect: Pendulum camera swing
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_017_pendulum_camera_swing.effect
// Category: Webcam motion pack
// Effect: Pendulum camera swing
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 17.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_018_dream_camera_drift.effect

Category: Webcam motion pack
Effect: Dream camera drift
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_018_dream_camera_drift.effect
// Category: Webcam motion pack
// Effect: Dream camera drift
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 0.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 18.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_019_earthquake_shake.effect

Category: Webcam motion pack
Effect: Earthquake shake
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_019_earthquake_shake.effect
// Category: Webcam motion pack
// Effect: Earthquake shake
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 19.0), cos(t * 0.73 + 8.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_020_security_camera_motor_pan.effect

Category: Webcam motion pack
Effect: Security camera motor pan
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_020_security_camera_motor_pan.effect
// Category: Webcam motion pack
// Effect: Security camera motor pan
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 20.0), cos(t * 0.73 + 9.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_021_teal_and_orange.effect

Category: Cinematic camera pack
Effect: Teal and orange
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_021_teal_and_orange.effect
// Category: Cinematic camera pack
// Effect: Teal and orange
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.100, 0.500, 0.620);
    float3 warm = float3(1.05, 0.88 + 1 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_022_bleach_bypass.effect

Category: Cinematic camera pack
Effect: Bleach bypass
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_022_bleach_bypass.effect
// Category: Cinematic camera pack
// Effect: Bleach bypass
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(1.000, 0.580, 0.250);
    float3 warm = float3(1.05, 0.88 + 2 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_023_cold_moonlight.effect

Category: Cinematic camera pack
Effect: Cold moonlight
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_023_cold_moonlight.effect
// Category: Cinematic camera pack
// Effect: Cold moonlight
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.480, 0.620, 0.920);
    float3 warm = float3(1.05, 0.88 + 3 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_024_supernatural_green_blue.effect

Category: Cinematic camera pack
Effect: Supernatural green blue
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_024_supernatural_green_blue.effect
// Category: Cinematic camera pack
// Effect: Supernatural green blue
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.100, 0.500, 0.620);
    float3 warm = float3(1.05, 0.88 + 0 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_025_rainy_noir.effect

Category: Cinematic camera pack
Effect: Rainy noir
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_025_rainy_noir.effect
// Category: Cinematic camera pack
// Effect: Rainy noir
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(1.000, 0.580, 0.250);
    float3 warm = float3(1.05, 0.88 + 1 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 001-025

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## shader_026_horror_red_shadows.effect

Category: Cinematic camera pack
Effect: Horror red shadows
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_026_horror_red_shadows.effect
// Category: Cinematic camera pack
// Effect: Horror red shadows
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.480, 0.620, 0.920);
    float3 warm = float3(1.05, 0.88 + 2 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_027_desert_dust_grade.effect

Category: Cinematic camera pack
Effect: Desert dust grade
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_027_desert_dust_grade.effect
// Category: Cinematic camera pack
// Effect: Desert dust grade
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.100, 0.500, 0.620);
    float3 warm = float3(1.05, 0.88 + 3 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_028_golden_hour.effect

Category: Cinematic camera pack
Effect: Golden hour
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_028_golden_hour.effect
// Category: Cinematic camera pack
// Effect: Golden hour
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(1.000, 0.580, 0.250);
    float3 warm = float3(1.05, 0.88 + 0 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_029_apocalyptic_gray.effect

Category: Cinematic camera pack
Effect: Apocalyptic gray
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_029_apocalyptic_gray.effect
// Category: Cinematic camera pack
// Effect: Apocalyptic gray
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.480, 0.620, 0.920);
    float3 warm = float3(1.05, 0.88 + 1 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_030_documentary_handheld_look.effect

Category: Cinematic camera pack
Effect: Documentary handheld look
Best for: webcam, game capture, video source, cinematic scenes
Visual inspiration: luminance-aware color remapping, contrast shaping, vignette, and animated grain
What makes it cool: it gives ordinary footage a clear emotional direction in one pass
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_030_documentary_handheld_look.effect
// Category: Cinematic camera pack
// Effect: Documentary handheld look
// Visual principle: luminance-aware color remapping, contrast shaping, vignette, and animated grain.
// What makes it cool: it gives ordinary footage a clear emotional direction in one pass.
// Suggested source type: webcam, game capture, video source, cinematic scenes
// Suggested shader-chain combinations: exposure controls -> this shader -> film grain
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float gray = luma3(color.rgb);
    float3 tint = float3(0.100, 0.500, 0.620);
    float3 warm = float3(1.05, 0.88 + 2 * 0.03, 0.72);
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
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_031_old_black_and_white_film.effect

Category: Retro analog pack
Effect: Old black and white film
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_031_old_black_and_white_film.effect
// Category: Retro analog pack
// Effect: Old black and white film
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.550, 0.700, 0.950);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_032_silent_movie_projector.effect

Category: Retro analog pack
Effect: Silent movie projector
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_032_silent_movie_projector.effect
// Category: Retro analog pack
// Effect: Silent movie projector
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.900, 0.200, 0.180);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_033_sepia_damaged_film.effect

Category: Retro analog pack
Effect: Sepia damaged film
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_033_sepia_damaged_film.effect
// Category: Retro analog pack
// Effect: Sepia damaged film
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.950, 0.880, 0.720);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_034_crt_scanlines.effect

Category: Retro analog pack
Effect: CRT scanlines
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_034_crt_scanlines.effect
// Category: Retro analog pack
// Effect: CRT scanlines
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.550, 0.700, 0.950);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_035_vhs_tracking_damage.effect

Category: Retro analog pack
Effect: VHS tracking damage
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_035_vhs_tracking_damage.effect
// Category: Retro analog pack
// Effect: VHS tracking damage
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.900, 0.200, 0.180);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_036_ntsc_color_bleed.effect

Category: Retro analog pack
Effect: NTSC color bleed
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_036_ntsc_color_bleed.effect
// Category: Retro analog pack
// Effect: NTSC color bleed
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.950, 0.880, 0.720);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_037_pal_phase_shift.effect

Category: Retro analog pack
Effect: PAL phase shift
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_037_pal_phase_shift.effect
// Category: Retro analog pack
// Effect: PAL phase shift
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.550, 0.700, 0.950);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_038_interlaced_jitter.effect

Category: Retro analog pack
Effect: Interlaced jitter
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_038_interlaced_jitter.effect
// Category: Retro analog pack
// Effect: Interlaced jitter
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.900, 0.200, 0.180);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_039_tape_wrinkle.effect

Category: Retro analog pack
Effect: Tape wrinkle
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_039_tape_wrinkle.effect
// Category: Retro analog pack
// Effect: Tape wrinkle
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.950, 0.880, 0.720);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_040_burned_film_edges.effect

Category: Retro analog pack
Effect: Burned film edges
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_040_burned_film_edges.effect
// Category: Retro analog pack
// Effect: Burned film edges
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.550, 0.700, 0.950);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_041_haunted_green_shadows.effect

Category: Horror / supernatural pack
Effect: Haunted green shadows
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_041_haunted_green_shadows.effect
// Category: Horror / supernatural pack
// Effect: Haunted green shadows
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.080, 0.020, 0.120);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_042_ghost_double_exposure.effect

Category: Horror / supernatural pack
Effect: Ghost double exposure
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_042_ghost_double_exposure.effect
// Category: Horror / supernatural pack
// Effect: Ghost double exposure
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.150, 0.380, 0.220);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_043_possession_pulse.effect

Category: Horror / supernatural pack
Effect: Possession pulse
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_043_possession_pulse.effect
// Category: Horror / supernatural pack
// Effect: Possession pulse
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.850, 0.050, 0.040);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_044_demonic_red_contrast.effect

Category: Horror / supernatural pack
Effect: Demonic red contrast
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_044_demonic_red_contrast.effect
// Category: Horror / supernatural pack
// Effect: Demonic red contrast
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.080, 0.020, 0.120);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_045_foggy_cemetery.effect

Category: Horror / supernatural pack
Effect: Foggy cemetery
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_045_foggy_cemetery.effect
// Category: Horror / supernatural pack
// Effect: Foggy cemetery
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.150, 0.380, 0.220);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_046_sleep_paralysis_edges.effect

Category: Horror / supernatural pack
Effect: Sleep paralysis edges
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_046_sleep_paralysis_edges.effect
// Category: Horror / supernatural pack
// Effect: Sleep paralysis edges
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.850, 0.050, 0.040);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_047_cursed_vhs.effect

Category: Horror / supernatural pack
Effect: Cursed VHS
Best for: game capture, retro scenes, video source, screen capture
Visual inspiration: scanlines, field jitter, chroma drift, and time-varying tape damage
What makes it cool: it sells nostalgic hardware instability with cheap procedural math
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_047_cursed_vhs.effect
// Category: Horror / supernatural pack
// Effect: Cursed VHS
// Visual principle: scanlines, field jitter, chroma drift, and time-varying tape damage.
// What makes it cool: it sells nostalgic hardware instability with cheap procedural math.
// Suggested source type: game capture, retro scenes, video source, screen capture
// Suggested shader-chain combinations: this shader -> chromatic aberration -> vignette
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.900, 0.200, 0.180);
    float3 out_rgb = float3(rch, gch, bch) * scan;
    out_rgb = lerp(out_rgb, tint * luma3(out_rgb), 0.18 * intensity);
    out_rgb += noise * 0.08 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_048_blood_moon_grade.effect

Category: Horror / supernatural pack
Effect: Blood moon grade
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_048_blood_moon_grade.effect
// Category: Horror / supernatural pack
// Effect: Blood moon grade
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.150, 0.380, 0.220);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_049_ritual_vignette.effect

Category: Horror / supernatural pack
Effect: Ritual vignette
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_049_ritual_vignette.effect
// Category: Horror / supernatural pack
// Effect: Ritual vignette
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.850, 0.050, 0.040);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_050_spirit_camera_distortion.effect

Category: Horror / supernatural pack
Effect: Spirit camera distortion
Best for: webcam, horror games, video source, dramatic scenes
Visual inspiration: crushed shadows, color-biased darkness, pulse timing, and unstable edges
What makes it cool: it adds dread by making the frame feel reactive and contaminated
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: no
Code:

```hlsl
// Filename: shader_050_spirit_camera_distortion.effect
// Category: Horror / supernatural pack
// Effect: Spirit camera distortion
// Visual principle: crushed shadows, color-biased darkness, pulse timing, and unstable edges.
// What makes it cool: it adds dread by making the frame feel reactive and contaminated.
// Suggested source type: webcam, horror games, video source, dramatic scenes
// Suggested shader-chain combinations: this shader -> ghost double image -> dark vignette
// Performance cost: low
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float pulse = 0.5 + 0.5 * sin(elapsed_time * speed * 2.4);
    float edge = smoothstep(0.15, 0.82, length((uv - float2(center_x, center_y)) * float2(1.1, 1.0)));
    float gray = luma3(color.rgb);
    float3 curse = float3(0.080, 0.020, 0.120);
    float3 out_rgb = lerp(color.rgb, curse * (gray + 0.15), 0.45 * intensity);
    out_rgb = (out_rgb - 0.5) * (1.35 + pulse * 0.35 * amount) + 0.5;
    out_rgb *= 1.0 - edge * (0.55 + 0.20 * pulse) * intensity;
    out_rgb.r += pulse * 0.10 * intensity;
    out_rgb += (hash12(floor(uv * uv_size / 4.0) + floor(elapsed_time * 10.0)) - 0.5) * 0.05;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 026-050

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## shader_051_rgb_split_glitch.effect

Category: Cyberpunk / glitch pack
Effect: RGB split glitch
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_051_rgb_split_glitch.effect
// Category: Cyberpunk / glitch pack
// Effect: RGB split glitch
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.000, 0.900, 1.000);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_052_datamosh_block_shift.effect

Category: Cyberpunk / glitch pack
Effect: Datamosh block shift
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_052_datamosh_block_shift.effect
// Category: Cyberpunk / glitch pack
// Effect: Datamosh block shift
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(1.000, 0.000, 0.550);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_053_digital_tearing.effect

Category: Cyberpunk / glitch pack
Effect: Digital tearing
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_053_digital_tearing.effect
// Category: Cyberpunk / glitch pack
// Effect: Digital tearing
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.150, 1.000, 0.350);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_054_broken_signal.effect

Category: Cyberpunk / glitch pack
Effect: Broken signal
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_054_broken_signal.effect
// Category: Cyberpunk / glitch pack
// Effect: Broken signal
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.000, 0.900, 1.000);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_055_cyberpunk_neon_boost.effect

Category: Cyberpunk / glitch pack
Effect: Cyberpunk neon boost
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_055_cyberpunk_neon_boost.effect
// Category: Cyberpunk / glitch pack
// Effect: Cyberpunk neon boost
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(1.000, 0.000, 0.550);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_056_matrix_terminal_green.effect

Category: Cyberpunk / glitch pack
Effect: Matrix terminal green
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_056_matrix_terminal_green.effect
// Category: Cyberpunk / glitch pack
// Effect: Matrix terminal green
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.150, 1.000, 0.350);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_057_hologram_flicker.effect

Category: Cyberpunk / glitch pack
Effect: Hologram flicker
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_057_hologram_flicker.effect
// Category: Cyberpunk / glitch pack
// Effect: Hologram flicker
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.000, 0.900, 1.000);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_058_robot_vision.effect

Category: Cyberpunk / glitch pack
Effect: Robot vision
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_058_robot_vision.effect
// Category: Cyberpunk / glitch pack
// Effect: Robot vision
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(1.000, 0.000, 0.550);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_059_scanner_sweep.effect

Category: Cyberpunk / glitch pack
Effect: Scanner sweep
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_059_scanner_sweep.effect
// Category: Cyberpunk / glitch pack
// Effect: Scanner sweep
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.150, 1.000, 0.350);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_060_corrupted_codec.effect

Category: Cyberpunk / glitch pack
Effect: Corrupted codec
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_060_corrupted_codec.effect
// Category: Cyberpunk / glitch pack
// Effect: Corrupted codec
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(0.000, 0.900, 1.000);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_061_fisheye.effect

Category: Lens / distortion pack
Effect: Fisheye
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_061_fisheye.effect
// Category: Lens / distortion pack
// Effect: Fisheye
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 19.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 1.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_062_barrel_distortion.effect

Category: Lens / distortion pack
Effect: Barrel distortion
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_062_barrel_distortion.effect
// Category: Lens / distortion pack
// Effect: Barrel distortion
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 20.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 2.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_063_pincushion.effect

Category: Lens / distortion pack
Effect: Pincushion
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_063_pincushion.effect
// Category: Lens / distortion pack
// Effect: Pincushion
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 21.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 3.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_064_chromatic_aberration.effect

Category: Lens / distortion pack
Effect: Chromatic aberration
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_064_chromatic_aberration.effect
// Category: Lens / distortion pack
// Effect: Chromatic aberration
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 22.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 4.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_065_fake_3d_anaglyph.effect

Category: Lens / distortion pack
Effect: Fake 3D anaglyph
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_065_fake_3d_anaglyph.effect
// Category: Lens / distortion pack
// Effect: Fake 3D anaglyph
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 23.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 0.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_066_heat_haze.effect

Category: Lens / distortion pack
Effect: Heat haze
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_066_heat_haze.effect
// Category: Lens / distortion pack
// Effect: Heat haze
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 24.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 1.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_067_water_ripple.effect

Category: Lens / distortion pack
Effect: Water ripple
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_067_water_ripple.effect
// Category: Lens / distortion pack
// Effect: Water ripple
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 25.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 2.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_068_shockwave_ring.effect

Category: Lens / distortion pack
Effect: Shockwave ring
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_068_shockwave_ring.effect
// Category: Lens / distortion pack
// Effect: Shockwave ring
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 26.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 3.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_069_tunnel_warp.effect

Category: Lens / distortion pack
Effect: Tunnel warp
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_069_tunnel_warp.effect
// Category: Lens / distortion pack
// Effect: Tunnel warp
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 27.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 4.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_070_broken_glass_approximation.effect

Category: Lens / distortion pack
Effect: Broken glass approximation
Best for: screen capture, game capture, music visuals, alerts
Visual inspiration: channel separation, block displacement, horizontal tears, and quantized corruption
What makes it cool: it creates readable digital failure while keeping the source recognizable
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_070_broken_glass_approximation.effect
// Category: Lens / distortion pack
// Effect: Broken glass approximation
// Visual principle: channel separation, block displacement, horizontal tears, and quantized corruption.
// What makes it cool: it creates readable digital failure while keeping the source recognizable.
// Suggested source type: screen capture, game capture, music visuals, alerts
// Suggested shader-chain combinations: this shader -> RGB split -> digital noise
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 accent = float3(1.000, 0.000, 0.550);
    float3 out_rgb = lerp(float3(rch, gch, bch), accent, gate * 0.12 * intensity);
    out_rgb += (hash12(floor(uv * uv_size / 2.0) + floor(t * 22.0)) - 0.5) * 0.07 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_071_rounded_corners.effect

Category: Streamer branding pack
Effect: Rounded corners
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_071_rounded_corners.effect
// Category: Streamer branding pack
// Effect: Rounded corners
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = max(abs(p.x) * 0.86 + abs(p.y) * 0.50, abs(p.y)) - 0.43;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.880, 0.580) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_072_animated_neon_border.effect

Category: Streamer branding pack
Effect: Animated neon border
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_072_animated_neon_border.effect
// Category: Streamer branding pack
// Effect: Animated neon border
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = abs(p.x) + abs(p.y) - 0.58;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(0.050, 0.850, 1.000) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_073_soft_drop_shadow.effect

Category: Streamer branding pack
Effect: Soft drop shadow
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_073_soft_drop_shadow.effect
// Category: Streamer branding pack
// Effect: Soft drop shadow
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = max(abs(p.x) - 0.43, abs(p.y) - 0.39);
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.250, 0.750) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_074_glass_webcam_frame.effect

Category: Streamer branding pack
Effect: Glass webcam frame
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_074_glass_webcam_frame.effect
// Category: Streamer branding pack
// Effect: Glass webcam frame
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 20.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 4.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_075_polaroid_webcam.effect

Category: Streamer branding pack
Effect: Polaroid webcam
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_075_polaroid_webcam.effect
// Category: Streamer branding pack
// Effect: Polaroid webcam
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = length(p) - 0.46;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(0.050, 0.850, 1.000) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 051-075

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## shader_076_cyberpunk_panel.effect

Category: Streamer branding pack
Effect: Cyberpunk panel
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_076_cyberpunk_panel.effect
// Category: Streamer branding pack
// Effect: Cyberpunk panel
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 76.0), cos(t * 0.73 + 10.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_077_circular_crop.effect

Category: Streamer branding pack
Effect: Circular crop
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_077_circular_crop.effect
// Category: Streamer branding pack
// Effect: Circular crop
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = abs(p.x) + abs(p.y) - 0.58;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.880, 0.580) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_078_hexagon_crop.effect

Category: Streamer branding pack
Effect: Hexagon crop
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_078_hexagon_crop.effect
// Category: Streamer branding pack
// Effect: Hexagon crop
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = max(abs(p.x) - 0.43, abs(p.y) - 0.39);
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(0.050, 0.850, 1.000) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_079_torn_paper_mask.effect

Category: Streamer branding pack
Effect: Torn paper mask
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_079_torn_paper_mask.effect
// Category: Streamer branding pack
// Effect: Torn paper mask
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = length(p * float2(1.08, 0.92)) - 0.47 + jag * 0.035;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.250, 0.750) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_080_security_camera_overlay.effect

Category: Streamer branding pack
Effect: Security camera overlay
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_080_security_camera_overlay.effect
// Category: Streamer branding pack
// Effect: Security camera overlay
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = length(p) - 0.46;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.880, 0.580) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_081_kaleidoscope.effect

Category: Experimental art pack
Effect: Kaleidoscope
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_081_kaleidoscope.effect
// Category: Experimental art pack
// Effect: Kaleidoscope
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(1.000, 0.700, 0.200) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_082_spiral_warp.effect

Category: Experimental art pack
Effect: Spiral warp
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_082_spiral_warp.effect
// Category: Experimental art pack
// Effect: Spiral warp
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.200, 0.650, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_083_pixel_melt.effect

Category: Experimental art pack
Effect: Pixel melt
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_083_pixel_melt.effect
// Category: Experimental art pack
// Effect: Pixel melt
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.850, 0.300, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_084_liquid_metal.effect

Category: Experimental art pack
Effect: Liquid metal
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_084_liquid_metal.effect
// Category: Experimental art pack
// Effect: Liquid metal
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(1.000, 0.700, 0.200) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_085_posterize.effect

Category: Experimental art pack
Effect: Posterize
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_085_posterize.effect
// Category: Experimental art pack
// Effect: Posterize
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.200, 0.650, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_086_comic_halftone.effect

Category: Experimental art pack
Effect: Comic halftone
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_086_comic_halftone.effect
// Category: Experimental art pack
// Effect: Comic halftone
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.850, 0.300, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_087_pencil_sketch.effect

Category: Experimental art pack
Effect: Pencil sketch
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_087_pencil_sketch.effect
// Category: Experimental art pack
// Effect: Pencil sketch
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(1.000, 0.700, 0.200) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_088_ink_outline.effect

Category: Experimental art pack
Effect: Ink outline
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_088_ink_outline.effect
// Category: Experimental art pack
// Effect: Ink outline
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.200, 0.650, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_089_oil_paint_approximation.effect

Category: Experimental art pack
Effect: Oil paint approximation
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_089_oil_paint_approximation.effect
// Category: Experimental art pack
// Effect: Oil paint approximation
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.850, 0.300, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_090_watercolor_wash.effect

Category: Experimental art pack
Effect: Watercolor wash
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_090_watercolor_wash.effect
// Category: Experimental art pack
// Effect: Watercolor wash
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(1.000, 0.700, 0.200) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_091_rain_on_glass.effect

Category: Weather / atmosphere pack
Effect: Rain on glass
Best for: webcam, game capture, image source, video source
Visual inspiration: radial or directional UV warping with small compensating zoom
What makes it cool: it bends the camera feed like a lens or energy field while preserving the source
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_091_rain_on_glass.effect
// Category: Weather / atmosphere pack
// Effect: Rain on glass
// Visual principle: radial or directional UV warping with small compensating zoom.
// What makes it cool: it bends the camera feed like a lens or energy field while preserving the source.
// Suggested source type: webcam, game capture, image source, video source
// Suggested shader-chain combinations: this shader -> chromatic aberration -> bloom
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 center = float2(center_x, center_y);
    float2 p = uv - center;
    float t = elapsed_time * speed;
    float radius = length(p);
    float wave = sin(radius * 25.0 - t * 3.0) * 0.025 * amount * intensity;
    float bend = dot(p, p) * (0.22 + 1.0 * 0.025) * amount;
    float2 dir = normalize(p + float2(0.0001, 0.0002));
    float2 uv = center + p / (1.04 + abs(wave) + bend * 0.2) + dir * wave + p * bend;
    float4 warped = image.Sample(textureSampler, clamp(uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_092_snow_overlay.effect

Category: Weather / atmosphere pack
Effect: Snow overlay
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_092_snow_overlay.effect
// Category: Weather / atmosphere pack
// Effect: Snow overlay
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = abs(p.x) + abs(p.y) - 0.58;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(1.000, 0.880, 0.580) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_093_smoke_drift.effect

Category: Weather / atmosphere pack
Effect: Smoke drift
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_093_smoke_drift.effect
// Category: Weather / atmosphere pack
// Effect: Smoke drift
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 93.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_094_ash_particles.effect

Category: Weather / atmosphere pack
Effect: Ash particles
Best for: webcam, image source, video source, VJ visuals
Visual inspiration: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling
What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: yes
Code:

```hlsl
// Filename: shader_094_ash_particles.effect
// Category: Weather / atmosphere pack
// Effect: Ash particles
// Visual principle: stylized color quantization, edge emphasis, pattern overlays, and painterly sampling.
// What makes it cool: it makes live footage look intentionally illustrated instead of merely filtered.
// Suggested source type: webcam, image source, video source, VJ visuals
// Suggested shader-chain combinations: this shader -> posterize or halftone -> light vignette
// Performance cost: medium
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 ink = lerp(quant, float3(0.200, 0.650, 1.000) * (0.25 + gray), 0.22 * intensity);
    ink = lerp(ink, float3(0.02, 0.02, 0.025), saturate(edge * 2.5 * intensity));
    ink += dots * 0.035 * intensity;
    return float4(saturate(ink), alphaOut(c.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_095_lightning_flash.effect

Category: Weather / atmosphere pack
Effect: Lightning flash
Best for: webcam, game capture, video source, image source
Visual inspiration: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses
What makes it cool: it adds environmental storytelling without external image textures
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_095_lightning_flash.effect
// Category: Weather / atmosphere pack
// Effect: Lightning flash
// Visual principle: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses.
// What makes it cool: it adds environmental storytelling without external image textures.
// Suggested source type: webcam, game capture, video source, image source
// Suggested shader-chain combinations: this shader -> cinematic grade -> lens dirt
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3(0.650, 0.550, 0.350);
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_096_frosted_lens.effect

Category: Weather / atmosphere pack
Effect: Frosted lens
Best for: webcam, game capture, video source, image source
Visual inspiration: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses
What makes it cool: it adds environmental storytelling without external image textures
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_096_frosted_lens.effect
// Category: Weather / atmosphere pack
// Effect: Frosted lens
// Visual principle: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses.
// What makes it cool: it adds environmental storytelling without external image textures.
// Suggested source type: webcam, game capture, video source, image source
// Suggested shader-chain combinations: this shader -> cinematic grade -> lens dirt
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3(0.700, 0.820, 1.000);
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_097_wet_lens_streaks.effect

Category: Weather / atmosphere pack
Effect: Wet lens streaks
Best for: webcam, game capture, video source, image source
Visual inspiration: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses
What makes it cool: it adds environmental storytelling without external image textures
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_097_wet_lens_streaks.effect
// Category: Weather / atmosphere pack
// Effect: Wet lens streaks
// Visual principle: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses.
// What makes it cool: it adds environmental storytelling without external image textures.
// Suggested source type: webcam, game capture, video source, image source
// Suggested shader-chain combinations: this shader -> cinematic grade -> lens dirt
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3(0.950, 0.930, 0.860);
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_098_sandstorm.effect

Category: Weather / atmosphere pack
Effect: Sandstorm
Best for: webcam, game capture, video source, image source
Visual inspiration: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses
What makes it cool: it adds environmental storytelling without external image textures
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_098_sandstorm.effect
// Category: Weather / atmosphere pack
// Effect: Sandstorm
// Visual principle: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses.
// What makes it cool: it adds environmental storytelling without external image textures.
// Suggested source type: webcam, game capture, video source, image source
// Suggested shader-chain combinations: this shader -> cinematic grade -> lens dirt
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3(0.650, 0.550, 0.350);
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_099_cloud_shadow.effect

Category: Weather / atmosphere pack
Effect: Cloud shadow
Best for: webcam camera source, streamer layouts, browser source
Visual inspiration: alpha-safe geometric masking, decorative frames, and procedural edge treatment
What makes it cool: it turns a plain source into a branded layout element
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_099_cloud_shadow.effect
// Category: Weather / atmosphere pack
// Effect: Cloud shadow
// Visual principle: alpha-safe geometric masking, decorative frames, and procedural edge treatment.
// What makes it cool: it turns a plain source into a branded layout element.
// Suggested source type: webcam camera source, streamer layouts, browser source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> animated border
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float2 p = uv - float2(center_x, center_y);
    float jag = hash12(floor(uv * 48.0) + floor(elapsed_time * speed)) - 0.5;
    float d = length(p * float2(1.08, 0.92)) - 0.47 + jag * 0.035;
    float mask = 1.0 - smoothstep(0.0, 0.018 * amount, d);
    float border = 1.0 - smoothstep(0.018, 0.055, abs(d));
    float pulse = 0.55 + 0.45 * sin(elapsed_time * speed * 2.0);
    float3 frame = float3(0.050, 0.850, 1.000) * (0.75 + 0.45 * pulse);
    float3 out_rgb = lerp(color.rgb, frame, saturate(border * intensity));
    float alpha = color.a * mask;
    [branch]
    if (!preserve_alpha)
    {
        out_rgb = lerp(float3(0.02, 0.025, 0.03), out_rgb, mask);
        alpha = 1.0;
    }
    return float4(saturate(out_rgb), alpha * saturate(opacity));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_100_sun_flare_approximation.effect

Category: Weather / atmosphere pack
Effect: Sun flare approximation
Best for: webcam, game capture, video source, image source
Visual inspiration: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses
What makes it cool: it adds environmental storytelling without external image textures
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_100_sun_flare_approximation.effect
// Category: Weather / atmosphere pack
// Effect: Sun flare approximation
// Visual principle: procedural atmospheric layers, moving shadows, lens streaks, and brightness pulses.
// What makes it cool: it adds environmental storytelling without external image textures.
// Suggested source type: webcam, game capture, video source, image source
// Suggested shader-chain combinations: this shader -> cinematic grade -> lens dirt
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float streak = pow(saturate(1.0 - abs(frac(uv.x * 28.0 + uv.y * 7.0 - t * 1.6) - 0.5) * 20.0), 2.0);
    float flakes = step(0.985 - amount * 0.006, hash12(floor((uv + float2(0.0, t * 0.05)) * uv_size / 6.0)));
    float shadow = 0.75 + 0.25 * sin(uv.x * 5.0 + uv.y * 3.0 + t * 0.7);
    float2 warp = float2(streak * 0.006 * amount, flakes * 0.003) * intensity;
    float4 src = image.Sample(textureSampler, clamp(uv + warp, 0.0, 1.0));
    float3 atmosphere = float3(0.950, 0.930, 0.860);
    float3 out_rgb = src.rgb * lerp(1.0, shadow, 0.20 * intensity);
    out_rgb = lerp(out_rgb, atmosphere, 0.12 * amount);
    out_rgb += (streak + flakes) * atmosphere * 0.35 * intensity;
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 076-100

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## shader_101_beat_pulse_tunnel.effect

Category: VJ / music video expansion
Effect: Beat pulse tunnel
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_101_beat_pulse_tunnel.effect
// Category: VJ / music video expansion
// Effect: Beat pulse tunnel
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 101.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_102_neon_kaleido_wash.effect

Category: VJ / music video expansion
Effect: Neon kaleido wash
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_102_neon_kaleido_wash.effect
// Category: VJ / music video expansion
// Effect: Neon kaleido wash
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 102.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_103_prism_trail_split.effect

Category: VJ / music video expansion
Effect: Prism trail split
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_103_prism_trail_split.effect
// Category: VJ / music video expansion
// Effect: Prism trail split
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 103.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_104_laser_grid_sweep.effect

Category: VJ / music video expansion
Effect: Laser grid sweep
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_104_laser_grid_sweep.effect
// Category: VJ / music video expansion
// Effect: Laser grid sweep
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 104.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_105_strobe_smear.effect

Category: VJ / music video expansion
Effect: Strobe smear
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_105_strobe_smear.effect
// Category: VJ / music video expansion
// Effect: Strobe smear
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 105.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_106_bass_glow_throb.effect

Category: VJ / music video expansion
Effect: Bass glow throb
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_106_bass_glow_throb.effect
// Category: VJ / music video expansion
// Effect: Bass glow throb
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 7.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 106.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_107_spectral_color_split.effect

Category: VJ / music video expansion
Effect: Spectral color split
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_107_spectral_color_split.effect
// Category: VJ / music video expansion
// Effect: Spectral color split
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 107.0), cos(t * 0.73 + 8.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_108_liquid_club_wash.effect

Category: VJ / music video expansion
Effect: Liquid club wash
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_108_liquid_club_wash.effect
// Category: VJ / music video expansion
// Effect: Liquid club wash
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 0.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 108.0), cos(t * 0.73 + 9.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_109_mirror_stage_flip.effect

Category: VJ / music video expansion
Effect: Mirror stage flip
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_109_mirror_stage_flip.effect
// Category: VJ / music video expansion
// Effect: Mirror stage flip
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 109.0), cos(t * 0.73 + 10.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_110_rave_posterize.effect

Category: VJ / music video expansion
Effect: Rave posterize
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_110_rave_posterize.effect
// Category: VJ / music video expansion
// Effect: Rave posterize
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 110.0), cos(t * 0.73 + 0.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_111_focus_spotlight.effect

Category: Screen capture utility expansion
Effect: Focus spotlight
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_111_focus_spotlight.effect
// Category: Screen capture utility expansion
// Effect: Focus spotlight
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 111.0), cos(t * 0.73 + 1.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_112_edge_readability_boost.effect

Category: Screen capture utility expansion
Effect: Edge readability boost
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_112_edge_readability_boost.effect
// Category: Screen capture utility expansion
// Effect: Edge readability boost
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 112.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_113_dashboard_glass_dim.effect

Category: Screen capture utility expansion
Effect: Dashboard glass dim
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_113_dashboard_glass_dim.effect
// Category: Screen capture utility expansion
// Effect: Dashboard glass dim
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 113.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_114_terminal_phosphor_glow.effect

Category: Screen capture utility expansion
Effect: Terminal phosphor glow
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_114_terminal_phosphor_glow.effect
// Category: Screen capture utility expansion
// Effect: Terminal phosphor glow
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 114.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_115_browser_privacy_haze.effect

Category: Screen capture utility expansion
Effect: Browser privacy haze
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_115_browser_privacy_haze.effect
// Category: Screen capture utility expansion
// Effect: Browser privacy haze
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.080, 0.100, 0.120);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_116_presentation_spotlight.effect

Category: Screen capture utility expansion
Effect: Presentation spotlight
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_116_presentation_spotlight.effect
// Category: Screen capture utility expansion
// Effect: Presentation spotlight
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 116.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_117_code_rain_overlay.effect

Category: Screen capture utility expansion
Effect: Code rain overlay
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_117_code_rain_overlay.effect
// Category: Screen capture utility expansion
// Effect: Code rain overlay
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 0.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 117.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_118_document_scanner_pass.effect

Category: Screen capture utility expansion
Effect: Document scanner pass
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_118_document_scanner_pass.effect
// Category: Screen capture utility expansion
// Effect: Document scanner pass
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 118.0), cos(t * 0.73 + 8.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_119_window_focus_vignette.effect

Category: Screen capture utility expansion
Effect: Window focus vignette
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_119_window_focus_vignette.effect
// Category: Screen capture utility expansion
// Effect: Window focus vignette
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 119.0), cos(t * 0.73 + 9.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_120_cursor_area_magnifier.effect

Category: Screen capture utility expansion
Effect: Cursor area magnifier
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_120_cursor_area_magnifier.effect
// Category: Screen capture utility expansion
// Effect: Cursor area magnifier
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 120.0), cos(t * 0.73 + 10.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_121_soft_skin_bloom.effect

Category: Portrait / beauty expansion
Effect: Soft skin bloom
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_121_soft_skin_bloom.effect
// Category: Portrait / beauty expansion
// Effect: Soft skin bloom
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 121.0), cos(t * 0.73 + 0.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_122_warm_portrait_lift.effect

Category: Portrait / beauty expansion
Effect: Warm portrait lift
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_122_warm_portrait_lift.effect
// Category: Portrait / beauty expansion
// Effect: Warm portrait lift
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 122.0), cos(t * 0.73 + 1.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_123_cool_studio_webcam.effect

Category: Portrait / beauty expansion
Effect: Cool studio webcam
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_123_cool_studio_webcam.effect
// Category: Portrait / beauty expansion
// Effect: Cool studio webcam
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 123.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_124_beauty_vignette.effect

Category: Portrait / beauty expansion
Effect: Beauty vignette
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_124_beauty_vignette.effect
// Category: Portrait / beauty expansion
// Effect: Beauty vignette
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 7.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 124.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_125_tiktok_soft_glam.effect

Category: Portrait / beauty expansion
Effect: TikTok soft glam
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_125_tiktok_soft_glam.effect
// Category: Portrait / beauty expansion
// Effect: TikTok soft glam
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 125.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 101-125

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## shader_126_instagram_peach_fade.effect

Category: Portrait / beauty expansion
Effect: Instagram peach fade
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_126_instagram_peach_fade.effect
// Category: Portrait / beauty expansion
// Effect: Instagram peach fade
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 0.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 126.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_127_smartphone_hdr_selfie.effect

Category: Portrait / beauty expansion
Effect: Smartphone HDR selfie
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_127_smartphone_hdr_selfie.effect
// Category: Portrait / beauty expansion
// Effect: Smartphone HDR selfie
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 127.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_128_old_laptop_webcam.effect

Category: Portrait / beauty expansion
Effect: Old laptop webcam
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_128_old_laptop_webcam.effect
// Category: Portrait / beauty expansion
// Effect: Old laptop webcam
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 128.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_129_news_anchor_clarity.effect

Category: Portrait / beauty expansion
Effect: News anchor clarity
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_129_news_anchor_clarity.effect
// Category: Portrait / beauty expansion
// Effect: News anchor clarity
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 129.0), cos(t * 0.73 + 8.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_130_low_light_webcam_rescue.effect

Category: Portrait / beauty expansion
Effect: Low light webcam rescue
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_130_low_light_webcam_rescue.effect
// Category: Portrait / beauty expansion
// Effect: Low light webcam rescue
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 130.0), cos(t * 0.73 + 9.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_131_arcane_mana_shimmer.effect

Category: Sci-fi / fantasy expansion
Effect: Arcane mana shimmer
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_131_arcane_mana_shimmer.effect
// Category: Sci-fi / fantasy expansion
// Effect: Arcane mana shimmer
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 131.0), cos(t * 0.73 + 10.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_132_portal_edge_glow.effect

Category: Sci-fi / fantasy expansion
Effect: Portal edge glow
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_132_portal_edge_glow.effect
// Category: Sci-fi / fantasy expansion
// Effect: Portal edge glow
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 132.0), cos(t * 0.73 + 0.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_133_dragon_fire_heat.effect

Category: Sci-fi / fantasy expansion
Effect: Dragon fire heat
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_133_dragon_fire_heat.effect
// Category: Sci-fi / fantasy expansion
// Effect: Dragon fire heat
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 7.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 133.0), cos(t * 0.73 + 1.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_134_ice_magic_border.effect

Category: Sci-fi / fantasy expansion
Effect: Ice magic border
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_134_ice_magic_border.effect
// Category: Sci-fi / fantasy expansion
// Effect: Ice magic border
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 134.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_135_poison_curse_green.effect

Category: Sci-fi / fantasy expansion
Effect: Poison curse green
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_135_poison_curse_green.effect
// Category: Sci-fi / fantasy expansion
// Effect: Poison curse green
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 0.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 135.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_136_holy_light_rays.effect

Category: Sci-fi / fantasy expansion
Effect: Holy light rays
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_136_holy_light_rays.effect
// Category: Sci-fi / fantasy expansion
// Effect: Holy light rays
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.93;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 136.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_137_shadow_realm_wash.effect

Category: Sci-fi / fantasy expansion
Effect: Shadow realm wash
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_137_shadow_realm_wash.effect
// Category: Sci-fi / fantasy expansion
// Effect: Shadow realm wash
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.01;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 137.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_138_space_monitor_tint.effect

Category: Sci-fi / fantasy expansion
Effect: Space monitor tint
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_138_space_monitor_tint.effect
// Category: Sci-fi / fantasy expansion
// Effect: Space monitor tint
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.09;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 138.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_139_alien_scanner_bands.effect

Category: Sci-fi / fantasy expansion
Effect: Alien scanner bands
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_139_alien_scanner_bands.effect
// Category: Sci-fi / fantasy expansion
// Effect: Alien scanner bands
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.17;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 139.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_140_forcefield_ripple.effect

Category: Sci-fi / fantasy expansion
Effect: Forcefield ripple
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_140_forcefield_ripple.effect
// Category: Sci-fi / fantasy expansion
// Effect: Forcefield ripple
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.85;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 140.0), cos(t * 0.73 + 8.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_141_fullscreen_melt.effect

Category: Extreme / transition expansion
Effect: Fullscreen melt
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_141_fullscreen_melt.effect
// Category: Extreme / transition expansion
// Effect: Fullscreen melt
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.93;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 141.0), cos(t * 0.73 + 9.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_142_rgb_explosion.effect

Category: Extreme / transition expansion
Effect: RGB explosion
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_142_rgb_explosion.effect
// Category: Extreme / transition expansion
// Effect: RGB explosion
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.01;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 7.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 142.0), cos(t * 0.73 + 10.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_143_whiteout_flash.effect

Category: Extreme / transition expansion
Effect: Whiteout flash
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_143_whiteout_flash.effect
// Category: Extreme / transition expansion
// Effect: Whiteout flash
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.09;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 8.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 143.0), cos(t * 0.73 + 0.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_144_blackout_pulse.effect

Category: Extreme / transition expansion
Effect: Blackout pulse
Best for: screen capture, browser source, IDEs, dashboards, documents
Visual inspiration: large-kernel signal destruction with pixel quantization and procedural privacy noise
What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: medium
Alpha safe: no
Code:

```hlsl
// Filename: shader_144_blackout_pulse.effect
// Category: Extreme / transition expansion
// Effect: Blackout pulse
// Visual principle: large-kernel signal destruction with pixel quantization and procedural privacy noise.
// What makes it cool: it hides readable details but leaves the audience aware that real content exists underneath.
// Suggested source type: screen capture, browser source, IDEs, dashboards, documents
// Suggested shader-chain combinations: soft vignette -> this shader -> subtle noise or scanline overlay
// Performance cost: medium
// Alpha safe: no
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.17;
uniform float speed = 1.37;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = false;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
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
    float3 tint = float3(0.620, 0.760, 0.860);
    float3 protected_rgb = lerp(blur.rgb, tint * (0.45 + gray * 0.55), 0.35 * intensity);
    protected_rgb = lerp(protected_rgb, float3(gray, gray, gray), 0.35);
    protected_rgb += (grain - 0.5) * 0.22 * intensity;
    protected_rgb *= 1.0 - 0.20 * saturate(intensity);
    float blend = saturate(0.82 + amount * 0.16);
    float3 out_rgb = lerp(color.rgb, protected_rgb, blend);
    return float4(saturate(out_rgb), alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_145_negative_inversion.effect

Category: Extreme / transition expansion
Effect: Negative inversion
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_145_negative_inversion.effect
// Category: Extreme / transition expansion
// Effect: Negative inversion
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 0.85;
uniform float speed = 1.55;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 1.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 145.0), cos(t * 0.73 + 2.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_146_solarize_threshold.effect

Category: Extreme / transition expansion
Effect: Solarize threshold
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_146_solarize_threshold.effect
// Category: Extreme / transition expansion
// Effect: Solarize threshold
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 0.93;
uniform float speed = 1.73;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 2.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 146.0), cos(t * 0.73 + 3.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_147_thermal_false_color.effect

Category: Extreme / transition expansion
Effect: Thermal false color
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_147_thermal_false_color.effect
// Category: Extreme / transition expansion
// Effect: Thermal false color
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 1.01;
uniform float speed = 0.65;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.21) + sin(t * 0.37 + 3.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 147.0), cos(t * 0.73 + 4.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_148_deep_fried_meme.effect

Category: Extreme / transition expansion
Effect: Deep fried meme
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_148_deep_fried_meme.effect
// Category: Extreme / transition expansion
// Effect: Deep fried meme
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.15;
uniform float amount = 1.09;
uniform float speed = 0.83;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.70) + sin(t * 0.37 + 4.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 148.0), cos(t * 0.73 + 5.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_149_jpeg_artifact_approximation.effect

Category: Extreme / transition expansion
Effect: JPEG artifact approximation
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_149_jpeg_artifact_approximation.effect
// Category: Extreme / transition expansion
// Effect: JPEG artifact approximation
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.30;
uniform float amount = 1.17;
uniform float speed = 1.01;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 0.87) + sin(t * 0.37 + 5.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 149.0), cos(t * 0.73 + 6.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```

## shader_150_corrupted_codec_blocks.effect

Category: Extreme / transition expansion
Effect: Corrupted codec blocks
Best for: webcam camera source, image source, video source
Visual inspiration: animated UV camera transforms around a stable center point
What makes it cool: it makes a static source feel physically alive without moving the OBS source transform
Controls: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha
Performance: low
Alpha safe: yes
Code:

```hlsl
// Filename: shader_150_corrupted_codec_blocks.effect
// Category: Extreme / transition expansion
// Effect: Corrupted codec blocks
// Visual principle: animated UV camera transforms around a stable center point.
// What makes it cool: it makes a static source feel physically alive without moving the OBS source transform.
// Suggested source type: webcam camera source, image source, video source
// Suggested shader-chain combinations: this shader -> soft drop shadow -> color grade
// Performance cost: low
// Alpha safe: yes
// Limitations: single-pass approximation; no external textures; heavy multi-pass reference looks are simplified for live OBS use.
// OBS Shaderfilter compatibility notes: HLSL-like .effect syntax, mainImage entry point, image.Sample(textureSampler, uv), no GLSL/Shadertoy-only uniforms.

uniform float4x4 ViewProj;
uniform texture2d image;
uniform float elapsed_time;
uniform float2 uv_pixel_interval;
uniform float2 uv_size;

uniform float intensity = 1.00;
uniform float amount = 0.85;
uniform float speed = 1.19;
uniform float center_x = 0.5;
uniform float center_y = 0.5;
uniform float opacity = 1.0;
uniform bool preserve_alpha = true;

sampler_state textureSampler {
    Filter = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
};

VertData VSDefault(VertData v_in)
{
    VertData vert_out;
    vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj);
    vert_out.uv = v_in.uv;
    return vert_out;
}

float hash12(float2 p)
{
    float3 p3 = frac(float3(p.x, p.y, p.x) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return frac((p3.x + p3.y) * p3.z);
}

float luma3(float3 c)
{
    return dot(c, float3(0.299, 0.587, 0.114));
}

float2 rotate2d(float2 p, float a)
{
    float s = sin(a);
    float c = cos(a);
    return float2(p.x * c - p.y * s, p.x * s + p.y * c);
}

float alphaOut(float sampled_alpha)
{
    float a = sampled_alpha;
    [branch]
    if (!preserve_alpha)
    {
        a = 1.0;
    }
    return a * saturate(opacity);
}

float4 mainImage(VertData v_in) : TARGET
{
    float2 uv = v_in.uv;
    float4 color = image.Sample(textureSampler, uv);
    float t = elapsed_time * speed;
    float2 center = float2(center_x, center_y);
    float angle = (sin(t * 1.04) + sin(t * 0.37 + 6.0) * 0.45) * 0.018 * amount * intensity;
    float2 drift = float2(sin(t * 0.91 + 150.0), cos(t * 0.73 + 7.0)) * 0.018 * amount * intensity;
    float zoom = 1.04 + abs(angle) * 1.4 + length(drift) * 2.0;
    float2 p = (uv - center) / zoom;
    float2 warped_uv = center + rotate2d(p, angle) - drift;
    float4 warped = image.Sample(textureSampler, clamp(warped_uv, float2(0.0, 0.0), float2(1.0, 1.0)));
    return float4(warped.rgb, alphaOut(color.a));
}

technique Draw
{
    pass
    {
        vertex_shader = VSDefault(v_in);
        pixel_shader = mainImage(v_in);
    }
}
```


### Compile-test checklist: shaders 126-150

- Load each `.effect` in OBS Shaderfilter as a user-defined shader.
- Confirm `mainImage(VertData v_in) : TARGET` compiles without GLSL-only symbol errors.
- Scrub `intensity`, `amount`, `speed`, `center_x`, `center_y`, and `opacity`.
- Verify alpha behavior on a webcam source and a full-screen source.
- Watch GPU load for 60 seconds at 1080p and 1440p; none of these shaders use external textures or more than five neighbor taps.
- Chain with one light grade or vignette shader and confirm no unexpected black corners.

## Final Known OBS Shaderfilter Pitfalls

- Use `.effect` files for this pack and load them through the Shaderfilter user-defined shader UI.
- Keep `image.Sample(textureSampler, uv)` syntax; `texture2D`, `sampler2D`, `iChannel`, `iResolution`, and `gl_FragCoord` are intentionally absent.
- OBS exposes uniforms as controls, but unsupported uniform types or typoed names can silently produce confusing UI.
- Multi-pass CRT and bloom references from other ecosystems are simplified here because Shaderfilter user shaders are usually single-pass source filters.
- Clamp or compensate UV warps with zoom to avoid black corners; these shaders clamp sampler addressing and most warps add zoom internally.
- Alpha masks should be tested on transparent webcam/browser sources and on full-screen captures because alpha behavior depends on the OBS source chain.
- If a shader appears unchanged, raise `intensity` and `amount`, then confirm `elapsed_time` is updating by adjusting `speed`.
- Heavy chains of multiple medium-cost shaders can cost more than one complex shader; profile the final OBS scene at the target canvas resolution.