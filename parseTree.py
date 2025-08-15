# This class is meant to represent a parse tree of a BODMAS mathematical expression.
# Allowed symbols: +, -, *, /, ^ and numbers.

# Class Diagrams:

# ParseNode
# ----------
# Represents a node in the parse tree.
# Attributes:
# - value (str): The value of the node (operator or operand).
# - is_operator (bool): True if the node is an operator, False otherwise.
# - left (ParseNode or None): The left child node.
# - right (ParseNode or None): The right child node.
# Methods:
# - __repr__(): Returns string representation for debugging.
# - __str__(): Returns value as string.
# - is_leaf() -> bool: Returns True if node is an operand (leaf).

# ParseTree
# ----------
# Represents the parse tree for a mathematical expression.
# Attributes:
# - __root (ParseNode or None): The root node of the parse tree (private).
# - __postfix (List[str]): The postfix expression used to build the tree (private).
# Methods:
# - __repr__(): Returns string representation for debugging.
# - __str__(): Returns JSON-like string of the tree.
# - build_tree(): Builds the tree from postfix.
# - get_root() -> ParseNode: Returns the root node.
# - get_postfix() -> List[str]: Returns the postfix expression.
# - execute() -> float: Evaluates the expression.

# Execute
# ----------
# Executes and evaluates the parse tree.
# Attributes:
# - tree (ParseTree): The parse tree to evaluate.
# Methods:
# - evaluate() -> float: Evaluates the expression and returns the result.

from operators import is_operator, apply_operator

class ParseNode:
    """ A node in the parse tree representing an operator or operand """

    def __init__(self, value: str, is_operator: bool = False):
        self.value = value
        self.is_operator = is_operator
        self.left = None  # type: ParseNode
        self.right = None  # type: ParseNode

    def __repr__(self):
        """ 
            String representation of the ParseNode
            eg. ParseNode(value='+', is_operator=True)
        """
        return f"ParseNode(value={self.value}, is_operator={self.is_operator})"
    
    def __str__(self):
        """
            String representation of the ParseNode for easy debugging
            eg. '+' , '3', '5', '24.5'
        """
        return self.value
    
    def is_leaf(self) -> bool:
        """
            Check if the node is a leaf node (i.e., it has no children).
            Returns True if the node is a leaf, False otherwise.
        """
        return not self.is_operator
        # A leaf node is an operand, hence it will not have any children.


class ParseTree:
    """ A parse tree for a mathematical expression """

    # The root of the parse tree
    __root: ParseNode = None

    # The postfix expression used to build the parse tree
    __postfix: list[str] = []

    # Constructor to initialize the parse tree with a postfix expression
    def __init__(self, postfix: list[str]):
        self.__root = None  # type: ParseNode
        self.__postfix = postfix

        self.build_tree()

    def __repr__(self):
        """ 
            String representation of the ParseTree
            eg. ParseTree(root=ParseNode(value='+', is_operator=True), postfix=['3', '4', '+'])
        """
        return f"ParseTree(root={self.__root}, postfix={self.__postfix})"
    
    def __str__(self):
        """
            String representation of the ParseTree for easy debugging
            It will be a formatted JSON representation of the parse tree.
            eg. If postfix is ['34', '5', '60', '*', '+', '8', '2', '/', '-']
            {
                "operator": "-",
                "right": {
                    "operator": "/",
                    "left": "8",
                    "right": "2"
                },
            "left": {
                "operator": "+",
                "left": "34",
                "right": {
                    "operator": "*",
                    "left": "5",
                    "right": "60"
                }
            }
        """
        if self.__root is None:
            return "{}"
        
        # Convert the parse tree to a dictionary representation and format with indentation
        import json
        return json.dumps(to_dict(self.__root), indent=4)


    # A recursive function to build the parse tree from the postfix expression
    def build_tree(self):
        """
        Build the parse tree from the postfix expression.
        The postfix expression is expected to be a list of strings.
        """
        stack : list[ParseNode] = []

        for token in self.__postfix:
            if is_operator(token):
                # If the token is an operator, pop two nodes from the stack
                right = stack.pop() if stack else None # It will be present always if postfix is correct
                left = stack.pop() if stack else None  # It will be present always if postfix is correct
                opNode = ParseNode(token, is_operator=True)
                opNode.left = left
                opNode.right = right
                stack.append(opNode)
            else:
                # If the token is an operand, create a new ParseNode and push it onto the stack
                stack.append(ParseNode(token, is_operator=False))

        # The last element in the stack is the root of the parse tree
        self.__root = stack.pop() if stack else None

    def get_root(self) -> ParseNode:
        """ 
        Get the root node of the parse tree.
        Returns None if the tree is empty.
        """
        return self.__root

    def get_postfix(self) -> list[str]:
        """ 
        Get the postfix expression used to build the parse tree.
        Returns a list of strings representing the postfix expression.
        """
        return self.__postfix

    def execute(self) -> float:
        """
        Create an Execute object to evaluate the expression represented by the parse tree.
        Returns an Execute object.
        """
        return Execute(self).evaluate()
    

# Helper function to convert a ParseNode to a dictionary representation for JSON serialization
def to_dict(node: ParseNode) -> dict:
        """
        Convert the ParseNode to a dictionary representation for JSON serialization.
        """
        if node is None:
            return None
        if node.is_operator:
            return {
                "operator": node.value,
                "left": to_dict(node.left),
                "right": to_dict(node.right)
            }
        else:
            return node.value
        

class Execute:
    """
    A class to execute the parse tree and evaluate the expression.
    It will traverse the parse tree and evaluate the expression.
    """

    def __init__(self, tree: ParseTree):
        self.tree = tree

    def evaluate(self) -> float:
        """
        Evaluate the expression represented by the parse tree.
        Returns a float representing the result of the expression.
        """
        return self.__evaluate_node(self.tree.get_root())

    def __evaluate_node(self, node: ParseNode) -> float:
        """
        Evaluate the expression represented by the given node.
        """
        if node is None:
            return 0.0
        if node.is_leaf():
            return float(node.value)
        # Operators can never be leaf nodes, hence we can safely assume that node is an operator here.
        # Recursively evaluate the left and right subtrees and apply the operator
        if node.left is None or node.right is None:
            raise ValueError("Invalid parse tree: operator node must have both left and right children.")
        left_value = self.__evaluate_node(node.left)
        right_value = self.__evaluate_node(node.right)
        return apply_operator(left_value, right_value, node.value)