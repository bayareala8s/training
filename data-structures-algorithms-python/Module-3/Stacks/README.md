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
