import io
import unittest
from contextlib import redirect_stdout

from pain_point_resolver import cli
from pain_point_resolver.core.module import CONTRACTS, pain_points
from pain_point_resolver.modules import MODULES


class RegistryTests(unittest.TestCase):
    def test_pain_map_has_62_stable_ids(self):
        self.assertEqual(sorted(pain_points()), list(range(1, 63)))

    def test_modules_declare_contract_and_real_pain_points(self):
        names = set()
        for cls in MODULES:
            m = cls()
            self.assertNotIn(m.name, names)
            names.add(m.name)
            self.assertIn(m.contract, CONTRACTS, m.name)
            self.assertIn(m.status, {"working", "partial", "planned"}, m.name)
            self.assertTrue(set(m.pain_points) <= set(pain_points()), m.name)

    def test_pain_map_matches_built_modules(self):
        built = {cls().name: set(cls().pain_points) for cls in MODULES if cls().status != "planned"}
        for pid, p in pain_points().items():
            claimed = {name for name, ids in built.items() if pid in ids}
            self.assertEqual(set(p["modules"]), claimed, f"pain point #{pid}")
            if p["status"] == "open":
                self.assertFalse(claimed, f"#{pid} is covered by {claimed} but marked open")

    def test_cli_runs(self):
        for argv in (["modules"], ["pain"], ["pain", "30"], ["a11y", "check", "#000000", "#ffffff"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(argv), 0, argv)

    def test_planned_module_explains_itself(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(cli.main(["install-api"]), 2)
        self.assertIn("planned", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
