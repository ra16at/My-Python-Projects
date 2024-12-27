start,end = map(int,input("\t<----- Welcome to Leap Year Finder ----->\nEnter your staring and ending year (e.g: 1900,2400)\n=> ").split(","))

while start <= end:
    if (start % 4 == 0 and start % 100 != 0) or start % 400 == 0:
        print(start)
    start += 1