import os
import tempfile
import unittest
from pathlib import Path

from aibeyin.utils import load_env_file


class UtilsTests(unittest.TestCase):
    def test_load_env_file_reads_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text("FOO=bar\nBAZ='qux'\n", encoding="utf-8")
            loaded = load_env_file(env_path, override=True)
            self.assertEqual(loaded["FOO"], "bar")
            self.assertEqual(loaded["BAZ"], "qux")
            self.assertEqual(os.environ["FOO"], "bar")
            self.assertEqual(os.environ["BAZ"], "qux")


if __name__ == "__main__":
    unittest.main()
