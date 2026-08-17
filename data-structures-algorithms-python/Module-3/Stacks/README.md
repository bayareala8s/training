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
  


Sure! Let's consider a real-world example where we can use the stack data structure to solve a problem: **Checking for balanced parentheses in an expression**. This is a common problem in compilers and interpreters to ensure that expressions have properly matched parentheses.

### Problem Statement
Given an expression containing various types of parentheses (i.e., `()`, `{}`, `[]`), check if the parentheses are balanced. An expression is considered balanced if:
- Every opening parenthesis has a corresponding closing parenthesis of the same type.
- Parentheses are closed in the correct order.

### Solution using Stack

Here's the complete implementation, including the `Stack` class and a function to check for balanced parentheses:

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


def is_balanced(expression):
    """
    Function to check if the parentheses in the expression are balanced.
    
    :param expression: The input string containing parentheses.
    :return: True if the parentheses are balanced, False otherwise.
    """
    stack = Stack()  # Create an instance of the Stack class
    matching_parentheses = {')': '(', '}': '{', ']': '['}  # Define matching pairs of parentheses

    for char in expression:
        if char in matching_parentheses.values():
            stack.push(char)  # Push opening parentheses onto the stack
        elif char in matching_parentheses.keys():
            if stack.is_empty() or stack.pop() != matching_parentheses[char]:
                return False  # Return False if a closing parenthesis does not match the top of the stack
    return stack.is_empty()  # Return True if the stack is empty (all parentheses matched)

# Example usage
if __name__ == "__main__":
    expressions = ["{[()()]}", "{[(])}", "{{[[(())]]}}", "((()))", "({[]})"]

    for expression in expressions:
        result = is_balanced(expression)
        print(f"Expression: {expression}, is balanced: {result}")
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

3. **is_balanced Function**:
   - Checks if the parentheses in the given expression are balanced using a stack.
   - Iterates through each character in the expression.
   - Pushes opening parentheses onto the stack.
   - For closing parentheses, checks if the stack is empty or if the top of the stack matches the corresponding opening parenthesis.
   - Returns `True` if all parentheses are matched and the stack is empty, otherwise returns `False`.

4. **Example Usage**:
   - Demonstrates how to use the `is_balanced` function to check various expressions for balanced parentheses.
  

Sure! Let's consider another real-world example where a stack data structure can be used effectively: **Implementing a browser's back button functionality**.

### Problem Statement

In a web browser, users can navigate to new pages and also go back to previously visited pages using the back button. We can use two stacks to implement this functionality:
1. **History Stack**: Keeps track of pages the user has visited.
2. **Back Stack**: Keeps track of pages the user navigates back from, allowing them to go forward again.

### Solution using Stack

Here's the complete implementation, including the `Stack` class and functions to simulate the browser's back and forward functionality:

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


class BrowserHistory:
    """
    Class to simulate a browser's back and forward functionality using stacks.
    """
    def __init__(self):
        """
        Initialize the browser history with empty history and back stacks.
        """
        self.history_stack = Stack()  # Stack to keep track of visited pages
        self.back_stack = Stack()  # Stack to keep track of pages navigated back from

    def visit(self, url):
        """
        Visit a new URL.
        
        :param url: The URL of the new page to visit.
        """
        self.history_stack.push(url)  # Push the new URL onto the history stack
        self.back_stack = Stack()  # Clear the back stack since we can't go forward from a new page
        print(f"Visited: {url}")

    def back(self):
        """
        Go back to the previous page.
        
        :return: The URL of the previous page.
        :raises IndexError: If there is no previous page.
        """
        if self.history_stack.size() > 1:
            current_page = self.history_stack.pop()  # Pop the current page from the history stack
            self.back_stack.push(current_page)  # Push the current page onto the back stack
            previous_page = self.history_stack.peek()  # Peek the previous page from the history stack
            print(f"Back to: {previous_page}")
            return previous_page
        raise IndexError("No previous page to go back to")

    def forward(self):
        """
        Go forward to the next page.
        
        :return: The URL of the next page.
        :raises IndexError: If there is no next page.
        """
        if not self.back_stack.is_empty():
            next_page = self.back_stack.pop()  # Pop the next page from the back stack
            self.history_stack.push(next_page)  # Push the next page onto the history stack
            print(f"Forward to: {next_page}")
            return next_page
        raise IndexError("No next page to go forward to")


# Example usage of the BrowserHistory class
if __name__ == "__main__":
    browser = BrowserHistory()
    browser.visit("https://example.com")
    browser.visit("https://google.com")
    browser.visit("https://github.com")

    browser.back()  # Output: Back to: https://google.com
    browser.back()  # Output: Back to: https://example.com

    browser.forward()  # Output: Forward to: https://google.com
    browser.visit("https://stackoverflow.com")  # Output: Visited: https://stackoverflow.com

    browser.back()  # Output: Back to: https://google.com
    browser.forward()  # Output: Forward to: https://stackoverflow.com
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

3. **BrowserHistory Class**:
   - Simulates a browser's back and forward functionality using two stacks.
   - `__init__(self)`: Initializes the browser history with empty history and back stacks.
   - `visit(self, url)`: Visits a new URL. Pushes the new URL onto the history stack and clears the back stack.
   - `back(self)`: Goes back to the previous page. Pops the current page from the history stack, pushes it onto the back stack, and peeks the previous page from the history stack. Raises an `IndexError` if there is no previous page.
   - `forward(self)`: Goes forward to the next page. Pops the next page from the back stack and pushes it onto the history stack. Raises an `IndexError` if there is no next page.

4. **Example Usage**:
   - Demonstrates how to use the `BrowserHistory` class to visit pages, go back to previous pages, and go forward to next pages.
  
Sure! Here is a visual text diagram to illustrate how the stack is used to manage browser history for the `BrowserHistory` class:

### Initial State

```
History Stack: [ ]
Back Stack:    [ ]
```

### Visit "https://example.com"

```
History Stack: [ "https://example.com" ]
Back Stack:    [ ]
```

### Visit "https://google.com"

```
History Stack: [ "https://example.com", "https://google.com" ]
Back Stack:    [ ]
```

### Visit "https://github.com"

```
History Stack: [ "https://example.com", "https://google.com", "https://github.com" ]
Back Stack:    [ ]
```

### Back

1. Pop "https://github.com" from `History Stack` and push it to `Back Stack`.
2. Peek "https://google.com" from `History Stack`.

```
History Stack: [ "https://example.com", "https://google.com" ]
Back Stack:    [ "https://github.com" ]
```

### Back

1. Pop "https://google.com" from `History Stack` and push it to `Back Stack`.
2. Peek "https://example.com" from `History Stack`.

```
History Stack: [ "https://example.com" ]
Back Stack:    [ "https://github.com", "https://google.com" ]
```

### Forward

1. Pop "https://google.com" from `Back Stack` and push it to `History Stack`.

```
History Stack: [ "https://example.com", "https://google.com" ]
Back Stack:    [ "https://github.com" ]
```

### Visit "https://stackoverflow.com"

1. Clear `Back Stack` since we're visiting a new page.
2. Push "https://stackoverflow.com" to `History Stack`.

```
History Stack: [ "https://example.com", "https://google.com", "https://stackoverflow.com" ]
Back Stack:    [ ]
```

### Back

1. Pop "https://stackoverflow.com" from `History Stack` and push it to `Back Stack`.
2. Peek "https://google.com" from `History Stack`.

```
History Stack: [ "https://example.com", "https://google.com" ]
Back Stack:    [ "https://stackoverflow.com" ]
```

### Forward

1. Pop "https://stackoverflow.com" from `Back Stack` and push it to `History Stack`.

```
History Stack: [ "https://example.com", "https://google.com", "https://stackoverflow.com" ]
Back Stack:    [ ]
```

### Summary

- **History Stack** keeps track of the current and previously visited pages.
- **Back Stack** stores pages that we navigate back from, allowing us to go forward to them again.

This diagram visually represents how the two stacks interact to provide back and forward navigation functionality in a browser-like application.



Here's the algorithm for checking balanced parentheses in an expression using a stack, with detailed comments to explain each part of the code:

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
```

### Explanation:

1. **Node Class**:
   - **`__init__(self, value)`**: Initializes a node with a given value and sets the next reference to `None`.

2. **Stack Class**:
   - **`__init__(self)`**: Initializes an empty stack with `top` set to `None` and `count` set to 0.
   - **`push(self, item)`**: Adds a new item to the top of the stack. Creates a new node, updates the `top`, and increments the count.
   - **`pop(self)`**: Removes and returns the top item from the stack. Updates the `top` and decrements the count. Raises an `IndexError` if the stack is empty.
   - **`peek(self)`**: Returns the top item without removing it. Raises an `IndexError` if the stack is empty.
   - **`is_empty(self)`**: Checks if the stack is empty by checking if `top` is `None`.
   - **`size(self)`**: Returns the number of items in the stack by returning the count.

3. **is_balanced Function**:
   - **`is_balanced(expression)`**: Checks if the parentheses in the given expression are balanced using a stack.
   - **`stack`**: Creates an instance of the `Stack` class.
   - **`matching_parentheses`**: Defines a dictionary to match closing parentheses with their corresponding opening parentheses.
   - **`for char in expression`**: Iterates through each character in the expression.
     - If the character is an opening parenthesis (`(`, `{`, `[`), it is pushed onto the stack.
     - If the character is a closing parenthesis (`)`, `}`, `]`), it checks if the stack is empty or if the top of the stack does not match the corresponding opening parenthesis. If either condition is true, it returns `False`.
   - **`return stack.is_empty()`**: Returns `True` if the stack is empty (all parentheses matched), otherwise `False`.

4. **Example Usage**:
   - Demonstrates how to use the `is_balanced` function to check various expressions for balanced parentheses.
  

Sure! Here’s a visual text diagram to illustrate the stack operations in the context of checking for balanced parentheses in an expression.

### Example Expression: `{[()()]}`

### Initial State

```
Expression: {[()()]}
Stack: [ ]
```

### Iteration through the expression:

1. **Character `{`**:
   - It's an opening parenthesis, so push it onto the stack.
   ```
   Stack: [ { ]
   ```

2. **Character `[`**:
   - It's an opening parenthesis, so push it onto the stack.
   ```
   Stack: [ {, [ ]
   ```

3. **Character `(`**:
   - It's an opening parenthesis, so push it onto the stack.
   ```
   Stack: [ {, [, ( ]
   ```

4. **Character `)`**:
   - It's a closing parenthesis. Check if it matches the top of the stack.
   - Top of the stack is `(`, which matches `)`, so pop the top.
   ```
   Stack: [ {, [ ]
   ```

5. **Character `(`**:
   - It's an opening parenthesis, so push it onto the stack.
   ```
   Stack: [ {, [, ( ]
   ```

6. **Character `)`**:
   - It's a closing parenthesis. Check if it matches the top of the stack.
   - Top of the stack is `(`, which matches `)`, so pop the top.
   ```
   Stack: [ {, [ ]
   ```

7. **Character `]`**:
   - It's a closing parenthesis. Check if it matches the top of the stack.
   - Top of the stack is `[`, which matches `]`, so pop the top.
   ```
   Stack: [ { ]
   ```

8. **Character `}`**:
   - It's a closing parenthesis. Check if it matches the top of the stack.
   - Top of the stack is `{`, which matches `}`, so pop the top.
   ```
   Stack: [ ]
   ```

### Final State

- The stack is empty, indicating all parentheses are balanced.
```
Stack: [ ]
```

### Summary

For each character in the expression:
1. **Opening Parentheses (`{`, `[`, `(`)**:
   - Push onto the stack.
   ```
   Stack after pushing opening parenthesis: [ ... ]
   ```

2. **Closing Parentheses (`}`, `]`, `)`)**:
   - Check if the stack is not empty and the top of the stack matches the corresponding opening parenthesis.
   - Pop the top of the stack if it matches.
   ```
   Stack after popping matching parenthesis: [ ... ]
   ```

### Diagram of the Process:

```
Initial:
Expression: {[()()]}
Stack: [ ]

1. Push '{':
Expression: {[()()]}
Stack: [ { ]

2. Push '[':
Expression: {[()()]}
Stack: [ {, [ ]

3. Push '(':
Expression: {[()()]}
Stack: [ {, [, ( ]

4. Pop '(' (matches ')'):
Expression: {[()()]}
Stack: [ {, [ ]

5. Push '(':
Expression: {[()()]}
Stack: [ {, [, ( ]

6. Pop '(' (matches ')'):
Expression: {[()()]}
Stack: [ {, [ ]

7. Pop '[' (matches ']'):
Expression: {[()()]}
Stack: [ { ]

8. Pop '{' (matches '}'):
Expression: {[()()]}
Stack: [ ]

Final:
Expression: {[()()]}
Stack: [ ]

All parentheses are balanced.
```

This visual text diagram illustrates how the stack operations maintain balance by matching every closing parenthesis with the correct opening parenthesis. If, at the end of the iteration, the stack is empty, it means all parentheses in the expression are balanced.
