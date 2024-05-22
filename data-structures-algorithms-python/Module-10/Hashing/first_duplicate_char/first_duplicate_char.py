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


import unittest

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
