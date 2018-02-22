import unittest

class TestInstrument(unittest.TestCase):

    @unittest.expectedFailure
    def test___init__(self):
        # instrument = Instrument(V0, V_correction, itcfile, description)
        assert False # TODO: implement your test here

    @unittest.expectedFailure
    def test_instrument_from_file(self):
        # instrument = Instrument(V0, V_correction, itcfile, description)
        # self.assertEqual(expected, instrument.instrument_from_file(filename))
        assert False # TODO: implement your test here

class TestVPITC(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # v_pit_c = VPITC()
        assert False # TODO: implement your test here

class TestITC200(unittest.TestCase):
    @unittest.expectedFailure
    def test___init__(self):
        # i_t_c200 = ITC200()
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
