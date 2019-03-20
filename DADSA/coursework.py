import csv
import os
days =0

class Warehouse():

    def __init__(self,name=None,insurance=None):
        self.insurance = insurance
        self.name = name
        self.items =[]
        self.shapes = []

    def add_item(self,item):       
           balance = self.check_insurance(item.price)
           if balance == True:
                support_shape = self.support_item_shape(item)
                if support_shape  == True:
                    self.items.append(item)
                    self.insurance-=item.price
                    print("Item {} added to warehouse {}".format(item.number,self.name))
                    return True
                else:
                    return False
           print("Not enough insurance for item {} for warehouse {}"
                 .format(item.number,self.name))
           return False

    def support_item_shape(self,item):
        for i in range(0,len(self.shapes)):
            if self.shapes[i][0] == item.shape:
                if item.weight <= self.shapes[i][2]:
                    if self.shapes[i][1] > 0:
                        self.shapes[i] = (self.shapes[i][0],self.shapes[i][1]-1,self.shapes[i][2])
                        return True
                    print("Insufficient {} shape quantity for warehouse {}"
                          .format(self.shapes[i][0],self.name))
                    return False
                print("Item {} too heavy for warehouse {}".format(item.number,self.name))
                return False
        print("Warehouse {} cannot support {} item {}"
              .format(self.name,item.shape,item.number))
        return False
     
      
    def check_insurance(self,price):
        if price < self.insurance:
            return True
    
    def before_van_check(self,item):
        balance = self.check_insurance(item.price)
        if balance == True:
                support_shape = self.support_item_shape(item)
                if support_shape  == True:
                   return True

        return False

    def __repr__(self):
        return '{} {}'.format(self.name,self.insurance)

class Item():

    def __init__(self,number=None,description=None,price=None,shape=None,weight=None):
        self.number = number
        self.description = description
        self.price = price
        self.shape = shape
        self.weight = weight
   
    def __repr__(self):
        return "{} {} {} {} {}".format(self.number,self.description,self.price,
                                         self.shape,self.weight)

class Van():

    def __init__(self,capacity=None,insurance=None):
        self.capacity = capacity
        self.insurance = insurance
        self.items =[]
    
    def add_item(self,item,toW):
        if item.price > self.insurance:
            print("Item {} rejected insurance is greater than van insurance"
                  .format(item.price))
        elif item.weight > self.capacity:
            print("Item {} rejected, capacity exceeds van capacity"
                  .format(item.weight))
        else:
            success = toW.before_van_check(item)
            if success == True:
                self.items.append(item)
            else:
                print("Item {} rejected destination warehouses {} cannot hold it"
                      .format(item.number,toW.name))

        
    def __repr__(self):
        return "{} {}".format(self.capacity,self.insurance)

def menu():
   
   task =0

   while task !=5:
       os.system("cls")
       print("1.Task 1")
       print("2.Task 2")
       task = getchoice(1,5)

       if task ==1:
          task1()
       elif task ==2:
          task2()



def addShape(A,B,C,D):

    Arectangle =("Rectangle",5,1000)
    Asquare = ("Square",5,2000)
    Apyramid =("Pyramid",10,2000)
    A.shapes.append(Arectangle)
    A.shapes.append(Asquare)
    A.shapes.append(Apyramid)

    Brectangle = ("Rectangle",10,500)
    Bpyramid =("Pyramid",10,250)
    Bsphere=("Sphere",5,2000)
    B.shapes.append(Brectangle)
    B.shapes.append(Bpyramid)
    B.shapes.append(Bsphere)

    Csphere=("Sphere",15,250)
    Cpyramid =("Pyramid",5,500)   
    C.shapes.append(Csphere)
    C.shapes.append(Cpyramid)

    Drectangle =("Rectangle",10,500)
    Dsquare = ("Square",10,750)
    Dpyramid =("Pyramid",2,3000)
    Dsphere=("Sphere",2,750)
    D.shapes.append(Drectangle)
    D.shapes.append(Dsquare)
    D.shapes.append(Dsphere)
    D.shapes.append(Dpyramid)

def readcsv(filename,warehouse):

     with open(filename) as csvFile:
                  reader = csv.reader(csvFile)
                  next(reader,None)
                  for number,description,price,shape,weight in reader:
                      number = int(number)
                      weight = int(weight)
                      price  = int(price)
                      item = Item(number,description,price,shape,weight)                                        
                      warehouse.add_item(item) 

def readtoA(filename,A,B,C,D):
    
    with open(filename) as csvFile:
                  reader = csv.reader(csvFile)
                  next(reader,None)
                  for number,description,price,shape,weight in reader:
                      added = False
                      number = int(number)
                      weight = int(weight)
                      price  = int(price)
                      item = Item(number,description,price,shape,weight)                      
                      added = A.add_item(item)
                      if added == False:
                         added = B.add_item(item)
                      if added == False:
                          added = C.add_item(item)
                      if added == False:
                          added = D.add_item(item)

def readcsvTask2(filename,datastored):

    with open(filename) as csvFile:
                  reader = csv.reader(csvFile)
                  next(reader,None)
                  for number,fromwarehouse,towarehouse in reader:
                      number = int(number)
                      route = (number,fromwarehouse,towarehouse)
                      datastored.append(route)

def task1():

    A = Warehouse("A",2000000000)
    B = Warehouse("B",2000000000)
    C = Warehouse("C",2000000000)
    D = Warehouse("D",2000000000)

    addShape(A,B,C,D)

    print("Warehouse A addings:\n")
    readcsv('Warehouse A.csv',A)
    print("\n")

    print("Warehouse B addings:\n")
    readcsv('Warehouse B.csv',B)
    print("\n")

    print("Warehouse C addings:\n")
    readcsv('Warehouse C.csv',C)
    print("\n")

    print("Warehouse D addings:\n")
    readcsv('Warehouse D.csv',D)
    print("\n")

    input("Press any key to continue")

    os.system("cls")
    print("\n\nLoad items through Warehouse A\n")
    readtoA('DATA TO INSERT INTO WAREHOUSE A.csv',A,B,C,D)
    input("Press any key to continue")

def task2():

    datastored =[]
    A = Warehouse("A",2000000000)
    B = Warehouse("B",2000000000)
    C = Warehouse("C",2000000000)
    D = Warehouse("D",2000000000)

    addShape(A,B,C,D)

    print("Warehouse A addings:\n")
    readcsv('Warehouse A.csv',A)
    print("\n")

    print("Warehouse B addings:\n")
    readcsv('Warehouse B.csv',B)
    print("\n")

    print("Warehouse C addings:\n")
    readcsv('Warehouse C.csv',C)
    print("\n")

    print("Warehouse D addings:\n")
    readcsv('Warehouse D.csv',D)
    print("\n")

    input("Press any key to continue")

    allwarehouses = []
    allwarehouses.append(A)
    allwarehouses.append(B)
    allwarehouses.append(C)
    allwarehouses.append(D)

    os.system("cls")
    readcsvTask2('TASK 2(1).csv',datastored)
    warehouses =['A','B','C','D']

    print("Task 2 choices")
    print("1.Part A")
    print("2.Part B")
    print("3.Exit")

    selection = getchoice(1,3)
    if selection ==1:
        task2A()
    elif selection ==2:




def task2A(datastored,allwarehouses):  
    
    warehouses =['A','B','C','D']
    for i in range(0,len(warehouses)-1):
        task2APlan(datastored,i,i+1,allwarehouses)

def task2APlan(datastored,fromW,toW,allwarehouses):
  
    warehouses =['A','B','C','D']
    for x in range(0,len(warehouses)):        
        van = Van(1500000000,2000)     
        for i in range(0,len(datastored)):
            if datastored[i][1]== warehouses[fromW] and datastored[i][2] == warehouses[toW]:                
                item = searchItem(allwarehouses[fromW],datastored[i][0])                                
                van.items.append(item)             
        deliverItems(van.items,allwarehouses[toW],warehouses[fromW])
        toW+=1
        if toW==4:
            break

def task2BPlan(datastored,fromW,toW,allwarehouses):
    
            
def deliverItems(trips,toW,fromW):

    if len(trips)>0:
        global days
        days+=1
        print("\nDays {}".format(days))
        for i in trips:
            print("Item {} added from {} to {}"
                  .format(i.number,fromW,toW.name))
            toW.items.append(i)

   
def searchItem(warehouse,itemNumber):

    for i in range(0,len(warehouse.items)):
        if warehouse.items[i].number == itemNumber:
            item = warehouse.items.pop(i)
            return item
  

def getchoice(min,max):
    incorrect = True
    while incorrect == True:
        try:
            choice = input("")
            if choice.isdigit():
                choice = int(choice)
        except:
            print("Incorrect choice,input correct choice: ")
        else:
            if choice >= min and choice <=max:
                return choice
            else:
                print("Incorrect choice,input correct choice: ")



menu()