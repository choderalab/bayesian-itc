import unittest


class TestInjection(unittest.TestCase):

    @unittest.expectedFailure
    def test___init__(self):
        # injection = Injection(number, volume, duration, spacing, filter_period, titrant_concentration)
        assert False # TODO: implement your test here
    @unittest.expectedFailure
    def test_contents(self):
        # injection = Injection(number, volume, duration, spacing, filter_period, titrant_concentration)
        # self.assertEqual(expected, injection.contents(titrant_concentration))
        assert False # TODO: implement your test here


class TestExperiment(unittest.TestCase):

    @unittest.expectedFailure
    def test___init__(self):
        # experiment = Experiment(data_filename)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test___str__(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.__str__())
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_fit_gaussian_process_baseline(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.fit_gaussian_process_baseline(frac, theta0, nugget, plot))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_integrate_heat(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.integrate_heat())
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_plot_baseline(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.plot_baseline(filename))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_read_integrated_heats(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.read_integrated_heats(heats_file, unit))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_write_heats_csv(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.write_heats_csv(filename))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_write_integrated_heats(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.write_integrated_heats(filename))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_write_power(self):
        # experiment = Experiment(data_filename)
        # self.assertEqual(expected, experiment.write_power(filename))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
