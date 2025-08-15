#!/usr/bin/env python3
# filepath: /home/uncanny/Desktop/Cutie/BodmasParser/test_parser.py

import unittest
from index import Parser
from parseTree import ParseNode, ParseTree, Execute
from operators import is_operator, get_precedence, is_valid_expression, valid_parentheses, apply_operator


class TestOperators(unittest.TestCase):
    """Test cases for the operators.py module"""
    
    def test_is_operator(self):
        """Test the is_operator function"""
        self.assertTrue(is_operator('+'))
        self.assertTrue(is_operator('-'))
        self.assertTrue(is_operator('*'))
        self.assertTrue(is_operator('/'))
        self.assertTrue(is_operator('^'))
        self.assertFalse(is_operator('a'))
        self.assertFalse(is_operator('1'))
        self.assertFalse(is_operator('()'))
    
    def test_get_precedence(self):
        """Test the get_precedence function"""
        self.assertEqual(get_precedence('+'), 1)
        self.assertEqual(get_precedence('-'), 1)
        self.assertEqual(get_precedence('*'), 2)
        self.assertEqual(get_precedence('/'), 2)
        self.assertEqual(get_precedence('^'), 3)
        self.assertEqual(get_precedence('a'), 0)  # Unknown operator
    
    def test_apply_operator(self):
        """Test the apply_operator function"""
        self.assertEqual(apply_operator(3, 4, '+'), 7)
        self.assertEqual(apply_operator(3, 4, '-'), -1)
        self.assertEqual(apply_operator(3, 4, '*'), 12)
        self.assertEqual(apply_operator(12, 4, '/'), 3)
        self.assertEqual(apply_operator(2, 3, '^'), 8)
        
        # Test with floating-point numbers
        self.assertAlmostEqual(apply_operator(3.5, 1.5, '+'), 5.0)
        self.assertAlmostEqual(apply_operator(3.5, 1.5, '-'), 2.0)
        
        # Test for error with unknown operator
        with self.assertRaises(ValueError):
            apply_operator(3, 4, '%')
            apply_operator(3, 4, '%')
    
    def test_valid_parentheses(self):
        """Test the valid_parentheses function"""
        self.assertTrue(valid_parentheses('()'))
        self.assertTrue(valid_parentheses('(())'))
        self.assertTrue(valid_parentheses('(a+b)'))
        self.assertFalse(valid_parentheses('('))
        self.assertFalse(valid_parentheses(')'))
        self.assertFalse(valid_parentheses(')('))
        self.assertFalse(valid_parentheses('())'))
    
    def test_is_valid_expression(self):
        """Test the is_valid_expression function"""
        # Valid expressions
        self.assertTrue(is_valid_expression('3+4'))
        self.assertTrue(is_valid_expression('3.5+4.2'))
        self.assertTrue(is_valid_expression('3+4*5'))
        
        # Invalid expressions
        self.assertFalse(is_valid_expression(''))
        self.assertFalse(is_valid_expression('3++4'))
        self.assertFalse(is_valid_expression('3+4)'))
        self.assertFalse(is_valid_expression('(3+4'))
        self.assertFalse(is_valid_expression('3+'))
        self.assertFalse(is_valid_expression('+3'))
        self.assertFalse(is_valid_expression('3.4.5'))


class TestParseNode(unittest.TestCase):
    """Test cases for the ParseNode class"""
    
    def test_init(self):
        """Test the initialization of a ParseNode"""
        node = ParseNode('42')
        self.assertEqual(node.value, '42')
        self.assertFalse(node.is_operator)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        
        op_node = ParseNode('+', is_operator=True)
        self.assertEqual(op_node.value, '+')
        self.assertTrue(op_node.is_operator)
    
    def test_str_repr(self):
        """Test string representation of ParseNode"""
        node = ParseNode('42')
        self.assertEqual(str(node), '42')
        self.assertEqual(repr(node), 'ParseNode(value=42, is_operator=False)')
        
        op_node = ParseNode('+', is_operator=True)
        self.assertEqual(str(op_node), '+')
        self.assertEqual(repr(op_node), 'ParseNode(value=+, is_operator=True)')
    
    def test_is_leaf(self):
        """Test the is_leaf method"""
        node = ParseNode('42')
        self.assertTrue(node.is_leaf())
        
        op_node = ParseNode('+', is_operator=True)
        self.assertFalse(op_node.is_leaf())


class TestParseTree(unittest.TestCase):
    """Test cases for the ParseTree class"""
    
    def test_simple_tree(self):
        """Test building a simple parse tree"""
        # Test a simple expression: 3 + 4
        postfix = ['3', '4', '+'] 
        tree = ParseTree(postfix)
        root = tree.get_root()
        
        self.assertEqual(root.value, '+')
        self.assertTrue(root.is_operator)
        self.assertEqual(root.left.value, '3')
        self.assertEqual(root.right.value, '4')
        self.assertFalse(root.left.is_operator)
        self.assertFalse(root.right.is_operator)
    
    def test_complex_tree(self):
        """Test building a more complex parse tree"""
        # Test expression: 3 + 4 * 5
        postfix = ['3', '4', '5', '*', '+']
        tree = ParseTree(postfix)
        root = tree.get_root()
        
        self.assertEqual(root.value, '+')
        self.assertEqual(root.left.value, '3')
        self.assertEqual(root.right.value, '*')
        self.assertEqual(root.right.left.value, '4')
        self.assertEqual(root.right.right.value, '5')
    
    def test_execute(self):
        """Test the execute method"""
        # Test: 3 + 4
        postfix1 = ['3', '4', '+']
        tree = ParseTree(postfix1)
        self.assertEqual(tree.execute(), 7)
        
        # Test: 3 + 4 * 5
        postfix2 = ['3', '4', '5', '*', '+']
        tree = ParseTree(postfix2)
        self.assertEqual(tree.execute(), 23)


class TestExecute(unittest.TestCase):
    """Test cases for the Execute class"""
    
    def test_evaluate_simple(self):
        """Test evaluating a simple expression"""
        postfix = ['3', '4', '+']
        tree = ParseTree(postfix)
        executor = Execute(tree)
        self.assertEqual(executor.evaluate(), 7)
    
    def test_evaluate_complex(self):
        """Test evaluating a complex expression"""
        postfix = ['3', '4', '5', '*', '+']
        tree = ParseTree(postfix)
        executor = Execute(tree)
        self.assertEqual(executor.evaluate(), 23)
    
    def test_evaluate_with_error(self):
        """Test error handling in evaluation"""
        # Create a parse tree with an invalid structure (missing child)
        postfix = ['3', '4', '+']
        tree = ParseTree(postfix)
        root = tree.get_root()
        root.left = None  # Deliberately break the tree
        
        executor = Execute(tree)
        with self.assertRaises(ValueError):
            executor.evaluate()


class TestParser(unittest.TestCase):
    """Test cases for the Parser class"""
    
    def test_infix_to_postfix(self):
        """Test conversion from infix to postfix"""
        parser = Parser("3+4")
        self.assertEqual(parser.postfix, ['3', '4', '+'])
        
        parser = Parser("3+4*5")
        self.assertEqual(parser.postfix, ['3', '4', '5', '*', '+'])
        
        parser = Parser("3*4+5")
        self.assertEqual(parser.postfix, ['3', '4', '*', '5', '+'])
    
    def test_evaluate(self):
        """Test evaluation of expressions"""
        parser = Parser("3+4")
        self.assertEqual(parser.evaluate(), 7)
        
        parser = Parser("3+4*5")
        self.assertEqual(parser.evaluate(), 23)
        
        # Skip parentheses test as current validation doesn't support parentheses
        # parser = Parser("(3+4)*5")
        # self.assertEqual(parser.evaluate(), 35)
        
        parser = Parser("3*4+5")
        self.assertEqual(parser.evaluate(), 17)
        
        parser = Parser("3^2")
        self.assertEqual(parser.evaluate(), 9)
        
        # Test expressions with parentheses
        parser = Parser("(3+4)*5")
        self.assertEqual(parser.evaluate(), 35)
        
        parser = Parser("3*(4+5)")
        self.assertEqual(parser.evaluate(), 27)
        
        parser = Parser("(3+4)*(5-2)")
        self.assertEqual(parser.evaluate(), 21)
        
        parser = Parser("((3+4)*2)")
        self.assertEqual(parser.evaluate(), 14)
    
    def test_invalid_expressions(self):
        """Test handling of invalid expressions"""
        with self.assertRaises(ValueError):
            Parser("3++4")
        
        with self.assertRaises(ValueError):
            Parser("3+")
        
        with self.assertRaises(ValueError):
            Parser("+3")
        
        with self.assertRaises(ValueError):
            Parser("3+4)")
        
        with self.assertRaises(ValueError):
            Parser("(3+4")


if __name__ == '__main__':
    unittest.main()
