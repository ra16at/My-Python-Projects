def find_factors(num):
  return [i for i in range(1, num + 1) if num % i == 0]

# Get input from the user
number = int(input(">>> "))

# Find the factors using list comprehension
all_factors = find_factors(number)

# Print the factors
print("Factors of", number, "are:", all_factors)
