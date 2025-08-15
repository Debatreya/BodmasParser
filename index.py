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

    # Currently assuming given expression will be a infix expression 
    def __infix_to_postfix(self) -> list[str]:
        """
            Convert the infix expression to postfix expression.
            Returns a list of strings representing the postfix expression.
        """
        stack : list[str] = []
        output : list[str] = []

        # Split the expression using regex into tokens using the operators
        import re
        tokens = re.split(r'(\+|\-|\*|\/|\^)', self.expression)
        # eg. tokens = ['34', '+', '5', '*', '60', '-', '8', '/', '2']

        for token in tokens:
            if token == '':
                continue  # Skip empty tokens
            
            if is_operator(token):
                # If the token is an operator
                while (stack and stack[-1] != '(' and 
                       get_precedence(stack[-1]) >= get_precedence(token)):
                    output.append(stack.pop())
                stack.append(token)
            else:
                # If the token is an operand (number)
                output.append(token)

        # Pop all the operators from the stack
        while stack:
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
#
# Invalid Expressions (will raise errors):
# 11. "3++4"           - Consecutive operators
# 12. "3+4)"           - Unbalanced parentheses
# 13. "(3+4"           - Unbalanced parentheses
# 14. "3+"             - Incomplete expression
# 15. "+3"             - Leading operator
# 16. "3.4.5+6"        - Invalid number format
# 17. "3a+4"           - Invalid character
# 18. "(3+4)*5"        - Currently not supported (leading parenthesis)
#
# Note: The current implementation doesn't support expressions starting or ending with parentheses.
# To handle parentheses, the is_valid_expression function would need to be modified. 