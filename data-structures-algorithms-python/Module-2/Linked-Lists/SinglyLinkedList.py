class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list

class SinglyLinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    def insert_at_beginning(self, data):
        new_node = Node(data)  # Create a new node with the given data
        new_node.next = self.head  # Point the new node to the current head
        self.head = new_node  # Update the head to be the new node

    def insert_at_end(self, data):
        new_node = Node(data)  # Create a new node with the given data
        if not self.head:  # If the list is empty
            self.head = new_node  # Set the head to the new node
            return
        last = self.head
        while last.next:  # Traverse to the last node
            last = last.next
        last.next = new_node  # Point the last node to the new node

    def delete_node(self, key):
        temp = self.head
        if temp and temp.data == key:  # If the head is the node to be deleted
            self.head = temp.next  # Update the head to the next node
            temp = None  # Free the old head
            return
        prev = None
        while temp and temp.data != key:  # Traverse to find the node to delete
            prev = temp
            temp = temp.next
        if temp is None:  # If the node was not found
            return
        prev.next = temp.next  # Remove the node from the list
        temp = None  # Free the node

    def search(self, key):
        current = self.head
        while current:  # Traverse the list
            if current.data == key:  # If the node is found
                return True
            current = current.next
        return False  # If the node was not found

    def traverse(self):
        elements = []
        current = self.head
        while current:  # Traverse the list
            elements.append(current.data)  # Add the node data to the list
            current = current.next
        return elements  # Return the list of elements

    def __str__(self):
        elements = self.traverse()
        return " -> ".join(map(str, elements))  # Format the list elements as a string

# Example Usage
if __name__ == "__main__":
    # Create a new linked list
    linked_list = SinglyLinkedList()

    # Insert elements at the beginning
    linked_list.insert_at_beginning(3)
    linked_list.insert_at_beginning(2)
    linked_list.insert_at_beginning(1)
    print("After inserting at the beginning:", linked_list)

    # Insert elements at the end
    linked_list.insert_at_end(4)
    linked_list.insert_at_end(5)
    print("After inserting at the end:", linked_list)

    # Search for elements
    print("Search for element 3:", linked_list.search(3))  # Output: True
    print("Search for element 6:", linked_list.search(6))  # Output: False

    # Delete elements
    linked_list.delete_node(3)
    print("After deleting element 3:", linked_list)

    linked_list.delete_node(1)
    print("After deleting element 1:", linked_list)

    # Traverse and print the list
    print("Final list traversal:", linked_list.traverse())
