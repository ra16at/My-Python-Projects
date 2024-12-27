# Description: This program will print a number pyramid based on the user input.
num = int(input("Enter the number of rows: "))
i = 1
while i <= num:
    j = 1
    while j <= i:
        print(i, end="")  # Print the number i instead of j
        j += 1
    print()  # Move to the next line after printing each row
    i += 1