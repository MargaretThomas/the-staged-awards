#!/usr/bin/env python3
"""Finish generated artwork as an exact 1200x900 Staged Awards PNG."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path


WIDTH = 1200
HEIGHT = 900


def ffmpeg_escape(value: str) -> str:
    """Escape a path for use as an FFmpeg filter value."""
    return value.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def find_font() -> Path:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Verdana Bold.ttf"),
        Path("/System/Library/Fonts/HelveticaNeue.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RuntimeError(
        "No supported bold font was found. Install DejaVu Sans or update the font "
        "candidates in compose_awards_image.py."
    )


def title_layout(repository_name: str) -> tuple[str, int]:
    length = len(repository_name)
    if length <= 24:
        font_size = 70
    elif length <= 40:
        font_size = 56
    elif length <= 64:
        font_size = 44
    else:
        font_size = 34
    approximate_characters = max(18, int(1060 / (font_size * 0.62)))
    wrapped = textwrap.fill(
        repository_name,
        width=approximate_characters,
        break_long_words=True,
        break_on_hyphens=True,
        max_lines=3,
        placeholder="...",
    )
    return wrapped, font_size


def compose(input_path: Path, output_path: Path, repository_name: str) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input artwork not found: {input_path}")
    if output_path.exists():
        raise FileExistsError(
            f"Refusing to overwrite {output_path}; choose a versioned filename instead."
        )
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "ffmpeg is required to create the exact 1200x900 image and title overlay."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    font = ffmpeg_escape(str(find_font()))
    title, title_size = title_layout(repository_name)

    with tempfile.TemporaryDirectory(prefix="staged-awards-image-") as temp_dir:
        temp = Path(temp_dir)
        series_file = temp / "series.txt"
        title_file = temp / "title.txt"
        composed_file = temp / "composed.png"
        series_file.write_text("THE STAGED AWARDS", encoding="utf-8")
        title_file.write_text(title, encoding="utf-8")

        filters = (
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            "drawbox=x=0:y=610:w=1200:h=290:color=black@0.62:t=fill,"
            f"drawtext=fontfile='{font}':textfile='{ffmpeg_escape(str(series_file))}':"
            "fontcolor=0xF2C14E:fontsize=34:x=70:y=654,"
            f"drawtext=fontfile='{font}':textfile='{ffmpeg_escape(str(title_file))}':"
            f"fontcolor=white:fontsize={title_size}:line_spacing=8:x=70:y=716"
        )
        result = subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(input_path),
                "-vf",
                filters,
                "-frames:v",
                "1",
                str(composed_file),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "ffmpeg could not compose the image")
        shutil.move(composed_file, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Generated background artwork")
    parser.add_argument("output", type=Path, help="New PNG path; existing files are preserved")
    parser.add_argument("--repository-name", required=True, help="Exact title to overlay")
    args = parser.parse_args()

    compose(args.input.resolve(), args.output.resolve(), args.repository_name)
    print(f"image_path={args.output.resolve()}")
    print(f"dimensions={WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
