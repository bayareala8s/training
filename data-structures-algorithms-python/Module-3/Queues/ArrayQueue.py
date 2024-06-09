class ArrayQueue:
    def __init__(self, size):
        self.queue = [None] * size
        self.max_size = size
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.max_size == self.front

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        if self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.max_size
        self.queue[self.rear] = item
        print(f"Enqueued {item}")

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.max_size
        print(f"Dequeued {item}")
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[self.front]

    def display(self):
        if self.is_empty():
            print("Queue is empty")
        else:
            index = self.front
            while index != self.rear:
                print(self.queue[index], end=" ")
                index = (index + 1) % self.max_size
            print(self.queue[index])

# Example Usage
queue = ArrayQueue(5)
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