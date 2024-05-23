def find_unique_numbers(nums):
    # Convert the list to a set for O(1) average time complexity checks.
    nums_set = set(nums)

    # Initialize an empty list to store the result.
    unique_numbers = []

    # Iterate through each number in the set to avoid duplicates.
    for num in nums_set:
        # Check if both (num - 1) and (num + 1) are not in the set.
        if (num - 1) not in nums_set and (num + 1) not in nums_set:
            # If both conditions are met, append the number to the result list.
            unique_numbers.append(num)

    # Return the list of unique numbers.
    return unique_numbers


# Example usage:
nums = [1, 2, 3, 5, 7, 8, 10]
result = find_unique_numbers(nums)
print(result)  # Output will be [5, 10]

import unittest


# Unit Test Class
class TestFindUniqueNumbers(unittest.TestCase):

    def test_all_unique(self):
        nums = [10, 12, 14]
        expected = [10, 12, 14]
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_no_unique(self):
        nums = [1, 2, 3, 4, 5]
        expected = []
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_some_unique(self):
        nums = [1, 2, 3, 5, 7, 8, 10]
        expected = [5, 10]
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_duplicates(self):
        nums = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
        expected = []
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_single_element(self):
        nums = [1]
        expected = [1]
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_empty_list(self):
        nums = []
        expected = []
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_negative_numbers(self):
        nums = [-3, -2, -1, 0, 1, 2, 4]
        expected = [4]
        self.assertEqual(find_unique_numbers(nums), expected)

    def test_mixed_numbers(self):
        nums = [-1, 0, 1, 3, 5, 7, 9, 11, 13]
        expected = [3, 5, 7, 9, 11, 13]
        self.assertEqual(find_unique_numbers(nums), expected)


# Run the tests
if __name__ == '__main__':
    unittest.main()