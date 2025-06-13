# Prompt user for a number
num = int(input("Enter a number: "))

# Prompt user for a potential factor
factor_of = int(input("Enter a potential factor: "))

def check_factor(num, factor_of):
    """
    Checks if 'factor_of' is a factor of 'num'.
    If not, prompts the user to enter a new number until it is.
    """
    while num % factor_of != 0:
        print("Try again")
        num = int(input("Enter a number: "))
    else:
        print("%d is a factor of %d" % (factor_of, num))

# Call the function
check_factor(num, factor_of)