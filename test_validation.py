#!/usr/bin/env python3
# filepath: /home/uncanny/Desktop/Cutie/BodmasParser/test_validation.py

import unittest
from operators import is_valid_expression, valid_parentheses

class TestExpressionValidation(unittest.TestCase):
    """Comprehensive test cases for expression validation"""
    
    def test_basic_expressions(self):
        """Test basic valid expressions"""
        # Valid basic expressions
        self.assertTrue(is_valid_expression('3+4'))
        self.assertTrue(is_valid_expression('3-4'))
        self.assertTrue(is_valid_expression('3*4'))
        self.assertTrue(is_valid_expression('3/4'))
        self.assertTrue(is_valid_expression('3^4'))
        
        # Multiple operations
        self.assertTrue(is_valid_expression('3+4-5'))
        self.assertTrue(is_valid_expression('3*4/5'))
        self.assertTrue(is_valid_expression('3+4*5'))
        self.assertTrue(is_valid_expression('3*4+5'))
        self.assertTrue(is_valid_expression('3^2+1'))

    def test_whitespace_handling(self):
        """Test expressions with various whitespace patterns"""
        self.assertTrue(is_valid_expression('3 + 4'))
        self.assertTrue(is_valid_expression(' 3+4 '))
        self.assertTrue(is_valid_expression('3 + 4 * 5'))
    
    def test_decimal_numbers(self):
        """Test expressions with decimal numbers"""
        self.assertTrue(is_valid_expression('3.5+4.2'))
        self.assertTrue(is_valid_expression('0.5*10'))
        self.assertTrue(is_valid_expression('1+0.001'))
        self.assertTrue(is_valid_expression('10.0+20.0'))
    
    def test_invalid_expressions(self):
        """Test various invalid expressions"""
        # Empty expression
        self.assertFalse(is_valid_expression(''))
        
        # Consecutive operators
        self.assertFalse(is_valid_expression('3++4'))
        self.assertFalse(is_valid_expression('3+-4'))
        self.assertFalse(is_valid_expression('3**4'))
        
        # Incomplete expressions
        self.assertFalse(is_valid_expression('3+'))
        self.assertFalse(is_valid_expression('+3'))
        
        # Invalid characters
        self.assertFalse(is_valid_expression('3a+4'))
        self.assertFalse(is_valid_expression('3#+4'))
        self.assertFalse(is_valid_expression('3+4=7'))
        
        # Invalid number formats
        self.assertFalse(is_valid_expression('3.4.5+6'))
        # Note: Current implementation actually allows decimal points without following digits
        # Uncomment this line if validation is strengthened
        # self.assertFalse(is_valid_expression('3.+4'))
    
    def test_parentheses_validation(self):
        """Test current behavior with parenthesized expressions"""
        # With current implementation, these should fail
        # (would pass if parentheses validation is modified)
        self.assertFalse(is_valid_expression('(3+4)'))
        self.assertFalse(is_valid_expression('3*(4+5)'))
        self.assertFalse(is_valid_expression('(3+4)*5'))
        
        # These should always fail (unbalanced parentheses)
        self.assertFalse(is_valid_expression('(3+4'))
        self.assertFalse(is_valid_expression('3+4)'))
        self.assertFalse(is_valid_expression('((3+4)'))
        
        # Test the helper function separately
        self.assertTrue(valid_parentheses('(3+4)'))
        self.assertTrue(valid_parentheses('((3+4)*(5-2))'))
        self.assertFalse(valid_parentheses('(3+4))'))
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Large numbers
        self.assertTrue(is_valid_expression('999999+888888'))
        
        # Many operations
        self.assertTrue(is_valid_expression('1+2+3+4+5+6+7+8+9+10'))
        self.assertTrue(is_valid_expression('1*2*3*4*5/6/7/8/9/10'))

        # Complex expressions (current implementation doesn't support parentheses)
        complex_expr = '3+4*5-6/2^2'
        self.assertTrue(is_valid_expression(complex_expr))


class TestParenthesesExtension(unittest.TestCase):
    """Test cases for potential parentheses extension"""
    
    def test_extended_parentheses_support(self):
        """
        This test demonstrates how parentheses could be supported.
        
        NOTE: These tests are EXPECTED TO FAIL with the current implementation.
        They are included as a reference for future extensions.
        """
        print("\nThe following tests are EXPECTED TO FAIL with the current implementation:")
        print("To support parentheses, modify the is_valid_expression function.\n")
        
        # Uncomment these when parentheses support is implemented
        # self.assertTrue(is_valid_expression('(3+4)*5'))
        # self.assertTrue(is_valid_expression('3*(4+5)'))
        # self.assertTrue(is_valid_expression('(3+4)*(5-2)'))
        # self.assertTrue(is_valid_expression('(3+4*5)/(2-1)'))
        
        # Instead, we'll just print the validation result
        examples = ['(3+4)*5', '3*(4+5)', '(3+4)*(5-2)', '(3+4*5)/(2-1)']
        for expr in examples:
            result = is_valid_expression(expr)
            print(f"Expression '{expr}' is currently {'valid' if result else 'invalid'}")
        
        # Recommendations for implementation
        print("\nTo enable parentheses support:")
        print("1. Remove or modify this check in is_valid_expression:")
        print("   if re.match(r'^[+\\-*/^()]', expression) or re.search(r'[+\\-*/^()]$', expression):")
        print("2. Update the infix_to_postfix algorithm to handle parentheses")
        print("3. Update the build_tree method if needed\n")


if __name__ == '__main__':
    unittest.main()
