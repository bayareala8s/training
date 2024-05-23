Python function to find all the unique numbers in an integer array `nums` that satisfy the conditions `x + 1` is not in `nums` and `x - 1` is not in `nums`. I'll include detailed comments to explain each step of the code.

```python
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
```

### Explanation:

1. **Convert List to Set**:
   ```python
   nums_set = set(nums)
   ```
   - Converting the list `nums` to a set `nums_set` allows for O(1) average time complexity for membership checks. This step is crucial for efficiently checking if `num - 1` and `num + 1` are in the array.

2. **Initialize Result List**:
   ```python
   unique_numbers = []
   ```
   - This list will store the numbers that meet the given conditions.

3. **Iterate Through Set**:
   ```python
   for num in nums_set:
   ```
   - Loop through each number in the set to ensure each number is checked only once, avoiding duplicates.

4. **Check Conditions**:
   ```python
   if (num - 1) not in nums_set and (num + 1) not in nums_set:
   ```
   - For each `num`, check if both `num - 1` and `num + 1` are not present in `nums_set`. If this condition is true, `num` is a unique number as per the problem's definition.

5. **Append to Result List**:
   ```python
   unique_numbers.append(num)
   ```
   - If the conditions are satisfied, add `num` to the `unique_numbers` list.

6. **Return Result**:
   ```python
   return unique_numbers
   ```
   - Return the list of unique numbers.

### Example:
```python
nums = [1, 2, 3, 5, 7, 8, 10]
result = find_unique_numbers(nums)
print(result)  # Output will be [5, 10]
```
- In the example, the numbers 5 and 10 satisfy the conditions, as there are no numbers 4 or 6 for 5, and no numbers 9 or 11 for 10 in the array. Thus, the function returns `[5, 10]`.


### Time Complexity:

1. **Converting List to Set**:
   ```python
   nums_set = set(nums)
   ```
   - This operation takes O(n) time, where n is the number of elements in the list `nums`.

2. **Iterating Through the Set**:
   ```python
   for num in nums_set:
   ```
   - Iterating through each element in the set takes O(n) time because there are n unique elements (in the worst case, all elements are unique).

3. **Checking Conditions**:
   ```python
   if (num - 1) not in nums_set and (num + 1) not in nums_set:
   ```
   - Checking membership in a set takes O(1) time on average. Since this check is done for each of the n elements, the total time for these checks is O(n).

Overall, the time complexity of the function is:
\[ O(n) + O(n) = O(n) \]
Thus, the time complexity is **O(n)**.

### Space Complexity:

1. **Set Creation**:
   ```python
   nums_set = set(nums)
   ```
   - The set `nums_set` requires O(n) space to store n unique elements.

2. **Result List**:
   ```python
   unique_numbers = []
   ```
   - In the worst case, where all elements satisfy the conditions, the result list `unique_numbers` will also contain up to n elements, requiring O(n) space.

Thus, the space complexity is:
\[ O(n) + O(n) = O(n) \]
Therefore, the space complexity is **O(n)**.

### Summary:

- **Time Complexity**: O(n)
- **Space Complexity**: O(n)

The function is efficient in both time and space, operating linearly with respect to the size of the input list `nums`.
