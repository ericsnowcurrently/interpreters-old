import unittest

from . import PROJECT_ROOT, TEST_ROOT


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(TEST_ROOT,
                                                top_level_dir=PROJECT_ROOT)
    unittest.TextTestRunner(verbosity=2).run(suite)
