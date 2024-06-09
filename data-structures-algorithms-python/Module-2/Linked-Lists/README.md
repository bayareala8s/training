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
