import unittest

class TestReport(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # report = Report(experiments)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_writeLaTeX(self):
        # report = Report(experiments)
        # self.assertEqual(expected, report.writeLaTeX(filename))
        assert False # TODO: implement your test here

class TestAnalyze(unittest.TestCase):
    @unittest.expectedFailure
    def test_analyze(self):
        # self.assertEqual(expected, plot_experiment(name, experiment))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
