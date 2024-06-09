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
