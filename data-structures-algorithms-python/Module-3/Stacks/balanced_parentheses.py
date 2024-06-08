class Node:
    """
    Class to represent a node in the stack.
    Each node contains a value and a reference to the next node.
    """

    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    """
    Class to represent the stack data structure.
    The stack follows the LIFO (Last In, First Out) principle.
    """

    def __init__(self):
        """
        Initialize an empty stack.
        The top attribute points to the top node in the stack.
        The count attribute keeps track of the number of elements in the stack.
        """
        self.top = None
        self.count = 0

    def push(self, item):
        """
        Add an item to the top of the stack.

        :param item: The item to be added to the stack.
        """
        new_node = Node(item)  # Create a new node with the given item
        new_node.next = self.top  # Make the new node point to the current top node
        self.top = new_node  # Update the top to be the new node
        self.count += 1  # Increment the count of elements

    def pop(self):
        """
        Remove and return the top item from the stack.

        :return: The value of the top item in the stack.
        :raises IndexError: If the stack is empty.
        """
        if not self.is_empty():
            popped_value = self.top.value  # Get the value of the top item
            self.top = self.top.next  # Update the top to the next node
            self.count -= 1  # Decrement the count of elements
            return popped_value
        raise IndexError("pop from empty stack")  # Raise an error if the stack is empty

    def peek(self):
        """
        Return the top item from the stack without removing it.

        :return: The value of the top item in the stack.
        :raises IndexError: If the stack is empty.
        """
        if not self.is_empty():
            return self.top.value  # Return the value of the top item
        raise IndexError("peek from empty stack")  # Raise an error if the stack is empty

    def is_empty(self):
        """
        Check if the stack is empty.

        :return: True if the stack is empty, False otherwise.
        """
        return self.top is None  # Return True if top is None, indicating the stack is empty

    def size(self):
        """
        Return the number of items in the stack.

        :return: The number of items in the stack.
        """
        return self.count  # Return the count of elements


def is_balanced(expression):
    """
    Function to check if the parentheses in the expression are balanced.

    :param expression: The input string containing parentheses.
    :return: True if the parentheses are balanced, False otherwise.
    """
    stack = Stack()  # Create an instance of the Stack class
    # Define matching pairs of parentheses
    matching_parentheses = {')': '(', '}': '{', ']': '['}

    # Iterate through each character in the expression
    for char in expression:
        if char in matching_parentheses.values():
            # If the character is an opening parenthesis, push it onto the stack
            stack.push(char)
        elif char in matching_parentheses.keys():
            # If the character is a closing parenthesis
            if stack.is_empty() or stack.pop() != matching_parentheses[char]:
                # Check if the stack is empty or the top item does not match the corresponding opening parenthesis
                return False  # If not balanced, return False

    # If the stack is empty, all parentheses were balanced, otherwise return False
    return stack.is_empty()


# Example usage of the is_balanced function
if __name__ == "__main__":
    expressions = ["{[()()]}", "{[(])}", "{{[[(())]]}}", "((()))", "({[]})"]

    for expression in expressions:
        result = is_balanced(expression)
        print(f"Expression: {expression}, is balanced: {result}")
