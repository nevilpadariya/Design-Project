def check_higher(a, b):
    if a > b:
        print(a, "is greater than", b)
    elif a < b:
        print(a, "is less than", b)
    else:
        print(a, "is equal to", b)

x = int(input("Enter first number: "))
y = int(input("Enter second number: "))
check_higher(x, y) 

c = int(input("enter 1st no."))
d = int(input("enter 2nd no."))
check_higher(c, d)