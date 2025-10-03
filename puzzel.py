code = int(input("Enter a number: "))

if code < 0:
    print("invalid")
elif code % 4 == 0 and code % 6 == 0:
    print("Open Sesame")
elif code % 4 == 0:
    print("North Gate")
elif code % 6 == 0:
    print("East Gate")
elif code % 2 != 0 and code % 5 == 0:
    print("secret tunnel")
elif code % 10 ==7:
    print("lucky seven")
else:
    print("access denied")