import csv
import os
import pickle
import copy
days = 0 
tripCount = 0
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
    
    def __init__(self,itemNumber=None,itemDescription=None,
                  itemPrice=None,itemShape = None,itemWeight =None):

        self.itemNumber = itemNumber
        self.itemDescription =itemDescription
        self.itemPrice = itemPrice
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
                      i.decreaseStorageWeight()
                      self.decreaseWarehouseInsurance(warehouseItem.itemPrice)
                      if(loadFromCsv==False):
                          print("Item %s added to Warehouse %s"
                          %(warehouseItem.itemNumber,self.warehouseName))
                      return True
                  else:
                      print("Item rejected, item %s storage weight %s exceeds warehouse %s %s quantity %s"
                            %(warehouseItem.itemNumber,
                              warehouseItem.itemWeight,
                              self.warehouseName,
                              i.shapeName,
                              i.storageQuantity))
                      return False
                else:
                    print("Item rejected, item %s value exceeds warehouse %s remaining insurance"
                          %(warehouseItem.itemNumber,self.warehouseName))
                    return False
         print("Item %s rejected, warehouse %s cannot accomodate %s item shapes"
            %(warehouseItem.itemNumber,
              self.warehouseName,
              warehouseItem.itemShape))
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

    def binarySearch(self,start,end,itemNumber):
        self.warehouseItems = self.insertionSort()
        while end>=start:     
           middle = start+(end-start)/2
           middle = int(middle)      
           if itemNumber==self.warehouseItems[middle].itemNumber:
              return middle
           else:           
              if self.warehouseItems[middle].itemNumber>itemNumber:
                 end = middle-1
              else : 
                start = middle+1             
        else:        
          print("An item with the id '%s' does not exits in the records..."%itemNumber)       
          return -1

    def moveItemtoVan(self,item,target):
      x =0  
      for i in range(0,len(target.warehouseShapes)):
          if target.warehouseShapes[i].shapeName == item.itemShape:
              x =i
              break
      if item.itemPrice > target.remainingInsurance:
          print("Van rejects item '%s', item price exceeds warehouse '%s' remaining insurance"
                 %(target.warehouseName,item.itemNumber))
    
      elif item.itemWeight > target.warehouseShapes[x].storageWeight:
          print("Van rejects item '%s' from warehouse %s, storage weight '%s' exceeds warehouse '%s' '%s' capacity '%s'"
                %(item.itemNumber,
                  self.warehouseName,
                  item.itemWeight,
                  target.warehouseName,
                  item.itemShape,
                  target.warehouseShapes[x].storageWeight))
      elif target.warehouseShapes[x].storageQuantity ==0:
          print("Van rejects item '%s from warehouse %s',warehouse '%s' '%s' storage quantity remaining is '%s' "
                %(item.itemNumber,
                  self.warehouseName,
                  target.warehouseName,
                  item.itemShape,                                             
                  target.warehouseShapes[x].storageQuantity))
      else:
          position = 0    
          position = self.binarySearch(0,len(self.warehouseItems),item.itemNumber)
          if position >= 0:
             temp = self.warehouseItems[position]
             self.increaseWarehouseInsurance(temp.itemPrice)
             self.increaseShapeValue(temp)
             del self.warehouseItems[position]
             target.warehouseShapes[x].decreaseStorageWeight()
             return temp

    def insertionSort(self):
        j=0   
        swapList=[]
        for i in range(1,len(self.warehouseItems)):     
            swapList.insert(0,self.warehouseItems[i])
            j =i-1 
            while swapList[0].itemNumber < self.warehouseItems[j].itemNumber and j>=0:
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
        temp = itemShapes(shapeName,weight,quantity) 
        self.warehouseShapes.append(temp)

    def increaseShapeValue(self,item):
        for i in range(0,len(self.warehouseShapes)):
            if(item.itemShape == self.warehouseShapes[i]):
                self.warehouseShapes[i].increaseStorageWeight()
    
    def decreaseShapeValue(self,item):
        for i in range(0,len(self.warehouseShapes)):
            if(item.itemShape == self.warehouseShapes[i]):
                self.warehouseShapes[i].decreaseStorageWeight()

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

class Van():

    def __init__(self,remainingInsurance=None,remainingWeightCapacity=None):
        self.remainingInsurance = remainingInsurance
        self.remainingWeightCapacity = remainingWeightCapacity
        self.vanItems=[]
        self.vanTrips=[]

    def addItem(self,vanItem):
        if vanItem.itemWeight > self.remainingWeightCapacity:
            print("Item weight exceeds van capacity")
        elif vanItem.itemPrice > self.remainingInsurance:
            print("Item price exceeds van capacity")
        else:
            self.vanItems.append(vanItem)
            self.decreaseRemainingInsurance(vanItem.itemPrice)
            self.decreaseRemainingWeightCapacity(vanItem.itemWeight)
            print("Van picks-up item %s "%(vanItem.itemNumber))

    def addItemtoTarget(self,target,item):
        x =0  
        for i in range(0,len(target.warehouseShapes)):
          if target.warehouseShapes[i].shapeName == item.itemShape:
              x =i
              break
        if item.itemPrice > target.remainingInsurance:
          print("Van rejects item '%s', item price exceeds warehouse '%s' remaining insurance"
                 %(target.warehouseName,item.itemNumber))
    
        elif item.itemWeight > target.warehouseShapes[x].storageWeight:
          print("Van rejects item '%s' from warehouse %s, storage weight '%s' exceeds warehouse '%s' '%s' capacity '%s'"
                %(item.itemNumber,
                  self.warehouseName,
                  item.itemWeight,
                  target.warehouseName,
                  item.itemShape,
                  target.warehouseShapes[x].storageWeight))
        elif target.warehouseShapes[x].storageQuantity ==0:
          print("Van rejects item '%s from warehouse %s',warehouse '%s' '%s' storage quantity remaining is '%s' "
                %(item.itemNumber,
                  self.warehouseName,
                  target.warehouseName,
                  item.itemShape,                                             
                  target.warehouseShapes[x].storageQuantity))
        else:
          position = 0    
          position = self.binarySearch(0,len(self.warehouseItems),item.itemNumber)
          if position >= 0:
             temp = self.warehouseItems[position]
             self.increaseWarehouseInsurance(temp.itemPrice)
             self.increaseShapeValue(temp)
             del self.warehouseItems[position]
             target.warehouseShapes[x].decreaseStorageWeight()
             return temp

    def resetVan(self):
        self.remainingInsurance = 1500000000
        self.remainingWeightCapacity = 2000
        self.vanTrips = []
        self.vanItems = []
      
    def decreaseRemainingInsurance(self,price):
        self.remainingInsurance-= price

    def decreaseRemainingWeightCapacity(self,weight):
        self.remainingWeightCapacity -= weight

    def printVanItems(self):
        print("\nItem No.  Description                                   Price       Shape      Weigth(kg)")
        print("--------  -----------                                   -----       -----      ------\n")
        for i in self.vanItems:
            print(i)

    def __str__(self):
         return "%s %s"%(self.remainingWeightCapacity,self.remainingInsurance)

    def __repr__(self):
         return "%s %s"%(self.remainingWeightCapacity, self.remainingInsurance)

class Trip():

    def __init__(self,startWarehouse=None,targetWarehouse=None):
        self.startWarehouse = startWarehouse
        self.targetWarehouse = targetWarehouse
        self.tripItems=[]

    def addItem(self,van,item):
        if item.itemPrice > van.remainingInsurance:
            print("Item cannot be added to trip,insurance exceeds van insurance")
        elif item.itemWeight >  van.remainingWeightCapacity:
            print("Item weight exceeds weight van remaining capacity")
        else:
            self.tripItems.append(item)
            van.decreaseRemainingInsurance(item.itemPrice)
            van.decreaseRemainingWeightCapacity(item.itemWeight)
         
    def __str__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)

    def __repr__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)

class itemShapes():
    
    def __init__(self,shapeName=None,storageWeight=None,storageQuantity=None):
        self.shapeName = shapeName
        self.storageWeight = storageWeight
        self.storageQuantity = storageQuantity
    
    def decreaseStorageWeight(self):
        self.storageQuantity-=1

    def increaseStorageWeight(self):
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
    print("     1 --> Load task 1 items to warehouses")
    print("     2 --> Days to relocate task 2 items")
    print("     3 --> Minimum number of trips")
    print("     4 --> Task 4")
    print("     5 --> Quit")
    print("\nSelect choice(1-5): ")

def menuSelection(menuChoice,Warehouses):

        task1MenuSelection = 0
        task1Warehouses = copy.deepcopy(Warehouses)
        task2Warehouses = copy.deepcopy(Warehouses)
        task3Warehouses = copy.deepcopy(Warehouses)
        task4Warehouses = copy.deepcopy(Warehouses)

        print(Warehouse.overallInsurance)

        if menuChoice ==1:             
            task1(task1Warehouses)
            input("\nPress any key to continue")
            displayResults(task1Warehouses)

        elif menuChoice==2:        
            task2(task2Warehouses)
            input("\nPress any key to continue")
            displayResults(task2Warehouses)
            

        elif menuChoice ==3:
            task3(task3Warehouses)
            input("\nPress any key to continue")
            displayResults(task3Warehouses)
        
        elif menuChoice ==4:
            task4(task4Warehouses)
            input("\nPress any key to continue")
            displayResults(task4Warehouses)
    

        return menuChoice

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

def task1(task1Warehouses):
         
        tempWarehouse = Warehouse("temp",2000000000)
        createTempWarehouse(tempWarehouse)
        loadItemsToWarehouseA(tempWarehouse,task1Warehouses)     
        
        
                                  
def displayResults(Warehouses):

      displayAnother ='Y'
      while displayAnother =='Y':
              displayWarehouses(Warehouses)
              warehouseChoice = getValidInteger(1,5)
              if warehouseChoice == 5:
                 break
              else:
                 Warehouses[warehouseChoice-1].displayWarehouse()
                 print("\nDisplay another warehouse?(Y/N): ")
                 displayAnother = getValidYesOrNo()
     
def task2(task2Warehouses):
    
    os.system('cls')
    print("\n\n               DAYS TO RELOCATE TASK 2 ITEMS")
    print("               ------------------------------")
    task2data =[]
    
    originWarehouse = 'A'   
    allWarehousesItems = []
    loadcsv2('TASK 2(1).csv',task2data)

    for i in range(0,3):
        targetWarehouse = 'B'
        print("\n---------  - -------")
        print("WAREHOUSE: %s pickups"%(originWarehouse))
        print("---------  - -------")
        for j in range(0,4):
            deliverItems = [False]             
            van = loadVan(originWarehouse,targetWarehouse,task2data,task2Warehouses,deliverItems)
            if deliverItems[0] == True:                                                
                deliverVanItems(targetWarehouse,van,task2Warehouses)          
            targetWarehouse = chr(ord(targetWarehouse)+1)
        originWarehouse = chr(ord(originWarehouse)+1)

    global days
    days =0
              
def loadVan(origin,target,task2data,task2Warehouses,deliverItems):

  van = Van(1500000000,2000) 
  itemsWeight = 0
  number = 0
  global days
 
  for i in range (0,len(task2data)):
     if task2data[i][1]==origin and task2data[i][2]==target:         
        originIndex = getWarehousePosition(task2Warehouses,origin)
        targetIndex = getWarehousePosition(task2Warehouses,target)        
        item = createItem(task2Warehouses[originIndex],task2data[i][0])      
        if number != targetIndex:          
            days+=1
            print("\n   Day:%s"%(days))
            print("   --- -") 
            temp = copy.deepcopy(task2Warehouses[targetIndex])
            number = targetIndex
        item11 = task2Warehouses[originIndex].moveItemtoVan(item,temp)
        if item11 != None:
            van.addItem(item11)           
            deliverItems[0] = True

  return van

def createItem(targetWarehouse,itemID):
   
    i = targetWarehouse.binarySearch(0,len(targetWarehouse.warehouseItems)-1,itemID)
    item = targetWarehouse.warehouseItems[i]
    return item

def getWarehousePosition(task2Warehouses,targetName):

    for i in range(0,len(task2Warehouses)):
        if task2Warehouses[i].warehouseName == targetName:
            return i

def deliverVanItems(targetWarehouse,van,task2Warehouses):
    
    index = getWarehousePosition(task2Warehouses,targetWarehouse)
    for i in range(0,len(van.vanItems)):
        task2Warehouses[index].addItem(van.vanItems[i],False)

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

def createTempWarehouse(tempWarehouse):

    tempWarehouse.addShape('Rectangle',2000,10)
    tempWarehouse.addShape('Square',2000,10)
    tempWarehouse.addShape('Sphere',2000,10)
    tempWarehouse.addShape('Pyramid',2000,10)
    loadcsv('DATA TO INSERT INTO WAREHOUSE A.csv',tempWarehouse)

def loadItemsToWarehouseA(tempWarehouse,task1Warehouses):

    itemAdded = True
    os.system('cls')
    print("\n")
    print("    Load Items through Warehouse A'")
    print("    ------------------------------\n")

    for i in range(0,len(tempWarehouse.warehouseItems)):
        for j in range(0,4):
            itemAdded = task1Warehouses[j].addItem(tempWarehouse.warehouseItems[i],False)
            if itemAdded == True:                
                break        
    return True

def task3(task3Warehouses):

    task3data = []
    global tripCount
    van = Van(1500000000,2000)

    origin ='A'
    target ='B'
    os.system('cls')
    print("          TASK 3")
    print("          ------\n")
    loadcsv2("TASK 3.csv",task3data)

    for i in range(0,3):
        
        van.resetVan()
        planTrip(task3data,origin,target,van,task3Warehouses)
        deliverItems(van.vanTrips,task3Warehouses,origin)
        origin = chr(ord(origin)+1)
        target = chr(ord(origin)+1)

    tripCount =0
    return

def planTrip(task3data,origin,target,van,task3Warehouses):

   number = 0
   for i in range(0,3):
        trip = Trip(origin,target) 
        for i in range(0,len(task3data)):
            if task3data[i][1]==origin and task3data[i][2]==target:

               originIndex = getWarehousePosition(task3Warehouses,origin)
               targetIndex = getWarehousePosition(task3Warehouses,target)
               item = createItem(task3Warehouses[originIndex],task3data[i][0])

               if number != targetIndex:
                   temp = copy.deepcopy(task3Warehouses[targetIndex])
                   number = targetIndex

               item11 = task3Warehouses[originIndex].moveItemtoVan(item,temp)
               if item11 != None:
                  trip.addItem(van,item11)
      
        target = chr(ord(target)+1)
        van.vanTrips.append(trip)
        if target=='E':
            break
        

   return

def task4(task4Warehouses):

    task4data = []
    van = Van(1500000000,2000)
    

    origin ='A'
    target ='B'
    os.system('cls')
    print("          TASK 4")
    print("          ------\n")
    loadcsv2("TASK 3.csv",task4data)


    for i in range(0,3):        
        van.resetVan()
        shapesFilter =[]
        print("\nWarehouse %s to %s delivery"%(origin,target))
        print("---------------------------")
        planTrip(task4data,origin,target,van,task4Warehouses)
        shapesFilter = seperateTripShapes(van)
        for i in shapesFilter:
           x = getWarehousePosition(task4Warehouses,target)
           if len(i) > 0:
            deliverByShape(i,task4Warehouses[x]) 

        origin = chr(ord(origin)+1)
        target = chr(ord(origin)+1)

def seperateTripShapes(van):

    rectangle =[]
    sphere =[]
    pyramid =[]
    square =[]
    allShapes=[]

    for i in van.vanTrips:
        for j in i.tripItems:
            if j.itemShape == 'Rectangle':
               rectangle.append(j)
            elif j.itemShape == 'Sphere':
                sphere.append(j)
            elif j.itemShape == 'Pyramid':   
                pyramid.append(j)
            else:
                square.append(j)

    allShapes.append(rectangle)
    allShapes.append(sphere )
    allShapes.append(pyramid)
    allShapes.append(square)
    
    return allShapes


def deliverItems(trips,task3Warehouses,origin):
    
    global tripCount

    target =  chr(ord(origin)+1)

    for i in range(0,len(trips)):

        if trips[i].targetWarehouse == target: 
           tripCount+=1 
           print("\nTrip %s: Warehouse %s to %s"%(tripCount,origin,target))
           print("------  ----------------")           
           targetIndex = getWarehousePosition(task3Warehouses,target)

           for j in trips[i].tripItems:               
                task3Warehouses[targetIndex].addItem(j,False)

        target = chr(ord(target)+1)

def deliverByShape(shapesItems,targetWarehouse):

    print("\n%s Items delivery: "%(shapesItems[0].itemShape))
    for i in shapesItems:
        targetWarehouse.addItem(i,False)


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

def getValidYesOrNo():

    flag =True
    while flag:
        yes_or_no = input(" ")
        if yes_or_no.upper() == 'Y' or yes_or_no.upper() == 'N':
           return yes_or_no.upper()
        else:
          print("Wrong input,enter Y OR N: ")

def getValidInteger(minimum,maximum):

        flag =True
        while flag == True:
             number= input("")   
             try:
                if number.isdigit:
                   number = int(number)
             except ValueError:
                   print('You didnt input an input an integer,try again: (%d-%d))' % (minimum,maximum))
             else:           
                 if number < minimum or number >maximum:
                    print('The entered number is out of range, try again: (%d-%d))' % (minimum,maximum))
                 else:
                    flag = False       
        return number

main()