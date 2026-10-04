# BlindLab self-hosted studio

## Goal

BlindLab can now produce the actual first film without a commercial image/video API. GitHub Actions is the orchestrator; the generation engine is a local/open-weight Wan2.2 TI2V-5B model running on an NVIDIA self-hosted runner.

The production path is:

idea -> BlindLab shot manifest -> Wan2.2 generation -> continuity reference frame -> FFmpeg assembly -> 15-second duration gate -> GitHub artifact.

Wan2.2's official TI2V-5B path supports 720p text/video generation and documents a 24 GB NVIDIA GPU floor for single-GPU inference with offloading.

Official repository: https://github.com/Wan-Video/Wan2.2

## Required runner

A GitHub Actions self-hosted runner must have these labels:

    self-hosted
    linux
    x64
    nvidia-gpu

The runner needs:

- NVIDIA CUDA-capable GPU with at least 24 GB VRAM for the chosen 720p TI2V-5B configuration.
- Working NVIDIA driver / nvidia-smi.
- Python 3.10+.
- ffmpeg.
- Enough persistent disk for the model and generated clips.

The ordinary GitHub-hosted Ubuntu runner is intentionally not used for generation. It does not provide the GPU memory required by the model.

## Generate the film

Open the BlindLab validation workflow and run it manually with:

    generate_film = true

The normal validation job still runs on the hosted runner. The generation job only starts when explicitly requested and only schedules onto the self-hosted NVIDIA runner.

The generator uses a continuity chain: shot 01 is text-to-video, then the final frame of each completed shot becomes the reference image for the next shot. This is intended to reduce scene/subject drift between independently generated clips.

Output:

    artifacts/blindlab_studio/blindlab_reality_has_a_glitch.mp4

The workflow uploads the full studio directory as blindlab-first-film.

## Important boundary

Generated media is creative output. BlindLab does not treat it as evidence of real-world optical performance, physical measurements, or photographic capture. The physical experiment and creative-generation systems remain separate.
