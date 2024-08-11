# class Student :        #grandparent class
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id 
#     def details(self):
#         print("Name:", self.name, "ID:", self.id)
# #===================================================================================================================
# class CSEStudent(Student):  #parent class
#     def __init__(self, name, id, labs):
#         super().__init__(name, id)
#         self.no_of_labs = labs 
#     def cry(self):
#         print(self.name, "is crying because of", 
#               self.no_of_labs, "labs") 
# #=============================================================================================================================
# class CSEFresher(CSEStudent):   #child class
#     def enroll_CSE103(self):
#         print(self.name, "enrolled in CSE103")
# #=================================================================================================================
# st1 = CSEStudent("Emon",32, 3)
# st2 = CSEFresher("Nazrul", 55, 1)
# st1.details()
# st2.details()
# st1.cry()
# st2.cry()
# st2.enroll_CSE103()
# st1.enroll_CSE103()

# class A:
#     def __init__(self):
#         print("__init__ of class A")
#     def method1(self):
#         print("Method1 of class A")
# #==========================================================================================
# class B:
#     def __init__(self):
#         print("__init__ of class B")
#     def method1(self):
#         print("Method1 of class B")
# #======================================================================================================
# class C(A,B):
#     def __init__(self):
#         super.__init__()
#         print("__init__ of class C")
#     def method2(self):
#         print("Method2 of class C")
# #==============================================================================
# c1 = C()

# class Animal :
#     def __init__(self, name):
#         self.name = name 
#         self.color = "White"
#     def eat(self):
#         print(self.color, self.name, "is eating")
# #======================================================================================
# class Dog(Animal):
#     def __init__(self, name, color):
#         super().__init__(name)
#         self.color = color
#     def bark(self):
#         print(self.color, self.name, "is barking")
# #=========================================================================
# d1 = Dog("Rover", "Black")
# print(d1.__dict__)
# d1.bark()
# d1.eat()

class Student:
    def __init__(self, name, id):
        self.name = name
        self.id =id 
        print(self)
    def __str__(self):
        return "This is " + self.name
#===================================================================
st1 = Student("Bob", 11)
st2 = Student("Carol", 22)
# print(st1)
# print(st1.__str__())
# print(st2)
# print(st2.__str__())
