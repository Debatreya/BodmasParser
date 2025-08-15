# For extensibility, we can add more operators in the future. Hence Operator list and Precedence are to be defined on a global level.

import re

# List of allowed Operators
operators : list[str] = ['+', '-', '*', '/', '^']

def is_operator(value: str) -> bool:
    """
        Check if the value is a valid operator.
        Returns True if the value is an operator, False otherwise.
    """
    return value in operators

# The precedence of operators is defined as follows: (will be needed only when converting infix to postfix)
# + and - have the lowest precedence (1)
# * and / have medium precedence (2)
# ^ has the highest precedence (3)
def get_precedence(operator: str) -> int:
    """
        Get the precedence of the operator.
        Returns 0 if the operator is not recognized.
    """
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    return precedence.get(operator, 0)
    # If the operator is not recognized, return 0.


# How operators are used in the code:
def apply_operator(left: str, right: str, operator: str) -> float:
    """
        Apply the operator on the left and right operands.
        Returns the result of the operation.
    """
    switcher = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ** y
    }
    func = switcher.get(operator)
    if func:
        return func(float(left), float(right))
    else:
        raise ValueError(f"Unknown operator: {operator}")
    # If the operator is not recognized, raise an error.
    # This function assumes that left and right are valid numbers in string format.
    # It converts them to float before applying the operator.
    # This is a utility function to apply the operator on the operands.
    # It can be used in the evaluation of the expression.
    # This function can be extended to support more operators in the future.
    # For now, it supports +, -, *, /, and ^ operators.


def is_valid_expression(expression: str) -> bool:
    """
        Check if the given expression is valid.
        expression must be a valid infix expression.
        Steps for validation:
        1. Empty expression check
        2. Valid characters check (digits, operators, parentheses, and decimal points)
        3. Consecutive operators check
        4. Balanced parentheses check
        5. Leading/trailing operators or parentheses check
        6. Invalid use of decimal points check (currently only 3.4 type is allowed, .4, 3. type is not allowed)
        7. Invalid sequences like '()', '(+)', '(-)', etc.
        Returns True if the expression is valid, False otherwise.
    """
    # Check if the expression is empty
    if not expression:
        return False
    
    # Check for valid characters (digits, operators, parentheses, and decimal points)
    if not re.match(r'^[0-9+\-*/^(). ]+$', expression):
        print("Invalid characters in expression. Only +, -, *, /, ^, decimal numbers and () are allowed.")
        return False
    
    # Check for consecutive operators or invalid sequences
    if re.search(r'[+\-*/^]{2,}', expression):
        print("Invalid expression. Consecutive operators are not allowed.")
        return False
    
    # Check for balanced parentheses
    if not valid_parentheses(expression):
        print("Invalid expression. Parentheses are not balanced.")
        return False
    
    # Check for leading/trailing operators or parentheses eg. "+3", "5*", "(3 + 5)", "(-2)", etc.
    if re.match(r'^[+\-*/^()]', expression) or re.search(r'[+\-*/^()]$', expression):
        print("Invalid expression. Expression cannot start or end with an operator or parentheses.")
        return False
    
    # Check for invalid use of decimal points e.g. "3.5.2", "3.+5", "3.-5", etc.
    # Logic: Replace all operators and parentheses with space 
    # then split the expression by space and use float() operator to check if these are valid
    tokens = re.sub(r'[+\-*/^()]', ' ', expression).split()
    for token in tokens:
        try:
            float(token)  # Try to convert the token to a float
        except ValueError:
            print(f"Invalid number in expression: {token}. Please use valid decimal numbers.")
            return False
    
    # Check for invalid sequences like '()' or '(+)', '(-)', etc.
    # Logic - Separate the a full parenthesis and pass it through is_valid_expression recursively
    # Eg: "(3 + 5) * (2 - 1)" are to be checked like -
    # ParenthesesExpressions = ['3 + 5', '2 - 1']
    # for each expression in ParenthesesExpressions, apply is_valid_expression(expression)
    parentheses_expressions = re.findall(r'\(([^()]+)\)', expression)
    for expr in parentheses_expressions:
        if not is_valid_expression(expr):
            return False
    
    return True
    # If all checks pass, the expression is valid.
    # This function checks if the expression is a valid mathematical expression.
    # It checks for valid characters, balanced parentheses, and invalid sequences of operators.



# Helper function to check if the expression has valid parentheses
def valid_parentheses(expression: str) -> bool:
    """
        Check if the parentheses in the expression are balanced.
        Returns True if the parentheses are balanced, False otherwise.
    """
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != '(':
                return False
            stack.pop()
    return len(stack) == 0
    # If the stack is empty, it means all parentheses are balanced.
    # If the stack is not empty, it means there are unmatched opening parentheses.