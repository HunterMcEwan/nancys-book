"""
Crop + enhance a region of a scrapbook scan for re-transcription by a vision LLM.

Pipeline (per research notes):
  1. Crop the requested region.
  2. Lanczos upscale to MAX_EDGE (default 2576 — Claude Opus 4.7 high-res cap).
  3. Background flatten: divide by Gaussian-blurred copy to neutralize yellowing
     and uneven lighting without binarizing.
  4. Mild blue-channel weighting: brown ink on cream paper contrasts strongest
     in the blue channel; we keep some color so the encoder still sees a
     natural-looking image.
  5. Save as PNG.

Usage:
  py enhance-crop.py <src.jpg> <dst.png> <x> <y> <w> <h> [--max-edge 2576]

All coordinates are in the source image's pixel space.
"""
import sys
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def enhance(src_path: Path, dst_path: Path, crop_xywh, max_edge: int) -> None:
    im = Image.open(src_path).convert("RGB")
    x, y, w, h = crop_xywh
    crop = im.crop((x, y, x + w, y + h))

    # 1. Lanczos upscale (or downscale) so long edge == max_edge.
    cw, ch = crop.size
    scale = max_edge / max(cw, ch)
    new_size = (max(1, round(cw * scale)), max(1, round(ch * scale)))
    crop = crop.resize(new_size, Image.LANCZOS)

    arr = np.asarray(crop).astype(np.float32)  # H,W,3

    # 2. Background flatten via Gaussian-blurred division.
    #    sigma ~ page-width/30  -> on a 2576-wide crop, sigma ~ 85px
    sigma = max(arr.shape[:2]) / 30.0
    blurred = crop.filter(ImageFilter.GaussianBlur(radius=sigma))
    bg = np.asarray(blurred).astype(np.float32) + 1.0  # avoid /0
    flattened = arr / bg * 220.0  # target a near-white background
    flattened = np.clip(flattened, 0, 255)

    # 3. Mild blue-channel weighting.
    #    Brown ink contrasts most in BLUE on cream paper. We construct a
    #    luminance from a blue-heavy mix, then blend it back into a slightly
    #    desaturated RGB image so the encoder still sees a natural look.
    R, G, B = flattened[..., 0], flattened[..., 1], flattened[..., 2]
    blue_luma = 0.15 * R + 0.20 * G + 0.65 * B   # heavier B than ITU-R BT.601
    blue_luma = np.clip(blue_luma, 0, 255)
    # Desaturate toward the blue-luma estimate (0 = original, 1 = pure luma)
    DESAT = 0.55
    out = (1 - DESAT) * flattened + DESAT * blue_luma[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)

    Image.fromarray(out).save(dst_path, "PNG", optimize=True)
    print(f"wrote {dst_path} ({new_size[0]}x{new_size[1]})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("x", type=int)
    ap.add_argument("y", type=int)
    ap.add_argument("w", type=int)
    ap.add_argument("h", type=int)
    ap.add_argument("--max-edge", type=int, default=2576)
    args = ap.parse_args()
    enhance(Path(args.src), Path(args.dst), (args.x, args.y, args.w, args.h), args.max_edge)
    return 0


if __name__ == "__main__":
    sys.exit(main())
