## Linked Lists

### Introduction
A linked list is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence. Unlike arrays, linked lists do not require a contiguous block of memory, making them dynamic and flexible for certain applications.

### Types of Linked Lists
1. **Singly Linked List**: Each node points to the next node.
2. **Doubly Linked List**: Each node points to both the next and previous nodes.
3. **Circular Linked List**: The last node points back to the first node, forming a circle.

### Basic Operations
1. **Insertion**: Adding a new node to the list.
2. **Deletion**: Removing an existing node from the list.
3. **Traversal**: Accessing each node in the list sequentially.
4. **Searching**: Finding a node with a specific value.

### Implementation in Python
#### Node Class
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None  # For doubly linked lists
```

#### Singly Linked List
```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete_node(self, key):
        temp = self.head
        if temp and temp.data == key:
            self.head = temp.next
            temp = None
            return
        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next
        if temp is None:
            return
        prev.next = temp.next
        temp = None

    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements
```

#### Doubly Linked List
```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def delete_node(self, key):
        temp = self.head
        while temp:
            if temp.data == key:
                if temp.prev:
                    temp.prev.next = temp.next
                if temp.next:
                    temp.next.prev = temp.prev
                if temp == self.head:
                    self.head = temp.next
                temp = None
                return
            temp = temp.next

    def traverse_forward(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def traverse_backward(self):
        elements = []
        current = self.head
        while current and current.next:
            current = current.next
        while current:
            elements.append(current.data)
            current = current.prev
        return elements
```

### Common Use Cases
- **Dynamic Memory Allocation**: Linked lists can efficiently manage memory by allocating and deallocating nodes as needed.
- **Implementing Data Structures**: Many complex data structures like stacks, queues, and graphs use linked lists as their building blocks.
- **Managing Ordered Data**: Linked lists are useful when the data needs to be ordered, but the order can change frequently.

### Performance Considerations
- **Insertion and Deletion**: These operations are generally efficient, especially at the beginning of the list, as they only require a few pointer updates.
- **Access Time**: Linked lists do not support efficient random access. Accessing an element requires traversing the list from the head, resulting in O(n) time complexity.
- **Memory Overhead**: Each node in a linked list requires additional memory for storing pointers, which can be a drawback compared to arrays.

### Practical Tips
- **Choosing the Right Data Structure**: Use linked lists when dynamic size and frequent insertions/deletions are needed. Opt for arrays when random access is a priority.
- **Memory Management**: Be cautious about memory leaks by ensuring all unused nodes are properly deallocated, especially in languages without automatic garbage collection.
- **Optimizations**: For doubly linked lists, consider using sentinel nodes (dummy nodes) to simplify edge case handling.

This should give you a comprehensive understanding of linked lists and their implementation. If you have any specific questions or need further details, feel free to ask!


Here are some real-world implementation examples of linked lists to illustrate their use in practical applications.

### 1. Implementing an Undo Feature

An undo feature in applications (e.g., text editors, drawing programs) can be efficiently managed using a linked list. Each state of the document can be represented by a node in a doubly linked list, allowing users to traverse back and forth through the history of changes.

```python
class DocumentState:
    def __init__(self, content):
        self.content = content

class UndoFeature:
    def __init__(self):
        self.current = None

    def save_state(self, content):
        new_state = DocumentState(content)
        if self.current:
            new_state.prev = self.current
            self.current.next = new_state
        self.current = new_state

    def undo(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.content if self.current else None

    def redo(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.content if self.current else None

# Example Usage
editor = UndoFeature()
editor.save_state("Version 1")
editor.save_state("Version 2")
editor.save_state("Version 3")

print(editor.undo())  # Output: Version 2
print(editor.undo())  # Output: Version 1
print(editor.redo())  # Output: Version 2
```

### 2. Browser History Management

A browser can use a doubly linked list to manage the history of visited web pages, allowing users to navigate back and forth between pages.

```python
class Page:
    def __init__(self, url):
        self.url = url

class BrowserHistory:
    def __init__(self):
        self.current = None

    def visit_page(self, url):
        new_page = Page(url)
        if self.current:
            new_page.prev = self.current
            self.current.next = new_page
        self.current = new_page

    def back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.url if self.current else None

    def forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.url if self.current else None

# Example Usage
history = BrowserHistory()
history.visit_page("google.com")
history.visit_page("github.com")
history.visit_page("stackoverflow.com")

print(history.back())  # Output: github.com
print(history.back())  # Output: google.com
print(history.forward())  # Output: github.com
```

### 3. LRU Cache Implementation

An LRU (Least Recently Used) cache can be implemented using a combination of a doubly linked list and a hash map. The doubly linked list maintains the order of elements, with the most recently accessed elements at the front.

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None

    def _remove(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.tail:
            self.tail = node.prev
        if node == self.head:
            self.head = node.next

    def _add_to_front(self, node):
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        new_node = Node(key, value)
        self._add_to_front(new_node)
        self.cache[key] = new_node
        if len(self.cache) > self.capacity:
            del self.cache[self.tail.key]
            self._remove(self.tail)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

# Example Usage
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Output: 1
cache.put(3, 3)  # LRU key was 2, evicts key 2
print(cache.get(2))  # Output: -1
cache.put(4, 4)  # LRU key was 1, evicts key 1
print(cache.get(1))  # Output: -1
print(cache.get(3))  # Output: 3
print(cache.get(4))  # Output: 4
```

### 4. Music Playlist Management

A music player can use a circular linked list to manage the playlist, allowing continuous play of songs in a loop.

```python
class Song:
    def __init__(self, title):
        self.title = title
        self.next = None

class MusicPlaylist:
    def __init__(self):
        self.current = None

    def add_song(self, title):
        new_song = Song(title)
        if not self.current:
            self.current = new_song
            self.current.next = self.current
        else:
            temp = self.current
            while temp.next != self.current:
                temp = temp.next
            temp.next = new_song
            new_song.next = self.current

    def play_next(self):
        if self.current:
            self.current = self.current.next
            return self.current.title
        return None

# Example Usage
playlist = MusicPlaylist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
playlist.add_song("Song 3")

print(playlist.play_next())  # Output: Song 1
print(playlist.play_next())  # Output: Song 2
print(playlist.play_next())  # Output: Song 3
print(playlist.play_next())  # Output: Song 1 (loop back to the beginning)
```

These examples demonstrate how linked lists can be applied in real-world scenarios to manage dynamic data efficiently.



Sure! Here are more real-world examples where linked lists are effectively used:

### 5. Task Scheduling

A task scheduler can use a circular linked list to cycle through tasks, allowing each task to be executed in a round-robin fashion.

```python
class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.next = None

class TaskScheduler:
    def __init__(self):
        self.current = None

    def add_task(self, name, duration):
        new_task = Task(name, duration)
        if not self.current:
            self.current = new_task
            self.current.next = self.current
        else:
            temp = self.current
            while temp.next != self.current:
                temp = temp.next
            temp.next = new_task
            new_task.next = self.current

    def execute_next(self):
        if self.current:
            task = self.current
            self.current = self.current.next
            return f"Executing task: {task.name} for {task.duration} minutes"
        return None

# Example Usage
scheduler = TaskScheduler()
scheduler.add_task("Task 1", 30)
scheduler.add_task("Task 2", 45)
scheduler.add_task("Task 3", 20)

print(scheduler.execute_next())  # Output: Executing task: Task 1 for 30 minutes
print(scheduler.execute_next())  # Output: Executing task: Task 2 for 45 minutes
print(scheduler.execute_next())  # Output: Executing task: Task 3 for 20 minutes
print(scheduler.execute_next())  # Output: Executing task: Task 1 for 30 minutes (cycle repeats)
```

### 6. Railway Reservation System

A railway reservation system can use a linked list to manage the reservation of seats. Each node can represent a seat with its reservation status.

```python
class Seat:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.is_reserved = False
        self.next = None

class RailwayReservation:
    def __init__(self):
        self.head = None

    def add_seat(self, seat_number):
        new_seat = Seat(seat_number)
        if not self.head:
            self.head = new_seat
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_seat

    def reserve_seat(self, seat_number):
        temp = self.head
        while temp:
            if temp.seat_number == seat_number and not temp.is_reserved:
                temp.is_reserved = True
                return f"Seat {seat_number} reserved successfully."
            temp = temp.next
        return f"Seat {seat_number} is already reserved or does not exist."

    def get_seat_status(self, seat_number):
        temp = self.head
        while temp:
            if temp.seat_number == seat_number:
                return f"Seat {seat_number} is {'reserved' if temp.is_reserved else 'available'}."
            temp = temp.next
        return f"Seat {seat_number} does not exist."

# Example Usage
reservation_system = RailwayReservation()
reservation_system.add_seat(1)
reservation_system.add_seat(2)
reservation_system.add_seat(3)

print(reservation_system.reserve_seat(2))  # Output: Seat 2 reserved successfully.
print(reservation_system.get_seat_status(2))  # Output: Seat 2 is reserved.
print(reservation_system.get_seat_status(3))  # Output: Seat 3 is available.
```

### 7. Polynomial Arithmetic

Polynomials can be represented using linked lists to perform arithmetic operations such as addition and multiplication.

```python
class PolynomialNode:
    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent
        self.next = None

class Polynomial:
    def __init__(self):
        self.head = None

    def add_term(self, coefficient, exponent):
        new_node = PolynomialNode(coefficient, exponent)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def display(self):
        terms = []
        temp = self.head
        while temp:
            terms.append(f"{temp.coefficient}x^{temp.exponent}")
            temp = temp.next
        return " + ".join(terms)

    def add_polynomial(self, other):
        p1 = self.head
        p2 = other.head
        result = Polynomial()
        while p1 and p2:
            if p1.exponent == p2.exponent:
                result.add_term(p1.coefficient + p2.coefficient, p1.exponent)
                p1 = p1.next
                p2 = p2.next
            elif p1.exponent > p2.exponent:
                result.add_term(p1.coefficient, p1.exponent)
                p1 = p1.next
            else:
                result.add_term(p2.coefficient, p2.exponent)
                p2 = p2.next
        while p1:
            result.add_term(p1.coefficient, p1.exponent)
            p1 = p1.next
        while p2:
            result.add_term(p2.coefficient, p2.exponent)
            p2 = p2.next
        return result

# Example Usage
poly1 = Polynomial()
poly1.add_term(3, 2)
poly1.add_term(5, 1)
poly1.add_term(6, 0)

poly2 = Polynomial()
poly2.add_term(2, 1)
poly2.add_term(4, 0)

sum_poly = poly1.add_polynomial(poly2)
print(sum_poly.display())  # Output: 3x^2 + 7x^1 + 10x^0
```

### 8. Sparse Matrix Representation

A sparse matrix, which contains mostly zeros, can be efficiently represented using a linked list to store only the non-zero elements.

```python
class SparseMatrixNode:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None

class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.head = None

    def add_element(self, row, col, value):
        if value == 0:
            return
        new_node = SparseMatrixNode(row, col, value)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def display(self):
        elements = []
        temp = self.head
        while temp:
            elements.append(f"({temp.row}, {temp.col}) = {temp.value}")
            temp = temp.next
        return "\n".join(elements)

# Example Usage
sparse_matrix = SparseMatrix(4, 4)
sparse_matrix.add_element(0, 1, 3)
sparse_matrix.add_element(1, 3, 4)
sparse_matrix.add_element(3, 2, 5)

print(sparse_matrix.display())
# Output:
# (0, 1) = 3
# (1, 3) = 4
# (3, 2) = 5
```

### 9. File System Navigation

A file system's hierarchical structure can be represented using a linked list to navigate through directories and files.

```python
class File:
    def __init__(self, name):
        self.name = name
        self.next = None

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = None
        self.subdirectories = None
        self.next = None

class FileSystem:
    def __init__(self):
        self.root = Directory("/")

    def add_file(self, dir_path, file_name):
        dir_node = self._find_directory(dir_path)
        if dir_node:
            new_file = File(file_name)
            if not dir_node.files:
                dir_node.files = new_file
            else:
                temp = dir_node.files
                while temp.next:
                    temp = temp.next
                temp.next = new_file

    def add_directory(self, dir_path, dir_name):
        dir_node = self._find_directory(dir_path)
        if dir_node:
            new_dir = Directory(dir_name)
            if not dir_node.subdirectories:
                dir_node.subdirectories = new_dir
            else:
                temp = dir_node.subdirectories
                while temp.next:
                    temp = temp.next
                temp.next = new_dir

    def _find_directory(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        current = self.root
        for part in parts:
            temp = current.subdirectories
            while temp and temp.name != part:
                temp = temp.next
            if temp:
                current = temp
            else:
                return None
        return current

    def list_directory(self, dir_path):
        dir_node = self._find_directory(dir_path)
        if dir_node:
            files = []
            temp = dir_node.files
            while temp:
                files.append(temp.name)
                temp = temp.next
            subdirectories = []
            temp = dir_node.subdirectories
            while temp:
                subdirectories.append(temp.name)
                temp = temp.next
            return {"files": files, "directories": subdirectories}
        return None

# Example

 Usage
fs = FileSystem()
fs.add_directory("/", "home")
fs.add_directory("/home", "user")
fs.add_file("/home/user", "file1.txt")
fs.add_file("/home/user", "file2.txt")

print(fs.list_directory("/home/user"))
# Output: {'files': ['file1.txt', 'file2.txt'], 'directories': []}
```

### 10. Implementing a Phonebook

A phonebook can be implemented using a linked list to store and manage contacts, allowing for efficient insertion and deletion.

```python
class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.next = None

class Phonebook:
    def __init__(self):
        self.head = None

    def add_contact(self, name, phone):
        new_contact = Contact(name, phone)
        if not self.head:
            self.head = new_contact
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_contact

    def delete_contact(self, name):
        temp = self.head
        prev = None
        while temp:
            if temp.name == name:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                return f"Contact {name} deleted."
            prev = temp
            temp = temp.next
        return f"Contact {name} not found."

    def find_contact(self, name):
        temp = self.head
        while temp:
            if temp.name == name:
                return f"Name: {temp.name}, Phone: {temp.phone}"
            temp = temp.next
        return f"Contact {name} not found."

    def list_contacts(self):
        contacts = []
        temp = self.head
        while temp:
            contacts.append(f"Name: {temp.name}, Phone: {temp.phone}")
            temp = temp.next
        return "\n".join(contacts)

# Example Usage
phonebook = Phonebook()
phonebook.add_contact("Alice", "123456789")
phonebook.add_contact("Bob", "987654321")

print(phonebook.find_contact("Alice"))  # Output: Name: Alice, Phone: 123456789
print(phonebook.delete_contact("Bob"))  # Output: Contact Bob deleted.
print(phonebook.list_contacts())  # Output: Name: Alice, Phone: 123456789
```

These additional examples demonstrate the versatility of linked lists in various practical applications.



Sure! Here's an analysis of the time and space complexities for the operations performed on linked lists in the real-world examples provided.

### 1. Undo Feature
#### Time Complexity
- **Save state**: O(1)
- **Undo**: O(1)
- **Redo**: O(1)

#### Space Complexity
- O(n) for storing the document states, where n is the number of states saved.

### 2. Browser History Management
#### Time Complexity
- **Visit page**: O(1)
- **Back**: O(1)
- **Forward**: O(1)

#### Space Complexity
- O(n) for storing the pages, where n is the number of pages visited.

### 3. LRU Cache Implementation
#### Time Complexity
- **Get**: O(1)
- **Put**: O(1)

#### Space Complexity
- O(capacity) for storing the cache items, where capacity is the maximum number of items in the cache.

### 4. Music Playlist Management
#### Time Complexity
- **Add song**: O(n) (since it involves finding the last node in a circular list)
- **Play next**: O(1)

#### Space Complexity
- O(n) for storing the songs, where n is the number of songs in the playlist.

### 5. Task Scheduling
#### Time Complexity
- **Add task**: O(n) (since it involves finding the last node in a circular list)
- **Execute next**: O(1)

#### Space Complexity
- O(n) for storing the tasks, where n is the number of tasks.

### 6. Railway Reservation System
#### Time Complexity
- **Add seat**: O(n) (for finding the last node)
- **Reserve seat**: O(n) (for finding the seat by seat number)
- **Get seat status**: O(n) (for finding the seat by seat number)

#### Space Complexity
- O(n) for storing the seats, where n is the number of seats.

### 7. Polynomial Arithmetic
#### Time Complexity
- **Add term**: O(n) (for finding the last node)
- **Display**: O(n) (for traversing the list)
- **Add polynomial**: O(m + n) (where m and n are the number of terms in the two polynomials)

#### Space Complexity
- O(m + n) for storing the terms of the polynomials.

### 8. Sparse Matrix Representation
#### Time Complexity
- **Add element**: O(n) (for finding the last node)
- **Display**: O(n) (for traversing the list)

#### Space Complexity
- O(k) for storing the non-zero elements, where k is the number of non-zero elements.

### 9. File System Navigation
#### Time Complexity
- **Add file**: O(n) (for finding the last node in the files list)
- **Add directory**: O(m) (for finding the last node in the subdirectories list)
- **List directory**: O(n + m) (for traversing the files and subdirectories)

#### Space Complexity
- O(n + m) for storing the files and subdirectories, where n is the number of files and m is the number of subdirectories.

### 10. Implementing a Phonebook
#### Time Complexity
- **Add contact**: O(n) (for finding the last node)
- **Delete contact**: O(n) (for finding the node to delete)
- **Find contact**: O(n) (for finding the node)
- **List contacts**: O(n) (for traversing the list)

#### Space Complexity
- O(n) for storing the contacts, where n is the number of contacts.

### Summary

#### Time Complexity
- **Insertion at end**: Generally O(n) (due to the need to traverse to the end of the list)
- **Insertion at beginning**: O(1)
- **Deletion**: O(n) (to find the node to delete)
- **Traversal**: O(n)
- **Search**: O(n)
- **Access**: O(n) (for a specific element)

#### Space Complexity
- O(n) for storing the elements in the linked list, where n is the number of elements.

These complexities highlight the performance characteristics of linked lists and help understand their efficiency in different scenarios.
