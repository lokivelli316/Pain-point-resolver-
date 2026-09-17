import tomllib
import unittest
from pathlib import Path

from pain_point_resolver.core import patterns
from pain_point_resolver.core.module import pain_points

SAMPLES = Path(__file__).parent / "samples"


class PatternTests(unittest.TestCase):
    def test_every_pattern_has_a_sample_that_matches(self):
        for pat in patterns.load_patterns():
            sample = SAMPLES / f"{pat.id}.txt"
            self.assertTrue(sample.exists(), f"add tests/samples/{pat.id}.txt")
            ids = [f.id for f in patterns.diagnose(sample.read_text())]
            self.assertIn(pat.id, ids, f"{pat.id} did not match its own sample")

    def test_ids_unique_and_fields_valid(self):
        pats = patterns.load_patterns()
        ids = [p.id for p in pats]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(pain_points())
        for p in pats:
            self.assertIn(p.confidence, {"high", "medium", "low"}, p.id)
            self.assertTrue(set(p.pain_points) <= known, p.id)
            self.assertTrue(p.diagnosis and p.fix, p.id)

    def test_extractors(self):
        text = "ModuleNotFoundError: No module named 'yaml'\nbash: line 1: foobar: command not found\n"
        found = {f.id: f for f in patterns.diagnose(text)}
        self.assertIn("yaml", found["missing-python-modules"].diagnosis)
        self.assertIn("foobar", found["missing-commands"].diagnosis)

    def test_clean_output_has_no_findings(self):
        self.assertEqual(patterns.diagnose("Build succeeded\nAll 12 tests passed\n"), [])


if __name__ == "__main__":
    unittest.main()
