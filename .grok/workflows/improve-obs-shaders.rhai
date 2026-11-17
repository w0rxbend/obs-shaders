let meta = #{
    name: "improve-obs-shaders",
    description: "Harden each OBS shader for live streaming, then commit and push it on main",
    when_to_use: "Production pass over shaders/*.effect. Five editors at a time, then one publisher.",
    phases: [
        #{ title: "Improve", detail: "five shaders at a time" },
        #{ title: "Publish", detail: "one commit and push per changed shader" },
    ],
};

const BATCH = 5;

let improve_schema = #{
    "type": "object",
    "required": ["path", "changed", "summary"],
    "properties": #{
        "path": #{ "type": "string" },
        "changed": #{ "type": "boolean" },
        "summary": #{ "type": "string" },
    },
};

fn improve_prompt(path) {
    let p = "";
    p += "Harden one OBS Shaderfilter file so it can be used for live streaming and recording. Work only in /home/worxbend/Projects/obs-shaders. Edit only the file named below. Read that file before any edit. Also read tools/validate_all_shaderfilter_files.py and obey its forbidden patterns.";
    p += " ";
    p += "File: ";
    p += path;
    p += " ";
    p += "Git is forbidden in this step. Do not run git add, git commit, git push, git reset, git restore, or git clean. A later publisher commits. Do not run tools/generate_premium_shader_pack.py or tools/fix_shader_techniques.py. Do not edit any other file, including README, media, tools, or the workflow.";
    p += " ";
    p += "Load path. If the file contains technique Draw, keep a full effect: vertex_shader must not be mainImage, pixel_shader must be mainImage, and the vertex shader must set pos with mul by ViewProj and set uv to v_in.uv * uv_scale + uv_offset. Declare uniform float4x4 ViewProj, uniform float2 uv_offset, and uniform float2 uv_scale with no initializer and no annotation. If the file has no technique, do not add a technique, a vertex shader, or ViewProj. The plugin wrapper supplies those.";
    p += " ";
    p += "Builtins get no initializer and no annotation. The names are ViewProj, image, prevous_image, prevous_output, elapsed_time, elapsed_time_start, elapsed_time_show, elapsed_time_active, elapsed_time_enable, local_time, loops, loop_second, current_time_ms, current_time_sec, current_time_min, current_time_hour, current_time_day_of_week, current_time_day_of_month, current_time_month, current_time_day_of_year, current_time_year, rand_f, rand_activation_f, rand_instance_f, uv_offset, uv_scale, uv_size, uv_pixel_interval. Declare a builtin only when the shader uses it. The spellings prevous_image and prevous_output are the plugin spellings. Do not invent previous_image.";
    p += " ";
    p += "Every user float gets an annotation block with string label, string widget_type set to slider, float minimum, float maximum, and float step, then the existing initializer. Keep the uniform name. Keep the current default unless that default hides the source, flashes the full frame at 3 Hz or faster, or throws the subject off screen. A safer default must still show the named effect. Do not put a slider on float4, bool, string, texture2d, or a builtin. float4 stays a color. Do not rename or remove an existing uniform. Add a uniform only when the named effect needs it.";
    p += " ";
    p += "The pixels must do what the filename and the Effect header say. A shared category template that does not match the name is a defect: replace mainImage with one single-pass version of that named effect. Keep any of these uniforms that already exist: intensity, amount, speed, center_x, center_y, opacity, preserve_alpha. At most 16 image.Sample calls. Every loop bound is a numeric literal. No uniform loop bound. Nested sample loops stay at or under 4 by 4.";
    p += " ";
    p += "Use HLSL only. Forbidden tokens: texture2D, sampler2D, iChannel, iResolution, gl_FragCoord, gl_FragColor, fragCoord, mix(, fract(, and the swizzles .xxx .yyy .zzz .www. Sample with image.Sample(textureSampler, uv). Clamp sampled UVs to 0..1 or rely on the Clamp address mode. Guard every divisor with max(denom, 0.001). Do not hardcode 1.78 or 16/9. When shape depends on aspect, declare uv_size with no initializer and use uv_size.x / max(uv_size.y, 1.0).";
    p += " ";
    p += "Alpha. If preserve_alpha exists, honor it. Mask, crop, and rounded-frame shaders may write alpha. Every other shader keeps the sampled alpha. Saturate rgb on grades, glitches, and stylized looks. Do not saturate a pass-through or an exposure control whose job is to keep the source values.";
    p += " ";
    p += "Stream safety. At the written default, a talking-head source stays recognizable. Privacy, blackout, and wipe shaders may cover the image because the name says so. Full-frame black or white flashes stay slower than 3 per second at the default. Delete functions that nothing calls after the edit, except inside shaders/_helpers. Do not split mainImage to chase a line limit. One pixel entry point stays.";
    p += " ";
    p += "Special files. If the path contains shaders/_helpers/, do not add mainImage, a sampler, or a technique. Fix only a definite HLSL compile bug. If there is none, leave the file unchanged. If the path contains shaders/_compatibility-test/, keep a visual no-op at opacity 1, add a slider annotation for opacity, and do not add a technique.";
    p += " ";
    p += "If the file already meets every rule, leave it unchanged and set changed to false. After an edit, run python3 tools/validate_all_shaderfilter_files.py. Errors for other files are not yours. Your file must not appear in the Errors list. Fix warnings that name your file. Then stop.";
    p += " ";
    p += "Return only the schema object. path is the file path. changed is true only if you wrote the file. summary is one sentence naming the production defect you fixed, or already production-ready.";
    p += " ";
    p
}

fn publish_prompt(paths) {
    let listing = "";
    for path in paths {
        listing += path;
        listing += " ";
    }
    let p = "";
    p += "You publish shaders in /home/worxbend/Projects/obs-shaders. The branch must be main. If git symbolic-ref --short HEAD is not main, stop and change nothing. Commit and push each changed file below, one file per commit, in the listed order. Do not commit any other path. Do not use git add -A, git commit --all, git push --force, git reset --hard, or git clean.";
    p += " ";
    p += "Paths:";
    p += " ";
    p += "For each path, in order: look at git diff -- path. If there is no diff, skip it. If the diff only changes comments, skip it. Run python3 tools/validate_all_shaderfilter_files.py. If the Errors section names that path, run git restore -- path and skip it. Do not fix a different file. If the validator reports an error in a file outside this list, leave that file alone and still commit the clean files from this list.";
    p += " ";
    p += "Commit from the repo root with this helper and no other commit command. Replace SCOPE and SUBJECT. Scope is the parent folder name with one leading underscore removed. Subject is imperative, under 72 characters, letters digits spaces and hyphens only.";
    p += " ";
    p += "bash /home/worxbend/.agents/skills/git-pushing/scripts/smart_commit.sh fix(SCOPE): SUBJECT -- PATH";
    p += " ";
    p += "The helper pushes to origin/main. If it says the commit already exists and the push was rejected because the remote moved, fetch origin main and rebase the local main onto origin/main, then push with git push origin HEAD:main. Do that recovery once. Never force-push. If the branch is protected or the push is rejected for credentials, stop the rest of the list and say so. After each successful push, go to the next path. When the list is done, reply with the commit hashes you created and the paths you skipped.";
    p += " ";
    p += listing;
    p
}

let files = [
    "shaders/_compatibility-test/compatibility-test.effect",
    "shaders/_helpers/helpers.effect",
    "shaders/acid-color-cycling/acid-color-cycling.effect",
    "shaders/alien-scanner/alien-scanner.effect",
    "shaders/animated-neon-border/animated-neon-border.effect",
    "shaders/anxiety-pulse/anxiety-pulse.effect",
    "shaders/arctic-blue/arctic-blue.effect",
    "shaders/arena-dark-grade/arena-dark-grade.effect",
    "shaders/bad-compression/bad-compression.effect",
    "shaders/barrel-distortion/barrel-distortion.effect",
    "shaders/bleach-bypass/bleach-bypass.effect",
    "shaders/blood-horror-grade/blood-horror-grade.effect",
    "shaders/blur/blur.effect",
    "shaders/broken-signal/broken-signal.effect",
    "shaders/burn-dissolve/burn-dissolve.effect",
    "shaders/bw-old-film/bw-old-film.effect",
    "shaders/camcorder-date/camcorder-date.effect",
    "shaders/cctv-surveillance/cctv-surveillance.effect",
    "shaders/chromatic-aberration/chromatic-aberration.effect",
    "shaders/cinematic-contrast/cinematic-contrast.effect",
    "shaders/cinematic-letterbox/cinematic-letterbox.effect",
    "shaders/circular-reveal/circular-reveal.effect",
    "shaders/circular-webcam-crop/circular-webcam-crop.effect",
    "shaders/cold-moonlight/cold-moonlight.effect",
    "shaders/confidential-screen-blur/shader_confidential_screen_blur.effect",
    "shaders/crt-scanlines/crt-scanlines.effect",
    "shaders/cyberpunk-neon/cyberpunk-neon.effect",
    "shaders/damage-pulse/damage-pulse.effect",
    "shaders/dark-ritual-vignette/dark-ritual-vignette.effect",
    "shaders/databending-blocks/databending-blocks.effect",
    "shaders/datamosh-block-shift/datamosh-block-shift.effect",
    "shaders/day-for-night/day-for-night.effect",
    "shaders/demonic-grade/demonic-grade.effect",
    "shaders/desert-western/desert-western.effect",
    "shaders/diamond-webcam-crop/diamond-webcam-crop.effect",
    "shaders/digital-noise/digital-noise.effect",
    "shaders/dirty-lens/dirty-lens.effect",
    "shaders/dream-blur/dream-blur.effect",
    "shaders/dream-pastel/dream-pastel.effect",
    "shaders/dream-pop-glow/dream-pop-glow.effect",
    "shaders/dreamy-rotation-drift/dreamy-rotation-drift.effect",
    "shaders/dropout-lines/dropout-lines.effect",
    "shaders/drunk-camera-wobble/drunk-camera-wobble.effect",
    "shaders/dust-scratches/dust-scratches.effect",
    "shaders/earthquake-shake/earthquake-shake.effect",
    "shaders/edge-darkener/edge-darkener.effect",
    "shaders/electric-shock/electric-shock.effect",
    "shaders/energy-shield-ripple/energy-shield-ripple.effect",
    "shaders/exposure-controls/exposure-controls.effect",
    "shaders/face-spotlight/face-spotlight.effect",
    "shaders/film-gate-jitter/film-gate-jitter.effect",
    "shaders/film-grain/film-grain.effect",
    "shaders/film-shutter/film-shutter.effect",
    "shaders/fire-heat-distortion/fire-heat-distortion.effect",
    "shaders/fisheye/fisheye.effect",
    "shaders/floating-head-cam/floating-head-cam.effect",
    "shaders/floating-webcam-drift/floating-webcam-drift.effect",
    "shaders/foggy-cemetery/foggy-cemetery.effect",
    "shaders/forcefield-distortion/forcefield-distortion.effect",
    "shaders/frozen-edges/frozen-edges.effect",
    "shaders/gentle-zoom-breathing/gentle-zoom-breathing.effect",
    "shaders/ghost-double-image/ghost-double-image.effect",
    "shaders/glitch-wipe/glitch-wipe.effect",
    "shaders/glow-bloom/glow-bloom.effect",
    "shaders/golden-hour/golden-hour.effect",
    "shaders/grunge-overlay/grunge-overlay.effect",
    "shaders/grunge-rock-video/grunge-rock-video.effect",
    "shaders/halftone/halftone.effect",
    "shaders/hallucination-drift/hallucination-drift.effect",
    "shaders/haunted-shadows/haunted-shadows.effect",
    "shaders/heat-haze/heat-haze.effect",
    "shaders/hexagon-webcam-crop/hexagon-webcam-crop.effect",
    "shaders/hologram/hologram.effect",
    "shaders/holographic-flicker/holographic-flicker.effect",
    "shaders/horizontal-tearing/horizontal-tearing.effect",
    "shaders/idle-streamer-camera-movement/idle-streamer-camera-movement.effect",
    "shaders/industrial-rust/industrial-rust.effect",
    "shaders/infrared-camera/infrared-camera.effect",
    "shaders/ink-outline/ink-outline.effect",
    "shaders/ink-spread/ink-spread.effect",
    "shaders/interlaced-jitter/interlaced-jitter.effect",
    "shaders/kaleidoscope/kaleidoscope.effect",
    "shaders/lens-dirt/lens-dirt.effect",
    "shaders/linear-wipe/linear-wipe.effect",
    "shaders/liquid-metal/liquid-metal.effect",
    "shaders/low-health-desat/low-health-desat.effect",
    "shaders/low-light-booster/low-light-booster.effect",
    "shaders/matrix-tint/matrix-tint.effect",
    "shaders/memory-flashback/memory-flashback.effect",
    "shaders/micro-shake/micro-shake.effect",
    "shaders/mirror-split/mirror-split.effect",
    "shaders/mtv-90s-distortion/mtv-90s-distortion.effect",
    "shaders/night-vision/night-vision.effect",
    "shaders/noir-detective/noir-detective.effect",
    "shaders/noise-dissolve/noise-dissolve.effect",
    "shaders/ntsc-color-bleed/ntsc-color-bleed.effect",
    "shaders/oil-paint/oil-paint.effect",
    "shaders/pal-phase-shift/pal-phase-shift.effect",
    "shaders/panic-tunnel/panic-tunnel.effect",
    "shaders/paranormal-camera-twitch/paranormal-camera-twitch.effect",
    "shaders/pencil-sketch/pencil-sketch.effect",
    "shaders/pendulum-swing/pendulum-swing.effect",
    "shaders/perspective-tilt/perspective-tilt.effect",
    "shaders/pincushion-distortion/pincushion-distortion.effect",
    "shaders/pixel-melt/pixel-melt.effect",
    "shaders/pixel-sorting/pixel-sorting.effect",
    "shaders/podcast-warm-grade/podcast-warm-grade.effect",
    "shaders/polaroid-frame/polaroid-frame.effect",
    "shaders/possession-pulse/possession-pulse.effect",
    "shaders/posterize/posterize.effect",
    "shaders/premium-pack/shader_001_strong_confidential_blur.effect",
    "shaders/premium-pack/shader_002_pixelated_privacy_shield.effect",
    "shaders/premium-pack/shader_003_frosted_glass_confidential_screen.effect",
    "shaders/premium-pack/shader_004_adaptive_text_destroying_blur.effect",
    "shaders/premium-pack/shader_005_redacted_document_look.effect",
    "shaders/premium-pack/shader_006_security_blackout_pulse.effect",
    "shaders/premium-pack/shader_007_privacy_noise_glass.effect",
    "shaders/premium-pack/shader_008_corporate_presentation_blur.effect",
    "shaders/premium-pack/shader_009_password_manager_destroyer.effect",
    "shaders/premium-pack/shader_010_emergency_privacy_wipe.effect",
    "shaders/premium-pack/shader_011_subtle_breathing_rotation.effect",
    "shaders/premium-pack/shader_012_floating_webcam_drift.effect",
    "shaders/premium-pack/shader_013_handheld_micro_sway.effect",
    "shaders/premium-pack/shader_014_paranormal_twitch.effect",
    "shaders/premium-pack/shader_015_vhs_frame_instability.effect",
    "shaders/premium-pack/shader_016_slow_cinematic_zoom.effect",
    "shaders/premium-pack/shader_017_pendulum_camera_swing.effect",
    "shaders/premium-pack/shader_018_dream_camera_drift.effect",
    "shaders/premium-pack/shader_019_earthquake_shake.effect",
    "shaders/premium-pack/shader_020_security_camera_motor_pan.effect",
    "shaders/premium-pack/shader_021_teal_and_orange.effect",
    "shaders/premium-pack/shader_022_bleach_bypass.effect",
    "shaders/premium-pack/shader_023_cold_moonlight.effect",
    "shaders/premium-pack/shader_024_supernatural_green_blue.effect",
    "shaders/premium-pack/shader_025_rainy_noir.effect",
    "shaders/premium-pack/shader_026_horror_red_shadows.effect",
    "shaders/premium-pack/shader_027_desert_dust_grade.effect",
    "shaders/premium-pack/shader_028_golden_hour.effect",
    "shaders/premium-pack/shader_029_apocalyptic_gray.effect",
    "shaders/premium-pack/shader_030_documentary_handheld_look.effect",
    "shaders/premium-pack/shader_031_old_black_and_white_film.effect",
    "shaders/premium-pack/shader_032_silent_movie_projector.effect",
    "shaders/premium-pack/shader_033_sepia_damaged_film.effect",
    "shaders/premium-pack/shader_034_crt_scanlines.effect",
    "shaders/premium-pack/shader_035_vhs_tracking_damage.effect",
    "shaders/premium-pack/shader_036_ntsc_color_bleed.effect",
    "shaders/premium-pack/shader_037_pal_phase_shift.effect",
    "shaders/premium-pack/shader_038_interlaced_jitter.effect",
    "shaders/premium-pack/shader_039_tape_wrinkle.effect",
    "shaders/premium-pack/shader_040_burned_film_edges.effect",
    "shaders/premium-pack/shader_041_haunted_green_shadows.effect",
    "shaders/premium-pack/shader_042_ghost_double_exposure.effect",
    "shaders/premium-pack/shader_043_possession_pulse.effect",
    "shaders/premium-pack/shader_044_demonic_red_contrast.effect",
    "shaders/premium-pack/shader_045_foggy_cemetery.effect",
    "shaders/premium-pack/shader_046_sleep_paralysis_edges.effect",
    "shaders/premium-pack/shader_047_cursed_vhs.effect",
    "shaders/premium-pack/shader_048_blood_moon_grade.effect",
    "shaders/premium-pack/shader_049_ritual_vignette.effect",
    "shaders/premium-pack/shader_050_spirit_camera_distortion.effect",
    "shaders/premium-pack/shader_051_rgb_split_glitch.effect",
    "shaders/premium-pack/shader_052_datamosh_block_shift.effect",
    "shaders/premium-pack/shader_053_digital_tearing.effect",
    "shaders/premium-pack/shader_054_broken_signal.effect",
    "shaders/premium-pack/shader_055_cyberpunk_neon_boost.effect",
    "shaders/premium-pack/shader_056_matrix_terminal_green.effect",
    "shaders/premium-pack/shader_057_hologram_flicker.effect",
    "shaders/premium-pack/shader_058_robot_vision.effect",
    "shaders/premium-pack/shader_059_scanner_sweep.effect",
    "shaders/premium-pack/shader_060_corrupted_codec.effect",
    "shaders/premium-pack/shader_061_fisheye.effect",
    "shaders/premium-pack/shader_062_barrel_distortion.effect",
    "shaders/premium-pack/shader_063_pincushion.effect",
    "shaders/premium-pack/shader_064_chromatic_aberration.effect",
    "shaders/premium-pack/shader_065_fake_3d_anaglyph.effect",
    "shaders/premium-pack/shader_066_heat_haze.effect",
    "shaders/premium-pack/shader_067_water_ripple.effect",
    "shaders/premium-pack/shader_068_shockwave_ring.effect",
    "shaders/premium-pack/shader_069_tunnel_warp.effect",
    "shaders/premium-pack/shader_070_broken_glass_approximation.effect",
    "shaders/premium-pack/shader_071_rounded_corners.effect",
    "shaders/premium-pack/shader_072_animated_neon_border.effect",
    "shaders/premium-pack/shader_073_soft_drop_shadow.effect",
    "shaders/premium-pack/shader_074_glass_webcam_frame.effect",
    "shaders/premium-pack/shader_075_polaroid_webcam.effect",
    "shaders/premium-pack/shader_076_cyberpunk_panel.effect",
    "shaders/premium-pack/shader_077_circular_crop.effect",
    "shaders/premium-pack/shader_078_hexagon_crop.effect",
    "shaders/premium-pack/shader_079_torn_paper_mask.effect",
    "shaders/premium-pack/shader_080_security_camera_overlay.effect",
    "shaders/premium-pack/shader_081_kaleidoscope.effect",
    "shaders/premium-pack/shader_082_spiral_warp.effect",
    "shaders/premium-pack/shader_083_pixel_melt.effect",
    "shaders/premium-pack/shader_084_liquid_metal.effect",
    "shaders/premium-pack/shader_085_posterize.effect",
    "shaders/premium-pack/shader_086_comic_halftone.effect",
    "shaders/premium-pack/shader_087_pencil_sketch.effect",
    "shaders/premium-pack/shader_088_ink_outline.effect",
    "shaders/premium-pack/shader_089_oil_paint_approximation.effect",
    "shaders/premium-pack/shader_090_watercolor_wash.effect",
    "shaders/premium-pack/shader_091_rain_on_glass.effect",
    "shaders/premium-pack/shader_092_snow_overlay.effect",
    "shaders/premium-pack/shader_093_smoke_drift.effect",
    "shaders/premium-pack/shader_094_ash_particles.effect",
    "shaders/premium-pack/shader_095_lightning_flash.effect",
    "shaders/premium-pack/shader_096_frosted_lens.effect",
    "shaders/premium-pack/shader_097_wet_lens_streaks.effect",
    "shaders/premium-pack/shader_098_sandstorm.effect",
    "shaders/premium-pack/shader_099_cloud_shadow.effect",
    "shaders/premium-pack/shader_100_sun_flare_approximation.effect",
    "shaders/premium-pack/shader_101_beat_pulse_tunnel.effect",
    "shaders/premium-pack/shader_102_neon_kaleido_wash.effect",
    "shaders/premium-pack/shader_103_prism_trail_split.effect",
    "shaders/premium-pack/shader_104_laser_grid_sweep.effect",
    "shaders/premium-pack/shader_105_strobe_smear.effect",
    "shaders/premium-pack/shader_106_bass_glow_throb.effect",
    "shaders/premium-pack/shader_107_spectral_color_split.effect",
    "shaders/premium-pack/shader_108_liquid_club_wash.effect",
    "shaders/premium-pack/shader_109_mirror_stage_flip.effect",
    "shaders/premium-pack/shader_110_rave_posterize.effect",
    "shaders/premium-pack/shader_111_focus_spotlight.effect",
    "shaders/premium-pack/shader_112_edge_readability_boost.effect",
    "shaders/premium-pack/shader_113_dashboard_glass_dim.effect",
    "shaders/premium-pack/shader_114_terminal_phosphor_glow.effect",
    "shaders/premium-pack/shader_115_browser_privacy_haze.effect",
    "shaders/premium-pack/shader_116_presentation_spotlight.effect",
    "shaders/premium-pack/shader_117_code_rain_overlay.effect",
    "shaders/premium-pack/shader_118_document_scanner_pass.effect",
    "shaders/premium-pack/shader_119_window_focus_vignette.effect",
    "shaders/premium-pack/shader_120_cursor_area_magnifier.effect",
    "shaders/premium-pack/shader_121_soft_skin_bloom.effect",
    "shaders/premium-pack/shader_122_warm_portrait_lift.effect",
    "shaders/premium-pack/shader_123_cool_studio_webcam.effect",
    "shaders/premium-pack/shader_124_beauty_vignette.effect",
    "shaders/premium-pack/shader_125_tiktok_soft_glam.effect",
    "shaders/premium-pack/shader_126_instagram_peach_fade.effect",
    "shaders/premium-pack/shader_127_smartphone_hdr_selfie.effect",
    "shaders/premium-pack/shader_128_old_laptop_webcam.effect",
    "shaders/premium-pack/shader_129_news_anchor_clarity.effect",
    "shaders/premium-pack/shader_130_low_light_webcam_rescue.effect",
    "shaders/premium-pack/shader_131_arcane_mana_shimmer.effect",
    "shaders/premium-pack/shader_132_portal_edge_glow.effect",
    "shaders/premium-pack/shader_133_dragon_fire_heat.effect",
    "shaders/premium-pack/shader_134_ice_magic_border.effect",
    "shaders/premium-pack/shader_135_poison_curse_green.effect",
    "shaders/premium-pack/shader_136_holy_light_rays.effect",
    "shaders/premium-pack/shader_137_shadow_realm_wash.effect",
    "shaders/premium-pack/shader_138_space_monitor_tint.effect",
    "shaders/premium-pack/shader_139_alien_scanner_bands.effect",
    "shaders/premium-pack/shader_140_forcefield_ripple.effect",
    "shaders/premium-pack/shader_141_fullscreen_melt.effect",
    "shaders/premium-pack/shader_142_rgb_explosion.effect",
    "shaders/premium-pack/shader_143_whiteout_flash.effect",
    "shaders/premium-pack/shader_144_blackout_pulse.effect",
    "shaders/premium-pack/shader_145_negative_inversion.effect",
    "shaders/premium-pack/shader_146_solarize_threshold.effect",
    "shaders/premium-pack/shader_147_thermal_false_color.effect",
    "shaders/premium-pack/shader_148_deep_fried_meme.effect",
    "shaders/premium-pack/shader_149_jpeg_artifact_approximation.effect",
    "shaders/premium-pack/shader_150_corrupted_codec_blocks.effect",
    "shaders/projector-flicker/projector-flicker.effect",
    "shaders/radial-blur/radial-blur.effect",
    "shaders/rain-on-glass/rain-on-glass.effect",
    "shaders/rainy-noir/rainy-noir.effect",
    "shaders/rave-strobe/rave-strobe.effect",
    "shaders/rgb-anaglyph/rgb-anaglyph.effect",
    "shaders/rgb-split-glitch/rgb-split-glitch.effect",
    "shaders/robot-hud-tint/robot-hud-tint.effect",
    "shaders/rounded-corners/rounded-corners.effect",
    "shaders/rusted-industrial/rusted-industrial.effect",
    "shaders/scanline-terminal/scanline-terminal.effect",
    "shaders/security-camera-motor-pan/security-camera-motor-pan.effect",
    "shaders/security-camera-overlay/security-camera.effect",
    "shaders/sepia-film/sepia-film.effect",
    "shaders/sharpen/sharpen.effect",
    "shaders/signal-loss-pulse/signal-loss-pulse.effect",
    "shaders/silent-movie/silent-movie.effect",
    "shaders/skin-softening/skin-softening.effect",
    "shaders/slight-3d-tilt-illusion/slight-3d-tilt-illusion.effect",
    "shaders/slow-handheld-camera-sway/slow-handheld-camera-sway.effect",
    "shaders/snow-overlay/snow-overlay.effect",
    "shaders/sodium-vapor/sodium-vapor.effect",
    "shaders/soft-drop-shadow/soft-drop-shadow.effect",
    "shaders/soft-vignette/soft-vignette.effect",
    "shaders/speed-streaks/speed-streaks.effect",
    "shaders/spiral-warp/spiral-warp.effect",
    "shaders/starship-monitor/starship-monitor.effect",
    "shaders/stealth-shimmer/stealth-shimmer.effect",
    "shaders/subtle-breathing-rotation/subtle-breathing-rotation.effect",
    "shaders/supernatural-grade/supernatural-grade.effect",
    "shaders/tape-color-bleed/tape-color-bleed.effect",
    "shaders/tape-wrinkle/tape-wrinkle.effect",
    "shaders/teal-and-orange/teal-and-orange.effect",
    "shaders/temperature-shift/temperature-shift.effect",
    "shaders/thermal-vision/thermal-vision.effect",
    "shaders/torn-paper-mask/torn-paper-mask.effect",
    "shaders/toxic-haze/toxic-haze.effect",
    "shaders/tunnel-warp/tunnel-warp.effect",
    "shaders/underwater/underwater.effect",
    "shaders/vaporwave-pastel/vaporwave-pastel.effect",
    "shaders/vhs-channel-switch/vhs-channel-switch.effect",
    "shaders/vhs-tracking/vhs-tracking.effect",
    "shaders/vhs-unstable-frame-drift/vhs-unstable-frame-drift.effect",
    "shaders/water-ripple/water-ripple.effect",
    "shaders/watercolor-wash/watercolor-wash.effect",
    "shaders/wave-distortion/wave-distortion.effect",
    "shaders/webcam-glass-reflection/webcam-glass-reflection.effect",
    "shaders/webcam-rounded-frame/webcam-rounded-frame.effect",
    "shaders/xray-look/xray-look.effect"
];

let cap = 0;
if args != () {
    if args.max_batches != () {
        cap = args.max_batches;
    }
}

let jobs = [];
let paths = [];
let n = 0;
let batches_done = 0;
let stop = false;
let publish_failures = 0;

for path in files {
    if stop == false {
        jobs.push(#{
            prompt: improve_prompt(path),
            label: "improve:" + path,
            capability_mode: "all",
            output_schema: improve_schema,
        });
        paths.push(path);
        n += 1;
        if n == BATCH {
            phase("Improve");
            let results = parallel(jobs);
            let edited = 0;
            for r in results {
                if r != () && r.success && r.output != () && r.output.changed == true {
                    edited += 1;
                }
            }
            log("batch " + batches_done.to_string() + " edited " + edited.to_string());
            phase("Publish");
            let pub = agent(publish_prompt(paths), #{
                label: "publish:" + batches_done.to_string(),
                capability_mode: "all",
            });
            if pub == () || pub.success != true {
                publish_failures += 1;
                log("publish failed for batch " + batches_done.to_string());
                await_user("verification", "Publish failed for batch " + batches_done.to_string() + ". Fix git status in the obs-shaders repo, then resume. Remaining shaders continue after resume.");
            }
            jobs.clear();
            paths.clear();
            n = 0;
            batches_done += 1;
            if cap > 0 && batches_done >= cap {
                stop = true;
            }
        }
    }
}

if stop == false && n > 0 {
    phase("Improve");
    let results = parallel(jobs);
    let edited = 0;
    for r in results {
        if r != () && r.success && r.output != () && r.output.changed == true {
            edited += 1;
        }
    }
    log("batch " + batches_done.to_string() + " edited " + edited.to_string());
    phase("Publish");
    let pub = agent(publish_prompt(paths), #{
        label: "publish:" + batches_done.to_string(),
        capability_mode: "all",
    });
    if pub == () || pub.success != true {
        publish_failures += 1;
        log("publish failed for batch " + batches_done.to_string());
        await_user("verification", "Publish failed for the last batch. Fix git status in the obs-shaders repo, then resume.");
    }
    batches_done += 1;
}

complete(#{
    summary: "OBS shader production pass finished",
    batches: batches_done,
    publish_failures: publish_failures,
    shader_count: files.len(),
});
