### Detailed Guidance for Data Structures and Algorithms: Stack in Python

#### Introduction to Stack

A stack is a linear data structure that follows the Last In, First Out (LIFO) principle. The most recently added element is the one that is removed first. Stacks are used in various applications such as function call management, expression evaluation, and syntax parsing.

#### Key Operations of a Stack

1. **Push**: Adds an element to the top of the stack.
2. **Pop**: Removes and returns the top element of the stack.
3. **Peek**: Returns the top element of the stack without removing it.
4. **isEmpty**: Checks if the stack is empty.
5. **size**: Returns the number of elements in the stack.

#### Implementing Stack in Python

There are different ways to implement a stack in Python, including using lists, collections.deque, or creating a custom class.

##### 1. Stack using Python List

```python
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

# Example usage
s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())    # Output: 3
print(s.peek())   # Output: 2
print(s.size())   # Output: 2
```

##### 2. Stack using `collections.deque`

The `collections.deque` module provides an efficient implementation of stack operations.

```python
from collections import deque

class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

# Example usage
s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())    # Output: 3
print(s.peek())   # Output: 2
print(s.size())   # Output: 2
```

##### 3. Custom Stack Class

Creating a custom class allows more control and can be extended with additional features if needed.

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.count += 1

    def pop(self):
        if not self.is_empty():
            popped_value = self.top.value
            self.top = self.top.next
            self.count -= 1
            return popped_value
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.top.value
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return self.top is None

    def size(self):
        return self.count

# Example usage
s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())    # Output: 3
print(s.peek())   # Output: 2
print(s.size())   # Output: 2
```

#### Real-World Applications of Stack

1. **Expression Evaluation**: Stacks are used to evaluate arithmetic expressions (infix, postfix, prefix).
2. **Backtracking**: In algorithms like maze solving or parsing, stacks are used to keep track of paths.
3. **Function Call Management**: In many programming languages, the call stack is used to manage function calls and local variables.
4. **Syntax Parsing**: Stacks are used in compilers and interpreters to parse expressions and syntax trees.

#### Algorithm Example: Balanced Parentheses

A common algorithmic problem involving stacks is checking for balanced parentheses in an expression.

```python
def is_balanced(expression):
    stack = Stack()
    matching_parentheses = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in matching_parentheses.values():
            stack.push(char)
        elif char in matching_parentheses.keys():
            if stack.is_empty() or stack.pop() != matching_parentheses[char]:
                return False
    return stack.is_empty()

# Example usage
print(is_balanced("{[()]}"))  # Output: True
print(is_balanced("{[(])}"))  # Output: False
```

#### Conclusion

Stacks are a fundamental data structure with numerous applications in computer science. Implementing a stack in Python can be done using lists, `collections.deque`, or a custom class, each offering different advantages. Understanding stacks and their operations is crucial for solving various algorithmic problems efficiently.



### Time and Space Complexity Analysis for Stack Operations

#### 1. Stack Using Python List

```python
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
```

**Time Complexity:**
- `push(item)`: O(1) - Appending an element to the end of a list is an O(1) operation in Python.
- `pop()`: O(1) - Removing the last element of a list is also an O(1) operation.
- `peek()`: O(1) - Accessing the last element of a list is an O(1) operation.
- `is_empty()`: O(1) - Checking the length of the list is an O(1) operation.
- `size()`: O(1) - Returning the length of the list is an O(1) operation.

**Space Complexity:**
- The space complexity is O(n), where n is the number of elements in the stack. This is because the list grows dynamically with the number of elements.

#### 2. Stack Using `collections.deque`

```python
from collections import deque

class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)
```

**Time Complexity:**
- `push(item)`: O(1) - Appending an element to the end of a deque is an O(1) operation.
- `pop()`: O(1) - Removing the last element of a deque is also an O(1) operation.
- `peek()`: O(1) - Accessing the last element of a deque is an O(1) operation.
- `is_empty()`: O(1) - Checking the length of the deque is an O(1) operation.
- `size()`: O(1) - Returning the length of the deque is an O(1) operation.

**Space Complexity:**
- The space complexity is O(n), where n is the number of elements in the stack. The deque grows dynamically with the number of elements.

#### 3. Custom Stack Class

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.count += 1

    def pop(self):
        if not self.is_empty():
            popped_value = self.top.value
            self.top = self.top.next
            self.count -= 1
            return popped_value
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.top.value
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return self.top is None

    def size(self):
        return self.count
```

**Time Complexity:**
- `push(item)`: O(1) - Inserting a new node at the beginning of a linked list is an O(1) operation.
- `pop()`: O(1) - Removing the node from the beginning of a linked list is an O(1) operation.
- `peek()`: O(1) - Accessing the top node is an O(1) operation.
- `is_empty()`: O(1) - Checking if the top node is None is an O(1) operation.
- `size()`: O(1) - Returning the count of nodes is an O(1) operation.

**Space Complexity:**
- The space complexity is O(n), where n is the number of elements in the stack. Each node in the linked list requires space for the value and a reference to the next node.

### Example Algorithm: Balanced Parentheses

```python
def is_balanced(expression):
    stack = Stack()
    matching_parentheses = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in matching_parentheses.values():
            stack.push(char)
        elif char in matching_parentheses.keys():
            if stack.is_empty() or stack.pop() != matching_parentheses[char]:
                return False
    return stack.is_empty()
```

**Time Complexity:**
- O(n), where n is the length of the expression. Each character is processed once, and stack operations (push and pop) are O(1).

**Space Complexity:**
- O(n) in the worst case, where all characters in the expression are opening parentheses and get pushed onto the stack.

### Summary

- **List-based Stack**: Efficient for typical stack operations with O(1) time complexity but may have memory overhead due to Python's dynamic list resizing.
- **Deque-based Stack**: Similar performance to list-based stack but is generally more memory efficient.
- **Custom Class-based Stack**: Slightly more complex implementation but provides more control and is ideal for educational purposes and understanding the underlying mechanics of stack operations.

Each implementation has its own use cases and trade-offs. For most practical purposes in Python, using a list or `collections.deque` will suffice due to their simplicity and efficiency.


Sure! Here is a detailed implementation of a stack in Python using a custom class, complete with comments to explain each part of the code.

```python
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


# Example usage of the Stack class
if __name__ == "__main__":
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.pop())    # Output: 3
    print(s.peek())   # Output: 2
    print(s.size())   # Output: 2
    print(s.is_empty())  # Output: False
    s.pop()
    s.pop()
    print(s.is_empty())  # Output: True
```

### Explanation:

1. **Node Class**:
   - Represents a node in the stack with a value and a reference to the next node.
   - `__init__(self, value)`: Initializes the node with a given value and sets the next reference to `None`.

2. **Stack Class**:
   - Represents the stack itself.
   - `__init__(self)`: Initializes an empty stack with `top` set to `None` and `count` set to 0.
   - `push(self, item)`: Adds a new item to the top of the stack. Creates a new node, updates the `top`, and increments the count.
   - `pop(self)`: Removes and returns the top item from the stack. Updates the `top` and decrements the count. Raises an `IndexError` if the stack is empty.
   - `peek(self)`: Returns the top item without removing it. Raises an `IndexError` if the stack is empty.
   - `is_empty(self)`: Checks if the stack is empty by checking if `top` is `None`.
   - `size(self)`: Returns the number of items in the stack by returning the count.

3. **Example Usage**:
   - Demonstrates how to use the `Stack` class by pushing, popping, peeking, and checking the size and emptiness of the stack.
