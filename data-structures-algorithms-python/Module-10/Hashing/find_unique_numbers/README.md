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

Let's break down the function step-by-step with a visual diagram to illustrate the process of finding the unique numbers in the array.

### Step 1: Convert List to Set
**Code:**
```python
nums_set = set(nums)
```
**Description:**
- Convert the input list `nums` to a set `nums_set`. This allows for O(1) average time complexity for membership checks.

**Example:**
- Input `nums`: [1, 2, 3, 5, 7, 8, 10]
- Converted to `nums_set`: {1, 2, 3, 5, 7, 8, 10}

**Diagram:**
```
nums -> [1, 2, 3, 5, 7, 8, 10]
        ↓
nums_set -> {1, 2, 3, 5, 7, 8, 10}
```

### Step 2: Initialize Result List
**Code:**
```python
unique_numbers = []
```
**Description:**
- Create an empty list `unique_numbers` to store the result.

**Diagram:**
```
unique_numbers -> []
```

### Step 3: Iterate Through the Set
**Code:**
```python
for num in nums_set:
```
**Description:**
- Iterate through each number in the set `nums_set`.

**Example:**
- Iteration over {1, 2, 3, 5, 7, 8, 10}

**Diagram:**
```
nums_set -> {1, 2, 3, 5, 7, 8, 10}
              ↑
             num
```

### Step 4: Check Conditions
**Code:**
```python
if (num - 1) not in nums_set and (num + 1) not in nums_set:
```
**Description:**
- For each `num`, check if both `num - 1` and `num + 1` are not in `nums_set`.

**Example:**
- For `num = 5`: Check if 4 and 6 are not in `nums_set`.

**Diagram:**
```
num = 5
Check: 4 ∉ {1, 2, 3, 5, 7, 8, 10}
       6 ∉ {1, 2, 3, 5, 7, 8, 10}
Result: True
```

### Step 5: Append to Result List
**Code:**
```python
unique_numbers.append(num)
```
**Description:**
- If the conditions are met, append `num` to the `unique_numbers` list.

**Example:**
- If `num = 5` meets the conditions, add it to `unique_numbers`.

**Diagram:**
```
unique_numbers -> [5]
```

### Step 6: Return Result
**Code:**
```python
return unique_numbers
```
**Description:**
- Return the list of unique numbers.

**Example:**
- Final `unique_numbers`: [5, 10]

**Diagram:**
```
unique_numbers -> [5, 10]
```

### Complete Example:
1. Input `nums`: [1, 2, 3, 5, 7, 8, 10]
2. Convert to set: `{1, 2, 3, 5, 7, 8, 10}`
3. Iterate and check conditions:
   - For `num = 1`: Check if 0 and 2 are in set. (Condition not met)
   - For `num = 2`: Check if 1 and 3 are in set. (Condition not met)
   - For `num = 3`: Check if 2 and 4 are in set. (Condition not met)
   - For `num = 5`: Check if 4 and 6 are in set. (Condition met)
   - For `num = 7`: Check if 6 and 8 are in set. (Condition not met)
   - For `num = 8`: Check if 7 and 9 are in set. (Condition not met)
   - For `num = 10`: Check if 9 and 11 are in set. (Condition met)
4. Append numbers meeting conditions to `unique_numbers`: [5, 10]
5. Return result: [5, 10]

### Visual Diagram Summary:
```
nums -> [1, 2, 3, 5, 7, 8, 10]
        ↓
nums_set -> {1, 2, 3, 5, 7, 8, 10}
unique_numbers -> []

Iterate nums_set:
  1: Check 0 ∉ {1, 2, 3, 5, 7, 8, 10}, 2 ∉ {1, 2, 3, 5, 7, 8, 10} -> Not met
  2: Check 1 ∉ {1, 2, 3, 5, 7, 8, 10}, 3 ∉ {1, 2, 3, 5, 7, 8, 10} -> Not met
  3: Check 2 ∉ {1, 2, 3, 5, 7, 8, 10}, 4 ∉ {1, 2, 3, 5, 7, 8, 10} -> Not met
  5: Check 4 ∉ {1, 2, 3, 5, 7, 8, 10}, 6 ∉ {1, 2, 3, 5, 7, 8, 10} -> Met
     unique_numbers -> [5]
  7: Check 6 ∉ {1, 2, 3, 5, 7, 8, 10}, 8 ∉ {1, 2, 3, 5, 7, 8, 10} -> Not met
  8: Check 7 ∉ {1, 2, 3, 5, 7, 8, 10}, 9 ∉ {1, 2, 3, 5, 7, 8, 10} -> Not met
 10: Check 9 ∉ {1, 2, 3, 5, 7, 8, 10}, 11 ∉ {1, 2, 3, 5, 7, 8, 10} -> Met
     unique_numbers -> [5, 10]

Return unique_numbers -> [5, 10]
```

Sure, here are some unit test cases for the `find_unique_numbers` function. These tests cover a variety of scenarios to ensure the function works correctly.

```python
import unittest

# Function to be tested
def find_unique_numbers(nums):
    nums_set = set(nums)
    unique_numbers = []
    for num in nums_set:
        if (num - 1) not in nums_set and (num + 1) not in nums_set:
            unique_numbers.append(num)
    return unique_numbers

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
```

### Explanation of Test Cases:

1. **test_all_unique**: Tests the function with a list where all elements are unique as per the conditions.
2. **test_no_unique**: Tests the function with a list where no element meets the unique condition.
3. **test_some_unique**: Tests the function with a list where some elements meet the unique condition.
4. **test_duplicates**: Tests the function with a list containing duplicate elements.
5. **test_single_element**: Tests the function with a list containing a single element.
6. **test_empty_list**: Tests the function with an empty list.
7. **test_negative_numbers**: Tests the function with a list containing negative numbers.
8. **test_mixed_numbers**: Tests the function with a list containing a mix of negative, zero, and positive numbers.

These tests should cover the common scenarios and edge cases for the `find_unique_numbers` function.
