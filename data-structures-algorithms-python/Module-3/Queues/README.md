### **Queue in Data Structures and Algorithms**

#### **1. Introduction to Queues**

A **queue** is a linear data structure that follows the **First In First Out (FIFO)** principle. This means that the element that is inserted first is the one that is removed first. Queues are used in various applications such as scheduling processes, managing requests in a web server, handling interrupts in an operating system, and more.

#### **2. Basic Operations**

Queues support the following basic operations:

- **Enqueue:** Add an element to the end of the queue.
- **Dequeue:** Remove an element from the front of the queue.
- **Front (or Peek):** Get the front element of the queue without removing it.
- **IsEmpty:** Check if the queue is empty.
- **IsFull:** Check if the queue is full (in case of a bounded queue).

#### **3. Types of Queues**

1. **Simple Queue:** Also known as a linear queue, it allows insertion at the rear and deletion from the front.
2. **Circular Queue:** A circular queue overcomes the limitations of a simple queue by connecting the end of the queue back to the front, forming a circle.
3. **Priority Queue:** Elements are inserted based on their priority, not just their position.
4. **Deque (Double-Ended Queue):** Allows insertion and deletion from both the front and rear ends.

#### **4. Implementing a Queue**

Queues can be implemented using arrays or linked lists.

**Array Implementation:**
```python
class Queue:
    def __init__(self, size):
        self.queue = [None] * size
        self.max_size = size
        self.front = self.rear = -1

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

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.max_size
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[self.front]
```

**Linked List Implementation:**
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.value

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.value
```

#### **5. Applications of Queues**

1. **CPU Scheduling:** Queues are used in operating systems for managing processes.
2. **Printer Spooling:** Managing multiple print jobs.
3. **Simulation:** Used to model real-world queues like checkout lines, call centers, etc.
4. **Breadth-First Search (BFS):** An algorithm for traversing or searching tree or graph data structures.

#### **6. Complexity Analysis**

- **Enqueue:** \(O(1)\)
- **Dequeue:** \(O(1)\)
- **Peek:** \(O(1)\)
- **IsEmpty:** \(O(1)\)
- **IsFull:** \(O(1)\)

The constant time complexity for these operations makes queues very efficient for the scenarios they are used in.

#### **7. Real-World Example**

Consider a simple example of a queue system in a bank:

```python
class BankQueue:
    def __init__(self):
        self.queue = []

    def join_queue(self, customer):
        self.queue.append(customer)
        print(f"{customer} has joined the queue.")

    def serve_customer(self):
        if not self.queue:
            print("No customers in queue.")
            return
        customer = self.queue.pop(0)
        print(f"Serving {customer}")

    def next_customer(self):
        if not self.queue:
            print("No customers in queue.")
            return
        print(f"Next customer to be served is {self.queue[0]}")

    def is_queue_empty(self):
        return len(self.queue) == 0
```

Usage:
```python
bank_queue = BankQueue()
bank_queue.join_queue("Alice")
bank_queue.join_queue("Bob")
bank_queue.next_customer()
bank_queue.serve_customer()
bank_queue.serve_customer()
bank_queue.serve_customer()
```

This simple example models a bank queue where customers join the queue and are served in the order they joined.

#### **Conclusion**

Queues are fundamental data structures that provide efficient management of ordered elements and have numerous applications in computer science and real-world scenarios. Understanding how to implement and use queues effectively is crucial for solving many algorithmic problems.



Certainly! Let's explore a few real-world implementations of queues.

### **1. Print Queue System**

**Scenario:** A print queue system in an office where multiple print jobs are queued up for a single printer.

**Implementation:**

```python
import time
from collections import deque

class PrintJob:
    def __init__(self, job_name, pages):
        self.job_name = job_name
        self.pages = pages

class PrinterQueue:
    def __init__(self):
        self.queue = deque()

    def add_job(self, job):
        self.queue.append(job)
        print(f"Added print job: {job.job_name} with {job.pages} pages")

    def print_job(self):
        if not self.queue:
            print("No jobs in the queue.")
            return
        job = self.queue.popleft()
        print(f"Printing job: {job.job_name}")
        for page in range(1, job.pages + 1):
            print(f"Printing page {page}")
            time.sleep(1)  # Simulate time taken to print a page
        print(f"Completed print job: {job.job_name}")

    def next_job(self):
        if not self.queue:
            print("No jobs in the queue.")
            return
        job = self.queue[0]
        print(f"Next job: {job.job_name} with {job.pages} pages")

    def is_empty(self):
        return len(self.queue) == 0

# Example Usage
printer_queue = PrinterQueue()
printer_queue.add_job(PrintJob("Document1", 3))
printer_queue.add_job(PrintJob("Document2", 5))

printer_queue.next_job()
printer_queue.print_job()
printer_queue.print_job()
printer_queue.print_job()
```

### **2. Task Scheduling in Operating Systems**

**Scenario:** Task scheduling where tasks are managed in a round-robin fashion, ensuring each task gets a fair share of CPU time.

**Implementation:**

```python
class Task:
    def __init__(self, task_id, duration):
        self.task_id = task_id
        self.duration = duration

class TaskScheduler:
    def __init__(self, time_slice):
        self.queue = deque()
        self.time_slice = time_slice

    def add_task(self, task):
        self.queue.append(task)
        print(f"Added task {task.task_id} with duration {task.duration}")

    def run(self):
        while self.queue:
            task = self.queue.popleft()
            print(f"Running task {task.task_id} for {self.time_slice} units")
            task.duration -= self.time_slice
            if task.duration > 0:
                print(f"Re-queueing task {task.task_id} with remaining duration {task.duration}")
                self.queue.append(task)
            else:
                print(f"Task {task.task_id} completed")

# Example Usage
scheduler = TaskScheduler(time_slice=5)
scheduler.add_task(Task("Task1", 10))
scheduler.add_task(Task("Task2", 15))
scheduler.add_task(Task("Task3", 5))

scheduler.run()
```

### **3. Call Center Queue Management**

**Scenario:** Managing incoming calls at a call center where calls are handled in the order they are received.

**Implementation:**

```python
class Call:
    def __init__(self, caller_id, call_reason):
        self.caller_id = caller_id
        self.call_reason = call_reason

class CallCenterQueue:
    def __init__(self):
        self.queue = deque()

    def add_call(self, call):
        self.queue.append(call)
        print(f"Added call from {call.caller_id} regarding {call.call_reason}")

    def handle_call(self):
        if not self.queue:
            print("No calls in the queue.")
            return
        call = self.queue.popleft()
        print(f"Handling call from {call.caller_id} regarding {call.call_reason}")

    def next_call(self):
        if not self.queue:
            print("No calls in the queue.")
            return
        call = self.queue[0]
        print(f"Next call from {call.caller_id} regarding {call.call_reason}")

    def is_empty(self):
        return len(self.queue) == 0

# Example Usage
call_center = CallCenterQueue()
call_center.add_call(Call("Caller1", "Billing issue"))
call_center.add_call(Call("Caller2", "Technical support"))

call_center.next_call()
call_center.handle_call()
call_center.handle_call()
call_center.handle_call()
```

### **4. Web Server Request Handling**

**Scenario:** Managing incoming HTTP requests to a web server.

**Implementation:**

```python
class HTTPRequest:
    def __init__(self, request_id, endpoint):
        self.request_id = request_id
        self.endpoint = endpoint

class WebServerQueue:
    def __init__(self):
        self.queue = deque()

    def add_request(self, request):
        self.queue.append(request)
        print(f"Added request {request.request_id} to {request.endpoint}")

    def handle_request(self):
        if not self.queue:
            print("No requests in the queue.")
            return
        request = self.queue.popleft()
        print(f"Handling request {request.request_id} to {request.endpoint}")

    def next_request(self):
        if not self.queue:
            print("No requests in the queue.")
            return
        request = self.queue[0]
        print(f"Next request {request.request_id} to {request.endpoint}")

    def is_empty(self):
        return len(self.queue) == 0

# Example Usage
server_queue = WebServerQueue()
server_queue.add_request(HTTPRequest("Req1", "/home"))
server_queue.add_request(HTTPRequest("Req2", "/contact"))

server_queue.next_request()
server_queue.handle_request()
server_queue.handle_request()
server_queue.handle_request()
```

These examples demonstrate how queues can be utilized in various real-world scenarios, from managing print jobs to scheduling tasks, handling calls in a call center, and managing web server requests.




Sure, let's go through a detailed implementation of a queue in Python using both an array (list) and a linked list approach.

### **1. Array (List) Implementation of Queue**

An array-based implementation of a queue is straightforward but has a limitation of fixed size unless we dynamically resize the array.

```python
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
```

### **2. Linked List Implementation of Queue**

A linked list-based implementation of a queue can grow dynamically, making it more flexible than the array-based approach.

```python
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
```

### **Explanation of the Code**

#### **Array (List) Implementation**

1. **Initialization:**
   - `self.queue`: List initialized with `None` values.
   - `self.max_size`: Maximum size of the queue.
   - `self.front` and `self.rear`: Pointers to the front and rear of the queue, initialized to -1.

2. **is_empty:** Checks if the queue is empty by checking if `self.front` is -1.

3. **is_full:** Checks if the queue is full by seeing if the next position of `self.rear` is equal to `self.front`.

4. **enqueue:** Adds an element to the end of the queue. If the queue is empty, both `self.front` and `self.rear` are set to 0. Otherwise, `self.rear` is incremented circularly.

5. **dequeue:** Removes an element from the front of the queue. If the queue becomes empty after dequeue, both `self.front` and `self.rear` are reset to -1. Otherwise, `self.front` is incremented circularly.

6. **peek:** Returns the front element without removing it.

7. **display:** Displays the elements in the queue.

#### **Linked List Implementation**

1. **Node Class:** Represents a node in the linked list with `value` and `next` attributes.

2. **Initialization:**
   - `self.front` and `self.rear`: Pointers to the front and rear nodes of the queue, initialized to `None`.

3. **is_empty:** Checks if the queue is empty by checking if `self.front` is `None`.

4. **enqueue:** Adds a new node to the end of the queue. If the queue is empty, both `self.front` and `self.rear` are set to the new node. Otherwise, the `next` pointer of the current rear node is set to the new node, and `self.rear` is updated.

5. **dequeue:** Removes the front node from the queue. If the queue becomes empty after dequeue, both `self.front` and `self.rear` are reset to `None`.

6. **peek:** Returns the value of the front node without removing it.

7. **display:** Displays the elements in the queue from front to rear.

Both implementations demonstrate the core functionality of a queue, but the linked list approach is more flexible in terms of size management, while the array approach can be more efficient in terms of memory access patterns.
