Sure! Below is a detailed guide on doubly linked lists, including an explanation, common operations, implementation in Python, and their time and space complexities.

### Introduction to Doubly Linked Lists

A doubly linked list is a type of linked list in which each node contains three fields:
1. **Data**: The value stored in the node.
2. **Next Pointer**: A reference to the next node in the list.
3. **Previous Pointer**: A reference to the previous node in the list.

The additional previous pointer allows traversal of the list in both forward and backward directions.

### Common Operations

1. **Insertion**: Adding a new node to the list.
2. **Deletion**: Removing an existing node from the list.
3. **Traversal**: Accessing each node in the list sequentially.
4. **Searching**: Finding a node with a specific value.

### Implementation in Python

#### Node Class
```python
class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list
        self.prev = None  # Reference to the previous node in the list
```

#### Doubly Linked List Class
```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    def insert_at_beginning(self, data):
        new_node = Node(data)  # Create a new node with the given data
        new_node.next = self.head  # Point the new node to the current head
        if self.head is not None:
            self.head.prev = new_node  # Update the previous head's previous pointer
        self.head = new_node  # Update the head to be the new node

    def insert_at_end(self, data):
        new_node = Node(data)  # Create a new node with the given data
        if self.head is None:  # If the list is empty
            self.head = new_node  # Set the head to the new node
            return
        last = self.head
        while last.next:  # Traverse to the last node
            last = last.next
        last.next = new_node  # Point the last node's next to the new node
        new_node.prev = last  # Point the new node's previous to the last node

    def delete_node(self, key):
        temp = self.head
        while temp and temp.data != key:  # Traverse to find the node to delete
            temp = temp.next
        if temp is None:  # If the node was not found
            return
        if temp.prev:  # If the node is not the head
            temp.prev.next = temp.next
        if temp.next:  # If the node is not the last
            temp.next.prev = temp.prev
        if temp == self.head:  # If the node is the head
            self.head = temp.next
        temp = None  # Free the node

    def search(self, key):
        current = self.head
        while current:  # Traverse the list
            if current.data == key:  # If the node is found
                return True
            current = current.next
        return False  # If the node was not found

    def traverse_forward(self):
        elements = []
        current = self.head
        while current:  # Traverse the list forward
            elements.append(current.data)  # Add the node data to the list
            current = current.next
        return elements  # Return the list of elements

    def traverse_backward(self):
        elements = []
        current = self.head
        while current and current.next:  # Traverse to the last node
            current = current.next
        while current:  # Traverse the list backward
            elements.append(current.data)  # Add the node data to the list
            current = current.prev
        return elements  # Return the list of elements

    def __str__(self):
        elements = self.traverse_forward()
        return " <-> ".join(map(str, elements))  # Format the list elements as a string
```

### Example Usage
```python
if __name__ == "__main__":
    # Create a new doubly linked list
    dll = DoublyLinkedList()

    # Insert elements at the beginning
    dll.insert_at_beginning(3)
    dll.insert_at_beginning(2)
    dll.insert_at_beginning(1)
    print("After inserting at the beginning:", dll)

    # Insert elements at the end
    dll.insert_at_end(4)
    dll.insert_at_end(5)
    print("After inserting at the end:", dll)

    # Search for elements
    print("Search for element 3:", dll.search(3))  # Output: True
    print("Search for element 6:", dll.search(6))  # Output: False

    # Delete elements
    dll.delete_node(3)
    print("After deleting element 3:", dll)

    dll.delete_node(1)
    print("After deleting element 1:", dll)

    # Traverse and print the list forward and backward
    print("Final list traversal forward:", dll.traverse_forward())
    print("Final list traversal backward:", dll.traverse_backward())
```

### Output
```
After inserting at the beginning: 1 <-> 2 <-> 3
After inserting at the end: 1 <-> 2 <-> 3 <-> 4 <-> 5
Search for element 3: True
Search for element 6: False
After deleting element 3: 1 <-> 2 <-> 4 <-> 5
After deleting element 1: 2 <-> 4 <-> 5
Final list traversal forward: [2, 4, 5]
Final list traversal backward: [5, 4, 2]
```

### Time Complexities
- **Insertion at Beginning**: O(1)
- **Insertion at End**: O(n)
- **Deletion**: O(n)
- **Search**: O(n)
- **Traversal Forward**: O(n)
- **Traversal Backward**: O(n)

### Space Complexities
- **Space Complexity for Operations**: O(1) (excluding the space for the linked list itself)
- **Space Complexity for Linked List Storage**: O(n)

### Detailed Steps with Visual Text Diagram

1. **Initial State**
   ```
   head -> None
   ```

2. **Insert 3 at the Beginning**
   - Create a new node with data 3.
   - Point the new node's next to the current head (which is None).
   - Update the head to the new node.
   ```
   head -> 3 <-> None
   ```

3. **Insert 2 at the Beginning**
   - Create a new node with data 2.
   - Point the new node's next to the current head (which is 3).
   - Update the previous head's (3) previous pointer to the new node.
   - Update the head to the new node.
   ```
   head -> 2 <-> 3 <-> None
   ```

4. **Insert 1 at the Beginning**
   - Create a new node with data 1.
   - Point the new node's next to the current head (which is 2).
   - Update the previous head's (2) previous pointer to the new node.
   - Update the head to the new node.
   ```
   head -> 1 <-> 2 <-> 3 <-> None
   ```

5. **Insert 4 at the End**
   - Create a new node with data 4.
   - Traverse to the last node (which is 3).
   - Point the last node's next to the new node.
   - Update the new node's previous pointer to the last node (3).
   ```
   head -> 1 <-> 2 <-> 3 <-> 4 <-> None
   ```

6. **Insert 5 at the End**
   - Create a new node with data 5.
   - Traverse to the last node (which is 4).
   - Point the last node's next to the new node.
   - Update the new node's previous pointer to the last node (4).
   ```
   head -> 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> None
   ```

7. **Search for Element 3**
   - Traverse the list and find the node with data 3.
   ```
   head -> 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> None
   ```

8. **Search for Element 6**
   - Traverse the list and do not find a node with data 6.
   ```
   head -> 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> None
   ```

9. **Delete Element 3**
   - Traverse the list to find the node with data 3.
   - Update the previous node's (2) next to point to the node after 3 (which is 4).
   - Update the next node's (4) previous to point to the node before 3 (which is 2).
   ```
   head -> 1 <-> 2 <-> 4 <-> 5 <-> None
   ```

10. **Delete Element 1**
    - Head is the node to be deleted (1).
    - Update the head to the next node (which is 2).
    - Update the new head's (2) previous pointer

 to None.
    ```
    head -> 2 <-> 4 <-> 5 <-> None
    ```

11. **Final List Traversal Forward**
    - Traverse the list and collect the node data.
    ```
    head -> 2 <-> 4 <-> 5 <-> None
    ```

12. **Final List Traversal Backward**
    - Traverse to the last node and then traverse backward, collecting the node data.
    ```
    head -> 2 <-> 4 <-> 5 <-> None
    ```

This detailed guide covers the basics of doubly linked lists, including their implementation, common operations, and complexities. If you have any questions or need further details, feel free to ask!


### Time and Space Analysis for Doubly Linked List

#### Time Complexities

1. **Insertion at Beginning**: `insert_at_beginning(data)`
   - **Time Complexity**: O(1)
     - Explanation: Inserting a node at the beginning involves creating a new node and adjusting a few pointers. This is a constant-time operation as it doesn't depend on the size of the list.

2. **Insertion at End**: `insert_at_end(data)`
   - **Time Complexity**: O(n)
     - Explanation: Inserting a node at the end requires traversing the entire list to find the last node, which takes linear time relative to the number of nodes in the list (n). Once the last node is found, the insertion operation itself is O(1).

3. **Deletion of a Node**: `delete_node(key)`
   - **Time Complexity**: O(n)
     - Explanation: Deleting a node involves traversing the list to find the node with the given key. In the worst case, the node to be deleted might be the last node or not present at all, requiring traversal of the entire list. Once the node is found, the deletion operation itself is O(1).

4. **Search for a Node**: `search(key)`
   - **Time Complexity**: O(n)
     - Explanation: Searching for a node involves traversing the list and comparing each node's data with the key. In the worst case, the node might be the last node or not present at all, requiring traversal of the entire list.

5. **Traversal of the List (Forward)**: `traverse_forward()`
   - **Time Complexity**: O(n)
     - Explanation: Traversing the list to collect all elements requires visiting each node once, which takes linear time relative to the number of nodes in the list.

6. **Traversal of the List (Backward)**: `traverse_backward()`
   - **Time Complexity**: O(n)
     - Explanation: Traversing the list backward also requires visiting each node once, which takes linear time relative to the number of nodes in the list.

7. **String Representation**: `__str__()`
   - **Time Complexity**: O(n)
     - Explanation: This method internally calls `traverse_forward()`, which takes O(n) time to gather all the elements of the list, and then performs additional operations to convert the list to a string, which is linear in time complexity.

#### Space Complexities

1. **Space Complexity for Insertion, Deletion, Search, and Traversal**
   - **Space Complexity**: O(1) (excluding the space for the linked list itself)
     - Explanation: These operations do not require extra space that grows with the input size. The space used by temporary variables or pointers is constant.

2. **Space Complexity for the Linked List Itself**
   - **Space Complexity**: O(n)
     - Explanation: The space required for the linked list is directly proportional to the number of nodes (n). Each node requires space for storing the data, a pointer to the next node, and a pointer to the previous node.

### Summary

#### Time Complexity
- **Insert at Beginning**: O(1)
- **Insert at End**: O(n)
- **Delete Node**: O(n)
- **Search Node**: O(n)
- **Traversal Forward**: O(n)
- **Traversal Backward**: O(n)
- **String Representation**: O(n)

#### Space Complexity
- **Operations**: O(1)
- **Linked List Storage**: O(n)

This analysis helps to understand the efficiency of doubly linked list operations and provides a clear picture of their performance characteristics. If you have any more questions or need further details, feel free to ask!



Sure! Here are detailed real-world use-case examples for doubly linked lists:

### 1. Implementing a Browser's Forward and Backward Navigation

A browser's history can be managed using a doubly linked list to allow users to move back and forth between previously visited pages.

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

    def __str__(self):
        history = []
        temp = self.current
        while temp.prev:  # Move to the first page
            temp = temp.prev
        while temp:  # Traverse forward to collect URLs
            history.append(temp.url)
            temp = temp.next
        return " -> ".join(history)

# Example Usage
browser = BrowserHistory()
browser.visit_page("google.com")
browser.visit_page("github.com")
browser.visit_page("stackoverflow.com")

print("Current History:", browser)
print("Back:", browser.back())  # Output: github.com
print("Back:", browser.back())  # Output: google.com
print("Forward:", browser.forward())  # Output: github.com
print("Current History:", browser)
```

### 2. Music Playlist Management

A music player can use a doubly linked list to manage a playlist, allowing users to move to the previous or next song easily.

```python
class Song:
    def __init__(self, title):
        self.title = title
        self.next = None
        self.prev = None

class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_song(self, title):
        new_song = Song(title)
        if not self.head:
            self.head = new_song
            self.tail = new_song
            self.current = new_song
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song

    def play_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.current.title if self.current else None

    def play_previous(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.current.title if self.current else None

    def __str__(self):
        songs = []
        temp = self.head
        while temp:
            songs.append(temp.title)
            temp = temp.next
        return " <-> ".join(songs)

# Example Usage
playlist = MusicPlaylist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
playlist.add_song("Song 3")

print("Current Playlist:", playlist)
print("Play Next:", playlist.play_next())  # Output: Song 2
print("Play Next:", playlist.play_next())  # Output: Song 3
print("Play Previous:", playlist.play_previous())  # Output: Song 2
print("Current Playlist:", playlist)
```

### 3. Implementing an Undo and Redo Functionality

Applications like text editors can use doubly linked lists to manage the history of states for implementing undo and redo operations.

```python
class DocumentState:
    def __init__(self, content):
        self.content = content

class UndoRedoManager:
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

    def __str__(self):
        states = []
        temp = self.current
        while temp.prev:  # Move to the first state
            temp = temp.prev
        while temp:  # Traverse forward to collect states
            states.append(temp.content)
            temp = temp.next
        return " -> ".join(states)

# Example Usage
editor = UndoRedoManager()
editor.save_state("Version 1")
editor.save_state("Version 2")
editor.save_state("Version 3")

print("Current States:", editor)
print("Undo:", editor.undo())  # Output: Version 2
print("Undo:", editor.undo())  # Output: Version 1
print("Redo:", editor.redo())  # Output: Version 2
print("Current States:", editor)
```

### 4. Text Buffer for Text Editors

A text editor can use a doubly linked list to manage the text buffer, allowing efficient insertions, deletions, and cursor movements.

```python
class TextNode:
    def __init__(self, char):
        self.char = char
        self.next = None
        self.prev = None

class TextBuffer:
    def __init__(self):
        self.head = None
        self.tail = None
        self.cursor = None

    def insert(self, char):
        new_node = TextNode(char)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.cursor = new_node
        else:
            if self.cursor == self.tail:
                self.cursor.next = new_node
                new_node.prev = self.cursor
                self.tail = new_node
            else:
                new_node.next = self.cursor.next
                new_node.prev = self.cursor
                if self.cursor.next:
                    self.cursor.next.prev = new_node
                self.cursor.next = new_node
            self.cursor = new_node

    def delete(self):
        if self.cursor:
            if self.cursor == self.head:
                self.head = self.cursor.next
                if self.head:
                    self.head.prev = None
            else:
                self.cursor.prev.next = self.cursor.next
                if self.cursor.next:
                    self.cursor.next.prev = self.cursor.prev
            self.cursor = self.cursor.prev if self.cursor.prev else self.head

    def move_cursor_left(self):
        if self.cursor and self.cursor.prev:
            self.cursor = self.cursor.prev

    def move_cursor_right(self):
        if self.cursor and self.cursor.next:
            self.cursor = self.cursor.next

    def __str__(self):
        text = []
        temp = self.head
        while temp:
            text.append(temp.char)
            temp = temp.next
        return "".join(text)

# Example Usage
buffer = TextBuffer()
buffer.insert('H')
buffer.insert('e')
buffer.insert('l')
buffer.insert('l')
buffer.insert('o')
print("Text Buffer:", buffer)

buffer.move_cursor_left()
buffer.move_cursor_left()
buffer.insert('p')
print("Text Buffer after insertion:", buffer)

buffer.delete()
print("Text Buffer after deletion:", buffer)
```

### 5. Task Scheduling

A doubly linked list can be used to manage and cycle through tasks in a task scheduler.

```python
class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.next = None
        self.prev = None

class TaskScheduler:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_task(self, name, duration):
        new_task = Task(name, duration)
        if not self.head:
            self.head = new_task
            self.tail = new_task
            self.current = new_task
        else:
            self.tail.next = new_task
            new_task.prev = self.tail
            self.tail = new_task

    def next_task(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            self.current = self.head  # Loop back to the start
        return self.current.name if self.current else None

    def prev_task(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail  # Loop back to the end
        return self.current.name if self.current else None

    def __str__(self):
        tasks = []
        temp = self.head
        while temp:
            tasks.append(f"{temp.name} ({temp.duration} mins)")
            temp = temp.next
        return " <-> ".join(tasks)

# Example Usage
scheduler = TaskScheduler()
scheduler.add_task("Task 1", 30)
scheduler.add_task("Task 2", 45)
scheduler.add_task("Task 3", 20)

print("Task Scheduler:", scheduler)
print("Next Task:", scheduler.next_task())  # Output: Task 2
print("Next Task:", scheduler.next_task())  # Output: Task 3
print("Next Task:", scheduler.next_task())  # Output: Task 1 (loops back)
print("Previous Task:", scheduler.prev_task())  # Output: Task 3
print("Previous Task:", scheduler.prev_task())  # Output: Task 2
print("Task Scheduler:", scheduler)
```

### Summary of Real-World Use-Cases

- **Browser History Navigation**: Allows moving

 back and forth between pages.
- **Music Playlist Management**: Enables playing previous and next songs.
- **Undo and Redo Functionality**: Manages the history of states for applications.
- **Text Buffer for Text Editors**: Efficiently handles text insertions, deletions, and cursor movements.
- **Task Scheduling**: Cycles through tasks for execution in a round-robin fashion.

These examples illustrate the versatility and practical applications of doubly linked lists in real-world scenarios. If you have any specific questions or need further details, feel free to ask!


Sure! Here are additional real-world examples where doubly linked lists are effectively utilized:

### 6. Memory Management in Operating Systems

Operating systems often use doubly linked lists to manage memory blocks for efficient allocation and deallocation.

```python
class MemoryBlock:
    def __init__(self, start, size):
        self.start = start  # Start address of the memory block
        self.size = size  # Size of the memory block
        self.next = None
        self.prev = None

class MemoryManager:
    def __init__(self):
        self.head = None  # Head of the free memory blocks list

    def allocate(self, size):
        current = self.head
        while current:
            if current.size >= size:
                allocated_block = MemoryBlock(current.start, size)
                current.start += size
                current.size -= size
                if current.size == 0:
                    self._remove_block(current)
                return allocated_block
            current = current.next
        return None  # Not enough memory

    def deallocate(self, block):
        if not self.head:
            self.head = block
        else:
            current = self.head
            while current and current.start < block.start:
                current = current.next
            block.next = current
            block.prev = current.prev if current else None
            if current:
                current.prev = block
            if block.prev:
                block.prev.next = block
            else:
                self.head = block

    def _remove_block(self, block):
        if block.prev:
            block.prev.next = block.next
        if block.next:
            block.next.prev = block.prev
        if block == self.head:
            self.head = block.next

    def __str__(self):
        blocks = []
        current = self.head
        while current:
            blocks.append(f"[{current.start}, {current.start + current.size - 1}]")
            current = current.next
        return " -> ".join(blocks)

# Example Usage
manager = MemoryManager()
manager.deallocate(MemoryBlock(0, 100))
manager.deallocate(MemoryBlock(200, 100))

print("Initial free blocks:", manager)

block = manager.allocate(50)
print("After allocating 50:", manager)

manager.deallocate(block)
print("After deallocating 50:", manager)
```

### 7. Train Composition Management

A train can be represented using a doubly linked list where each node represents a train car, allowing for easy addition, removal, and traversal of cars.

```python
class TrainCar:
    def __init__(self, car_id):
        self.car_id = car_id
        self.next = None
        self.prev = None

class Train:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_car_to_front(self, car_id):
        new_car = TrainCar(car_id)
        if not self.head:
            self.head = new_car
            self.tail = new_car
        else:
            new_car.next = self.head
            self.head.prev = new_car
            self.head = new_car

    def add_car_to_end(self, car_id):
        new_car = TrainCar(car_id)
        if not self.tail:
            self.head = new_car
            self.tail = new_car
        else:
            new_car.prev = self.tail
            self.tail.next = new_car
            self.tail = new_car

    def remove_car(self, car_id):
        current = self.head
        while current and current.car_id != car_id:
            current = current.next
        if current:
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next
            if current == self.tail:
                self.tail = current.prev

    def __str__(self):
        cars = []
        current = self.head
        while current:
            cars.append(f"Car {current.car_id}")
            current = current.next
        return " <-> ".join(cars)

# Example Usage
train = Train()
train.add_car_to_front(1)
train.add_car_to_front(2)
train.add_car_to_end(3)

print("Train composition:", train)

train.remove_car(2)
print("After removing car 2:", train)
```

### 8. Inventory Management in Warehouses

Warehouses can use doubly linked lists to manage items in storage, enabling efficient addition, removal, and traversal of inventory items.

```python
class InventoryItem:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name
        self.next = None
        self.prev = None

class Inventory:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_item(self, item_id, name):
        new_item = InventoryItem(item_id, name)
        if not self.head:
            self.head = new_item
            self.tail = new_item
        else:
            self.tail.next = new_item
            new_item.prev = self.tail
            self.tail = new_item

    def remove_item(self, item_id):
        current = self.head
        while current and current.item_id != item_id:
            current = current.next
        if current:
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next
            if current == self.tail:
                self.tail = current.prev

    def find_item(self, item_id):
        current = self.head
        while current:
            if current.item_id == item_id:
                return f"Item found: {current.name}"
            current = current.next
        return "Item not found"

    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(f"{current.item_id}: {current.name}")
            current = current.next
        return " -> ".join(items)

# Example Usage
inventory = Inventory()
inventory.add_item(101, "Item A")
inventory.add_item(102, "Item B")
inventory.add_item(103, "Item C")

print("Current Inventory:", inventory)

print(inventory.find_item(102))  # Output: Item found: Item B
inventory.remove_item(102)
print("After removing item 102:", inventory)
print(inventory.find_item(102))  # Output: Item not found
```

### 9. Implementing a Deque (Double-Ended Queue)

A deque allows insertions and deletions from both ends. A doubly linked list can efficiently support these operations.

```python
class DequeNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_front(self, value):
        new_node = DequeNode(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def add_to_rear(self, value):
        new_node = DequeNode(value)
        if not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def remove_from_front(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return value

    def remove_from_rear(self):
        if not self.tail:
            return None
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        return value

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.value))
            current = current.next
        return " <-> ".join(elements)

# Example Usage
deque = Deque()
deque.add_to_front(1)
deque.add_to_rear(2)
deque.add_to_front(0)
deque.add_to_rear(3)

print("Deque:", deque)

print("Remove from front:", deque.remove_from_front())  # Output: 0
print("Remove from rear:", deque.remove_from_rear())  # Output: 3
print("Deque after removals:", deque)
```

### 10. Task Priority Management

A doubly linked list can manage tasks with different priorities, allowing efficient addition, removal, and traversal based on priority.

```python
class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        self.next = None
        self.prev = None

class TaskManager:
    def __init__(self):
        self.head = None

    def add_task(self, priority, description):
        new_task = Task(priority, description)
        if not self.head:
            self.head = new_task
            return
        current = self.head
        while current and current.priority <= priority:
            current = current.next
        if not current:
            self.head.prev = new_task
            new_task.next = self.head
            self.head = new_task
        else:
            new_task.next = current
            new_task.prev = current.prev
            if current.prev:
                current.prev.next = new_task


            current.prev = new_task
            if current == self.head:
                self.head = new_task

    def remove_task(self, description):
        current = self.head
        while current and current.description != description:
            current = current.next
        if current:
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next

    def __str__(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(f"Priority {current.priority}: {current.description}")
            current = current.next
        return " -> ".join(tasks)

# Example Usage
task_manager = TaskManager()
task_manager.add_task(1, "Low priority task")
task_manager.add_task(3, "High priority task")
task_manager.add_task(2, "Medium priority task")

print("Task Manager:", task_manager)

task_manager.remove_task("Medium priority task")
print("After removing medium priority task:", task_manager)
```

### Summary of Additional Real-World Use-Cases

- **Memory Management**: Operating systems use doubly linked lists to manage memory blocks for allocation and deallocation.
- **Train Composition Management**: Efficiently add, remove, and traverse train cars.
- **Inventory Management**: Manage items in a warehouse, allowing for easy addition, removal, and traversal.
- **Deque Implementation**: Support for double-ended queue operations.
- **Task Priority Management**: Manage tasks with different priorities.

These examples demonstrate the versatility and practical applications of doubly linked lists in various real-world scenarios. If you have any specific questions or need further details, feel free to ask!
