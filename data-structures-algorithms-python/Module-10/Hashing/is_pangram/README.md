To check if a given string is a pangram, we need to verify that it contains every letter of the English alphabet at least once. Here’s a function to accomplish this, followed by an explanation and some unit tests.

### Function to Check if a Sentence is a Pangram

```python
def is_pangram(sentence):
    # Create a set of all lowercase English letters
    alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
    
    # Create a set of characters in the given sentence
    sentence_set = set(sentence)
    
    # Check if the alphabet set is a subset of the sentence set
    return alphabet_set.issubset(sentence_set)
```

### Explanation

1. **Create a Set of Alphabet**:
   ```python
   alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
   ```
   - This set contains all the lowercase letters from 'a' to 'z'.

2. **Create a Set of Sentence Characters**:
   ```python
   sentence_set = set(sentence)
   ```
   - This set contains all unique characters present in the sentence.

3. **Check Subset Condition**:
   ```python
   return alphabet_set.issubset(sentence_set)
   ```
   - This checks if every letter in the `alphabet_set` is present in the `sentence_set`.

### Unit Test Cases

Here are some unit test cases for the `is_pangram` function:

```python
import unittest

class TestIsPangram(unittest.TestCase):
    
    def test_pangram(self):
        sentence = "the quick brown fox jumps over the lazy dog"
        self.assertTrue(is_pangram(sentence))
    
    def test_missing_letters(self):
        sentence = "the quick brown fox jumps over the lazy"
        self.assertFalse(is_pangram(sentence))
    
    def test_empty_string(self):
        sentence = ""
        self.assertFalse(is_pangram(sentence))
    
    def test_single_letter(self):
        sentence = "a"
        self.assertFalse(is_pangram(sentence))
    
    def test_all_letters(self):
        sentence = "abcdefghijklmnopqrstuvwxyz"
        self.assertTrue(is_pangram(sentence))
    
    def test_mixed_case(self):
        sentence = "The Quick Brown Fox Jumps Over The Lazy Dog"
        self.assertTrue(is_pangram(sentence.lower()))
    
    def test_special_characters(self):
        sentence = "the quick brown fox jumps over the lazy dog!@#"
        self.assertTrue(is_pangram(sentence))
    
    def test_repeated_letters(self):
        sentence = "a quick movement of the enemy will jeopardize five gunboats"
        self.assertTrue(is_pangram(sentence))

# Run the tests
if __name__ == '__main__':
    unittest.main()
```

### Explanation of Test Cases:

1. **test_pangram**: A sentence that is a known pangram.
2. **test_missing_letters**: A sentence missing one or more letters to ensure it returns `false`.
3. **test_empty_string**: An empty string should return `false`.
4. **test_single_letter**: A sentence with only one letter should return `false`.
5. **test_all_letters**: A sentence containing all letters exactly once should return `true`.
6. **test_mixed_case**: A pangram with mixed case letters should return `true` after converting to lowercase.
7. **test_special_characters**: A pangram with additional special characters should still return `true`.
8. **test_repeated_letters**: A sentence that is a pangram with repeated letters should return `true`.

These test cases cover a wide range of scenarios to ensure the `is_pangram` function works correctly.


### Step-by-Step Explanation with Visual Diagram

Let's break down the function `is_pangram` step-by-step, and illustrate the process with a visual diagram.

#### Step 1: Create a Set of Alphabet

**Code:**
```python
alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
```
**Description:**
- This step creates a set containing all the lowercase English letters from 'a' to 'z'.
- A set is used because it allows for efficient membership testing.

**Diagram:**
```
alphabet_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
```

#### Step 2: Create a Set of Sentence Characters

**Code:**
```python
sentence_set = set(sentence)
```
**Description:**
- This step converts the input sentence into a set of unique characters.
- This helps in efficiently checking if all the letters in `alphabet_set` are present in the `sentence`.

**Example:**
- For the sentence: "the quick brown fox jumps over the lazy dog"

**Diagram:**
```
sentence = "the quick brown fox jumps over the lazy dog"
sentence_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
```

#### Step 3: Check Subset Condition

**Code:**
```python
return alphabet_set.issubset(sentence_set)
```
**Description:**
- This checks if every letter in the `alphabet_set` is present in the `sentence_set`.
- If `alphabet_set` is a subset of `sentence_set`, the function returns `true`, indicating that the sentence is a pangram. Otherwise, it returns `false`.

**Diagram:**
```
alphabet_set ⊆ sentence_set
```
- If `alphabet_set` is a subset of `sentence_set`, return `true`.
- Otherwise, return `false`.

### Complete Example with Visual Diagram

Let's go through an example with the sentence "the quick brown fox jumps over the lazy dog":

1. **Input Sentence**:
   ```
   sentence = "the quick brown fox jumps over the lazy dog"
   ```

2. **Step 1: Create Alphabet Set**:
   ```
   alphabet_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
   ```

3. **Step 2: Create Sentence Set**:
   ```
   sentence_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
   ```

4. **Step 3: Check Subset Condition**:
   ```
   alphabet_set.issubset(sentence_set)  # returns True
   ```

**Visual Diagram**:

1. **Input Sentence**:
   ```
   "the quick brown fox jumps over the lazy dog"
   ```

2. **Convert to Alphabet Set**:
   ```
   alphabet_set:
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   | a | b | c | d | e | f | g | h | i | j | k | l | m |
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   | n | o | p | q | r | s | t | u | v | w | x | y | z |
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   ```

3. **Convert Sentence to Set**:
   ```
   sentence_set:
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   | a | b | c | d | e | f | g | h | i | j | k | l | m |
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   | n | o | p | q | r | s | t | u | v | w | x | y | z |
   +---+---+---+---+---+---+---+---+---+---+---+---+---+
   ```

4. **Check Subset Condition**:
   ```
   alphabet_set ⊆ sentence_set  # True
   ```

In this example, since `alphabet_set` is a subset of `sentence_set`, the function returns `true`.

### Summary of Steps:
1. **Create a set of all lowercase English letters**.
2. **Create a set of characters in the given sentence**.
3. **Check if the alphabet set is a subset of the sentence set**.
4. **Return `true` if it is a subset, otherwise return `false`**.

### Time Complexity

1. **Creating Alphabet Set**:
   ```python
   alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
   ```
   - This operation takes O(1) time because it involves a fixed number of elements (26 letters).

2. **Creating Sentence Set**:
   ```python
   sentence_set = set(sentence)
   ```
   - Converting a string of length `n` to a set involves iterating over each character in the string, which takes O(n) time.

3. **Checking Subset Condition**:
   ```python
   return alphabet_set.issubset(sentence_set)
   ```
   - Checking if one set is a subset of another takes O(1) time for each element in the alphabet set, which contains 26 elements. Therefore, this step takes O(26) = O(1) time.

Overall, the time complexity is:
\[ O(1) + O(n) + O(1) = O(n) \]
Thus, the time complexity is **O(n)**, where `n` is the length of the input string.

### Space Complexity

1. **Alphabet Set**:
   ```python
   alphabet_set = set('abcdefghijklmnopqrstuvwxyz')
   ```
   - The alphabet set requires O(1) space because it contains a fixed number of elements (26 letters).

2. **Sentence Set**:
   ```python
   sentence_set = set(sentence)
   ```
   - The sentence set requires O(n) space in the worst case, where `n` is the number of unique characters in the input string.

Overall, the space complexity is:
\[ O(1) + O(n) = O(n) \]
Thus, the space complexity is **O(n)**, where `n` is the length of the input string.

### Summary:
- **Time Complexity**: O(n)
- **Space Complexity**: O(n)

Both the time and space complexity are linear with respect to the length of the input string, making the function efficient.
