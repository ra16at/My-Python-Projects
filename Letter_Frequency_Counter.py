user_word = input("Enter a word: ")
target_letter = input("Enter the counter letter: ")
counter = 0
words = user_word.split(" ")

''' This loop will iterate through each word
    in the list of words and count the number
    of times the target letter appears in the word. '''
for word in words:
    counter += word.count(target_letter)

# Output the results
print("The letter", target_letter, "appears", counter, "times in the words", user_word)
