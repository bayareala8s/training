### Python Refresher: Syntax, Functions, and Classes

This section provides a refresher on Python syntax, functions, and classes, which are fundamental for understanding and implementing data structures and algorithms.

---

### Basic Python Syntax

Python is a high-level, interpreted programming language known for its readability and simplicity. Here are some basic concepts:

#### Variables and Data Types

```python
# Variables do not need explicit declaration
x = 10        # Integer
y = 20.5      # Float
name = "Alice" # String
is_student = True # Boolean

# Printing variables
print(x)       # Output: 10
print(y)       # Output: 20.5
print(name)    # Output: Alice
print(is_student) # Output: True
```

#### Data Structures

```python
# Lists
numbers = [1, 2, 3, 4, 5]
print(numbers)      # Output: [1, 2, 3, 4, 5]

# Tuples
coordinates = (10.0, 20.0)
print(coordinates)  # Output: (10.0, 20.0)

# Dictionaries
student = {"name": "Alice", "age": 22}
print(student)      # Output: {'name': 'Alice', 'age': 22}

# Sets
unique_numbers = {1, 2, 3, 3, 4}
print(unique_numbers) # Output: {1, 2, 3, 4}
```

#### Control Structures

```python
# If-else statement
age = 18
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# For loop
for num in numbers:
    print(num)  # Output: 1 2 3 4 5

# While loop
count = 0
while count < 5:
    print(count)
    count += 1  # Output: 0 1 2 3 4
```

#### List Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(1, 6)]
print(squares)  # Output: [1, 4, 9, 16, 25]
```

### Functions

Functions are blocks of code that perform a specific task and can be reused. They are defined using the `def` keyword.

#### Defining and Calling Functions

```python
# Defining a function
def greet(name):
    return f"Hello, {name}!"

# Calling a function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

#### Function Parameters and Return Values

```python
# Function with parameters
def add(a, b):
    return a + b

# Calling the function
result = add(5, 3)
print(f"Sum: {result}")  # Output: Sum: 8
```

#### Default Parameters

```python
# Function with default parameter
def greet(name, message="Hello"):
    return f"{message}, {name}!"

# Calling the function with and without the default parameter
print(greet("Alice"))              # Output: Hello, Alice!
print(greet("Bob", "Good morning")) # Output: Good morning, Bob!
```

#### Variable Scope

```python
# Global and local variables
x = 10  # Global variable

def modify_variable():
    global x  # Use global variable
    x = 5     # Modify global variable
    print(f"Inside function: {x}")  # Output: Inside function: 5

modify_variable()
print(f"Outside function: {x}")     # Output: Outside function: 5
```

### Classes and Objects

Classes provide a means of bundling data and functionality together. Creating a new class creates a new type of object, allowing new instances of that type to be made.

#### Defining a Class

```python
# Defining a class
class Person:
    def __init__(self, name, age):  # Constructor
        self.name = name            # Instance variable
        self.age = age

    def greet(self):                # Method
        return f"Hello, my name is {self.name} and I am {self.age} years old."

# Creating an object
alice = Person("Alice", 30)

# Calling a method
print(alice.greet())  # Output: Hello, my name is Alice and I am 30 years old.
```

#### Inheritance

Inheritance allows a class to inherit attributes and methods from another class.

```python
# Defining a parent class
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclasses must implement this method")

# Defining a child class
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

# Creating an object of the child class
dog = Dog("Buddy")
print(dog.speak())  # Output: Buddy says Woof!
```

#### Encapsulation

Encapsulation restricts access to certain methods and variables. This can prevent the data from being modified by accident and is implemented by using private variables.

```python
# Encapsulation
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private variable

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance

# Creating an object
account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())  # Output: 1300
```

### Practical Exercises

#### Exercise 1: Basic Function

```python
# Define a function to calculate the square of a number
def square(n):
    return n * n

# Test the function
print(square(4))  # Output: 16
print(square(5))  # Output: 25
```

#### Exercise 2: Class Implementation

```python
# Define a class for a simple calculator
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Division by zero is undefined."

# Create an object of the Calculator class
calc = Calculator()
print(calc.add(10, 5))        # Output: 15
print(calc.subtract(10, 5))   # Output: 5
print(calc.multiply(10, 5))   # Output: 50
print(calc.divide(10, 5))     # Output: 2.0
print(calc.divide(10, 0))     # Output: Division by zero is undefined.
```

These examples and exercises provide a solid foundation in Python syntax, functions, and classes, which are essential for understanding and implementing data structures and algorithms.
