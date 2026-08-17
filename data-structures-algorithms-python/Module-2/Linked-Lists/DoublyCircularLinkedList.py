class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list
        self.prev = None  # Reference to the previous node in the list


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
        while True:
            if current.data == key:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    if self.head.next == self.head:
                        self.head = None
                    else:
                        self.head = current.next
                return
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
