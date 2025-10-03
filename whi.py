print("Welcome to California Lottery")
x= int(input("enter your birth year: "))

while 2025 - x >= 18:
    print("Congrats you are eligible to play the lottery")
    break
else:
    print("opps! you're not eligible to play the lottery")