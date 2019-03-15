import csv
import os
import pickle
import copy

class Warehouse(object):

    overallInsurance =8000000000

    def __init__(self,warehouseName=None,remainingInsurance=None):

        self.warehouseName = warehouseName
        self.remainingInsurance = remainingInsurance
        self.warehouseItems =[]
        self.warehouseShapes=[]

    def addItem(self,item,loadFromCsv):

        for i in self.warehouseShapes:
            if item.itemShape in self.warehouseShapes:
                if item.itemPrice > self.remainingInsurance:
                    print("Item rejected, item %s value exceeds warehouse %s remaining insurance"
                               %(item.itemNumber,
                               self.warehouseName))
                elif item.itemWeight > i.storageWeight and i.storageQuantity ==0:
                    if i.storageQuantity ==0:
                        print("Item rejected, warehouse %s %s remaining storage quantity is %s"
                              %(self.warehouseName,
                                i.itemShape,
                                i.storageQuantity))
                    else:
                        print("Items rejected, item storage weight exceeds warehouse %s %s capacity %s"
                              %(self.warehouseName,
                               i.shapeName,
                               i.storageWeight))
                else:
                    self.warehouseItems.append(item)
                    i.decreaseStorageWeight()
                    self.decreaseWarehouseInsurance(item.itemPrice)
                    if(loadFromCsv==False):
                          print("Item %s added to Warehouse %s"
                          %(item.itemNumber,
                            self.warehouseName))
                          return True
        print("Item rejected, warehouse %s cannot accomodate %s shapes"
                   %(self.warehouseName,
                     item.itemShape))
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
          print("An item with the id '%s' does not exits in the records."%itemNumber)       
          return -1

    def moveItemtoVan(self,item,van,target):
        
      if item.itemPrice > van.remainingInsurance:
          print("Van rejects item '%s', item price %s exceeds Van remaining insurance %s"
                 %(item.itemNumber,
                   item.itemPrice,
                   van.remainingInsurance))
    
      elif item.itemWeight > van.remainingWeightCapacity:
          print("Van rejects item '%s', item's storage weight '%s' exceeds Van's remaining weight capacity %s"
                %(item.itemNumber,               
                  item.itemWeight,
                  van.remainingWeightCapacity))          
      else:
          success = van.addItemtoTarget(item,target,self)
          return success

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
        temp = storageShapes(shapeName,weight,quantity) 
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

    def addItemtoTarget(self,target,item,origin):
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
          position = origin.binarySearch(0,len(origin.warehouseItems),item.itemNumber)
          if position >= 0:
             temp = origin.warehouseItems[position]
             origin.increaseWarehouseInsurance(temp.itemPrice)
             origin.increaseShapeValue(temp)
             del origin.warehouseItems[position]
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
            self.tripItems.append(item)
            van.decreaseRemainingInsurance(item.itemPrice)
            van.decreaseRemainingWeightCapacity(item.itemWeight)
            
    def __str__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)

    def __repr__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)

def main():

    menuChoice = 0
    Warehouses = createWarehouses()
    readcsvFiletoWarehouse(Warehouses)
    
  
    while(menuChoice!=5):     
        mainMenu()
        menuChoice = getValidInteger(1,5)
        menuSelection(menuChoice,Warehouses)       
    return

def createWarehouses():

    Warehouses = []
    WarehouseName = 'A'

    for i in range(0,4):
        Warehouses.append(Warehouse(WarehouseName,2000000000))
        WarehouseName = chr(ord(WarehouseName)+1)

    setupItemShapes(Warehouses)
    return Warehouses

def setupItemShapes(Warehouses):

    warehouseShapes = []
    warehouseShapes.append([['Rectangle',1000,5],['Pyramid',2000,10],['Square',2000,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',2000,5],['Pyramid',250,10]])
    warehouseShapes.append([['Sphere',250,15],['Pyramid',500,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',750,2],['Pyramid',3000,2],['Square',750,10]])

    for i in range(0,4):
      setShapesValues(warehouseShapes[i],Warehouses[i])

def setShapesValues(warehouse,selectedWarehouse):

    shapesIndex=0
    index=0
    shapes = ['Rectangle','Sphere','Pyramid','Square']

    for i in range(0,len(warehouse)):
        for shapesIndex in range(0,len(shapes)):
            if warehouse[i][index]==shapes[shapesIndex]:
               selectedWarehouse.addShape(warehouse[i][index],warehouse[i][1],warehouse[i][2])
               break
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


        if menuChoice ==1:             
            task1(task1Warehouses)
            input("\nPress any key to continue")
            displayResults(task1Warehouses)

        elif menuChoice ==2:
            task2(task2Warehouses)
            input("\nPress any key to continue")
            displayResults(task1Warehouses)


        
        return menuChoice

def task1(task1Warehouses):
         
        tempWarehouse = Warehouse("temp",2000000000)
        createTempWarehouse(tempWarehouse)
        loadItemsToWarehouseA(tempWarehouse,task1Warehouses)     

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
    return  

def task2(task2Warehouses):
    
    os.system('cls')
    print("\n\n               DAYS TO RELOCATE TASK 2 ITEMS")
    print("               ------------------------------")
    task2data =[]
    loadcsv2('TASK 2(1).csv',task2data)

    van  = Van(1500000000,2000)
    names = getWarehousesNames(task2Warehouses)

    for i in range(0,len(names)-1):
        planTrip(i,i+1,task2data,task2Warehouses)
        deliverItems(van,task2Warehouses[i+1])
        van.resetVan()

def planTrip(startPos,endPos,csvData,Warehouses):

    flag =0
    names = getWarehousesNames(Warehouses)

    for i in range(startPos,len(names)):
        trip = Trip(names[startPos],names[endPos])
        for i in range(0,len(csvData)):

            itemNumber = csvdata[i][0]
            fromWarehouse = csvdata[i][1]
            toWarehouse = csvdata[i][2]

            originIndex = getWarehousePos(Warehouses,start)
            targetIndex = getWarehousePos(Warehouses,end)

            item = createItem(Warehouses[originIndex],itemNumber)
            if flag != targetIndex:
                   fakeWarehouse = copy.deepcopy(Warehouses[targetIndex])
                   flag = targetIndex
            validItem = Warehouses[originIndex].moveItemtoVan(item,temp)
            if validItem != None:
                  trip.addItem(van,validItem)

        endPos+=1
        van.vanTrips.append(trip)

    return

def deliverItems(van,target):

    for i in range (0,len(van.vanTrips)):
        if van.vanTrips[i].targetWarehouse == target:
            for i in van.vanTrips[i].tripItems:
                target.addItem(i,False)           
    return

def getWarehousesNames(Warehouses):
    names =[]
    for i in Warehouses:
        names.append(i.warehouseName)
    return names

def getWarehousePos(Warehouse,targetName):

    for i in range(0,len(Warehouse)):
        if Warehouse[i].warehouseName == targetName:
           break
    return i

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
