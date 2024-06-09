### Circular Linked Lists: Detailed Guide

### Introduction
A circular linked list is a variation of a linked list where the last node points back to the first node, forming a circular structure. This can be implemented in both singly and doubly linked list forms.

### Types of Circular Linked Lists
1. **Singly Circular Linked List**: Each node points to the next node, with the last node pointing back to the first node.
2. **Doubly Circular Linked List**: Each node points to both the next and previous nodes, with the last node's next pointing to the first node and the first node's previous pointing to the last node.

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
        self.prev = None  # Reference to the previous node in the list (for doubly circular linked list)
```

### Singly Circular Linked List

#### Singly Circular Linked List Class
```python
class SinglyCircularLinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node.next = self.head
            current.next = new_node
            self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def delete_node(self, key):
        if self.head is None:
            return

        if self.head.data == key and self.head.next == self.head:
            self.head = None
            return

        last = self.head
        d = None

        if self.head.data == key:
            while last.next != self.head:
                last = last.next
            last.next = self.head.next
            self.head = last.next
        else:
            while last.next != self.head:
                if last.next.data == key:
                    d = last.next
                    break
                last = last.next
            if d:
                last.next = d.next
                d = None

    def traverse(self):
        elements = []
        if self.head is None:
            return elements
        current = self.head
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.head:
                break
        return elements

    def search(self, key):
        if self.head is None:
            return False
        current = self.head
        while True:
            if current.data == key:
                return True
            current = current.next
            if current == self.head:
                break
        return False

    def __str__(self):
        elements = self.traverse()
        return " -> ".join(map(str, elements)) + " -> " + str(self.head.data)  # To show the circular nature

# Example Usage
if __name__ == "__main__":
    scll = SinglyCircularLinkedList()
    scll.insert_at_beginning(3)
    scll.insert_at_beginning(2)
    scll.insert_at_beginning(1)
    print("After inserting at the beginning:", scll)

    scll.insert_at_end(4)
    scll.insert_at_end(5)
    print("After inserting at the end:", scll)

    print("Search for element 3:", scll.search(3))
    print("Search for element 6:", scll.search(6))

    scll.delete_node(3)
    print("After deleting element 3:", scll)

    scll.delete_node(1)
    print("After deleting element 1:", scll)

    print("Final list traversal:", scll.traverse())
```

### Doubly Circular Linked List

#### Doubly Circular Linked List Class
```python
class DoublyCircularLinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            last = self.head.prev
            new_node.next = self.head
            new_node.prev = last
            last.next = new_node
            self.head.prev = new_node
            self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
        else:
            last = self.head.prev
            new_node.next = self.head
            new_node.prev = last
            last.next = new_node
            self.head.prev = new_node

    def delete_node(self, key):
        if self.head is None:
            return

        current = self.head
        previous = None

        while True:
            if current.data == key:
                if previous:
                    previous.next = current.next
                    current.next.prev = previous
                else:
                    last = self.head.prev
                    last.next = self.head.next
                    self.head.next.prev = last
                    self.head = self.head.next
                return
            previous = current
            current = current.next
            if current == self.head:
                break

    def traverse_forward(self):
        elements = []
        if self.head is None:
            return elements
        current = self.head
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.head:
                break
        return elements

    def traverse_backward(self):
        elements = []
        if self.head is None:
            return elements
        current = self.head.prev
        while True:
            elements.append(current.data)
            current = current.prev
            if current == self.head.prev:
                break
        return elements

    def search(self, key):
        if self.head is None:
            return False
        current = self.head
        while True:
            if current.data == key:
                return True
            current = current.next
            if current == self.head:
                break
        return False

    def __str__(self):
        elements = self.traverse_forward()
        return " <-> ".join(map(str, elements)) + " <-> " + str(self.head.data)  # To show the circular nature

# Example Usage
if __name__ == "__main__":
    dcll = DoublyCircularLinkedList()
    dcll.insert_at_beginning(3)
    dcll.insert_at_beginning(2)
    dcll.insert_at_beginning(1)
    print("After inserting at the beginning:", dcll)

    dcll.insert_at_end(4)
    dcll.insert_at_end(5)
    print("After inserting at the end:", dcll)

    print("Search for element 3:", dcll.search(3))
    print("Search for element 6:", dcll.search(6))

    dcll.delete_node(3)
    print("After deleting element 3:", dcll)

    dcll.delete_node(1)
    print("After deleting element 1:", dcll)

    print("Final list traversal forward:", dcll.traverse_forward())
    print("Final list traversal backward:", dcll.traverse_backward())
```

### Time and Space Complexities

#### Time Complexities

1. **Insertion at Beginning**:
   - **Time Complexity**: O(1)
   - Explanation: Inserting a node at the beginning involves creating a new node and adjusting a few pointers. This is a constant-time operation as it doesn't depend on the size of the list.

2. **Insertion at End**:
   - **Time Complexity**: O(n) for singly circular linked list, O(1) for doubly circular linked list
   - Explanation: Inserting a node at the end of a singly circular linked list requires traversing the entire list to find the last node, which takes linear time relative to the number of nodes in the list (n). For a doubly circular linked list, the last node can be accessed in constant time.

3. **Deletion of a Node**:
   - **Time Complexity**: O(n)
   - Explanation: Deleting a node involves traversing the list to find the node with the given key. In the worst case, the node to be deleted might be the last node or not present at all, requiring traversal of the entire list.

4. **Search for a Node**:
   - **Time Complexity**: O(n)
   - Explanation: Searching for a node involves traversing the list and comparing each node's data with the key. In the worst case, the node might be the last node or not present at all, requiring traversal of the entire list.

5. **Traversal of the List**:
   - **Time Complexity

**: O(n)
   - Explanation: Traversing the list to collect all elements requires visiting each node once, which takes linear time relative to the number of nodes in the list.

#### Space Complexities

1. **Space Complexity for Operations**: O(1) (excluding the space for the linked list itself)
   - Explanation: These operations do not require extra space that grows with the input size. The space used by temporary variables or pointers is constant.

2. **Space Complexity for the Linked List Itself**: O(n)
   - Explanation: The space required for the linked list is directly proportional to the number of nodes (n). Each node requires space for storing the data and pointers to the next and previous nodes (for doubly circular linked lists).

### Real-World Use Cases

1. **Round-Robin Scheduling**:
   - Circular linked lists are used in round-robin scheduling algorithms, where each process is assigned a fixed time slot in a cyclic order.

2. **FIFA Rankings**:
   - Circular linked lists can be used to manage FIFA rankings, where each team points to the next team in the ranking, and the last team points back to the first team.

3. **Circular Buffers**:
   - Circular linked lists are used in implementing circular buffers, which are used in data streaming applications where data is continuously produced and consumed.

4. **Music Playlist Management**:
   - Circular linked lists can be used to manage music playlists, allowing continuous play of songs in a loop.

5. **Implementation of Deques**:
   - Circular linked lists can be used to implement deques (double-ended queues) where elements can be inserted and removed from both ends.

6. **Traffic Light Management**:
   - Circular linked lists can manage traffic lights at an intersection, where each light points to the next one in the sequence, and the last light points back to the first.

7. **Game Development**:
   - In games, circular linked lists can be used to manage the sequence of players' turns, ensuring each player gets a turn in a cyclic order.

These examples and explanations illustrate the versatility and practicality of circular linked lists in various real-world applications. If you have any specific questions or need further details, feel free to ask!



Sure! Here are detailed code examples for real-world use cases of circular linked lists:

### 1. Round-Robin Scheduling

Circular linked lists are used in round-robin scheduling algorithms, where each process is assigned a fixed time slot in a cyclic order.

```python
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.next = None

class RoundRobinScheduler:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_process(self, pid):
        new_process = Process(pid)
        if not self.head:
            self.head = new_process
            self.tail = new_process
            self.tail.next = self.head
        else:
            self.tail.next = new_process
            self.tail = new_process
            self.tail.next = self.head

    def remove_process(self, pid):
        if not self.head:
            return
        
        current = self.head
        prev = None

        while True:
            if current.pid == pid:
                if prev:
                    prev.next = current.next
                else:
                    if self.head == self.tail:
                        self.head = None
                        self.tail = None
                    else:
                        self.tail.next = current.next
                        self.head = current.next
                break

            prev = current
            current = current.next

            if current == self.head:
                break

    def schedule(self):
        if not self.head:
            return None
        
        current = self.head
        while True:
            print(f"Running process {current.pid}")
            current = current.next

            if current == self.head:
                break

    def __str__(self):
        if not self.head:
            return "No processes"
        
        elements = []
        current = self.head
        while True:
            elements.append(str(current.pid))
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
scheduler = RoundRobinScheduler()
scheduler.add_process(1)
scheduler.add_process(2)
scheduler.add_process(3)

print("Processes in scheduler:", scheduler)
scheduler.schedule()

scheduler.remove_process(2)
print("Processes in scheduler after removing process 2:", scheduler)
scheduler.schedule()
```

### 2. FIFA Rankings

Circular linked lists can be used to manage FIFA rankings, where each team points to the next team in the ranking, and the last team points back to the first team.

```python
class Team:
    def __init__(self, name):
        self.name = name
        self.next = None

class FIFARankings:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_team(self, name):
        new_team = Team(name)
        if not self.head:
            self.head = new_team
            self.tail = new_team
            self.tail.next = self.head
        else:
            self.tail.next = new_team
            self.tail = new_team
            self.tail.next = self.head

    def remove_team(self, name):
        if not self.head:
            return
        
        current = self.head
        prev = None

        while True:
            if current.name == name:
                if prev:
                    prev.next = current.next
                else:
                    if self.head == self.tail:
                        self.head = None
                        self.tail = None
                    else:
                        self.tail.next = current.next
                        self.head = current.next
                break

            prev = current
            current = current.next

            if current == self.head:
                break

    def traverse(self):
        if not self.head:
            return "No teams"
        
        elements = []
        current = self.head
        while True:
            elements.append(current.name)
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
rankings = FIFARankings()
rankings.add_team("Team A")
rankings.add_team("Team B")
rankings.add_team("Team C")

print("FIFA Rankings:", rankings.traverse())

rankings.remove_team("Team B")
print("FIFA Rankings after removing Team B:", rankings.traverse())
```

### 3. Circular Buffers

Circular linked lists are used in implementing circular buffers, which are used in data streaming applications where data is continuously produced and consumed.

```python
class BufferNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularBuffer:
    def __init__(self, size):
        self.size = size
        self.head = None
        self.tail = None
        self.current_size = 0

    def enqueue(self, value):
        new_node = BufferNode(value)
        if self.current_size < self.size:
            if not self.head:
                self.head = new_node
                self.tail = new_node
                self.tail.next = self.head
            else:
                self.tail.next = new_node
                self.tail = new_node
                self.tail.next = self.head
            self.current_size += 1
        else:
            self.head = self.head.next
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head

    def dequeue(self):
        if not self.head:
            return None
        if self.head == self.tail:
            value = self.head.value
            self.head = None
            self.tail = None
            self.current_size = 0
            return value
        else:
            value = self.head.value
            self.head = self.head.next
            self.tail.next = self.head
            self.current_size -= 1
            return value

    def __str__(self):
        if not self.head:
            return "Buffer is empty"
        
        elements = []
        current = self.head
        while True:
            elements.append(str(current.value))
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
buffer = CircularBuffer(3)
buffer.enqueue(1)
buffer.enqueue(2)
buffer.enqueue(3)
print("Buffer after enqueueing 3 elements:", buffer)

buffer.enqueue(4)
print("Buffer after enqueueing 4th element:", buffer)

print("Dequeued element:", buffer.dequeue())
print("Buffer after dequeueing an element:", buffer)
```

### 4. Music Playlist Management

Circular linked lists can be used to manage music playlists, allowing continuous play of songs in a loop.

```python
class Song:
    def __init__(self, title):
        self.title = title
        self.next = None

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
            self.tail.next = self.head
        else:
            self.tail.next = new_song
            self.tail = new_song
            self.tail.next = self.head

    def play_next(self):
        if not self.current:
            self.current = self.head
        else:
            self.current = self.current.next
        return self.current.title if self.current else None

    def __str__(self):
        if not self.head:
            return "No songs in the playlist"
        
        elements = []
        current = self.head
        while True:
            elements.append(current.title)
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
playlist = MusicPlaylist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
playlist.add_song("Song 3")

print("Music Playlist:", playlist)

print("Play Next:", playlist.play_next())
print("Play Next:", playlist.play_next())
print("Play Next:", playlist.play_next())
print("Play Next:", playlist.play_next())  # Loops back to the beginning
```

### 5. Implementation of Deques (Double-Ended Queues)

Circular linked lists can be used to implement deques, where elements can be inserted and removed from both ends.

```python
class DequeNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularDeque:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_front(self, value):
        new_node = DequeNode(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.head = new_node

    def add_to_rear(self, value):
        new_node = DequeNode(value)
        if not self.tail:
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head

    def remove_from_front(self):
        if not self.head:
            return None
        value = self.head.value
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head
        return value

    def remove_from_rear(self):
        if not self.tail:
            return None
        value = self.tail.value
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next


            current.next = self.head
            self.tail = current
        return value

    def __str__(self):
        if not self.head:
            return "Deque is empty"
        
        elements = []
        current = self.head
        while True:
            elements.append(str(current.value))
            current = current.next
            if current == self.head:
                break
        return " <-> ".join(elements)

# Example Usage
deque = CircularDeque()
deque.add_to_front(1)
deque.add_to_rear(2)
deque.add_to_front(0)
deque.add_to_rear(3)

print("Deque:", deque)

print("Remove from front:", deque.remove_from_front())
print("Remove from rear:", deque.remove_from_rear())
print("Deque after removals:", deque)
```

### 6. Traffic Light Management

Circular linked lists can manage traffic lights at an intersection, where each light points to the next one in the sequence, and the last light points back to the first.

```python
class TrafficLight:
    def __init__(self, color):
        self.color = color
        self.next = None

class TrafficLightManager:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_light(self, color):
        new_light = TrafficLight(color)
        if not self.head:
            self.head = new_light
            self.tail = new_light
            self.tail.next = self.head
        else:
            self.tail.next = new_light
            self.tail = new_light
            self.tail.next = self.head

    def next_light(self):
        if not self.current:
            self.current = self.head
        else:
            self.current = self.current.next
        return self.current.color if self.current else None

    def __str__(self):
        if not self.head:
            return "No traffic lights"
        
        elements = []
        current = self.head
        while True:
            elements.append(current.color)
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
manager = TrafficLightManager()
manager.add_light("Red")
manager.add_light("Green")
manager.add_light("Yellow")

print("Traffic Light Sequence:", manager)

print("Next Light:", manager.next_light())
print("Next Light:", manager.next_light())
print("Next Light:", manager.next_light())
print("Next Light:", manager.next_light())  # Loops back to the beginning
```

### 7. Game Development

In games, circular linked lists can be used to manage the sequence of players' turns, ensuring each player gets a turn in a cyclic order.

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.next = None

class Game:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_player(self, name):
        new_player = Player(name)
        if not self.head:
            self.head = new_player
            self.tail = new_player
            self.tail.next = self.head
        else:
            self.tail.next = new_player
            self.tail = new_player
            self.tail.next = self.head

    def next_turn(self):
        if not self.current:
            self.current = self.head
        else:
            self.current = self.current.next
        return self.current.name if self.current else None

    def __str__(self):
        if not self.head:
            return "No players"
        
        elements = []
        current = self.head
        while True:
            elements.append(current.name)
            current = current.next
            if current == self.head:
                break
        return " -> ".join(elements)

# Example Usage
game = Game()
game.add_player("Player 1")
game.add_player("Player 2")
game.add_player("Player 3")

print("Player Sequence:", game)

print("Next Turn:", game.next_turn())
print("Next Turn:", game.next_turn())
print("Next Turn:", game.next_turn())
print("Next Turn:", game.next_turn())  # Loops back to the beginning
```

These detailed code examples illustrate how circular linked lists can be utilized in various real-world scenarios. If you have any specific questions or need further details, feel free to ask!




### Time and Space Complexities for Circular Linked Lists

Here is the analysis of the time and space complexities for the operations performed on the circular linked list implementations provided in the examples.

#### General Operations

1. **Insertion at Beginning**
   - **Time Complexity**: O(n) for singly circular linked list (due to finding the last node), O(1) for doubly circular linked list
     - Explanation: Inserting at the beginning requires updating the head and ensuring the last node points to the new head. For a doubly circular linked list, the last node is directly accessible.
   
2. **Insertion at End**
   - **Time Complexity**: O(n) for singly circular linked list, O(1) for doubly circular linked list
     - Explanation: Inserting at the end of a singly circular linked list requires traversing the entire list to find the last node. For a doubly circular linked list, the last node is directly accessible.

3. **Deletion of a Node**
   - **Time Complexity**: O(n)
     - Explanation: Deleting a node involves traversing the list to find the node with the given key. In the worst case, the node to be deleted might be the last node or not present at all, requiring traversal of the entire list.

4. **Search for a Node**
   - **Time Complexity**: O(n)
     - Explanation: Searching for a node involves traversing the list and comparing each node's data with the key. In the worst case, the node might be the last node or not present at all, requiring traversal of the entire list.

5. **Traversal of the List**
   - **Time Complexity**: O(n)
     - Explanation: Traversing the list to collect all elements requires visiting each node once, which takes linear time relative to the number of nodes in the list.

#### Space Complexities

1. **Space Complexity for Operations**: O(1) (excluding the space for the linked list itself)
   - Explanation: These operations do not require extra space that grows with the input size. The space used by temporary variables or pointers is constant.

2. **Space Complexity for the Linked List Itself**: O(n)
   - Explanation: The space required for the linked list is directly proportional to the number of nodes (n). Each node requires space for storing the data and pointers to the next and previous nodes (for doubly circular linked lists).

### Specific Examples

1. **Round-Robin Scheduling**

   **Operations:**
   - `add_process(pid)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `remove_process(pid)`
     - **Time Complexity**: O(n)
     - **Space Complexity**: O(1)
   - `schedule()`
     - **Time Complexity**: O(n)
     - **Space Complexity**: O(1)

2. **FIFA Rankings**

   **Operations:**
   - `add_team(name)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `remove_team(name)`
     - **Time Complexity**: O(n)
     - **Space Complexity**: O(1)
   - `traverse()`
     - **Time Complexity**: O(n)
     - **Space Complexity**: O(1)

3. **Circular Buffers**

   **Operations:**
   - `enqueue(value)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `dequeue()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)

4. **Music Playlist Management**

   **Operations:**
   - `add_song(title)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `play_next()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)

5. **Implementation of Deques**

   **Operations:**
   - `add_to_front(value)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `add_to_rear(value)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `remove_from_front()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `remove_from_rear()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)

6. **Traffic Light Management**

   **Operations:**
   - `add_light(color)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `next_light()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)

7. **Game Development**

   **Operations:**
   - `add_player(name)`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)
   - `next_turn()`
     - **Time Complexity**: O(1)
     - **Space Complexity**: O(1)

### Summary

#### Time Complexity
- **Insertion at Beginning**: O(1) for doubly circular linked list, O(n) for singly circular linked list
- **Insertion at End**: O(1) for doubly circular linked list, O(n) for singly circular linked list
- **Delete Node**: O(n)
- **Search Node**: O(n)
- **Traversal**: O(n)

#### Space Complexity
- **Operations**: O(1)
- **Linked List Storage**: O(n)

This analysis provides a comprehensive understanding of the performance characteristics of circular linked lists and their operations in various real-world scenarios. If you have any more questions or need further details, feel free to ask!




Certainly! Below is the complete implementation of a singly circular linked list in Python, including common operations such as insertion, deletion, traversal, and searching.

### Node Class

The `Node` class represents an individual element in the linked list. Each node contains the data and a reference to the next node.

```python
class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list
```

### Singly Circular Linked List Class

The `SinglyCircularLinkedList` class manages the linked list, including operations like insertion, deletion, traversal, and search.

```python
class SinglyCircularLinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node.next = self.head
            current.next = new_node
            self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def delete_node(self, key):
        if self.head is None:
            return

        current = self.head
        prev = None

        while True:
            if current.data == key:
                if prev:
                    prev.next = current.next
                else:
                    if self.head == self.head.next:
                        self.head = None
                    else:
                        last = self.head
                        while last.next != self.head:
                            last = last.next
                        last.next = self.head.next
                        self.head = self.head.next
                return

            prev = current
            current = current.next

            if current == self.head:
                break

    def search(self, key):
        if self.head is None:
            return False
        current = self.head
        while True:
            if current.data == key:
                return True
            current = current.next
            if current == self.head:
                break
        return False

    def traverse(self):
        elements = []
        if self.head is None:
            return elements
        current = self.head
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.head:
                break
        return elements

    def __str__(self):
        elements = self.traverse()
        return " -> ".join(map(str, elements)) + " -> " + str(self.head.data)  # To show the circular nature

# Example Usage
if __name__ == "__main__":
    scll = SinglyCircularLinkedList()
    scll.insert_at_beginning(3)
    scll.insert_at_beginning(2)
    scll.insert_at_beginning(1)
    print("After inserting at the beginning:", scll)

    scll.insert_at_end(4)
    scll.insert_at_end(5)
    print("After inserting at the end:", scll)

    print("Search for element 3:", scll.search(3))
    print("Search for element 6:", scll.search(6))

    scll.delete_node(3)
    print("After deleting element 3:", scll)

    scll.delete_node(1)
    print("After deleting element 1:", scll)

    print("Final list traversal:", scll.traverse())
```

### Explanation
- **Node Class**: Represents an individual element in the linked list. Each node contains the data and a reference to the next node.
- **SinglyCircularLinkedList Class**: Manages the linked list, including methods for insertion, deletion, searching, and traversal.
  - `insert_at_beginning(data)`: Inserts a new node at the beginning of the list.
  - `insert_at_end(data)`: Inserts a new node at the end of the list.
  - `delete_node(key)`: Deletes the first node found with the specified key.
  - `search(key)`: Searches for a node with the specified key.
  - `traverse()`: Traverses the list and returns a list of node data.
  - `__str__()`: Returns a string representation of the linked list.

### Output
```
After inserting at the beginning: 1 -> 2 -> 3 -> 1
After inserting at the end: 1 -> 2 -> 3 -> 4 -> 5 -> 1
Search for element 3: True
Search for element 6: False
After deleting element 3: 1 -> 2 -> 4 -> 5 -> 1
After deleting element 1: 2 -> 4 -> 5 -> 2
Final list traversal: [2, 4, 5]
```

This implementation covers the basic operations for a singly circular linked list in Python. Each method includes comments to explain the logic and steps involved. If you have any questions or need further details, feel free to ask!
