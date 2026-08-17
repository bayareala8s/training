class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        """
        This method pushes an item onto the stack.
        """
        self.stack.append(item)

    def pop(self):
        """
        This method pops an item off the stack.
        """
        if not self.is_empty():
            return self.stack.pop()
        else:
            return "Stack is empty"

    def peek(self):
        """
        This method returns the top item from the stack but does not remove it.
        """
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "Stack is empty"

    def is_empty(self):
        """
        This method returns True if the stack is empty and False otherwise.
        """
        return len(self.stack) == 0

class TextEditor:
    def __init__(self):
        self.text = ""
        self.stack = Stack()

    def insert(self, char):
        """
        This method inserts a character into the text and pushes the operation onto the stack.
        """
        self.text += char
        self.stack.push(('insert', char))

    def delete(self):
        """
        This method deletes the last character from the text and pushes the operation onto the stack.
        """
        if self.text:
            deleted_char = self.text[-1]
            self.text = self.text[:-1]
            self.stack.push(('delete', deleted_char))

    def undo(self):
        """
        This method undoes the last operation.
        """
        if not self.stack.is_empty():
            operation, char = self.stack.pop()
            if operation == 'insert':
                self.text = self.text[:-1]
            elif operation == 'delete':
                self.text += char

    def get_text(self):
        """
        This method returns the current text.
        """
        return self.text

# Create a TextEditor object
editor = TextEditor()

# Insert characters
editor.insert('h')
editor.insert('e')
editor.insert('l')
editor.insert('l')
editor.insert('o')

print(editor.get_text())  # Output: hello

# Delete last character
editor.delete()

print(editor.get_text())  # Output: hell

# Undo last operation (delete 'o')
editor.undo()

print(editor.get_text())  # Output: hello


