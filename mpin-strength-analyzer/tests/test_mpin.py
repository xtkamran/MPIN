import unittest
from mpin_analyzer import MPINAnalyzer

class TestMPINAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer_4 = MPINAnalyzer(4)
        self.analyzer_6 = MPINAnalyzer(6)
        self.demographics = {
            'user_dob': '02/01/1998',
            'spouse_dob': '15/07/1995',
            'anniversary': '10/05/2020'
        }

    # Part A: Common 4-digit MPINs
    def test_common_4digit_pins(self):
        self.assertEqual(self.analyzer_4.analyze('1234')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_4.analyze('1111')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_4.analyze('0000')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_4.analyze('2580')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_4.analyze('4321')['reasons'], ['COMMONLY_USED'])

    # Part B: Demographic checks for 4-digit
    def test_demographic_4digit(self):
        # User DOB patterns
        self.assertIn('DEMOGRAPHIC_DOB_SELF', self.analyzer_4.analyze('0201', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_DOB_SELF', self.analyzer_4.analyze('0102', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_DOB_SELF', self.analyzer_4.analyze('9802', self.demographics)['reasons'])
        
        # Spouse DOB patterns
        self.assertIn('DEMOGRAPHIC_DOB_SPOUSE', self.analyzer_4.analyze('1507', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_DOB_SPOUSE', self.analyzer_4.analyze('0715', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_DOB_SPOUSE', self.analyzer_4.analyze('9515', self.demographics)['reasons'])
        
        # Anniversary patterns
        self.assertIn('DEMOGRAPHIC_ANNIVERSARY', self.analyzer_4.analyze('1005', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_ANNIVERSARY', self.analyzer_4.analyze('0510', self.demographics)['reasons'])
        self.assertIn('DEMOGRAPHIC_ANNIVERSARY', self.analyzer_4.analyze('2010', self.demographics)['reasons'])

    # Part C: Combination checks for 4-digit
    def test_combination_4digit(self):
        # Common + demographic
        result = self.analyzer_4.analyze('2000', {
            'user_dob': '20/01/2000'
        })
        self.assertEqual(result['strength'], 'WEAK')
        self.assertIn('COMMONLY_USED', result['reasons'])
        self.assertIn('DEMOGRAPHIC_DOB_SELF', result['reasons'])

    # Part D: 6-digit MPIN tests
    def test_6digit_pins(self):
        # Common 6-digit
        self.assertEqual(self.analyzer_6.analyze('123456')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_6.analyze('111111')['reasons'], ['COMMONLY_USED'])
        self.assertEqual(self.analyzer_6.analyze('654321')['reasons'], ['COMMONLY_USED'])

        # Demographic 6-digit
        result = self.analyzer_6.analyze('020198', self.demographics)
        self.assertIn('DEMOGRAPHIC_DOB_SELF', result['reasons'])
        
        result = self.analyzer_6.analyze('980102', self.demographics)
        self.assertIn('DEMOGRAPHIC_DOB_SELF', result['reasons'])
        
        result = self.analyzer_6.analyze('100520', self.demographics)
        self.assertIn('DEMOGRAPHIC_ANNIVERSARY', result['reasons'])

    # Edge cases
    def test_edge_cases(self):
        # Invalid lengths
        self.assertEqual(self.analyzer_4.analyze('123')['strength'], 'INVALID')
        self.assertEqual(self.analyzer_4.analyze('12345')['strength'], 'INVALID')
        self.assertEqual(self.analyzer_6.analyze('12345')['strength'], 'INVALID')
        self.assertEqual(self.analyzer_6.analyze('1234567')['strength'], 'INVALID')
        
        # Non-digit characters
        self.assertEqual(self.analyzer_4.analyze('12a4')['strength'], 'INVALID')
        self.assertEqual(self.analyzer_6.analyze('12345x')['strength'], 'INVALID')

    # Strong MPINs
    def test_strong_pins(self):
        self.assertEqual(self.analyzer_4.analyze('3847')['strength'], 'STRONG')
        self.assertEqual(self.analyzer_4.analyze('3847', self.demographics)['strength'], 'STRONG')
        self.assertEqual(self.analyzer_6.analyze('472913')['strength'], 'STRONG')
        self.assertEqual(self.analyzer_6.analyze('472913', self.demographics)['strength'], 'STRONG')

    # Generate strong PINs
    def test_generate_strong_pins(self):
        for _ in range(10):  # Test multiple times to ensure randomness
            pin = self.analyzer_4.generate_strong_pin()
            self.assertEqual(len(pin), 4)
            self.assertTrue(pin.isdigit())
            self.assertEqual(self.analyzer_4.analyze(pin)['strength'], 'STRONG')
            
            pin = self.analyzer_6.generate_strong_pin()
            self.assertEqual(len(pin), 6)
            self.assertTrue(pin.isdigit())
            self.assertEqual(self.analyzer_6.analyze(pin)['strength'], 'STRONG')

if __name__ == '__main__':
    unittest.main()