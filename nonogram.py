#comment
'''
multi
line 
comment
'''
x = 5
y = "hello y"
v = 'hello v'   #same
print(type(x))
x=5.6
print(type(x))
z = float(3)    #declaration is not needed
print(z)
print(type(z))

if x>2:
    print("hello if")
    print(y)
x=y=z = 5
print(x,y,z)
x,y,z = 2,4,"orange"
print(x,y,z)

fruit = ["apple", "banana", "cherry"]
x,y,z = fruit
print(x,y,z)