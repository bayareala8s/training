#Example: A Simple E-commerce Discount System

# Define the total amount of purchase
total_amount = 150

# Apply discount based on the amount
if total_amount > 200:
    discount = 20  # 20% discount
elif total_amount > 100:
    discount = 10  # 10% discount
else:
    discount = 0   # No discount

# Calculate the final amount after discount
final_amount = total_amount - (total_amount * discount / 100)

print(f"Total Amount: ${total_amount}")
print(f"Discount Applied: {discount}%")
print(f"Final Amount to Pay: ${final_amount}")

#Using a for Loop for a To-Do List Application

# Define a list of tasks
tasks = ["Send email to client", "Submit report", "Prepare presentation"]

# Iterate through the list and print each task
for task in tasks:
    print(f"Task: {task}")


#Using a while Loop for a Number Guessing Game
import random

# Generate a random number between 1 and 10
target_number = random.randint(1, 10)
attempts = 0

# Loop until the user guesses the correct number
while True:
    guess = int(input("Guess the number between 1 and 10: "))
    attempts += 1
    if guess < target_number:
        print("Too low! Try again.")
    elif guess > target_number:
        print("Too high! Try again.")
    else:
        print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
        break

#Using a while Loop for a Feedback Collection System

# Initialize variables to store total rating and number of feedbacks
total_rating = 0
feedback_count = 0

# Define a list of valid ratings
valid_ratings = [1, 2, 3, 4, 5]

# Loop to collect feedback from multiple customers
while True:
    rating = int(input("Please rate our service (1-5): "))
    if rating in valid_ratings:
        total_rating += rating
        feedback_count += 1
    else:
        print("Invalid rating. Please enter a rating between 1 and 5.")

    # Ask if there are more customers
    more_customers = input("Are there more customers to rate? (yes/no): ").lower()
    if more_customers != "yes":
        break

# Calculate the average rating
if feedback_count > 0:
    average_rating = total_rating / feedback_count
    print(f"Total feedbacks: {feedback_count}")
    print(f"Average Rating: {average_rating:.2f}")
else:
    print("No feedbacks received.")


#Using a for Loop for Calculating Average Grades

# List of student grades
grades = [85, 92, 78, 90, 88]

# Initialize total to 0
total = 0

# Iterate through the grades list
for grade in grades:
    total += grade

# Calculate average
average = total / len(grades)

print(f"The average grade is {average:.2f}")



#Using a while Loop for a Simple ATM Withdrawal Simulation
# Initial balance
balance = 500

# Loop until balance is zero
while balance > 0:
    # Prompt user for withdrawal amount
    withdrawal = int(input("Enter the amount to withdraw: "))

    if withdrawal > balance:
        print("Insufficient balance! Try a smaller amount.")
    else:
        balance -= withdrawal
        print(f"Withdrawal successful! Remaining balance: ${balance}")

    if balance == 0:
        print("Your account balance is zero. No further withdrawals possible.")
        break

#Using a for Loop with a Break Statement to Find the First Even Number in a List
# List of numbers
numbers = [1, 3, 7, 9, 12, 15]

# Loop through the list
for number in numbers:
    if number % 2 == 0:
        print(f"First even number found: {number}")
        break

#Using a for Loop with a Continue Statement to Skip Negative Numbers in a List
# List of integers
numbers = [5, -3, 8, -1, 12, -7, 9]

# Loop through the list
for number in numbers:
    if number < 0:
        continue
    print(f"Processing number: {number}")

#Using a for Loop with a Pass Statement to Skip a Task
# List of tasks
tasks = ["task1", "task2", "task3"]

# Loop through tasks
for task in tasks:
    if task == "task2":
        pass  # Placeholder for future code
    else:
        print(f"Executing {task}")

#Inventory Management System Using a While Loop
# Sample inventory
inventory = {
    "apple": 10,
    "banana": 5,
    "orange": 8
}

# Main loop to manage inventory
while True:
    print("\nCurrent Inventory:")
    for item, quantity in inventory.items():
        print(f"{item}: {quantity}")

    action = input("Enter action (add/remove/check/exit): ").lower()

    if action == "exit":
        print("Exiting the inventory management system.")
        break

    elif action == "add":
        item = input("Enter the item to add: ").lower()
        quantity = int(input(f"Enter the quantity of {item} to add: "))
        if item in inventory:
            inventory[item] += quantity
        else:
            inventory[item] = quantity
        print(f"Added {quantity} of {item}.")

    elif action == "remove":
        item = input("Enter the item to remove: ").lower()
        if item in inventory:
            quantity = int(input(f"Enter the quantity of {item} to remove: "))
            if quantity > inventory[item]:
                print("Insufficient quantity to remove.")
            else:
                inventory[item] -= quantity
                print(f"Removed {quantity} of {item}.")
        else:
            print(f"{item} not found in inventory.")

    elif action == "check":
        item = input("Enter the item to check: ").lower()
        if item in inventory:
            print(f"{item}: {inventory[item]}")
        else:
            print(f"{item} not found in inventory.")

    else:
        print("Invalid action. Please try again.")

#Sending Emails to Multiple Recipients Using a for Loop
emails = ["alice@example.com", "bob@example.com", "charlie@example.com"]

for email in emails:
    print(f"Sending email to {email}")

#Iterating Over a List of Tuples Using a for Loop
coordinates = [(1, 2), (3, 4), (5, 6)]

for x, y in coordinates:
    print(f"Coordinate: x={x}, y={y}")

#Iterating Over a Dictionary Using a for Loop
inventory = {"apple": 10, "banana": 5, "orange": 8}

for item, quantity in inventory.items():
    print(f"Item: {item}, Quantity: {quantity}")

#Counting the Number of Vowels in a Text Using a for Loop
text = "Hello, World!"
vowels = "aeiouAEIOU"
vowel_count = 0

for char in text:
    if char in vowels:
        vowel_count += 1

print(f"Number of vowels: {vowel_count}")

#Iterating Over a Set Using a for Loop
unique_ids = {101, 102, 103, 104}

for uid in unique_ids:
    print(f"Verifying ID: {uid}")

#Using a for Loop with the range() Function
for i in range(10):
    print(f"Number: {i}")

#Nested for Loops to Generate Multiplication Tables
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i} x {j} = {i * j}")
    print("-----")

#Using a List Comprehension to Generate Squares of Numbers
squares = [x ** 2 for x in range(1, 6)]
print(squares)

items = ["apple", "banana", "cherry"]

# Using enumerate to get both index and item
for index, item in enumerate(items):
    print(f"Index: {index}, Item: {item}")

# Using zip to iterate over two lists simultaneously
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"Name: {name}, Score: {score}")

#Analyzing Sales Data Using a Dictionary and for Loop
# Sales data for each region
sales_data = {
    "North": [1200, 1300, 1150, 1400],
    "South": [1000, 950, 1050, 1100],
    "East": [1150, 1250, 1200, 1300],
    "West": [1300, 1350, 1400, 1450]
}

# Initialize total sales
total_sales = 0
region_count = 0

# Iterate over each region and their sales
for region, sales in sales_data.items():
    print(f"Region: {region}")

    # Calculate total sales for the region
    region_total = sum(sales)
    total_sales += region_total
    region_count += 1

    # Calculate average sales for the region
    region_average = region_total / len(sales)

    print(f"Total Sales: {region_total}")
    print(f"Average Sales: {region_average:.2f}\n")

# Calculate overall average sales
overall_average = total_sales / region_count
print(f"Overall Total Sales: {total_sales}")
print(f"Overall Average Sales: {overall_average:.2f}")

#Basic for Loop with range() Function
for i in range(10):
    print(i)

#Using range() Function with Start and End Values
for i in range(5, 15):
    print(i)

#Using range() Function with Start, End, and Step Values
for i in range(0, 20, 2):
    print(i)

#Reverse Iteration with range() Function
for i in range(10, 0, -1):
    print(i)


#Using a for Loop to Generate Employee IDs
employee_count = 5
employee_ids = []

for i in range(1, employee_count + 1):
    employee_ids.append(f"EMP{i:03}")

print(employee_ids)

#Creating a Multiplication Table Using a for Loop
number = 7
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")

#Simulating a Simple Voting System
candidates = ["Alice", "Bob", "Charlie"]
votes = [0] * len(candidates)

# Simulate voting
num_voters = 10

for i in range(num_voters):
    vote = int(input(f"Voter {i + 1}, vote for (0: Alice, 1: Bob, 2: Charlie): "))
    if 0 <= vote < len(candidates):
        votes[vote] += 1
    else:
        print("Invalid vote.")

# Display voting results
for i in range(len(candidates)):
    print(f"{candidates[i]}: {votes[i]} votes")

#Generating First N Fibonacci Numbers
n = 10
fib_series = [0, 1]

for i in range(2, n):
    next_number = fib_series[-1] + fib_series[-2]
    fib_series.append(next_number)

print(f"First {n} Fibonacci numbers: {fib_series}")

#Processing Multiple Files
import os

files = ["report1.txt", "report2.txt", "report3.txt"]

for i in range(len(files)):
    new_name = f"renamed_report_{i + 1}.txt"
    os.rename(files[i], new_name)
    print(f"Renamed {files[i]} to {new_name}")


#Generating Random Test Scores for Students
import random

num_students = 5
test_scores = []

for i in range(num_students):
    score = random.randint(50, 100)
    test_scores.append(score)

print(f"Generated test scores: {test_scores}")

#Analyzing Temperature Data
temperatures = [70, 72, 68, 65, 74, 73, 71]

total_temp = 0

for temp in range(len(temperatures)):
    total_temp += temperatures[temp]

average_temp = total_temp / len(temperatures)
print(f"The average temperature over the week is {average_temp:.2f}°F")