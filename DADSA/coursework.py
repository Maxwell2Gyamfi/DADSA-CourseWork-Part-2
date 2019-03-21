import csv
import os
import copy
 
class Warehouse():

    #contructor
    def __init__(self,name=None,insurance=None):
        self.insurance = insurance
        self.name = name
        self.items =[]
        self.shapes = []
    
    
    ''' this function checks if an item can be added to the warehouse
        it checks for remaining insurance
        it checks if warehouse can support the shape
        it finally checks for the item weight and qauntity of specific item shape
        '''
    def add_item(self,item):       
           balance = self.check_insurance(item.price)#checks remaining insurance
           if balance == True:
                support_shape = self.support_item_shape(item)#checks for shape support
                if support_shape > -1:#checks for remaining quantity
                    self.items.append(item)
                    self.insurance-=item.price
                    self.shapes[support_shape] = (self.shapes[support_shape][0],self.shapes[support_shape][1]-1,self.shapes[support_shape][2])
                    print("Item {} added to warehouse {}".format(item.number,self.name))
                    return True
                else:
                    return False
           print("Not enough insurance for item {} for warehouse {}"
                 .format(item.number,self.name))
           return False

    '''this function checks if the warehouse can support specific item shapes
       it first checks for the item shape
       it then checks for item weight
       it finally checks for the remaining quantity
       it returns position of shape if supported otherwise it returns a negative index '''
    def support_item_shape(self,item):
        for i in range(0,len(self.shapes)):
            if self.shapes[i][0] == item.shape:#check item shape
                if item.weight <= self.shapes[i][2]:
                    if self.shapes[i][1] > 0:#checks quantity
                        return i 
                    else:                       
                        print("Item {} rejected ,insufficient {} shape quantity for warehouse {}"
                          .format(item.number,self.shapes[i][0],self.name))
                        return -1
                print("Item {} too heavy for warehouse {}".format(item.number,self.name))
                return -1
        print("Warehouse {} cannot support {} item {}"
              .format(self.name,item.shape,item.number))
        return -1
     

    '''checks if enough insurance for item to be added '''  
    def check_insurance(self,price):
        if price < self.insurance:
            return True

    '''this function checks if an item can board the van
       it prevents an item to be brought and sent back '''
    def before_van_check(self,item):
        balance = self.check_insurance(item.price) #checks insurance
        if balance == True:
                support_shape = self.support_item_shape(item)#checks shape type
                if support_shape > -1:
                   return True
                else:           
                    return -1  
        else:                 
            return -1

    ''' converts object to string '''   
    def __repr__(self):
        return '{} {}'.format(self.name,self.insurance)

class Item():
    #constructor
    def __init__(self,number=None,description=None,price=None,shape=None,weight=None):
        self.number = number
        self.description = description
        self.price = price
        self.shape = shape
        self.weight = weight

    ''' converts object to string '''   
    def __repr__(self):
        return "{} {} {} {} {}".format(self.number,self.description,self.price,
                                         self.shape,self.weight)

class Van():
    #constructor
    def __init__(self,capacity=None,insurance=None):
        self.capacity = capacity
        self.insurance = insurance
        self.items =[]
    
    '''adds item to van
       it checks for remaining insurance, capacity 
       it adds item if possible otherwise it rejects it displays error'''
    def add_item(self,item,toW):
        if item.price > self.insurance:#check insurance
            print("Item {} rejected item {} insurance is greater than van insurance"
                  .format(item.number,item.price))
            return False
        elif item.weight > self.capacity:#checks capacity
            print("Item {} rejected, capacity exceeds van capacity {}"
                  .format(item.weight,self.capacity))
            return False
        else:
            success = toW.before_van_check(item)#checks if warehouse can add item
            if success == True:
                print("Item {} added to van".format(item.number))
                self.items.append(item)
                self.capacity-=item.weight
                self.insurance-=item.price
                return True
            else:
                print("Van rejects item {} rejected destination warehouses {} cannot hold it"
                      .format(item.number,toW.name))
                return False      

    ''' converts object to string '''   
    def __repr__(self):
        return "{} {}".format(self.capacity,self.insurance)


'''this function contains the main menu of the program
   it first create warehoues objects, loads data from csv into them
   it then asks user for menu choice selection
   it repeats until user decide to quit '''

def menu():
   
   task =0
   #warehouses objects
   A = Warehouse("A",2000000000)
   B = Warehouse("B",2000000000)
   C = Warehouse("C",2000000000)
   D = Warehouse("D",2000000000)
   
   #adds shapes to warehouses
   addShape(A,B,C,D)
   #loads csv to warehouses
   initial_load(A,B,C,D)
   allwarehouses = copyWarehouses(A,B,C,D)
   
   #repeats while task not 3
   while task !=3:

       os.system("cls")
       print("\n\n            Menu\n")
       print("1.Task 1")
       print("2.Task 2")
       print("3.Exit")
       print("Select task(1,3): ")

       #copy all warehouses
       warehouses = copy.deepcopy(allwarehouses)

       task = getchoice(1,3)

       if task == 1:     
          task1(warehouses)
       elif task ==2:
          task2(warehouses)
       elif task ==3:
           break

''' this function loads cvs data into warehouses 
    '''
def initial_load(A,B,C,D):
    print("Warehouse A addings:\n")
    readcsv('DADSA Assignment 2018-19 PART B Warehouse A.csv',A)
    print("\n")

    print("Warehouse B addings:\n")
    readcsv('DADSA Assignment 2018-19 PART B Warehouse B.csv',B)
    print("\n")

    print("Warehouse C addings:\n")
    readcsv('DADSA Assignment 2018-19 PART B Warehouse C.csv',C)
    print("\n")

    print("Warehouse D addings:\n")
    readcsv('DADSA Assignment 2018-19 PART B Warehouse D.csv',D)
    print("\n")

    input("Press any key to continue")

'''this function adds shapes to warehouses
   it creates a tuple of shapes and appends to warehouse shapes'''

def addShape(A,B,C,D):

    #create tuple and add to warehouses
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

'''this funcion reads csv file and stores data into warehouse
   it creates an Item object and attempts to add to warehouse '''
def readcsv(filename,warehouse):

     with open(filename) as csvFile:#open file
                  reader = csv.reader(csvFile)
                  next(reader,None)#skip header
                  for number,description,price,shape,weight in reader:
                      #convert to integer
                      number = int(number)
                      weight = int(weight)
                      price  = int(price)
                      item = Item(number,description,price,shape,weight)  #item object                                      
                      warehouse.add_item(item) 

'''this function reads data from cvs file
   it adds item to warehouse A, if it doesnt fit it attemps to add to the next warehouse
   and so on
   If it doesnt fit in any the reject item '''
def readtoA(filename,A,B,C,D):
    
    with open(filename) as csvFile:#open file
                  reader = csv.reader(csvFile)
                  next(reader,None)#skip header
                  for number,description,price,shape,weight in reader:
                      added = False
                      #convert string to integer
                      number = int(number)
                      weight = int(weight)
                      price  = int(price)
                      item = Item(number,description,price,shape,weight)
                      #attempt adding                      
                      added = A.add_item(item)
                      if added == False:
                         added = B.add_item(item)
                      if added == False:
                          added = C.add_item(item)
                      if added == False:
                          added = D.add_item(item)


'''this fuction opens the cvs file and stores the data into a list '''
def readcsvTask2(filename,datastored):
    with open(filename) as csvFile:#open file
                  reader = csv.reader(csvFile)
                  next(reader,None)#skip header
                  for number,fromwarehouse,towarehouse in reader:
                      number = int(number)
                      route = (number,fromwarehouse,towarehouse)#tuple of delivery movements
                      datastored.append(route)

'''this function copies all warehouses into a list which is iterable '''

def copyWarehouses(A,B,C,D):

    allwarehouses = []
    allwarehouses.append(A)
    allwarehouses.append(B)
    allwarehouses.append(C)
    allwarehouses.append(D)
    return allwarehouses

days =0
'''this funcion reads the data for task 1 and displays to user '''

def task1(warehouses):
    
    os.system("cls")
    print("\n\nLoad items through Warehouse A\n")
    readtoA('DADSA Assignment 2018-19 PART B DATA TO INSERT INTO WAREHOUSE A TASK 1.csv',warehouses[0],warehouses[1],warehouses[2],warehouses[3])
    input("Press any key to continue")


''' this function contains the main menu of task 2
    prompts user for input and runs appropriate task based on user choice
 '''

def task2(allwarehouses):
    datastored =[]
    readcsvTask2('DADSA Assignment 2018-19 PART B DATA FOR TASK 2.csv',datastored)  #read movements data
    global days
    selection = 0
    #repeats until choice not 3
    while(selection != 3):
        partA = copy.deepcopy(allwarehouses)##copy default warehouses
        partB = copy.deepcopy(allwarehouses)
        os.system("cls")
        print("\n\n")
        print("Task 2 choices")
        print("1.Part A")
        print("2.Part B")
        print("3.Exit")
        days = 0
        selection = getchoice(1,3)#get user input
        if selection ==1:
            task2A(datastored,partA)
            input("Press any key to continue")
        elif selection ==2:
            task2B(datastored,partB)
            input("Press any key to continue")
        else:
            return     

'''
this function which warehouse to select for items delivery in the order
A-B-C-D 
'''
def task2A(datastored,allwarehouses):  
    
    warehouses =['A','B','C','D']
    for i in range(0,len(warehouses)-1):
        print("Van starts from {}".format(warehouses[i]))
        task2APlan(datastored,i,i+1,allwarehouses)

'''this function draws the plan for task 2
   it creates a van object with the capacity and insurance
   it loops in the movement data stored in the list
   it selects the appropriate from warehouse and towarehouse,picks up items and deliver by van'''

def task2APlan(datastored,fromW,toW,allwarehouses):
  
    warehouses =['A','B','C','D']
    for x in range(fromW,len(warehouses)-1):       
        van = Van()    #van object ignoring insurance and capacity
        for i in range(0,len(datastored)):
            if datastored[i][1]== warehouses[fromW] and datastored[i][2] == warehouses[toW]:                
                item = searchItem(allwarehouses[fromW],datastored[i][0])  #search for item with item number                              
                van.items.append(item) 
        #deliver item through van                     
        deliverItems(van.items,allwarehouses[toW],warehouses[fromW],False)
        toW+=1

'''
this function which warehouse to select for items delivery in the order
A-B-C-D 
'''
def task2B(datastored,allwarehouses):
    warehouses =['A','B','C','D']
    for i in range(0,len(warehouses)-1):
        print("Warehouse {} pickups".format(warehouses[i]))
        task2BPlan(datastored,i,i+1,allwarehouses)

'''this function draws the plan for task 2
   it creates a van object with the capacity and insurance
   it loops in the movement data stored in the list
   it selects the appropriate from warehouse and towarehouse,picks up items and deliver by van'''
def task2BPlan(datastored,fromW,toW,allwarehouses):
    warehouses =['A','B','C','D']    
    for x in range(fromW,len(warehouses)-1):                
        van = Van(2000,1500000000)  #van object  
        for i in range(0,len(datastored)):
            #compare from warehouse to to warehouse
            if datastored[i][1]== warehouses[fromW] and datastored[i][2] == warehouses[toW]:                
                item = searchItem(allwarehouses[fromW],datastored[i][0]) #search for item with item number
                if item !=None:                               
                    van.add_item(item,allwarehouses[toW])
        #deliver item through van                  
        deliverItems(van.items,allwarehouses[toW],warehouses[fromW],True)
        toW+=1

'''this function delivers items picked by the van
   it checks if any times are available to be delivered and increments 
   day by one'''            
def deliverItems(trips,toW,fromW,task2B):

    if len(trips)>0:
        global days
        days+=1 
        print("Day {}".format(days))       
        for i in trips:
            if task2B is False:
                #add item to warehouse                
                print("Item {} added from {} to {}"
                    .format(i.number,fromW,toW.name))
                toW.items.append(i)
            else:
                toW.add_item(i)

'''this function searches for an item in the warehouse
   it finds the item, pops it returns it'''
   
def searchItem(warehouse,itemNumber):
    #looping to find item
    for i in range(0,len(warehouse.items)):
        if warehouse.items[i].number == itemNumber:
            item = warehouse.items.pop(i)#remove item from warehouse
            return item
  
'''this function allows a use to make 
   a selection between min and max
   checks if input is a digit othewise,displays error
'''
def getchoice(min,max):
    incorrect = True
    #repeats until correct input
    while incorrect == True:
        try:
            choice = input("")
            if choice.isdigit:
                choice = int(choice)#convert input to integer
        except:
            print("Incorrect choice,input correct choice: ")
        else:
            if choice >= min and choice <=max:
                return choice
            else:
                print("Incorrect choice,input correct choice: ")

menu()