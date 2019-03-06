import csv
import os
import pickle
import copy

class Node: 
  
    def __init__(self, data): 
        self.data = data 
        self.next = None

    def __str__(self):
        return "%s %s"%(self.data,self.next)

    def __repr__(self):
        return "%s %s"%(self.data,self.next)
    
class LinkedList: 
  
    def __init__(self): 
        self.head = None

    def push(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = self.head 
        self.head = new_node 
    
    def append(self, new_data): 
        new_node = Node(new_data)   
        if self.head is None: 
            self.head = new_node 
            return 
        last = self.head 
        while (last.next): 
            last = last.next  
        last.next = new_node 

    def printList(self): 
        temp = self.head 
        while (temp): 
            print(temp.data) 
            temp = temp.next
    def searchItem(self,itemNumber):
        current = self.head     
        while current != None:
            for i in current.data.warehouseItems:
                if i.itemNumber == itemNumber: 
                    return current.data.warehouseName            
            current = current.next          
        return False

    def __str__(self):
        return "%s"%(self.head)
    def __repr__(self):
        return "%s"%(self.head)

class Item():

    def __init__(self,item_number=None,itemDescription=None,
                  item_price=None,itemShape = None,itemWeight =None):

        self.itemNumber = item_number
        self.itemDescription =itemDescription
        self.itemPrice = item_price
        self.itemShape = itemShape
        self.itemWeight = itemWeight
  
    def __str__(self):
        return "%-8s  %-45s £%-10s %-10s %s "%(self.itemNumber,self.itemDescription,self.itemPrice,
                                          self.itemShape,self.itemWeight)
    
    def __repr__(self):
        return "%s %s %s %s %s"%(self.itemNumber,self.itemDescription,self.itemPrice,
                                         self.itemShape,self.itemWeight)

class Warehouse(object):

    overallInsurance =8000000000

    #default constructor
    def __init__(self,warehouseName=None,remainingInsurance=None):
        self.warehouseName = warehouseName
        self.remainingInsurance = remainingInsurance
        self.warehouseItems =[]
        self.warehouseShapes=[]

    def addItem(self,warehouseItem,loadFromCsv):
         for i in self.warehouseShapes:
             if(warehouseItem.itemShape == i.shapeName):
                if(self.remainingInsurance > warehouseItem.itemPrice):
                  if i.storageQuantity > 0 and i.storageWeight >= warehouseItem.itemWeight:
                      self.warehouseItems.append(warehouseItem)
                      i.decreaseStorageWeigth()
                      self.decreaseWarehouseInsurance(warehouseItem.itemPrice)
                      if(loadFromCsv==False):
                          print("Item %s added to Warehouse %s"
                          %(warehouseItem.itemNumber,self.warehouseName))
                      return True
                  else:
                      print("Item rejected, item %s storage capacity exceeds warehouse %s capacity"
                            %(warehouseItem.itemNumber,self.warehouseName))
                      return False
                else:
                    print("Item rejected, item %s value exceeds warehouse %s remaining insurance"
                          %(warehouseItem.itemNumber,self.warehouseName))
                    return False
         print("Item %s rejected, warehouse %s cannot accomodate %s item shapes"
               %(warehouseItem.itemNumber,self.warehouseName,i.shapeName))
         return False
    
    def displayWarehouse(self):
        os.system('cls')
        print("\nWAREHOUSE INFORMATION: ")
        print("---------------------")
        print("  ---> Warehouse Name : %s"%self.warehouseName)
        print("  ---> Total elements : %s"%len(self.warehouseItems))
        print("  ---> Remaining Insurance: £%s"%(self.remainingInsurance))
        print("  ---> Remaining Overall Warehouse Insurance: £%s"%(Warehouse.overallInsurance))
        print("  ---> Available Shapes: %s"%(self.warehouseShapes))
        self.warehouseItems = self.insertionSort()
        self.printWarehouseItems()
  

    def insertionSort(self):
        j=0   
        swapList=[]
        for i in range(1,len(self.warehouseItems)):     
            swapList.insert(0,self.warehouseItems[i])
            j =i-1 
            while swapList[0].itemPrice > self.warehouseItems[j].itemPrice and j>=0:
                    self.warehouseItems[j+1] = self.warehouseItems[j]
                    j=j-1
            self.warehouseItems[j+1] = swapList[0]
        return self.warehouseItems

    def printWarehouseItems(self):
        print("\nItem No.  Description                                   Price       Shape      Weigth(kg)")
        print("--------  -----------                                   -----       -----      ------\n")
        for i in self.warehouseItems:
            print(i)

    def addShape(self,shapeName,weight,quantity):
        temp = storageShapes(shapeName,weight,quantity) 
        self.warehouseShapes.append(temp)

    def increaseWarehouseInsurance(self,amount):
        self.remainingInsurance+=amount
        Warehouse.overallInsurance+=amount
    
    def decreaseWarehouseInsurance(self,amount):
        self.remainingInsurance-=amount
        Warehouse.overallInsurance-=amount
    
    def getWarehouseName(self):
        return self.warehouseName

    def getWarehouseRemainingInsurance(self):
        return self.remainingInsurance

    def __str__(self):
         return "%s %s"%(self.warehouseName,self.remainingInsurance)

    def __repr__(self):
         return "%s %s"%(self.warehouseName, self.remainingInsurance)

class storageShapes():
    
    def __init__(self,shapeName=None,storageWeight=None,storageQuantity=None):
        self.shapeName = shapeName
        self.storageWeight = storageWeight
        self.storageQuantity = storageQuantity
    
    def decreaseStorageWeigth(self):
        self.storageQuantity-=1

    def increaseStorageWeigth(self):
        self.storageQuantity+=1
        
    def __str__(self):
         return "%s %s %s"%(self.shapeName,self.storageWeight,self.storageQuantity)

    def __repr__(self):
        return "%s %s %s"%(self.shapeName,self.storageWeight,self.storageQuantity)

def setValues(warehouse,selectedWarehouse):

    shapesIndex=0
    index=0
    shapes = ['Rectangle','Sphere','Pyramid','Square']

    for i in range(0,len(warehouse)):
        for shapesIndex in range(0,len(shapes)):
            if warehouse[i][index]==shapes[shapesIndex]:
               selectedWarehouse.addShape(warehouse[i][index],warehouse[i][1],warehouse[i][2])
               break
    return

def setupWarehouses(allWarehouses):

    warehouseShapes = []
    warehouseShapes.append([['Rectangle',1000,5],['Pyramid',2000,10],['Square',2000,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',2000,5],['Pyramid',250,10]])
    warehouseShapes.append([['Sphere',250,15],['Pyramid',500,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',750,2],['Pyramid',3000,2],['Square',750,10]])

    for i in range(0,4):
      setValues(warehouseShapes[i],allWarehouses[i])

def createWarehouses():

    Warehouses = []
    WarehouseName = 'A'

    for i in range(0,4):
        Warehouses.append(Warehouse(WarehouseName,2000000000))
        WarehouseName = chr(ord(WarehouseName)+1)

    setupWarehouses(Warehouses)
    return Warehouses


def main():

    global Warehouses
    Warehouses = []
    menuChoice = 0
    Warehouses = createWarehouses()
    readcsvFiletoWarehouse(Warehouses)

    while(menuChoice!=5):     
        mainMenu()
        menuChoice = getValidInteger(1,5)
        menuSelection(menuChoice,Warehouses)
       
    return

def readcsvFiletoWarehouse(Warehouses):

    loadcsv('Warehouse A.csv',Warehouses[0])
    loadcsv('Warehouse B.csv',Warehouses[1])
    loadcsv('Warehouse C.csv',Warehouses[2])
    loadcsv('Warehouse D.csv',Warehouses[3])
    
def mainMenu():

    os.system('cls')
    print("            MAIN MENU")
    print("            ---------\n")
    print("     1 --> Task 1")
    print("     2 --> Task 2")
    print("     3 --> Task 3")
    print("     4 --> Task 4")
    print("     5 --> Quit")
    print("\nSelect choice(1-5): ")

def menuSelection(menuChoice,Warehouses):

        if menuChoice ==1:                 
           task1Menu()
           taskMenuSelection = getValidInteger(1,3)
           task1MenuChoice(taskMenuSelection,Warehouses)
        elif menuChoice==2:
           setupBinaryTree(Warehouses)
           task2Menu()
           taskMenuSelection = getValidInteger(1,3)
           task2MenuChoice(taskMenuSelection,Warehouses)

def displayWarehouses(Warehouses):
    
    os.system('cls')
    print("            DISPLAY WAREHOUSES")
    print("            -----------------\n")
    allWarehousesDetails(Warehouses)
    print("1 --> A")
    print("2 --> B")
    print("3 --> C")
    print("4 --> D")
    print("5 --> Quit")
    print("\nSelect choice(1-5): ")

def allWarehousesDetails(Warehouses):

        print("\nWAREHOUSES INFORMATION: ")
        print("----------------------")
        print("\nWarehouse Name       Total Elements    Remaing Insurance   Remaining Shapes")
        print("--------------       -------------     -----------------   ----------------")
        
        for i in range(0,len(Warehouses)):
            print("%-20s %-17s %-19s %s"%
                  (Warehouses[i].warehouseName,
                   len(Warehouses[i].warehouseItems),
                   Warehouses[i].remainingInsurance,
                   Warehouses[i].warehouseShapes))
        print("\n")

def task1Menu():

    os.system('cls')
    print("         TASK 1")
    print("         ------")
    print("1 --> Display Warehouses")
    print("2 --> Load task 1 csv to Warehouse A")
    print("3 --> Quit")
    print("\nSelect choice(1-3): ")

def task1MenuChoice(menuChoice,Warehouses):
    while(menuChoice!=3):
        task1MenuChoice.itemsLoaded = getattr(task1MenuChoice,'itemsLoaded',False)
        if menuChoice == 1:
           displayWarehouses(Warehouses)
           warehouseChoice = getValidInteger(1,5)
           if warehouseChoice !=5:
               Warehouses[warehouseChoice-1].displayWarehouse()
           else:
               return
        elif menuChoice ==2:
              if task1MenuChoice.itemsLoaded == False:
                  tempWarehouse = Warehouse("temp",2000000000)
                  createTempWarehouse(tempWarehouse)         
                  task1MenuChoice.itemsLoaded = loadItemsToWarehouseA(tempWarehouse,Warehouses)              
              else:
                  print("Data Loaded into warehouses already")
             
    input("Press any key to continue") 
    return

def task2MenuChoice(menuChoice,Warehouses):
     while(menuChoice!=3):
       pass

def setupBinaryTree(Warehouses):
    
    llist = LinkedList()
    llist.append(Warehouses[0])
    llist.append(Warehouses[1])
    llist.append(Warehouses[2])
    llist.append(Warehouses[3])
    llist.printList()
    item = llist.searchItem(17598)
    print(item)
    item = llist.searchItem(13111)
    print(item)
    item = llist.searchItem(13110)
    print(item)

def task2Menu():

    os.system('cls')
    print("         TASK 1")
    print("         ------")
    print("1 --> Days to relocate items from task 2 csv.")
    print("2 --> Days to relocate taking into consideration weight and value of each item.")
    print("3 --> Quit")
    print("\nSelect choice(1-3): ")

def createTempWarehouse(tempWarehouse):

    tempWarehouse.addShape('Rectangle',2000,10)
    tempWarehouse.addShape('Square',2000,10)
    tempWarehouse.addShape('Sphere',2000,10)
    tempWarehouse.addShape('Pyramid',2000,10)
    loadcsv('DATA TO INSERT INTO WAREHOUSE A.csv',tempWarehouse)

def loadItemsToWarehouseA(tempWarehouse,Warehouses):

    itemAdded = True
    os.system('cls')
    print("\n")
    print("    Load Items through Warehouse A'")
    print("    ------------------------------\n")

    for i in range(0,len(tempWarehouse.warehouseItems)):
        for j in range(0,4):
            itemAdded = Warehouses[j].addItem(tempWarehouse.warehouseItems[i],False)
            if itemAdded == True:                
                break        
    return True

def loadcsv(csvFilename,selectedWarehouse):
    try:
        with open(csvFilename) as csvFile:
                  reader = csv.reader(csvFile)
                  next(reader,None)
                  for itemnumber,itemdescription,itemprice,itemShape,itemWeigth in reader:                  
                      newItem = Item(int(itemnumber),itemdescription,int(itemprice),itemShape,int(itemWeigth))
                      selectedWarehouse.addItem(newItem,True)                                      
    except FileNotFoundError:
          print(FileNotFoundError)
    return

def getValidInteger(minimum,maximum):

        #sets flag
        flag =True
        while flag == True:
             number= input("")
             #checks if input is valid integer
             try:
                if number.isdigit:
                   number = int(number)
             except ValueError:
                   print('You didnt input an input an integer,try again: (%d-%d))' % (minimum,maximum))
             else:
                 #checks if input is out of range
                 if number < minimum or number >maximum:
                    print('The entered number is out of range, try again: (%d-%d))' % (minimum,maximum))
                 else:
                    flag = False       
        return number

main()