#!/usr/bin/env python3
"""Select one Staged Awards image style with equal probability."""

from __future__ import annotations

import argparse
import random
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class ImageStyle:
    slug: str
    name: str
    prompt: str


STYLES = (
    ImageStyle(
        "paper-cut-diorama",
        "Theatrical paper-cut diorama",
        (
            "A handcrafted layered paper-cut theatre diorama with tactile paper "
            "edges, curtains, spotlights, a celebratory podium, and repository-specific "
            "props. Warm, whimsical, dimensional, and polished."
        ),
    ),
    ImageStyle(
        "retro-pixel-art",
        "Retro pixel-art ceremony",
        (
            "A polished 16-bit pixel-art awards ceremony with a tiny stage, dramatic "
            "lighting, crisp pixel clusters, and repository-specific technical props. "
            "Playful and nostalgic without resembling a particular game."
        ),
    ),
    ImageStyle(
        "isometric-3d-miniature",
        "Isometric 3D miniature",
        (
            "A refined isometric 3D miniature world that turns the repository's real "
            "components into a coherent awards-stage scene. Soft studio lighting, "
            "tactile materials, charming scale, and clean spatial storytelling."
        ),
    ),
    ImageStyle(
        "vintage-screen-print",
        "Vintage screen-print poster",
        (
            "A bold vintage screen-print celebration poster with simplified geometric "
            "forms, a limited warm palette, subtle halftone texture, strong contrast, "
            "and repository-specific symbols arranged around an awards stage."
        ),
    ),
    ImageStyle(
        "technical-cyanotype",
        "Technical blueprint or cyanotype",
        (
            "An elegant cyanotype-inspired technical blueprint where verified repository "
            "components become architectural lines, dependency paths, annotations without "
            "words, and schematic details surrounding a luminous trophy or stage."
        ),
    ),
)


def choose_style(seed: str | None = None) -> ImageStyle:
    """Choose uniformly; a seed exists only for repeatable tests and debugging."""
    if seed is None:
        return secrets.choice(STYLES)
    return random.Random(seed).choice(STYLES)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed",
        help="Make selection repeatable for tests or debugging; omit for a fresh random choice.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print all available styles instead of choosing one.",
    )
    args = parser.parse_args()

    selected = STYLES if args.list else (choose_style(args.seed),)
    for index, style in enumerate(selected):
        if index:
            print()
        print(f"style_slug={style.slug}")
        print(f"style_name={style.name}")
        print(f"style_prompt={style.prompt}")


if __name__ == "__main__":
    main()
