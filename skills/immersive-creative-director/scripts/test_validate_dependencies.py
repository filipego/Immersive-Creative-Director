import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_dependencies.py")


class DependencyValidatorTests(unittest.TestCase):
    def test_local_required_capabilities_resolve(self):
        result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)
        self.assertIn("scrollcraft", result.stdout)


if __name__ == "__main__":
    unittest.main()
