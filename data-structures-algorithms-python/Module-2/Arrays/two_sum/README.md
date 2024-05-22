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
