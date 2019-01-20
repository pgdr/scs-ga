import unittest
import scs

class TestScs(unittest.TestCase):

    def test_superseq(self):
        cases = {
            'a b' : 0,
            'a a' : 1,
            'aa a' : 1,
            'aa aa' : 2,
            'a aa' : 1,
        }
        for inp, exp in cases.items():
            sub, sup = inp.split()
            act = scs.superseq(sub, sup)
            msg = 'superseq({}, {}) act: {}  |  exp: {}'.format(
                sub, sup, act, exp)
        self.assertEquals(act, exp, msg)

    def test_random_char(self):
        ga = scs.GA('abc', 'def')
        chrs = set([ga.random_char() for _ in range(100)])
        self.assertEquals(chrs, set('abcdef'))

    def test_mutation(self):
        ga = scs.GA('abc', 'def')
        ind = 'abcdef'
        muts = [ ga.mutate(ind) for _ in range(100) ]
        lens = set([len(x) for x in muts])
        self.assertIn(len(ind)-1, lens)
        self.assertIn(len(ind), lens)
        self.assertIn(len(ind)+1, lens)
        self.assertNotIn(2, lens)

    def test_crossover(self):
        ga = scs.GA('abc', 'def')
        ind1, ind2 = 'abc def'.split()
        cs = set([ ga.crossover(ind1, ind2) for _ in range(1000) ])
        self.assertEquals(set('abc abf dbc dbf aef def aec dec'.split()), cs)


if __name__ == '__main__':
    unittest.main()
