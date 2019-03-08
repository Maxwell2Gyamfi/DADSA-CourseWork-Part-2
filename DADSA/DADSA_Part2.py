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


    #default constructor
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
            %(warehouseItem.itemNumber,self.warehouseName,warehouseItem.itemShape))
         return False

    def getItemsWeight(self):
        itemsWeigth =0
        for i in self.warehouseItems:
            itemsWeigth+=i.itemWeight
        return itemsWeigth

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

    while(menuChoice!=5):
        if(menuChoice ==1):                 
           task1Menu()
           task1MenuSelection = getValidInteger(1,3)
           task1MenuChoice(task1MenuSelection,Warehouses)
        elif(menuChoice==2):
            task2MenuSelection = getValidInteger(1,3)
            task2MenuChoice(task2MenuSelection,Warehouses)   

    return 

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

    task1MenuChoice.itemsLoaded = getattr(task1MenuChoice,'itemsLoaded',False)
    if menuChoice == 1:
       displayWarehouses(Warehouses)
       warehouseChoice = getValidInteger(1,5)
       if menuChoice !=5:
           Warehouses[warehouseChoice-1].displayWarehouse()
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
   if menuChoice == 1:
       task2Menu()
       setupTask2(Warehouses)
     

def setupTask2(Warehouses):
    
    task2data =[]
    days =0   
    originWarehouse = 'A'   
    allWarehousesItems = []
    WarehousesCopy = copy.deepcopy(Warehouses)
    loadcsv2('TASK 2(1).csv',task2data)

    for i in range(0,3):
        targetWarehouse = 'A'
        print("\nItems from Warehouse:%s"%(originWarehouse))
        print("-----------------------")
        for j in range(0,4):
            deliverItems = [False]          
            van = loadVan(originWarehouse,targetWarehouse,task2data,WarehousesCopy,deliverItems)
            if deliverItems[0] == True:                  
                deliverVanItems(targetWarehouse,van,WarehousesCopy)
                days+=1 
                print("Total Days:%s\n"%(days))                                            
            targetWarehouse = chr(ord(targetWarehouse)+1)
        originWarehouse = chr(ord(originWarehouse)+1)   
        
def loadVan(originWarehouse,targetWarehouse,task2data,WarehousesCopy,deliverItems):

    van = Warehouse("van",2000000000)
    van.addShape("Rectangle",2000,10)
    van.addShape("Square",2000,10)
    van.addShape("Sphere",2000,10)
    van.addShape("Pyramid",2000,10)
    itemsWeight = 0

    for i in range (0,len(task2data)):
        if task2data[i][1]==originWarehouse and task2data[i][2]==targetWarehouse:         
           warehousePosition = getWarehousePosition(WarehousesCopy,originWarehouse)
           WarehousesCopy[warehousePosition].warehouseItems = mergeSort(WarehousesCopy[warehousePosition].warehouseItems)
           itemPosition = interpolationSearch(WarehousesCopy[warehousePosition].warehouseItems,task2data[i][0])
           van.addItem(WarehousesCopy[warehousePosition].warehouseItems[itemPosition],False)           
           deliverItems[0] = True

    itemsWeight = van.getItemsWeight()
    print(itemsWeight)

    return van

def getWarehousePosition(WarehousesCopy,selectedwarehouseName):

    for i in range(0,len(WarehousesCopy)):
        if WarehousesCopy[i].warehouseName == selectedwarehouseName:
            return i

def deliverVanItems(targetWarehouse,van,WarehousesCopy):
    
    warehousepos = getWarehousePosition(WarehousesCopy,targetWarehouse)
    for i in range(0,len(van.warehouseItems)):
        WarehousesCopy[warehousepos].addItem(van.warehouseItems[i],False)


def interpolationSearch(warehouseItems,id):

    #calculates lenght of warehouse contents
    lenght= len(warehouseItems)
    #indexes
    start =0
    end = lenght-1
    #return false if warehouse contents is empty
    if end ==-1:
        return False
    
    #repeat while start index is less than end index and item number not found
    while ((start<end) <=id and (id >=warehouseItems[start].itemNumber)and (id <=warehouseItems[end].itemNumber)):
          try:
            position = int(start+(float((end-start)
           /(warehouseItems[end].itemNumber-warehouseItems[start].itemNumber))*(id-warehouseItems[start].itemNumber)))
          except ZeroDivisionError:#ignores error if only an item in warehouse contents
              return 0
          if warehouseItems[position].itemNumber ==id:#returns item position
              return position
          #reset start and end indexes 
          if id > warehouseItems[position].itemNumber:
              start = position+1 
          else:
               end = position-1
    return False

def copyAllWarehouses(WarehousesCopy):

    allWarehousesItems = []
    for i in WarehousesCopy:
        allWarehousesItems.extend(i.warehouseItems)

    return allWarehousesItems

def mergeSort(selectedWarehouse):
    #returns sorted selected warehouse items
        if len(selectedWarehouse)<=1:
            return selectedWarehouse
        #get middle value
        mid = int(len(selectedWarehouse)/2)
        #sorts each halve of selected warehouse items
        lefthalf,righthalf = mergeSort(selectedWarehouse[:mid]),mergeSort(selectedWarehouse[mid:])
        return merge(lefthalf,righthalf)


'''
Function Name: 
  --> merge(left,right)

Function Description:
  --> This function compares the left index value to the right index value and appends
      the values to result_container list in ascending order.
  --> If leftindex or rightindex variable is above the lenght of left or right list then copy
      the remaining values to result_container.  

User Interface Variables:
  --> OUT(Return Values):
      - result_container
  --> IN(Value Parameters):
      - left half and right half of selected warehouse
  --> IN and OUT (Reference Parameters):
      - None
'''              
def merge(left,right):

    #local variables
    resultContainer=[]
    leftIndex=rightIndex=0

    while leftIndex<len(left) and rightIndex <len(right):
        #appends item to result_container list and increase index
         if left[leftIndex].itemNumber<right[rightIndex].itemNumber:
            resultContainer.append(left[leftIndex])
            leftIndex+=1
         else:
           resultContainer.append(right[rightIndex])
           rightIndex+=1
    #copy remaining elements of a half into result_container
    resultContainer.extend(left[leftIndex:])
    resultContainer.extend(right[rightIndex:])
   
    return resultContainer


def loadcsv2(csvFilename,task2data):
    
    
    try:
        with open(csvFilename) as csvFile:
                  reader = csv.reader(csvFile)
                  next(reader,None)
                  for itemNumber,selectedWarehouse,targetWarehouse in reader:
                      temp =[]
                      itemNumber = int(itemNumber)
                      temp.append(itemNumber)
                      temp.append(selectedWarehouse)
                      temp.append(targetWarehouse)                      
                      task2data.append(temp)

    except FileNotFoundError:
          print(FileNotFoundError)
    return


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