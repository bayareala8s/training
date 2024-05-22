Certainly! Let's solve the problem of finding the first character to appear twice in a string. We'll use a set to keep track of characters we've seen so far. As we iterate through the string, we'll check if the character is already in the set. If it is, we've found our answer. If not, we'll add the character to the set.

Here is a step-by-step visual explanation:

### Step-by-Step Solution

1. **Initialize an Empty Set**:
   - We'll use a set to keep track of characters we've seen.
   - Let's call this set `seen`.

2. **Iterate Through the String**:
   - We'll iterate through each character in the string `s`.

3. **Check if the Character is in the Set**:
   - For each character, we'll check if it is already in the `seen` set.
   - If it is, we've found the first duplicate character.
   - If it isn't, we'll add the character to the set and continue.

4. **Return the First Duplicate Character**:
   - Once we find the first duplicate character, we'll return it.

### Example

Let's go through an example string `s = "abca"` step by step.

#### Initial State

- String: `"abca"`
- Set `seen`: `{}` (empty)

#### Step 1: Process the First Character 'a'

- Current character: `'a'`
- Check if `'a'` is in `seen`: No
- Add `'a'` to `seen`
- Set `seen`: `{'a'}`

#### Step 2: Process the Second Character 'b'

- Current character: `'b'`
- Check if `'b'` is in `seen`: No
- Add `'b'` to `seen`
- Set `seen`: `{'a', 'b'}`

#### Step 3: Process the Third Character 'c'

- Current character: `'c'`
- Check if `'c'` is in `seen`: No
- Add `'c'` to `seen`
- Set `seen`: `{'a', 'b', 'c'}`

#### Step 4: Process the Fourth Character 'a'

- Current character: `'a'`
- Check if `'a'` is in `seen`: Yes
- `'a'` is the first character to appear twice
- Return `'a'`

### Visual Diagram

```
String: "abca"
Set: {}

Step 1: Process 'a'
- Seen set: {'a'}

Step 2: Process 'b'
- Seen set: {'a', 'b'}

Step 3: Process 'c'
- Seen set: {'a', 'b', 'c'}

Step 4: Process 'a'
- 'a' is in the seen set: {'a', 'b', 'c'}
- Return 'a'
```

### Python Code

Here is the Python code that implements the above logic:

```python
def first_duplicate_char(s):
    # Initialize an empty set to keep track of seen characters
    seen = set()
    
    # Iterate through each character in the string
    for char in s:
        # Check if the character is already in the set
        if char in seen:
            # If yes, return the character (first duplicate)
            return char
        # Otherwise, add the character to the set
        seen.add(char)

# Example usage
s = "abca"
result = first_duplicate_char(s)
print(result)  # Output: 'a'
```

### Explanation of the Code

1. **Initialization**:
   - We initialize an empty set `seen` to keep track of the characters we encounter.

2. **Iteration**:
   - We iterate through each character in the string `s` using a `for` loop.

3. **Check for Duplicate**:
   - For each character, we check if it is already in the `seen` set.
   - If it is, we return that character as it is the first duplicate.
   - If it isn't, we add the character to the `seen` set and continue.

4. **Return the Result**:
   - The function returns the first duplicate character found.

This approach ensures that we find the first character to appear twice in an efficient manner, 
with a time complexity of O(n) and space complexity of O(n), where n is the length of the string.

Below are unit test cases for the `first_duplicate_char` function using Python's built-in `unittest` framework. These tests cover various scenarios, 
including cases with different characters and positions of the first duplicate character.

### Unit Test Cases

```python
import unittest

def first_duplicate_char(s):
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None  # This line should never be reached because it is guaranteed there will be a duplicate character

class TestFirstDuplicateChar(unittest.TestCase):
    def test_example_case(self):
        self.assertEqual(first_duplicate_char("abca"), 'a')

    def test_all_unique_then_duplicate(self):
        self.assertEqual(first_duplicate_char("abcdefghija"), 'a')

    def test_immediate_duplicate(self):
        self.assertEqual(first_duplicate_char("aabbcc"), 'a')

    def test_duplicate_in_middle(self):
        self.assertEqual(first_duplicate_char("abcdefcgh"), 'c')

    def test_long_string_with_late_duplicate(self):
        self.assertEqual(first_duplicate_char("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstu"), 'a')

    def test_numbers(self):
        self.assertEqual(first_duplicate_char("123451234"), '1')

    def test_mixed_characters(self):
        self.assertEqual(first_duplicate_char("abc123cba"), 'c')

    def test_single_character_repeated(self):
        self.assertEqual(first_duplicate_char("zzzz"), 'z')

    def test_multiple_same_characters(self):
        self.assertEqual(first_duplicate_char("abababab"), 'a')

if __name__ == '__main__':
    unittest.main()
```

### Explanation of Test Cases

1. **Example Case**:
   - Input: `"abca"`
   - Expected Output: `'a'`
   - Explanation: `'a'` is the first character to appear twice.

2. **All Unique Characters Followed by Duplicate**:
   - Input: `"abcdefghija"`
   - Expected Output: `'a'`
   - Explanation: `'a'` is the first character to appear twice after all unique characters.

3. **Immediate Duplicate**:
   - Input: `"aabbcc"`
   - Expected Output: `'a'`
   - Explanation: The first two characters are the same, so `'a'` is the first duplicate.

4. **Duplicate in Middle**:
   - Input: `"abcdefcgh"`
   - Expected Output: `'c'`
   - Explanation: `'c'` is the first character to appear twice in the middle of the string.

5. **Long String with Late Duplicate**:
   - Input: `"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstu"`
   - Expected Output: `'a'`
   - Explanation: `'a'` is the first character to appear twice, even though the string is long.

6. **Numbers**:
   - Input: `"123451234"`
   - Expected Output: `'1'`
   - Explanation: `'1'` is the first character to appear twice.

7. **Mixed Characters**:
   - Input: `"abc123cba"`
   - Expected Output: `'c'`
   - Explanation: `'c'` is the first character to appear twice among letters and numbers.

8. **Single Character Repeated**:
   - Input: `"zzzz"`
   - Expected Output: `'z'`
   - Explanation: `'z'` is repeated immediately.

9. **Multiple Same Characters**:
   - Input: `"abababab"`
   - Expected Output: `'a'`
   - Explanation: `'a'` is the first character to appear twice.

### Running the Tests

To run these tests, save the code in a file named `test_first_duplicate_char.py` and execute the file using Python:

```bash
python test_first_duplicate_char.py
```

The `unittest` framework will run the tests and provide a report indicating whether the tests passed or failed. 
This ensures that the `first_duplicate_char` function is thoroughly tested for various input scenarios.
