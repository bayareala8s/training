class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list
        self.prev = None  # Reference to the previous node in the list

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

# Example Usage
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
