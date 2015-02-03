import unittest

class TestRescalingStep(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_competence(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        # self.assertEqual(expected, rescaling_step.competence(stochastic))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_propose(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        # self.assertEqual(expected, rescaling_step.propose())
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_reject(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        # self.assertEqual(expected, rescaling_step.reject())
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_step(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        # self.assertEqual(expected, rescaling_step.step())
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_tune(self):
        # rescaling_step = RescalingStep(dictionary, beta, max_scale, interval, verbose)
        # self.assertEqual(expected, rescaling_step.tune(verbose))
        assert False # TODO: implement your test here


class TestBindingModel(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # binding_model = BindingModel()
        assert False # TODO: implement your test here


class TestTwoComponentBindingModel(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # two_component_binding_model = TwoComponentBindingModel(experiment, instrument)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_expected_injection_heats(self):
        # two_component_binding_model = TwoComponentBindingModel(experiment, instrument)
        # self.assertEqual(expected, two_component_binding_model.expected_injection_heats(DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, beta, N))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_tau(self):
        # two_component_binding_model = TwoComponentBindingModel(experiment, instrument)
        # self.assertEqual(expected, two_component_binding_model.tau())
        assert False # TODO: implement your test here


class TestCompetitiveBindingModel(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # competitive_binding_model = CompetitiveBindingModel(experiments, receptor, V0, concentration_uncertainty, verbose)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_equilibrium_concentrations(self):
        # competitive_binding_model = CompetitiveBindingModel(experiments, receptor, V0, concentration_uncertainty, verbose)
        # self.assertEqual(expected, competitive_binding_model.equilibrium_concentrations(Ka_n, C0_R, C0_Ln, V, c0))
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_expected_injection_heats(self):
        # competitive_binding_model = CompetitiveBindingModel(experiments, receptor, V0, concentration_uncertainty, verbose)
        # self.assertEqual(expected, competitive_binding_model.expected_injection_heats(experiment, true_sample_cell_concentrations, true_syringe_concentrations, DeltaH_0, thermodynamic_parameters))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
