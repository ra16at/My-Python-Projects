# Description: This program will check if a number is prime or not.
num = int(input("Enter a number: "))
for i in range(2, num):
    if num % i == 0:
        print("Prime")
        break
    else:
        print("Not Prime")
        break
