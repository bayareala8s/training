def two_sum(nums, target):
    # Initialize dictionary to store numbers and their indices
    num_to_index = {}

    # Iterate over the array
    for i, num in enumerate(nums):
        # Calculate the complement
        complement = target - num

        # Check if complement exists in the dictionary
        if complement in num_to_index:
            # If found, return the indices
            return [num_to_index[complement], i]

        # Otherwise, store the current number and its index
        num_to_index[num] = i

    # If no solution found, return an empty list (though the problem guarantees a solution)
    return []


# Example usage
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))  # Output: [0, 1]

import unittest

class TestTwoSum(unittest.TestCase):
    def test_basic_case(self):
        nums = [2, 7, 11, 15]
        target = 9
        self.assertEqual(two_sum(nums, target), [0, 1])

    def test_multiple_pairs(self):
        nums = [1, 2, 3, 4, 5]
        target = 6
        result = two_sum(nums, target)
        self.assertTrue(result in [[1, 3], [0, 4]])

    def test_negative_numbers(self):
        nums = [-1, -2, -3, -4, -5]
        target = -8
        self.assertEqual(two_sum(nums, target), [2, 4])

    def test_no_solution(self):
        nums = [1, 2, 3, 4, 5]
        target = 10
        self.assertEqual(two_sum(nums, target), [])

    def test_same_element_twice(self):
        nums = [3, 3]
        target = 6
        self.assertEqual(two_sum(nums, target), [0, 1])

    def test_large_numbers(self):
        nums = [1000000, 500000, -1500000, 2000000]
        target = 500000
        self.assertEqual(two_sum(nums, target), [2, 3])

    def test_single_element(self):
        nums = [1]
        target = 2
        self.assertEqual(two_sum(nums, target), [])

    def test_empty_array(self):
        nums = []
        target = 0
        self.assertEqual(two_sum(nums, target), [])

if __name__ == '__main__':
    unittest.main()