# Number swapper using While loop
num = int(input("=> "))

# Print the number in reverse order
def num_swapper(num):
    while num > 0:
        ''' Print the last digit by using modulo operator 
        that divides the number by 10 and the remainder 
        is stored in the variable num. Then the "end" is
        used to print the number in the same line. '''
        print(num % 10, end="") 
        # Remove the last digit by using floor division
        num = num // 10

print(num_swapper(num))