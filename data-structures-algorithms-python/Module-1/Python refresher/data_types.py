

#Numeric Types
# int
num_shares = 150
# float
price_per_share = 23.45
# complex
complex_interest = 1.05 + 0.01j

# Calculate total investment
total_investment = num_shares * price_per_share
print(f"Total Investment: ${total_investment}")

# Using complex numbers to calculate compound interest
future_value = complex_interest ** 2
print(f"Future Value with complex interest: {future_value}")

#Sequence Types
# list
shopping_cart = ["apple", "banana", "milk", "bread"]
shopping_cart.append("eggs")
print(f"Shopping Cart: {shopping_cart}")

# tuple
cart_item = ("apple", 2, 1.50)  # item name, quantity, price per item
print(f"Cart Item: {cart_item}")

# range
for i in range(1, 6):
    print(f"Item {i}")

#Text Type
user_name = "Alice"
greeting = f"Hello, {user_name}! Welcome to our store."
print(greeting)

#Mapping Type
customer_data = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}
print(f"Customer Name: {customer_data['name']}")
print(f"Customer Email: {customer_data['email']}")

#Set Types
# set
product_categories = {"electronics", "clothing", "groceries", "electronics"}
print(f"Unique Categories: {product_categories}")

# frozenset
immutable_categories = frozenset(product_categories)
print(f"Immutable Categories: {immutable_categories}")

#Boolean Type
in_stock = True
if in_stock:
    print("The product is available for purchase.")
else:
    print("The product is currently out of stock.")

#Binary Types
# bytes
byte_data = b"This is some byte data."
print(byte_data)

# bytearray
mutable_byte_data = bytearray(byte_data)
mutable_byte_data[0] = 84  # Changing 'T' to 't'
print(mutable_byte_data)

# memoryview
mem_view = memoryview(byte_data)
print(mem_view[0])  # Accessing the first byte

#Real-World Examples Combining Multiple Data Types
# Inventory with item name, quantity, and price
inventory = {
    "apple": {"quantity": 50, "price": 0.50},
    "banana": {"quantity": 30, "price": 0.30},
    "milk": {"quantity": 20, "price": 1.20},
}

# Checking and updating stock
item = "apple"
if inventory[item]["quantity"] > 0:
    print(f"{item} is in stock.")
    # Sell 5 apples
    inventory[item]["quantity"] -= 5
    print(f"New quantity of {item}: {inventory[item]['quantity']}")
else:
    print(f"{item} is out of stock.")


#User Registration System
# User information
users = []

# Register a new user
new_user = {
    "username": "johndoe",
    "password": "securepassword123",
    "email": "johndoe@example.com",
    "age": 25,
    "is_active": True
}

# Add new user to the users list
users.append(new_user)

# Display user information
for user in users:
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Active: {user['is_active']}")