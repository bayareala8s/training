class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        """
        This method pushes an item onto the stack.
        """
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """
        This method pops an item off the stack.
        """
        if self.top is None:
            return "Stack is empty"
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        """
        This method returns the top item from the stack but does not remove it.
        """
        if self.top is None:
            return "Stack is empty"
        else:
            return self.top.data

    def is_empty(self):
        """
        This method returns True if the stack is empty and False otherwise.
        """
        return self.top is None

def reverse_string(stack, input_str):
    """
    This function uses a stack to reverse a string.
    """
    # Push all characters of the string onto the stack
    for char in input_str:
        stack.push(char)

    reversed_str = ""
    # Pop all characters from the stack and append them to the reversed string
    while not stack.is_empty():
        reversed_str += stack.pop()

    return reversed_str

# Create a new stack
stack = Stack()

# Use the stack to reverse a string
input_str = "Hello, World!"
print(reverse_string(stack, input_str))  # Output: "!dlroW ,olleH"