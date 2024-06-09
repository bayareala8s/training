class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """
        This method adds an item to the end of the queue.
        """
        self.queue.append(item)

    def dequeue(self):
        """
        This method removes an item from the front of the queue.
        """
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    def size(self):
        """
        This method returns the number of items in the queue.
        """
        return len(self.queue)

    def is_empty(self):
        """
        This method checks if the queue is empty.
        """
        return self.size() == 0

    def peek(self):
        """
        This method returns the item at the front of the queue without removing it.
        """
        if self.is_empty():
            return None
        return self.queue[0]

def printer_queue(queue, jobs):
    """
    This function simulates a printer queue.
    """
    # Add all print jobs to the queue
    for job in jobs:
        queue.enqueue(job)

    while not queue.is_empty():
        # Process the next job in the queue
        current_job = queue.dequeue()
        print(f"Processing job: {current_job}")

# Create a new queue
queue = Queue()

# Simulate a printer queue
print_jobs = ["job1", "job2", "job3", "job4", "job5"]
printer_queue(queue, print_jobs)