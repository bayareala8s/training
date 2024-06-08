class Node:
    """
    Class to represent a node in the stack.
    Each node contains a value and a reference to the next node.
    """

    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    """
    Class to represent the stack data structure.
    The stack follows the LIFO (Last In, First Out) principle.
    """

    def __init__(self):
        """
        Initialize an empty stack.
        The top attribute points to the top node in the stack.
        The count attribute keeps track of the number of elements in the stack.
        """
        self.top = None
        self.count = 0

    def push(self, item):
        """
        Add an item to the top of the stack.

        :param item: The item to be added to the stack.
        """
        new_node = Node(item)  # Create a new node with the given item
        new_node.next = self.top  # Make the new node point to the current top node
        self.top = new_node  # Update the top to be the new node
        self.count += 1  # Increment the count of elements

    def pop(self):
        """
        Remove and return the top item from the stack.

        :return: The value of the top item in the stack.
        :raises IndexError: If the stack is empty.
        """
        if not self.is_empty():
            popped_value = self.top.value  # Get the value of the top item
            self.top = self.top.next  # Update the top to the next node
            self.count -= 1  # Decrement the count of elements
            return popped_value
        raise IndexError("pop from empty stack")  # Raise an error if the stack is empty

    def peek(self):
        """
        Return the top item from the stack without removing it.

        :return: The value of the top item in the stack.
        :raises IndexError: If the stack is empty.
        """
        if not self.is_empty():
            return self.top.value  # Return the value of the top item
        raise IndexError("peek from empty stack")  # Raise an error if the stack is empty

    def is_empty(self):
        """
        Check if the stack is empty.

        :return: True if the stack is empty, False otherwise.
        """
        return self.top is None  # Return True if top is None, indicating the stack is empty

    def size(self):
        """
        Return the number of items in the stack.

        :return: The number of items in the stack.
        """
        return self.count  # Return the count of elements


class BrowserHistory:
    """
    Class to simulate a browser's back and forward functionality using stacks.
    """

    def __init__(self):
        """
        Initialize the browser history with empty history and back stacks.
        """
        self.history_stack = Stack()  # Stack to keep track of visited pages
        self.back_stack = Stack()  # Stack to keep track of pages navigated back from

    def visit(self, url):
        """
        Visit a new URL.

        :param url: The URL of the new page to visit.
        """
        self.history_stack.push(url)  # Push the new URL onto the history stack
        self.back_stack = Stack()  # Clear the back stack since we can't go forward from a new page
        print(f"Visited: {url}")

    def back(self):
        """
        Go back to the previous page.

        :return: The URL of the previous page.
        :raises IndexError: If there is no previous page.
        """
        if self.history_stack.size() > 1:
            current_page = self.history_stack.pop()  # Pop the current page from the history stack
            self.back_stack.push(current_page)  # Push the current page onto the back stack
            previous_page = self.history_stack.peek()  # Peek the previous page from the history stack
            print(f"Back to: {previous_page}")
            return previous_page
        raise IndexError("No previous page to go back to")

    def forward(self):
        """
        Go forward to the next page.

        :return: The URL of the next page.
        :raises IndexError: If there is no next page.
        """
        if not self.back_stack.is_empty():
            next_page = self.back_stack.pop()  # Pop the next page from the back stack
            self.history_stack.push(next_page)  # Push the next page onto the history stack
            print(f"Forward to: {next_page}")
            return next_page
        raise IndexError("No next page to go forward to")


# Example usage of the BrowserHistory class
if __name__ == "__main__":
    browser = BrowserHistory()
    browser.visit("https://example.com")
    browser.visit("https://google.com")
    browser.visit("https://github.com")

    browser.back()  # Output: Back to: https://google.com
    browser.back()  # Output: Back to: https://example.com

    browser.forward()  # Output: Forward to: https://google.com
    browser.visit("https://stackoverflow.com")  # Output: Visited: https://stackoverflow.com

    browser.back()  # Output: Back to: https://google.com
    browser.forward()  # Output: Forward to: https://stackoverflow.com
