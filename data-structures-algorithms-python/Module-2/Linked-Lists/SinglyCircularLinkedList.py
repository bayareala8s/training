class Node:
    def __init__(self, data):
        self.data = data  # The value stored in the node
        self.next = None  # Reference to the next node in the list



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
