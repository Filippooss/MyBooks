class MyClass:
    class_var = "I'm a class variable"

    def __init__(self, name):
        self.instance_var = name  # Instance variable

obj1 = MyClass("Alice")
obj2 = MyClass("Bob")

print(obj1.instance_var)  # Alice (specific to obj1)
print(obj2.instance_var)  # Bob (specific to obj2)

print(MyClass.class_var)  # Accessible via class