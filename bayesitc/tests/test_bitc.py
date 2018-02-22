import unittest


class TestImports(unittest.TestCase):
    """Test if all submodules import properly.
    """
    def _imports(self, mod):
        from types import ModuleType
        self.assertIsInstance(__import__(mod), ModuleType)

    def test_imports(self):
        """Test the importing of all libraries."""
        module_names = ['models', 'experiments', 'instruments', 'report', 'units']
        for mod in module_names:
            self._imports('bitc.' + mod)
