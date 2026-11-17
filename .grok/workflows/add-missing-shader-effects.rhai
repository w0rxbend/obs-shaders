let meta = #{
    name: "add-missing-shader-effects",
    description: "Write the missing .effect file in each shader folder that only has media/.gitkeep",
    when_to_use: "A shaders/<name>/ folder has no .effect file. Five writers at a time, then one check, then a repair pass. Does not commit or push.",
    phases: [
        #{ title: "Write", detail: "five new effects at a time" },
        #{ title: "Check", detail: "validator plus the OpenGL traps" },
        #{ title: "Repair", detail: "only the files that failed the check" },
    ],
};

let check_schema = #{
    "type": "object",
    "required": ["failed", "summary"],
    "properties": #{
        "failed": #{
            "type": "array",
            "maxItems": 30,
            "items": #{
                "type": "object",
                "required": ["folder", "reason"],
                "properties": #{
                    "folder": #{ "type": "string" },
                    "reason": #{ "type": "string" },
                },
            },
        },
        "summary": #{ "type": "string" },
    },
};

let queue = [
    #{ folder: "apocalyptic-dust", goal: "Slow dust and grit veiling the frame. A talking head stays recognizable." },
    #{ folder: "ash-particles", goal: "Slow falling ash flakes and a faint gray veil, thinner over the subject." },
    #{ folder: "bleached-magazine", goal: "Washed print: lifted blacks, weak color, a light halftone. The face stays readable." },
    #{ folder: "broken-glass", goal: "Impact cracks from the center, a small per-shard refraction, and a thin bright rim. The face stays in frame." },
    #{ folder: "burned-film-edges", goal: "Ragged char along the frame with a slow ember band. The center stays clear." },
    #{ folder: "cloud-shadow", goal: "Slow procedural clouds cast soft cool shadows. Daylight dims in patches. The face stays recognizable." },
    #{ folder: "crt-curved-mask", goal: "Mild CRT barrel, scanlines, and a dark rounded mask. The source stays readable." },
    #{ folder: "cyberpunk-panel", goal: "Inset HUD panel with a dark bezel, cyan-magenta corner brackets, and a slow scan. The face stays in place." },
    #{ folder: "deja-vu-echo", goal: "A faint delayed echo offset a few pixels at low opacity. The subject stays put." },
    #{ folder: "dissociation", goal: "A slight double image, mild desaturation, and a slow drift. The face stays recognizable." },
    #{ folder: "dream-fade", goal: "A slow soft fade toward a pastel wash. At the default it never goes full black or full white." },
    #{ folder: "fractal-tunnel", goal: "A mild tunnel warp from the center with a few repeating rings. The subject stays in frame." },
    #{ folder: "frosted-glass-panel", goal: "A frosted rectangular panel over part of the frame. The rest of the source stays clear." },
    #{ folder: "frosted-lens", goal: "Small-kernel diffusion through a milky lens, stronger away from center, with a cool highlight veil." },
    #{ folder: "lightning-flash", goal: "Short cool-white strikes. Between strikes the face is visible. At the default, full-frame flashes stay slower than 3 per second." },
    #{ folder: "liminal-desat", goal: "Drained color with a slight green-gray cast and a soft vignette. The subject stays recognizable." },
    #{ folder: "lucid-dream-bloom", goal: "Soft bloom and a pastel lift. The face stays sharp enough to read." },
    #{ folder: "nightmare-contrast", goal: "Deep shadows and hot highlights. No full-frame flash. The face stays readable." },
    #{ folder: "old-tv-screen", goal: "Scanlines, a slight barrel, soft chroma bleed, and a rounded dark bezel." },
    #{ folder: "overexposed-projector", goal: "Lifted exposure and a soft projector hotspot. At the default the frame is not clipped to white." },
    #{ folder: "portal-opening", goal: "A growing ring from the center. Inside the ring the source stays. Outside is a dim rim." },
    #{ folder: "sandstorm-grade", goal: "A warm blowing-sand grade and horizontal streaks. The subject stays recognizable." },
    #{ folder: "shockwave-ring", goal: "One ring expands from the center and refracts on the crest. Elsewhere the source stays put." },
    #{ folder: "sleep-paralysis", goal: "The center stays readable. The border crawls and sinks into a cold shadow." },
    #{ folder: "smoke-drift", goal: "Layered wisps drift upward and lightly veil the source. The subject stays recognizable." },
    #{ folder: "stream-alert-flash", goal: "A border pulse for a stream alert. At the default it is slower than 3 per second. The center stays clear." },
    #{ folder: "sun-flare", goal: "A sun disk, a warm halo, a streak, and a few ghosts. The source remains visible." },
    #{ folder: "synthwave-sunset", goal: "A magenta-orange sunset grade, a sun band, and a mild scan. The face stays recognizable." },
    #{ folder: "time-loop-echo", goal: "A few trailing echoes with a small UV offset. The subject stays put." },
    #{ folder: "wet-lens-streaks", goal: "Water beads and thin trails refract the image. The face between streaks stays clear." },
];

fn writer_prompt(folder, goal) {
    let path = "shaders/" + folder + "/" + folder + ".effect";
    let p = "";
    p += "Create one OBS Shaderfilter effect for live streaming. Work only in /home/worxbend/Projects/obs-shaders. ";
    p += "Write only this file: ";
    p += path;
    p += ". Read shaders/sepia-film/sepia-film.effect before you write, and copy that complete-effect shape. ";
    p += "Read tools/validate_all_shaderfilter_files.py and obey it. ";
    p += "If ";
    p += path;
    p += " already contains technique Draw and float4 mainImage, leave it unchanged. ";
    p += "Do not edit any other file. Do not edit shaders/premium-pack. Do not delete media/.gitkeep. ";
    p += "Git is forbidden. Do not run git add, git commit, git push, git reset, git restore, or git clean. ";
    p += "Do not run tools/generate_premium_shader_pack.py or tools/fix_shader_techniques.py. ";
    p += "Folder: ";
    p += folder;
    p += ". Visual goal: ";
    p += goal;
    p += " ";
    p += "The file is a complete effect. A .effect path is drawn with technique Draw and is not wrapped by the plugin. ";
    p += "Include uniform float4x4 ViewProj, uniform float2 uv_offset, and uniform float2 uv_scale with no initializer and no annotation. ";
    p += "VertData VSDefault must set vert_out.pos = mul(float4(v_in.pos.xyz, 1.0), ViewProj) and vert_out.uv = v_in.uv * uv_scale + uv_offset. ";
    p += "technique Draw must bind vertex_shader = VSDefault(v_in) and pixel_shader = mainImage(v_in). ";
    p += "Entry is float4 mainImage(VertData v_in) : TARGET. Sample with image.Sample(textureSampler, uv). ";
    p += "Declare uniform texture2d image. Declare elapsed_time and uv_size only if you use them, with no initializer and no annotation. ";
    p += "Every user float gets an annotation block: string label, string widget_type = slider, float minimum, float maximum, float step, then an initializer. ";
    p += "Keep sampled alpha. Saturate rgb on grades and stylized looks. ";
    p += "At most 12 image.Sample calls. Every loop bound is a numeric literal of 4 or less. No uniform loop bound. ";
    p += "Guard every divisor with max(denom, 0.001). Do not hardcode 1.78 or 16/9. Aspect is uv_size.x / max(uv_size.y, 1.0). ";
    p += "HLSL only. Forbidden tokens: texture2D, sampler2D, iChannel, iResolution, gl_FragCoord, gl_FragColor, fragCoord, mix(, fract(, atan2(, and the swizzles .xxx .yyy .zzz .www. ";
    p += "Use lerp, saturate, frac, and mul. No C-style casts. Write float(x) and int(x). ";
    p += "No attribute lines: no [loop], [branch], [unroll], [flatten], or [fastopt]. ";
    p += "Do not use these words as variable names: active, flat, cast, input, output, filter, sample. ";
    p += "GLSL pow needs the same type on both sides. A float3 base needs a float3 exponent, for example float3(curve, curve, curve). ";
    p += "At the written default a talking-head source stays recognizable. Full-frame black or white flashes stay slower than 3 per second. ";
    p += "After writing, run python3 tools/validate_all_shaderfilter_files.py. If the Errors section names your file, fix only your file and run it again. Then stop. ";
    p += "Reply with the path and one sentence on what you wrote.";
    p
}

fn repair_prompt(folder, reason) {
    let path = "shaders/" + folder + "/" + folder + ".effect";
    let p = "";
    p += "Fix one OBS Shaderfilter file in /home/worxbend/Projects/obs-shaders. Edit only ";
    p += path;
    p += ". Read it first. Read tools/validate_all_shaderfilter_files.py. ";
    p += "Git is forbidden. Do not edit any other file. ";
    p += "Failure: ";
    p += reason;
    p += " ";
    p += "Keep technique Draw, VSDefault, ViewProj, and vert_out.uv = v_in.uv * uv_scale + uv_offset. ";
    p += "No C-style casts. No [loop], [branch], or [unroll] lines. No variable named active, flat, or cast. ";
    p += "pow on a float3 uses a float3 exponent. At most 12 image.Sample calls. Loop bounds are numeric literals. ";
    p += "Then run python3 tools/validate_all_shaderfilter_files.py. Your file must not appear in Errors. Stop.";
    p
}

fn check_prompt() {
    let p = "";
    p += "Check the new OBS effects in /home/worxbend/Projects/obs-shaders. Do not edit any file. Do not run git. ";
    p += "Use the shell and read_file. Run python3 tools/validate_all_shaderfilter_files.py. ";
    p += "For each folder below, the file shaders/<folder>/<folder>.effect must exist and contain technique Draw, VSDefault, and v_in.uv * uv_scale + uv_offset. ";
    p += "Read each of those files. Fail a folder if the validator Errors section names it, if the file is missing, or if the code contains texture2D, mix(, fract(, atan2(, a C-style cast such as (float) or (int), an attribute line [loop] [branch] or [unroll], or a variable named active, flat, or cast. ";
    p += "Fail it if you see pow( used with a vector base and a single float exponent. ";
    p += "Folders: apocalyptic-dust, ash-particles, bleached-magazine, broken-glass, burned-film-edges, cloud-shadow, crt-curved-mask, cyberpunk-panel, deja-vu-echo, dissociation, dream-fade, fractal-tunnel, frosted-glass-panel, frosted-lens, lightning-flash, liminal-desat, lucid-dream-bloom, nightmare-contrast, old-tv-screen, overexposed-projector, portal-opening, sandstorm-grade, shockwave-ring, sleep-paralysis, smoke-drift, stream-alert-flash, sun-flare, synthwave-sunset, time-loop-echo, wet-lens-streaks. ";
    p += "Return failed as an array of objects with folder and reason. folder is the bare folder name, not a path. Use an empty array when every file passes. summary is one sentence.";
    p
}

fn take_batch(items, start) {
    let jobs = [];
    let k = 0;
    for item in items {
        if k >= start && k < start + 5 {
            jobs.push(item);
        }
        k += 1;
    }
    jobs
}

phase("Write");
let written = 0;
for start in [0, 5, 10, 15, 20, 25] {
    let slice = take_batch(queue, start);
    let jobs = [];
    for item in slice {
        jobs.push(#{
            prompt: writer_prompt(item.folder, item.goal),
            label: "write:" + item.folder,
            capability_mode: "all",
        });
    }
    if jobs.len() > 0 {
        let results = parallel(jobs);
        for r in results {
            if r != () && r.success {
                written += 1;
            }
        }
        log("write batch " + start.to_string() + " done");
    }
}

phase("Check");
let check = agent(check_prompt(), #{
    label: "check-new-effects",
    capability_mode: "execute",
    output_schema: check_schema,
});

let failed = [];
if check != () && check.success && check.output != () && type_of(check.output) == "map" && check.output.failed != () && type_of(check.output.failed) == "array" {
    for item in check.output.failed {
        if item != () && type_of(item) == "map" && item.folder != () && item.reason != () {
            let known = false;
            for spec in queue {
                if spec.folder == item.folder {
                    known = true;
                }
            }
            if known {
                failed.push(item);
            } else {
                log("dropped out-of-scope check result " + item.folder);
            }
        }
    }
} else {
    log("check returned no usable failed list");
}

phase("Repair");
let repaired = 0;
if failed.len() == 0 {
    log("no files to repair");
} else {
    log(failed.len().to_string() + " files need repair");
    for start in [0, 5, 10, 15, 20, 25] {
        let slice = take_batch(failed, start);
        let jobs = [];
        for item in slice {
            jobs.push(#{
                prompt: repair_prompt(item.folder, item.reason),
                label: "repair:" + item.folder,
                capability_mode: "all",
            });
        }
        if jobs.len() > 0 {
            let results = parallel(jobs);
            for r in results {
                if r != () && r.success {
                    repaired += 1;
                }
            }
        }
    }
}

complete(#{
    summary: "Wrote " + written.to_string() + " shader attempts. Repair calls: " + repaired.to_string() + ".",
    write_calls: written,
    repair_calls: repaired,
    failed_count: failed.len(),
});
