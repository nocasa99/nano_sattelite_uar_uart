# class Student:
#     def __init__(self, name, Id):
#         self.name = name          #instance
#         self.__Id = Id            #instance

#     def info(self):
#         print("Name:" , self.name, "Id:" , self.__Id)
    
#     def set_ID(self, Id):
#         if(Id>0):
#             self.__Id = Id
#         else:
#             print("Invalid ID. Please Enter Again.")

#     def get_ID(self):
#         return self.__Id
    
#     def set_name(self, name):
#          self.name = name 

#     def get_name(self):
#         return self.name
# #=================================================================================

# st1 = Student("Tawhid", 333)
# st2 = Student("Tusher", 65)


# st1.set_ID(88)
# print(st1.get_ID())

# st2.set_ID(9882)
# print(st2.get_ID())

# st1.set_name("Sakib")
# print(st1.get_name())


# #st1.update_ID(999)
# st1.info()
# st2.info()
# #print(st1.__dict__)


# class ABC:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def details(self):
#         print("X:", self.x, "Y:", self.y )

# #=================================================================================================================================

# a1 = ABC(5,6)
# a2 = ABC(55,66)

# a1.details()
# a2.details()

# class Player:
#     team_run = 0                #static or class variable 

#     def __init__(self, run):
#         self.run = run          #instance variable
         
#     def hit_four(self):
#         self.run += 4
#         Player.team_run += 4
#     def hit_six(self):
#         self.run += 6
#         Player.team_run += 6
# #==============================================================================================================

# #print(Player.team_run)

# sakib = Player(0)
# tamim = Player(0)
# tamim.hit_four()
# tamim.hit_four()
# sakib.hit_six()
# tamim.hit_six()
# tamim.hit_six()
# sakib.hit_six()
# sakib.hit_four()

# print("Sakib:", sakib.run)
# print("Tamim:", tamim.run)
# print("Team Run:", Player.team_run)
# # print("Tamim", tamim.__dict__)
# # print("Sakib", sakib.__dict__)



# class Student:
#     uni_name = "EWU"

#     def __init__(self, name, id):
#         self.name = name
#         self.id = id  
#     def details(self):
#         print("Name: ", self.name, "ID: ", self.id, Student.uni_name)
#     @classmethod
#     def up_uni_name(cls, u_name):
#         cls.uni_name = u_name
#     # @classmethod
#     # def from_string(cls, info):
#     #     name, id = info.split('-')
#     #     obj =cls(name, id)
#     #     return obj 
#     @staticmethod
#     def check_department(id):
#         if id[5:7] == "60":
#             print("CSE")
#         elif id[5:7] == "10":
#             print("BBA")
# #=======================================================================================================================================================
# st1 = Student("Tawhid", 223)
# st2 = Student("Priyo", 224)
# st1.details()
# st2.details()
# Student.check_department("2022260133")

# # Student.up_uni_name("East West University")
# # st1.details()
# # st2.details()
# # st1.details()
# # st2.details()
# Student.check_department("2023160133")

# #Single Inheritance
# class Animal:
#     def __init__(self, name):
#         self.name = name 
#     def eat(self):
#         print(self.name, "is eating")
# #=================================================================
# class Dog(Animal):
#     def bark(self):
#         print(self.name, "is barking")
# #=======================================================================
# a1 = Animal("Tommy")
# d1 = Dog("Jack")
# d1.bark()
# d1.eat()
# a1.eat()
# print(isinstance(d1,Dog))
# print(issubclass(Animal, Dog))

#Hierarchical Inheritance
class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id 
    def details(self):
        print("Name: ", self.name, "ID: ", self.id)

#======================================================================================================================
class CSEStudent(Student):
    def __init__(self, name, id, labs):
        super().__init__(name, id)  
        self.no_of_labs = labs
    def cry(self):
        print("CSE student is crying because of",
              self.no_of_labs, "labs")
#===============================================================================================================================
class BBAStudent(Student):
    def __init__(self, name, id):
        self.name = name
        self.id = id 
    def party(self):
        print("All day Party")
#=============================================================================================
s1 = CSEStudent("Priyo", 133, 2)
s2 = BBAStudent("Sakib", 12)
print(s1.__dict__)
print(s2.__dict__)
s1.details()
s2.details()
s1.cry()
s2.party()
        
        