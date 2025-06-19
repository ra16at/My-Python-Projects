def find_factors(num):
  factors = []                    # Initialize an empty list to store factors
  for i in range(1, num + 1):     # Iterate from 1 to num (inclusive)
      if num % i == 0:            # Check if i is a factor of num
          factors.append(i)       # Add i to the list if it is a factor
  return factors                  # Return the list of factors

# Get input from the user
number = int(input(">>> "))

# Find the factors using list comprehension
all_factors = find_factors(number)

# Print the factors
print("Factors of", number, "are:", all_factors)
