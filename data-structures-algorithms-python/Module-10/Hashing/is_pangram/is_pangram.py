def is_pangram(sentence):
    # Create a set of all lowercase English letters
    alphabet_set = set('abcdefghijklmnopqrstuvwxyz')

    # Create a set of characters in the given sentence
    sentence_set = set(sentence)

    # Check if the alphabet set is a subset of the sentence set
    return alphabet_set.issubset(sentence_set)


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
        sentence = "the five boxing wizards jump quickly"
        self.assertTrue(is_pangram(sentence), "The sentence should be a pangram even with repeated letters")



# Run the tests
if __name__ == '__main__':
    unittest.main()