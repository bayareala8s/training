class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
            print(f"Enqueued {item}")
            return
        self.rear.next = new_node
        self.rear = new_node
        print(f"Enqueued {item}")

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        print(f"Dequeued {temp.value}")
        return temp.value

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.value

    def display(self):
        if self.is_empty():
            print("Queue is empty")
            return
        temp = self.front
        while temp:
            print(temp.value, end=" -> ")
            temp = temp.next
        print("None")

# Example Usage
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)
queue.enqueue(40)
queue.enqueue(50)
queue.display()
queue.dequeue()
queue.dequeue()
queue.enqueue(60)
queue.display()