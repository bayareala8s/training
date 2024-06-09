class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def is_empty(self):
        """
        This method checks if the queue is empty.
        """
        return self.front is None

    def enqueue(self, item):
        """
        This method adds an item to the end of the queue.
        """
        temp = Node(item)

        if self.rear is None:
            self.front = self.rear = temp
            return
        self.rear.next = temp
        self.rear = temp

    def dequeue(self):
        """
        This method removes an item from the front of the queue.
        """
        if self.is_empty():
            return
        temp = self.front
        self.front = temp.next

        if self.front is None:
            self.rear = None

        return str(temp.data)

def customer_service(queue, customers):
    """
    This function simulates a customer service queue.
    """
    # Add all customers to the queue
    for customer in customers:
        queue.enqueue(customer)

    while not queue.is_empty():
        # Process the next customer in the queue
        current_customer = queue.dequeue()
        print(f"Processing customer: {current_customer}")

# Create a new queue
queue = Queue()

# Simulate a customer service queue
customers = ["Customer1", "Customer2", "Customer3", "Customer4", "Customer5"]
customer_service(queue, customers)