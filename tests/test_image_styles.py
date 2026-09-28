"""Checks for image-style rotation and exact image composition."""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "skills/the-staged-awards/scripts/select_image_style.py"
COMPOSER = ROOT / "skills/the-staged-awards/scripts/compose_awards_image.py"


def load_selector():
    spec = importlib.util.spec_from_file_location("select_image_style", SELECTOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ImageStyleTests(unittest.TestCase):
    def test_rotation_has_five_unique_styles(self):
        selector = load_selector()
        self.assertEqual(len(selector.STYLES), 5)
        self.assertEqual(len({style.slug for style in selector.STYLES}), 5)
        self.assertEqual(len({style.prompt for style in selector.STYLES}), 5)

    def test_seed_makes_debug_selection_repeatable(self):
        selector = load_selector()
        first = selector.choose_style("same-run")
        second = selector.choose_style("same-run")
        self.assertEqual(first, second)

    def test_cli_reports_machine_readable_fields(self):
        result = subprocess.run(
            ["python3", str(SELECTOR), "--seed", "ceremony"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("style_slug=", result.stdout)
        self.assertIn("style_name=", result.stdout)
        self.assertIn("style_prompt=", result.stdout)

    @unittest.skipUnless(
        shutil.which("ffmpeg") and shutil.which("ffprobe"),
        "ffmpeg and ffprobe are required",
    )
    def test_composer_outputs_exact_landscape_png(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "source.ppm"
            output = temp / "finished.png"
            source.write_text("P3\n4 3\n255\n" + "30 50 90\n" * 12)
            subprocess.run(
                [
                    "python3",
                    str(COMPOSER),
                    str(source),
                    str(output),
                    "--repository-name",
                    "example-repo",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            probe = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=width,height",
                    "-of",
                    "csv=p=0:s=x",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(probe.stdout.strip(), "1200x900")


if __name__ == "__main__":
    unittest.main()
