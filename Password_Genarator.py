import random
import string

''' First, we import the random and string modules.
 Then, we ask the user to enter the length of the password.
 We store the length in a variable pass_length.
 We define a function password_generator that takes the length of the password as an argument.
 We define a variable characters that contains all the characters that we want to use in the password.
 We use the random.choices() method to generate a password of the given length.
 Finally, we return the password. '''

def password_generator(length=pass_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password
pass_length = int(input("Enter the length: "))

print(password_generator(pass_length))