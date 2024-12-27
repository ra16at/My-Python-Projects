num = int(input("=> "))
factor_of = int(input("[Factor of] => "))

def factoral(num, factor_of):
    while num % factor_of != 0:
        print("Try again")
        num = int(input("=> "))
    else:
        print("%d is a factor of %d" % (factor_of, num))

factoral(num, factor_of)