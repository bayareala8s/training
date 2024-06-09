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
