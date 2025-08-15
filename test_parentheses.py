#!/usr/bin/env python3
# filepath: /home/uncanny/Desktop/Cutie/BodmasParser/test_parentheses.py

import unittest
from operators import is_valid_expression

class TestParenthesesValidation(unittest.TestCase):
    """Test cases for the parentheses validation in the operators.py module"""
    
    def test_parentheses_validation(self):
        """Test the validation of expressions with parentheses"""
        
        # These should be valid with a modified validation function
        expressions_should_be_valid = [
            "(3+4)*5",
            "3*(4+5)",
            "(3+4)*(5-2)",
        ]
        
        # Print information about current validation behavior
        print("\nCurrent validation behavior for parenthesized expressions:")
        for expr in expressions_should_be_valid:
            result = is_valid_expression(expr)
            print(f"Expression '{expr}' is {'valid' if result else 'invalid'} with current validation.")
            
        print("\nNote: Parenthesized expressions are currently marked as invalid.")
        print("To support them, you'll need to modify the is_valid_expression function")
        print("by removing or modifying this check:")
        print("if re.match(r'^[+\\-*/^()]', expression) or re.search(r'[+\\-*/^()]$', expression):")

if __name__ == '__main__':
    unittest.main()
