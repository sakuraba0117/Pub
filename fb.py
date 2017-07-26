f='fizz'
b='buzz'
fb=f+b

for i in range(1,100):
    if(i%3==0 and i%5==0):
        print("内定ください!")
    elif(i%3==0):
        print("御社")
    elif(i%5==0):
        print("弊社")
    else:
        print(i)
