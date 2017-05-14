"""Test parsing Roman numerals int literals."""
import itertools
import re
import unittest
from test import support


def is_proper_roman_numeral(s):
    return re.fullmatch('(?xi)'
                        '(?=[MDCLXVI])'
                        '(?P<thousands> M{,3})'
                        '(?P<hundreds>D?C{,3}|CM|CD)'
                        '(?P<tens>    L?X{,3}|XC|XL)'
                        '(?P<units>   V?I{,3}|IX|IV)', s)


class TestRomanNumeral(unittest.TestCase):
    def test_all_valid(self):
        for n in range(1, 4000):
            numerals = roman(n)
            assert is_proper_roman_numeral(numerals[2:])
            for sign in ['-', '', '+']:
                kw = {'roman': sign + numerals,
                      'expected': -n if sign == '-' else n}
                with self.subTest(**kw):
                    self.assertEqual(eval(kw['roman']), kw['expected'])
                    self.assertEqual(int(kw['roman'], 0), kw['expected'])

    @support.requires_resource('cpu')
    def test_all_upto(self, maxlen=6):
        for numeral in (''.join(p) for r in range(maxlen + 1)
                        for p in itertools.product('ZMDCLXVI', repeat=r)):
            with self.subTest(numeral=numeral):
                literal = '0r' + numeral
                if not is_proper_roman_numeral(numeral):
                    self.assertRaises(SyntaxError, eval, literal)
                    self.assertRaises(ValueError, int, literal, 0)
                else:
                    n = eval(literal)
                    self.assertEqual(n, int(literal, 0))
                    self.assertEqual(roman(n), literal)

    def test_four_tens(self):
        for numeral in 'MDCLXVI':
            self._test_invalid('0r' + (numeral * 4))

    def test_repeated_fives(self):
        for five in 'DLV':
            self._test_invalid('0r' + (five * 2))

    def test_unicode(self):
        for r in map(chr, range(0x2160, 0x2180)):
            self._test_invalid(r)

    def _test_invalid(self, s):
        self.assertRaises(SyntaxError, eval, '0r' + s)
        self.assertRaises(ValueError, int, '0r' + s, 0)

    def test_wrong_letter(self):
        self._test_invalid('Z')
        self._test_invalid('IZ')

    def test_quote_valid_quote(self):
        # test empty input
        self._test_invalid('')

        # test invalid (unless middle ages or ancient multiplication rule)
        # double  # subtraction
        self._test_invalid('IIX')

        # test invalid subtraction
        self._test_invalid('IM')
        self._test_invalid('IL')

        # test invalid repetition
        self._test_invalid('IIIIIIIIIIIIIIII')

        # numerals from https://projecteuler.net/about=roman_numerals
        for quote_valid_quote in ['XIIIIII', 'XIIIIIIIII', 'XLIIIIIIII',
                                  'XXXXIIIIIIIII', 'MCCCCCCVI']:
            self._test_invalid(quote_valid_quote)

        # numerals from https://able2know.org/topic/54469-1
        for wrong in ['IIX', 'CCM', 'DMCCC', 'CMC', 'XMX',
                      'IM', 'IC', 'XMIX', 'VIL', 'XVX', 'VIX', 'IVX', 'XIIX']:
            self._test_invalid(wrong)

        # from https://www.unc.edu/~rowlett/units/roman.html
        # and http://www.numericana.com/answer/roman.htm
        for sometimes_valid in ['XIIJ', 'xiij', 'VIIC', 'VIM']:
            self._test_invalid(sometimes_valid)

    def test_nodigits(self):
        with self.assertRaises(SyntaxError):
            eval("0r")
        with self.assertRaises(ValueError):
            int("0r", 0)

    def test_zero(self):
        with self.assertRaises(SyntaxError):
            eval("0r0")
        with self.assertRaises(ValueError):
            int("0r0", 0)

    def test_leading_zero(self):
        with self.assertRaises(SyntaxError):
            eval("0r0I")
        with self.assertRaises(ValueError):
            int("0r0I", 0)

    def test_thousands_separator(self):
        self.assertEqual(0r_I, 1)
        self.assertEqual(0r_I_I_I, 3)
        self.assertEqual(0r_I_V, 4)
        self.assertEqual(0r_I_X, 9)
        self.assertEqual(0rXXX_III, 33)
        with self.assertRaises(SyntaxError):
            eval("0rI_")
        with self.assertRaises(ValueError):
            int("0rI_", 0)

    def test_space(self):
        self.assertEqual(int(' 0ri', 0), 1)
        self.assertEqual(int('  0ri', 0), 1)
        self.assertEqual(int('0ri ', 0), 1)
        self.assertEqual(int('0ri  ', 0), 1)
        self.assertEqual(int(' 0ri ', 0), 1)
        self.assertEqual(int('  0ri ', 0), 1)
        self.assertEqual(int(' 0ri  ', 0), 1)
        self.assertEqual(int('  0ri  ', 0), 1)

    def test_loweruppercase(self):
        self.assertEqual(0ri, 1)
        self.assertEqual(0rI, 1)
        self.assertEqual(0Ri, 1)
        self.assertEqual(0RI, 1)
        self.assertEqual(0rii, 2)
        self.assertEqual(0riI, 2)
        self.assertEqual(0rIi, 2)
        self.assertEqual(0rII, 2)
        self.assertEqual(0Rii, 2)
        self.assertEqual(0RiI, 2)
        self.assertEqual(0RIi, 2)
        self.assertEqual(0RII, 2)


if __name__ == '__main__':
    unittest.main()
