import time

if (time.localtime().tm_hour >= 9 and time.localtime().tm_hour < 17):
    print("Working hours")
elif (time.localtime().tm_hour >= 17 and time.localtime().tm_hour < 21):
    print("Evening hours")
else:
    print("Off hours") 

