To solve the problem of finding two indices in an array whose values add up to a given target, we'll use a hash map (or dictionary in Python) to track the indices of the elements we've seen so far. This approach allows us to find the solution in linear time, O(n).

### Steps and Visual Diagrams

Let's break down the solution step-by-step with visual diagrams:

1. **Initialization**:
   - We initialize an empty dictionary `num_to_index` to store the numbers we've seen so far and their indices.

2. **Iterate through the Array**:
   - For each element in the array `nums`, calculate the complement of the current element, which is `target - nums[i]`.
   - Check if the complement exists in `num_to_index`.
   - If it exists, return the indices of the complement and the current element.
   - Otherwise, store the current element and its index in `num_to_index`.

### Example
Given `nums = [2, 7, 11, 15]` and `target = 9`, we want to find two numbers that add up to `9`.

#### Step-by-Step Execution

1. **Initialization**:
   - `num_to_index = {}`

2. **First Iteration** (`i = 0`):
   - `current element = nums[0] = 2`
   - `complement = target - nums[0] = 9 - 2 = 7`
   - `7` is not in `num_to_index`.
   - Store `2` with index `0`: `num_to_index = {2: 0}`
   
   **Visual Diagram**:
   ```
   nums: [2, 7, 11, 15]
          ^
   num_to_index: {2: 0}
   ```

3. **Second Iteration** (`i = 1`):
   - `current element = nums[1] = 7`
   - `complement = target - nums[1] = 9 - 7 = 2`
   - `2` is in `num_to_index` with index `0`.
   - We found the pair: `nums[0] + nums[1] = 2 + 7 = 9`.
   - Return indices `[0, 1]`.

   **Visual Diagram**:
   ```
   nums: [2, 7, 11, 15]
             ^
   num_to_index: {2: 0}
   ```

### Python Code Implementation

```python
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
```

### Detailed Step-by-Step Diagrams

1. **Initialization**:
   ```
   num_to_index: {}
   ```

2. **First Iteration** (`i = 0`, `num = 2`):
   - `complement = 9 - 2 = 7`
   - `7` is not in `num_to_index`.
   - Update `num_to_index`:
   ```
   nums: [2, 7, 11, 15]
          ^
   num_to_index: {2: 0}
   ```

3. **Second Iteration** (`i = 1`, `num = 7`):
   - `complement = 9 - 7 = 2`
   - `2` is in `num_to_index` with index `0`.
   - Indices found: `[0, 1]`
   ```
   nums: [2, 7, 11, 15]
             ^
   num_to_index: {2: 0}
   ```

### Conclusion

By using a hash map, we efficiently solve the problem in O(n) time complexity, where n is the number of elements in the array. 
The visual diagrams help illustrate each step of the process, showing how we build and use the hash map to find the solution.

The space complexity of the provided solution to the "Two Sum" problem is O(n), where n is the number of elements in the input array `nums`. Here's a detailed explanation:

### Space Complexity Analysis

1. **Dictionary `num_to_index`**:
   - The dictionary `num_to_index` is used to store each element of the array and its corresponding index.
   - In the worst case, where no two elements sum up to the target until the last element is processed, all n elements of the array will be stored in the dictionary.
   - Therefore, the space required for the dictionary is O(n).

2. **Additional Variables**:
   - The function uses a few additional variables (`i`, `num`, `complement`) which all require constant space.
   - However, these do not depend on the input size and therefore contribute O(1) to the space complexity.

### Total Space Complexity

Combining the space required for the dictionary and the constant space for the additional variables, the total space complexity of the solution is:

\[ \text{Space Complexity} = O(n) \]

This means that the space used by the algorithm grows linearly with the size of the input array.

### Detailed Breakdown

1. **Input Array**: The space used by the input array `nums` is not considered part of the algorithm's space complexity because it is given as input.
2. **Dictionary**: Stores up to `n` key-value pairs, where `n` is the number of elements in `nums`.
3. **Variables**: A constant number of extra variables, which do not grow with the input size.

### Conclusion

The space complexity of the provided solution is O(n) due to the usage of the dictionary `num_to_index` to store the indices of the elements seen so far. This space complexity is optimal for this approach, as it allows us to achieve the desired O(n) time complexity for finding the two indices that sum up to the target.


Certainly! Here are unit test cases for the `two_sum` function using Python's built-in `unittest` framework. The test cases cover various scenarios, including positive cases, edge cases, and cases where no solution exists.

### Unit Test Cases

```python
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
```

### Explanation of Test Cases

1. **Basic Case**: 
   - Input: `nums = [2, 7, 11, 15]`, `target = 9`
   - Expected Output: `[0, 1]`
   - Explanation: The numbers at indices 0 and 1 add up to 9.

2. **Multiple Pairs**:
   - Input: `nums = [1, 2, 3, 4, 5]`, `target = 6`
   - Expected Output: One of `[[1, 3], [0, 4]]`
   - Explanation: Both pairs (2, 4) and (1, 5) add up to 6.

3. **Negative Numbers**:
   - Input: `nums = [-1, -2, -3, -4, -5]`, `target = -8`
   - Expected Output: `[2, 4]`
   - Explanation: The numbers at indices 2 and 4 add up to -8.

4. **No Solution**:
   - Input: `nums = [1, 2, 3, 4, 5]`, `target = 10`
   - Expected Output: `[]`
   - Explanation: No two numbers add up to 10.

5. **Same Element Twice**:
   - Input: `nums = [3, 3]`, `target = 6`
   - Expected Output: `[0, 1]`
   - Explanation: The same element at indices 0 and 1 add up to 6.

6. **Large Numbers**:
   - Input: `nums = [1000000, 500000, -1500000, 2000000]`, `target = 500000`
   - Expected Output: `[1, 2]`
   - Explanation: The numbers at indices 1 and 2 add up to 500000.

7. **Single Element**:
   - Input: `nums = [1]`, `target = 2`
   - Expected Output: `[]`
   - Explanation: There is only one element, so no pair exists.

8. **Empty Array**:
   - Input: `nums = []`, `target = 0`
   - Expected Output: `[]`
   - Explanation: The array is empty, so no pair exists.

### Running the Tests

To run these tests, save the code in a file named `test_two_sum.py` and execute the file using Python:

```bash
python test_two_sum.py
```

The `unittest` framework will run the tests and provide a report indicating whether the tests passed or failed. This approach ensures that the `two_sum` function is thoroughly tested for various input scenarios.
