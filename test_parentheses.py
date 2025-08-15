#!/usr/bin/env python3
# filepath: /home/uncanny/Desktop/Cutie/BodmasParser/test_parentheses.py

import unittest
from operators import is_valid_expression
from index import Parser

class TestParenthesesValidation(unittest.TestCase):
    """Test cases for the parentheses validation and functionality"""
    
    def test_parentheses_validation(self):
        """Test the validation of expressions with parentheses"""
        
        # These should now be valid with the updated validation function
        expressions_should_be_valid = [
            "(3+4)*5",
            "3*(4+5)",
            "(3+4)*(5-2)",
            "((3+4)*2)",
            "(3+4*5)/(2-1)"
        ]
        
        for expr in expressions_should_be_valid:
            self.assertTrue(is_valid_expression(expr), f"Expression '{expr}' should be valid")
    
    def test_parentheses_invalid(self):
        """Test invalid parentheses expressions"""
        invalid_expressions = [
            "()",              # Empty parentheses
            "(+)",             # Only operator in parentheses
            "((3+4)",          # Unbalanced opening parentheses
            "(3+4))",          # Unbalanced closing parentheses
            ")3+4(",           # Reversed parentheses
            "(3+)",            # Incomplete expression in parentheses
            "(+3)",            # Leading operator in parentheses
        ]
        
        for expr in invalid_expressions:
            self.assertFalse(is_valid_expression(expr), f"Expression '{expr}' should be invalid")
    
    def test_parentheses_evaluation(self):
        """Test correct evaluation of expressions with parentheses"""
        test_cases = [
            ("(3+4)*5", 35),          # Basic parentheses
            ("3*(4+5)", 27),          # Right-side parentheses
            ("(3+4)*(5-2)", 21),      # Multiple parentheses groups
            ("3+4*5", 23),            # Without parentheses
            ("(3+4*5)", 23),          # Redundant parentheses
            ("((3+4)*2)", 14),        # Nested parentheses
            ("(3+4*5)/(2-1)", 23),    # Complex expression
        ]
        
        for expr, expected in test_cases:
            parser = Parser(expr)
            result = parser.evaluate()
            self.assertEqual(result, expected, f"Expression '{expr}' should evaluate to {expected}")
    
    def test_nested_parentheses(self):
        """Test nested parentheses handling"""
        test_cases = [
            ("((3+4)*(5-2))", 21),        # Fully parenthesized
            ("((3+4)*2)/((6/3)+1)", 4.666666666666667),   # Multiple nested groups
            ("(((3+4)))", 7),             # Multiple redundant parentheses
        ]
        
        for expr, expected in test_cases:
            parser = Parser(expr)
            result = parser.evaluate()
            self.assertAlmostEqual(result, expected, 
                                  msg=f"Expression '{expr}' should evaluate to {expected}")

if __name__ == '__main__':
    unittest.main()
