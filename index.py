from operators import is_operator, get_precedence, is_valid_expression
from parseTree import ParseTree

class Parser:
    """ 
        A class to parse a mathematical expression.
        eg. "34 + 5 * 60 - 8/2"
        It will be first converted to "34+5*60-8/2" by removing whitespace.
        Then it will be converted to postfix expression.
        The postfix expression will be a list of strings.
        eg. ['34', '5', '60', '*', '+', '8', '2', '/', '-']
        Finally, it will create a parse tree from the postfix expression.
        The parse tree will be used to evaluate the expression.
    """

    postfix : list[str] = []
    parsetree : ParseTree = None

    def __init__(self, expression: str):
        """
            Initialize the Parser with a mathematical expression.
            The expression should be a valid infix expression.
            It will be converted to postfix expression and a parse tree will be created.
        """
        if not is_valid_expression(expression):
            raise ValueError("Invalid expression. Please provide a valid mathematical expression.")

        # First remove any whitespace from the expression
        self.expression = expression.replace(" ", "")

        # Convert the infix expression to postfix expression
        self.postfix = self.__infix_to_postfix()

        # Create a parse tree from the postfix expression
        self.parsetree = ParseTree(self.postfix)

    # Converting infix expression to postfix expression 
    def __infix_to_postfix(self) -> list[str]:
        """
            Convert the infix expression to postfix expression.
            Returns a list of strings representing the postfix expression.
            
            This implementation handles parentheses and follows operator precedence:
            - Parentheses have the highest precedence
            - Exponentiation (^) next
            - Multiplication and division (* and /)
            - Addition and subtraction (+ and -)
        """
        stack : list[str] = []
        output : list[str] = []

        # Split the expression using regex into tokens including parentheses
        import re
        tokens = re.findall(r'\d+\.\d+|\d+|[()+\-*/^]', self.expression)
        # eg. tokens = ['34', '+', '5', '*', '60', '-', '8', '/', '2']
        # or for expressions with parentheses: ['(', '3', '+', '4', ')', '*', '5']

        for token in tokens:
            if token == '':
                continue  # Skip empty tokens
            
            if token == '(':
                # If token is an opening parenthesis, push it to the stack
                stack.append(token)
            elif token == ')':
                # If token is a closing parenthesis, pop from the stack
                # until an opening parenthesis is encountered
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                
                # Remove the opening parenthesis
                if stack and stack[-1] == '(':
                    stack.pop()
                # Note: If stack is empty, there was a parentheses mismatch
                # But this should be caught by is_valid_expression
            elif is_operator(token):
                # If the token is an operator
                while (stack and stack[-1] != '(' and 
                       get_precedence(stack[-1]) >= get_precedence(token)):
                    output.append(stack.pop())
                stack.append(token)
            else:
                # If the token is an operand (number)
                output.append(token)

        # Pop all the remaining operators from the stack
        while stack:
            # If there's a parenthesis left, there was a mismatch
            # This should be caught by is_valid_expression
            if stack[-1] == '(' or stack[-1] == ')':
                stack.pop()
                continue
            output.append(stack.pop())

        return output
    
    # Show JSON representation of the parse tree
    def get_parse_tree(self) -> ParseTree:
        """
            Get the parse tree for the postfix expression.
            Returns a ParseTree object.
        """
        print(self.parsetree) # This will call the __str__ method of ParseTree class

    # A evaluate function to evaluate the expression
    def evaluate(self) -> float:
        """
            Evaluate the expression represented by the parse tree.
            Returns the result as a float.
        """
        if not self.parsetree:
            self.parsetree = ParseTree(self.postfix)
        
        return self.parsetree.execute()
    


if __name__ == "__main__":
    def main():
        expr = input("Enter a mathematical expression: ")
        parser = Parser(expr)
        print("Postfix Expression:", parser.postfix)
        print("Parse Tree:")
        parser.get_parse_tree()
        result = parser.evaluate()
        print("Result:", result)

    main()

# This code is a simple parser for mathematical expressions.
# It converts infix expressions to postfix and builds a parse tree.
# The parser can evaluate the expression and print the result. 

# Test Cases:
# Here are sample expressions to try when running this script:
#
# Valid Expressions:
# 1. "3+4"             - Simple addition
# 2. "3.5+4.2"         - Decimal numbers
# 3. "3+4*5"           - Mixed operations with precedence
# 4. "3*4+5"           - Different order of operations
# 5. "3^2"             - Exponentiation
# 6. "10-3-2"          - Sequential subtraction
# 7. "10/2*3"          - Division and multiplication
# 8. "10+20+30+40"     - Multiple additions
# 9. "5^2+3*4-6/2"     - Complex expression with all operators
# 10. "0.5*10+2.5"     - Mixed decimals
# 11. "(3+4)*5"        - Parentheses changing precedence
# 12. "3*(4+5)"        - Grouping operations
# 13. "(3+4)*(5-2)"    - Multiple parentheses groups
# 14. "(3+4*5)/(2-1)"  - Nested operations
# 15. "((3+4)*2)"      - Nested parentheses
#
# Invalid Expressions (will raise errors):
# 16. "3++4"           - Consecutive operators
# 17. "3+4)"           - Unbalanced parentheses
# 18. "(3+4"           - Unbalanced parentheses
# 19. "3+"             - Incomplete expression
# 20. "+3"             - Leading operator
# 21. "3.4.5+6"        - Invalid number format
# 22. "3a+4"           - Invalid character
# 23. "()"             - Empty parentheses
# 24. "(+)"            - Invalid content in parentheses
#
# Note: This implementation now supports expressions with parentheses!
# Parentheses can be used to group operations and change the order of evaluation. 