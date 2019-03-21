#python libraries
import csv
import os
import pickle
import copy

#global variables
deliveryDays =0
totaldays = 0

class Warehouse(object):

    #default constructor
    def __init__(self,warehouseName=None,remainingInsurance=None):
        #class variables
        self.warehouseName = warehouseName
        self.remainingInsurance = remainingInsurance
        self.warehouseItems =[]
        self.warehouseShapes=[]
        self.overnightSpace =[]
        self.leftItemsTrip = []

    ''' 
    Method name: addItem(self,item,loadFromCsv)
    --> The purpose of this method is to allow items to be added to a warehouse
    --> It checks if a warehouse a warehouse supports an item shape,it goes ahead
        and checks for remaining insurance, at last it checks the item weight and
        quantity. If an item satisfies all the requirements, it is added to warehouse
        otherwise it is rejected and appropriate message is displayed           
    '''
    def addItem(self,item,loadFromCsv):
        for i in self.warehouseShapes:#loops and check for item shape
            if item.itemShape == i.shapeName:
                if item.itemPrice > self.remainingInsurance:#compares item price to insurance
                    print("Item rejected, item %s value exceeds warehouse %s remaining insurance"
                               %(item.itemNumber,
                               self.warehouseName))
                    return False
                #compares item weight 
                elif item.itemWeight > i.storageWeight:
                    #checks shape remaining quantity
                    if i.storageQuantity ==0:
                        print("Item %s rejected, warehouse %s %s remaining storage quantity is %s"
                              %(item.itemNumber,
                                self.warehouseName,
                                i.shapeName,
                                i.storageQuantity))
                        
                    else:
                        print("Items %s rejected, item storage weight exceeds warehouse %s %s capacity %s"
                              %(item.itemNumber,
                                self.warehouseName,
                                i.shapeName,
                                i.storageWeight))
                    return False
                elif i.storageQuantity ==0:
                        print("Item %s rejected, warehouse %s %s remaining storage quantity is %s"
                              %(item.itemNumber,
                                self.warehouseName,
                                i.shapeName,
                                i.storageQuantity))
                        return False
                else:
                    #append item to warehouse items
                    self.warehouseItems.append(item)
                    i.decreaseStorageWeight()
                    self.decreaseWarehouseInsurance(item.itemPrice)
                    if(loadFromCsv==False):
                          print("Item %s added to Warehouse %s"
                          %(item.itemNumber,
                            self.warehouseName))
                    return True
        print("Item %s rejected, warehouse %s cannot accomodate %s shapes"
                   %(item.itemNumber,
                     self.warehouseName,
                     item.itemShape))
        return False

    ''' 
    Method name: displayWarehouse(self) 
    --> This method displays the details of a warehouse
    --> This include displaying warehouse name, insurance, total elements
        and available shapes as well as all the items in the warehouse
    '''
    def displayWarehouse(self):
        os.system('cls')#clears screen
        print("\nWAREHOUSE INFORMATION: ")
        print("---------------------")
        print("  ---> Warehouse Name : %s"%self.warehouseName)
        print("  ---> Total elements : %s"%len(self.warehouseItems))
        print("  ---> Remaining Insurance: £%s"%(self.remainingInsurance))
        print("  ---> Available Shapes: %s"%(self.warehouseShapes))
        self.warehouseItems = self.insertionSort()#sorts warehouse item with insertion
        self.printWarehouseItems()#prints warehouse items

    ''' 
    Method name: binarySearch(self,start,end,itemNumber)
    --> This function looks for item number by comparing it to the middle index value.
    --> If item number is greater than middle index value then set start index to midde index+1      
    --> If item number is less than middle index value then set last index value to middle index -1     
    --> If start index is greater than end index then return -1
    --> If item is found then  return index.    
    '''
    def binarySearch(self,start,end,itemNumber):

        self.warehouseItems = self.insertionSort()#sorts warehouse item
        while end>=start:     
           middle = start+(end-start)/2#calculate middle value
           middle = int(middle)      
           if itemNumber==self.warehouseItems[middle].itemNumber:#compares for correct value
              return middle
           else:           
              if self.warehouseItems[middle].itemNumber>itemNumber:
                 end = middle-1
              else : 
                start = middle+1             
        else:        
          #print("An item with the id '%s' does not exits in the records."%itemNumber)       
          return -1

    ''' 
    Method name: moveItemtoVan(self,item,van,target)
    --> This method checks if a warehouse item can be moved to a warehouse
    --> It compares the item price and weight with the the van
    --> If item can be moved it returns True otherwise false
    '''
    def moveItemtoVan(self,item,van,target):
       #compares item price 
      if item.itemPrice > van.remainingInsurance:
          print("Van rejects item '%s', item price %s exceeds Van remaining insurance %s"
                 %(item.itemNumber,
                   item.itemPrice,
                   van.remainingInsurance))
      #compares item weight
      elif item.itemWeight > van.remainingWeightCapacity:
          print("Van rejects item '%s', item's storage weight '%s' exceeds Van's remaining weight capacity %s"
                %(item.itemNumber,               
                  item.itemWeight,
                  van.remainingWeightCapacity))          
      else:
          success = van.addItemtoTarget(item,target,self)
          return success

    '''
    Method name:insertionSort(self)
    --> This method sorts warehouse items by using insertion sort
    --> Assuming its sorting in ascending order:
     1 - It begins by asssuming that th element at position 0 is already sorted.
     2 - It compares element at position j to element at position i and swaps them if j is greater
     3 - It then compares the new element at position j to j-1 and swap the elements until we reacha smaller
         element at the beginning of the warehouse list.
       - It then repeats the above 3 steps until the warehouse list is finally sorted.
    '''
    def insertionSort(self):
        j=0   
        swapList=[]
        for i in range(1,len(self.warehouseItems)):    
            #inserts element at position 1 to swap list
            swapList.insert(0,self.warehouseItems[i])
            j =i-1 
            #compares item number of swap list to warehouse and swap is bigger
            while swapList[0].itemNumber < self.warehouseItems[j].itemNumber and j>=0:
                    self.warehouseItems[j+1] = self.warehouseItems[j]#keep swapping until bigger value found
                    j=j-1
            self.warehouseItems[j+1] = swapList[0]
        return self.warehouseItems

    '''
    Method name: printWarehouseItems(self)
    --> This method prints all the items belonging to a warehouse
    '''
    def printWarehouseItems(self):
        print("\nItem No.  Description                                   Price       Shape      Weigth(kg)")
        print("--------  -----------                                   -----       -----      ------\n")
        for i in self.warehouseItems:
            print(i)
    '''
    Method name: printGarage(self)
    --> This method prints all items on the van aka garage
    '''
    def printGarage(self):
        print("Item No.  Description                                   Price       Shape      Weigth(kg)")
        print("--------  -----------                                   -----       -----      ------")
        for i in self.overnightSpace:
            for x in i:#prints item
                for m in x.tripItems:
                    print(m)
    '''
    Method name: addShape(self,shapeName,weight,quantity)
    --> Method allows a new shape to be added to warehouse
    --> It creates an itemShapes shape object with contains shape weight
        weight and name
    --> The created shape is then added warehouse shapes
    '''
    def addShape(self,shapeName,weight,quantity):
        temp = itemShapes(shapeName,weight,quantity) #creates itemshapes object
        self.warehouseShapes.append(temp)
    
    '''
    Method name: increaseShapeValue(self,item)
    --> This method increases the shape value of warehouse shape
    '''
    def increaseShapeValue(self,item):
        for i in range(0,len(self.warehouseShapes)):#find correct item shape and increment value
            if(item.itemShape == self.warehouseShapes[i].shapeName):
                self.warehouseShapes[i].increaseStorageWeight()
                break
    '''
    Method name: decreaseShapeValue(self,item)
    --> This method decreases the shape value of warehouse shape
    '''
    def decreaseShapeValue(self,item):
        for i in range(0,len(self.warehouseShapes)):#find correct item shape and decrement value
            if(item.itemShape == self.warehouseShapes[i].shapeName):
                self.warehouseShapes[i].decreaseStorageWeight()
                break
    '''
    Method name: increaseWarehouseInsurance(self,amount)
    --> This method increases the remaining insurance of a warehouse
    '''
    def increaseWarehouseInsurance(self,amount):
        self.remainingInsurance+=amount
      
    
    '''
    Method name: decreaseWarehouseInsurance(self,amount)
    --> This method decreases the remaining insurance of a warehouse
    '''
    def decreaseWarehouseInsurance(self,amount):
        self.remainingInsurance-=amount
      
    
    '''
    Method name: getWarehouseName(self)
    --> This method returns warehouse name
    '''
    def getWarehouseName(self):
        return self.warehouseName

    '''
    Method name: getWarehouseRemainingInsurance(self)
    --> This method returns warehouse remaining warehouse insurance
    '''
    def getWarehouseRemainingInsurance(self):
        return self.remainingInsurance

    #converts object to string
    def __str__(self):
         return "%s %s"%(self.warehouseName,self.remainingInsurance)

    #converts object to string
    def __repr__(self):
         return "%s %s"%(self.warehouseName, self.remainingInsurance)

class Item():
    
    #constructor
    def __init__(self,itemNumber=None,itemDescription=None,
                  itemPrice=None,itemShape = None,itemWeight =None):
        #class variables
        self.itemNumber = itemNumber
        self.itemDescription =itemDescription
        self.itemPrice = itemPrice
        self.itemShape = itemShape
        self.itemWeight = itemWeight
    
    #converts object to string
    def __str__(self):
        return "%-8s  %-45s £%-10s %-10s %s "%(self.itemNumber,self.itemDescription,self.itemPrice,
                                          self.itemShape,self.itemWeight)
    #converts object to string
    def __repr__(self):
        return "%s %s %s %s %s"%(self.itemNumber,self.itemDescription,self.itemPrice,
                                         self.itemShape,self.itemWeight)

class itemShapes():
    
    #constructor
    def __init__(self,shapeName=None,storageWeight=None,storageQuantity=None):
        self.shapeName = shapeName
        self.storageWeight = storageWeight
        self.storageQuantity = storageQuantity
    
    '''
    Method name:
    --> This method decreases storage quantity by one
    '''
    def decreaseStorageWeight(self):
        self.storageQuantity-=1
    
    '''
    Method name:
    --> This method increases storage quantity by one
    '''
    def increaseStorageWeight(self):
        self.storageQuantity+=1
    
    #converts object to string    
    def __str__(self):
         return "%s %s %s"%(self.shapeName,self.storageWeight,self.storageQuantity)
    #converts object to string
    def __repr__(self):
        return "%s %s %s"%(self.shapeName,self.storageWeight,self.storageQuantity)

class Van():

    #default constructor
    def __init__(self,remainingInsurance=None,remainingWeightCapacity=None):

        #class variables
        self.remainingInsurance = remainingInsurance
        self.remainingWeightCapacity = remainingWeightCapacity
        self.vanItems=[]
        self.vanTrips=[]
    
    '''
    Method name: addItem(self,vanItem)
    --> This method allows a new item to be added on the van
    --> It checks the item weight and insurance and adds item if possible
        It decreases van insurance and weight capacity by item number and weight
    '''
    def addItem(self,vanItem):
        #checks item weigh
        if vanItem.itemWeight > self.remainingWeightCapacity:
            print("Item weight exceeds van capacity")
        #checks item price
        elif vanItem.itemPrice > self.remainingInsurance:
            print("Item price exceeds van capacity")
        else:
            #adds item to van 
            self.vanItems.append(vanItem)
            self.decreaseRemainingInsurance(vanItem.itemPrice)
            self.decreaseRemainingWeightCapacity(vanItem.itemWeight)
            print("Van picks-up item %s "%(vanItem.itemNumber))

    '''
    Method name: addItemtoTarget(self,item,target,origin)
    --> This method checks if an item can be added to a target warehouse
        before boarding the van
    --> It checks the shape of the item, the price the item weight and remainging quantity
        of the target warehouse 
    --> If item can be added it removes it origin warehouse and adds onto the van

    '''
    def addItemtoTarget(self,item,target,origin):
        x =0  
        #checks for item shape
        for i in range(0,len(target.warehouseShapes)):
          if target.warehouseShapes[i].shapeName == item.itemShape:
              x =i
              break
          #compares price
        if item.itemPrice > target.remainingInsurance:
          print("Van rejects item '%s', item price exceeds warehouse '%s' remaining insurance"
                 %(target.warehouseName,item.itemNumber))
        #compares item weight
        elif item.itemWeight > target.warehouseShapes[x].storageWeight:
          print("Van rejects item '%s' from warehouse %s, storage weight '%s' exceeds warehouse '%s' '%s' capacity '%s'"
                %(item.itemNumber,
                  origin.warehouseName,
                  item.itemWeight,
                  target.warehouseName,
                  item.itemShape,
                  target.warehouseShapes[x].storageWeight))
        #checks remaining quantity of item shape
        elif target.warehouseShapes[x].storageQuantity ==0:
          print("Van rejects item '%s from warehouse %s',warehouse '%s' '%s' storage quantity remaining is '%s' "
                %(item.itemNumber,
                  origin.warehouseName,
                  target.warehouseName,
                  item.itemShape,                                             
                  target.warehouseShapes[x].storageQuantity))
        else:
          position = 0   
          #search for item and remove it from origin warehouse
          position = origin.binarySearch(0,len(origin.warehouseItems),item.itemNumber)
          if position >= 0:
             temp = origin.warehouseItems.pop(position)
             origin.increaseWarehouseInsurance(temp.itemPrice)
             origin.increaseShapeValue(temp)             
             target.warehouseShapes[x].decreaseStorageWeight()
             print("Van picks-up item %s for warehouse %s "%(item.itemNumber,target.warehouseName))
             return temp

    '''
    Method name: resetVan(self)
    --> This method resets the van
    '''
    def resetVan(self):
        self.remainingInsurance = 1500000000
        self.remainingWeightCapacity = 2000
        self.vanTrips = []
        self.vanItems = []
    '''
    Method name: decreaseRemainingInsurance(self,price)
    --> This method decreases remainig insurance value of the van
    '''
    def decreaseRemainingInsurance(self,price):
        self.remainingInsurance-= price

    '''
    Method name: decreaseRemainingWeightCapacity(self,weight)
    --> This method decreases remainig weight capacity of the van
    '''     
    def decreaseRemainingWeightCapacity(self,weight):
        self.remainingWeightCapacity -= weight
    
    
    '''
    Method name: printVanItems(self)
    --> This method prints items on the van
    '''  
    def printVanItems(self):
        print("\nItem No.  Description                                   Price       Shape      Weight(kg)")
        print("--------  -----------                                   -----       -----      ------\n")
        for i in self.vanTrips:
            for x in i.tripItems:#print item
              print(x)
    #converts object to string 
    def __str__(self):
         return "%s %s"%(self.remainingWeightCapacity,self.remainingInsurance)
    #converts object to string 
    def __repr__(self):
         return "%s %s"%(self.remainingWeightCapacity, self.remainingInsurance)

class Trip():

    #default constructor
    def __init__(self,startWarehouse=None,targetWarehouse=None):
        self.startWarehouse = startWarehouse
        self.targetWarehouse = targetWarehouse
        self.tripItems=[]        
    
    '''
    Method name: addItem(self,van,item)
    --> This method adds item to a trip
    --> It then decreases van remaining insurance and remaining capacity by the item
    '''
    def addItem(self,van,item):
            self.tripItems.append(item)#add item to trip items
            van.decreaseRemainingInsurance(item.itemPrice)
            van.decreaseRemainingWeightCapacity(item.itemWeight)
    #converts object to string        
    def __str__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)
    #converts object to string 
    def __repr__(self):
        return "%s %s"%(self.startWarehouse,self.targetWarehouse)
'''
Function name: main()
--> This function contains the main menu of the program
--> It creates warehouses and loads csv file to them
--> It repeats until user decides to quit program
'''
def main():

    menuChoice = 0
    global totaldays
    #creates warehouses
    Warehouses = createWarehouses()
    readcsvFiletoWarehouse(Warehouses)#read csv data
    
    #repeats until choice =5
    while(menuChoice!=5): 
        totaldays = 0    
        mainMenu()#display main menu
        menuChoice = getValidInteger(1,5)
        menuSelection(menuChoice,Warehouses)       
    return

'''
Function name: createWarehouses()
--> This function creates 4 warehouses starting from letter A
--> It then sets up shapes for each warehouse
--> It then returns a list of warehouses created
'''
def createWarehouses():

    Warehouses = []
    WarehouseName = 'A'

    #loop 4 times and craeate 4 warehouses
    for i in range(0,4):
        Warehouses.append(Warehouse(WarehouseName,2000000000))#create warehouse object
        WarehouseName = chr(ord(WarehouseName)+1)#increment character

    setupItemShapes(Warehouses)#setup shapes
    return Warehouses

'''
Function name: setupItemShapes(Warehouses)
--> This function setups appropriate shapes for each warehouse
'''
def setupItemShapes(Warehouses):

    warehouseShapes = []
    #appends shapes to warehouse shapes list
    warehouseShapes.append([['Rectangle',1000,5],['Pyramid',2000,10],['Square',2000,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',2000,5],['Pyramid',250,10]])
    warehouseShapes.append([['Sphere',250,15],['Pyramid',500,5]])
    warehouseShapes.append([['Rectangle',500,10],['Sphere',750,2],['Pyramid',3000,2],['Square',750,10]])

    for i in range(0,4):
      setShapesValues(warehouseShapes[i],Warehouses[i])

'''
Function name: setShapesValues(warehouse,selectedWarehouse)
--> This fuctions sets up warehouse shapes for each warehouse
--> It adds shapes to warehouse by calling the method addshape in Warehouse class
'''
def setShapesValues(warehouse,selectedWarehouse):

    shapesIndex=0
    index=0
    #available shapes
    shapes = ['Rectangle','Sphere','Pyramid','Square']

    for i in range(0,len(warehouse)):
        for shapesIndex in range(0,len(shapes)):
            if warehouse[i][index]==shapes[shapesIndex]:#compares shapes
                #adds shapes to warehouse
               selectedWarehouse.addShape(warehouse[i][index],warehouse[i][1],warehouse[i][2])
               break
    return

'''
Function name: readcsvFiletoWarehouse(Warehouses)
--> This fuctions loads csvs file data into warehouse depending on the index
'''
def readcsvFiletoWarehouse(Warehouses):

    loadcsv('Warehouse A.csv',Warehouses,0,False)
    loadcsv('Warehouse B.csv',Warehouses,1,False)
    loadcsv('Warehouse C.csv',Warehouses,2,False)
    loadcsv('Warehouse D.csv',Warehouses,3,False)

'''
Function name: loadcsv(csvFilename,Warehouses,index,task1)
--> This fuctions reads csvs file data into warehouse depending on the index
--> If task 1 is true it adds an item to warehouse based on the index value
--> If task 1 is false it tries to add item to warehouse,
    if it fails it will add to the next warehouses.
--> If no warehouse can accomodate the item it rejects it
'''
def loadcsv(csvFilename,Warehouses,index,task1):
    
    try:
        with open(csvFilename) as csvFile:#open csv file
                  reader = csv.reader(csvFile)
                  next(reader,None)#skips header
                  for itemnumber,itemdescription,itemprice,itemShape,itemWeigth in reader: 
                      start = 0
                      #creat item object
                      newItem = Item(int(itemnumber),itemdescription,int(itemprice),itemShape,int(itemWeigth))
                      if task1 ==False:
                        Warehouses[index].addItem(newItem,True)                        
                      else:
                          #attempts to add item to warehouses until success is True
                          success = Warehouses[start].addItem(newItem,False)
                          while success==False:
                              start+=1
                              if start == index:
                                 break
                              success = Warehouses[start].addItem(newItem,False)                             
    except FileNotFoundError:
          print(FileNotFoundError)
    return

'''
Function name: loadcsv2(csvFilename,task2data)
--> This function opens a csv file and appends data read into a list
    which will contain all the data read
'''
def loadcsv2(csvFilename,task2data):        
    try:
        with open(csvFilename) as csvFile:#open csv file
                  reader = csv.reader(csvFile)
                  next(reader,None)#skip header
                  for itemNumber,selectedWarehouse,targetWarehouse in reader:
                      #append data read to list
                      temp =[]
                      itemNumber = int(itemNumber)
                      temp.append(itemNumber)
                      temp.append(selectedWarehouse)
                      temp.append(targetWarehouse)                      
                      task2data.append(temp)

    except FileNotFoundError:
          print(FileNotFoundError)
    return

'''
Function name: mainMenu()
--> This function displays the main menu of the program
'''
def mainMenu():

    os.system('cls')
    print("            MAIN MENU")
    print("            ---------\n")
    print("     1 --> Load task 1 items to warehouses")
    print("     2 --> Days to relocate task 2 items")
    print("     3 --> Minimum number of trips")
    print("     4 --> Deliver by Shapes")
    print("     5 --> Quit")
    print("\nSelect task(1-5): ")

'''
Function name: menuSelection(menuChoice,Warehouses)
--> This function selects menu option based on user input
--> It deep copies default warehouses values every time for a fresh start
--> It then displays the final changes made by each task selection
'''
def menuSelection(menuChoice,Warehouses):
                             
        if menuChoice ==1:
            task1Warehouses = copy.deepcopy(Warehouses)#deep copy default warehouses
            task1(task1Warehouses)
            input("\nPress any key to continue")
            displayResults(task1Warehouses)#displays final changes

        elif menuChoice ==2:
            task2Warehouses = copy.deepcopy(Warehouses)
            task2(task2Warehouses)
            input("\nPress any key to continue")
            displayResults(task2Warehouses)

        elif menuChoice ==3:
            task3Warehouses = copy.deepcopy(Warehouses)
            task3(task3Warehouses)
            input("\nPress any key to continue")
            displayResults(task3Warehouses)
       
        elif menuChoice ==4:
            task4Warehouses = copy.deepcopy(Warehouses)
            task4(task4Warehouses)
            input("\nPress any key to continue")
            displayResults(task4Warehouses)
     
        return menuChoice

'''
Function name: task1(task1Warehouses)
--> This function loads task 1 csv items through warehouse A
'''
def task1(task1Warehouses): 
    os.system("cls")
    print("\n\n    LOAD ITEMS THROUGH WAREHOUSE A")
    print("    ------------------------------\n")
    loadcsv('DATA TO INSERT INTO WAREHOUSE A.csv',task1Warehouses,4,True)

'''
Function name: task2(task2Warehouses)
--> This calculates days required to relocate task 2 items 
--> It first read task 2 data
--> It gets the names of the warehouses and draws plan by taking a warehouse
    and its nearest neighbour
--> It then delivers items on the van to target warehouses
'''
def task2(task2Warehouses):    
    os.system('cls')
    print("\n\n               DAYS TO RELOCATE TASK 2 ITEMS")
    print("               ------------------------------")
    task2data =[]
    itemTypes = []
    loadcsv2('TASK 2(1).csv',task2data)#reads movement from csv data
    global deliveryDays

    van  = Van(1500000000,2000)#creates van object
    names = getWarehousesNames(task2Warehouses)#gets warehouses names

    for i in range(0,len(names)-1):
        print("\n---------  - -------")
        print("WAREHOUSE: %s pickups"%(names[i]))
        print("---------  - -------")
        tripPlan(i,i+1,task2data,task2Warehouses,van,itemTypes,False)#draws plan for moving items   
        deliverItems(van,task2Warehouses,i+1)#delivers items on the van
        van.resetVan()#resets van

    deliveryDays=0

'''
Function name: createItem(targetWarehouse,itemID)
--> This function returns an item by searching it through binary search method
    designed in the warehouse class
--> It searches the item by using the item id
'''
def createItem(targetWarehouse,itemID):  
    #gets position of item
    i = targetWarehouse.binarySearch(0,len(targetWarehouse.warehouseItems)-1,itemID)
    item = targetWarehouse.warehouseItems[i]
    return item

'''
Function name: deliverItems(van,Warehouses,position)
--> This function delivers items on the van to destination warehouses
--> If a delivery is to be made it increments delivvery days by 1
'''
def deliverItems(van,Warehouses,position):
    global deliveryDays
    names = getWarehousesNames(Warehouses)#gets warehouses name
    for i in range (0,len(van.vanTrips)):
        if van.vanTrips[i].targetWarehouse == names[position]:#compares targets name
            if len(van.vanTrips[i].tripItems) > 0:
                deliveryDays+=1
                print("\nDay: %s"%(deliveryDays))
                print("---  -")
                for x in van.vanTrips[i].tripItems:
                    Warehouses[position].addItem(x,False)  #adds item to warehouse
        position+=1
        
    return

'''
Function name: getWarehousesNames(Warehouses)
--> This function returns the names of all the warehouses
'''
def getWarehousesNames(Warehouses):
    names =[]
    for i in Warehouses:
        names.append(i.warehouseName)#appends warehouses names
    return names

'''
Function name: getWarehousesNames(Warehouses)
--> This function returns the position of a warehouse based on warehouse name
'''
def getWarehousePos(Warehouse,targetName):
    #loops and compares warehouses name to targetname
    for i in range(0,len(Warehouse)):
        if Warehouse[i].warehouseName == targetName:
           break
    return i#returns position

'''
Function name: task3(task3Warehouses)
--> This function draws the plan for items that are to be moved in task 3
    csv file
--> It first read the movements into an empty list
--> It plans the trip by taking the first warehouse and its nearest neighbour
--> It collects all the items to be delivered to neighbours and delivers them in 2 trips
    Two trips makes up a day.
--> It records the information of the items delivered to prevent items for moving into 2 
    different warehouses on the same day
'''
def task3(task3Warehouses):

    #local variables
    global totaldays
    deliveredItems = []
    task3data = []
    trip = 0       
    van = Van(1500000000,2000)#van object
    names = getWarehousesNames(task3Warehouses)#gets warehouses name

    os.system('cls')
    print("          TASK 3")
    print("          ------\n")
    loadcsv2("TASK 3.csv",task3data)

    for i in range(0,len(names)-1): 
        if trip%2==0:
            totaldays+=1#incremenst day if remainder of trip is 0
            print("\nDay:",totaldays)
            print("---  -")
        print("\n---------  - -------")
        print("WAREHOUSE: %s pickups"%(names[i]))
        print("---------  - -------")
        #plan trip by taking index of i in warehouse names and nearest neighbour
        tripPlan(i,i+1,task3data,task3Warehouses,van,deliveredItems,False)
        if trip%2!=0:
            #prevents items from being moved twice in a day
            removeItemsSameDay(deliveredItems,task3Warehouses[i],van)
        print("\n --> Van moves to warehouse %s\n"%(names[i+1]))
        #delivers items left overnight
        deliverOvernightItems(task3Warehouses[i],task3Warehouses[i+1],names[-1])
        #keeps record of delivered items
        deliveredItems = deliverItems2(van.vanTrips,task3Warehouses[i+1],names[-1])
        trip+=1
        van.resetVan()
    
    #deliver items which can not be deliverd twice a day    
    deliverLeftOvers(task3Warehouses)


'''
Function name: deliverItems2(trips,selectedWarehouse,lastWarehouse)
--> This function adds trips items to target warehouses
--> It then adds the rest of trip items to the target warehouse
    so they can delivered on the next delivery
'''
def deliverItems2(trips,selectedWarehouse,lastWarehouse):
    deliveredItems =[]
    flag = False
    for i in trips:
        #delivers items to target Warehouse
        if i.targetWarehouse == selectedWarehouse.warehouseName:          
            for x in i.tripItems:
                selectedWarehouse.addItem(x,False)
                deliveredItems.append(x.itemNumber)
            break   
    #adds remaining trips tp target warehouse    
    selectedWarehouse.overnightSpace.append(trips[1:])
    if selectedWarehouse.warehouseName !=lastWarehouse:
        for i in selectedWarehouse.overnightSpace:
            for x in i:
                if len(x.tripItems) > 0:
                    flag = True
    if flag == True:
         print(" --> Following items left on the van: \n")
         selectedWarehouse.printGarage()               
    return deliveredItems

'''
Function name: deliverOvernightItems(Warehouse,target,lastWarehouse)
--> This function delivers items which were left on the van overnight in the garage
--> It compares the target warehouse of trips to target selected warehouse and if 
    there's a match it adds item to selected target warehouse
--> It then adds the remaining items from overnight to the target warehouse
'''
def deliverOvernightItems(Warehouse,target,lastWarehouse):
    if len(Warehouse.overnightSpace) > 0: 
        #checks lenght of items left behind
        for i in range(0,len(Warehouse.overnightSpace)):
            #compares trip target warehouse with target warehouse
            if Warehouse.overnightSpace[i][0].targetWarehouse == target.warehouseName:               
               for x in Warehouse.overnightSpace[i][0].tripItems:
                    target.addItem(x,False)#adds item to target      
               if target.warehouseName !=lastWarehouse:
                    del Warehouse.overnightSpace[i][0]#delete delivered items from overnight                 
                    target.overnightSpace.extend(Warehouse.overnightSpace)
                    break   
    return

'''
Function name: removeItemsSameDay(deliveredItems,targetWarehouse,van)
--> This function prevents items from being delivered twice in a single day
--> It compares the item number 
'''
def removeItemsSameDay(deliveredItems,targetWarehouse,van):
   
    dev = 0
    leftItems =[]

    if len(deliveredItems) > 0:
        for i in van.vanTrips:  
           for x in range(0,len(i.tripItems)):         
               if i.tripItems[x].itemNumber == deliveredItems[dev]:
                   print("Van drops item %s, same day delivery not allowed"%(deliveredItems[dev])) 
                   dev+=1
                   item = i.tripItems.pop(x)
                   leftItems.append(item)
                   if dev == len(deliveredItems):
                       trip = Trip(i.startWarehouse,i.targetWarehouse)
                       trip.tripItems.extend(leftItems)
                       targetWarehouse.leftItemsTrip.append(trip)
                       return
'''
Function name: deliverLeftOvers(Warehouses)
--> This function delivers the items which could not be moved twice 
    in the days to the appropriate warehouses
--> It checks if there are leffovers, it picks-up leftover item
    and moves to the target location and delivers items
'''                    
def deliverLeftOvers(Warehouses):
    global totaldays
    for i in range(0,len(Warehouses)):
        #checks if any leftovers
        if len(Warehouses[i].leftItemsTrip) > 0:
            totaldays+=1
            print("\nDay:",totaldays)
            print("---  -")
            print("\n --> Van starts at Warehouse %s"%(Warehouses[i].warehouseName))
            print("---------  - -------")
            print("WAREHOUSE: %s pickups"%(Warehouses[i].warehouseName))
            print("---------  - -------")
            for x in Warehouses[i].leftItemsTrip:
                for y in x.tripItems:
                    print("Van picks-up item %s"%(y.itemNumber))
            #moves to target warehouse and delivers items
            print("\n --> Van moves to warehouse %s\n"%(x.targetWarehouse))
            position = getWarehousePos(Warehouses,x.targetWarehouse)            
            deliverItems2(Warehouses[i].leftItemsTrip,Warehouses[position],Warehouses[-1].warehouseName)


'''
Function name: task4(task4Warehouses)
--> This function draws the plan for items that are to be moved in task 3
    csv file for task 4 
--> It first read the movements into an empty list
--> It plans the trip by taking the first warehouse and its nearest neighbour
--> It collects all the items by shape that are to be delivered to neighbours 
    and delivers them in 2 trips. Two trips makes up a day.
--> It records the information of the items delivered to prevent items for moving into 2 
    different warehouses on the same day
'''
def task4(task4Warehouses):
    #local variables
    global totaldays
    deliveredItems = []
    task4data = []
    itemTypes =['Rectangle','Pyramid','Sphere','Square']
    trip = 0
    days =0    
    van = Van(1500000000,2000)#van object
    names = getWarehousesNames(task4Warehouses)#collect warehouses names

    os.system('cls')
    print("          TASK 4")
    print("          ------\n")
    loadcsv2("TASK 3.csv",task4data)#load csv

    for x in range(0,len(itemTypes)): 
        totaldays+=1
        print("\nDay %s"%(totaldays))
        print("--- -")      
        print("%s PICK-UPS"%(itemTypes[x].upper()))              
        for i in range(0,len(names)-1):
            if trip%2==0:#starts new day if remainder is 0
                    print("---------  - -------")                    
                    print("WAREHOUSE: %s pickups"%(names[i]))
                    print("---------  - -------") 
            #plans route by item shape        
            tripPlan(i,i+1,task4data,task4Warehouses,van,itemTypes[x],True)
            if trip%2!=0:
                removeItemsSameDay(deliveredItems,task4Warehouses[i],van)
            print("\n --> Warehouse %s\n"%(names[i+1])) 
            #deliver items left overnight
            deliverOvernightItems(task4Warehouses[i],task4Warehouses[i+1],names[-1])
            #delivers and keeps record of items delivered in a trip
            deliveredItems = deliverItems2(van.vanTrips,task4Warehouses[i+1],names[-1])
            if len(deliveredItems) > 0:
                trip+=1
            van.resetVan()
        #delivers same day delivery items     
        deliverLeftOvers(task4Warehouses)
        emptyWarehouse(task4Warehouses)     
        

'''
Function name: tripPlan(startPos,endPos,csvData,Warehouses,van,itemTypes,task4)
--> This plans the route of items to be moved from one warehouse to another
--> It creates a trip for every new end position and appends item to be the
    moved to the trip's warehouse item list
'''
def tripPlan(startPos,endPos,csvData,Warehouses,van,itemTypes,task4):

    global deliveryDays
    flag =0
    names = getWarehousesNames(Warehouses)#gets warehouses names

    for x in range(startPos,len(names)-1):
        #creates trip object with starting and ending warehouse
        trip = Trip(names[startPos],names[endPos])
        for i in range(0,len(csvData)):
                '''read csv to variables '''
                itemNumber = csvData[i][0]
                fromWarehouse = csvData[i][1]
                toWarehouse = csvData[i][2]             
                if fromWarehouse == names[startPos] and toWarehouse == names[endPos]:   
                    #creates item object
                    item = createItem(Warehouses[startPos],itemNumber)
                    #creats a copy of current warehouse to compare items to be added values
                    if flag != endPos:                 
                           fakeWarehouse = copy.deepcopy(Warehouses[endPos])
                           flag = endPos
                    if task4 == True:
                        #delivers items by shape if task 4 is true
                        if item.itemShape == itemTypes:
                            validItem = Warehouses[startPos].moveItemtoVan(item,van,fakeWarehouse)
                            if validItem != None:                      
                               trip.addItem(van,validItem)
                    else:
                        #adds selected item to trip if valid
                        validItem = Warehouses[startPos].moveItemtoVan(item,van,fakeWarehouse)
                        if validItem != None:                      
                           trip.addItem(van,validItem)
        #increment end position
        endPos+=1
        #add trip to van
        van.vanTrips.append(trip)

'''
Function name: emptyWarehouse(Warehouses)
--> This function resets the van attributes to avoid duplicates for each
    target warehouse
'''
def emptyWarehouse(Warehouses):
    for i in range(0,len(Warehouses)):
        Warehouses[i].overnightSpace =[]
        Warehouses[i].leftItemsTrip =[]

'''
Function name: emptyWarehouse(Warehouses)
--> This function displays the warehouses to be selected 
'''        
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

'''
Function name: allWarehousesDetails(Warehouses)
--> This function displays the details of all the warehouses in the system
''' 
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



'''
Function name:  displayResults(Warehouses)
--> This function displays a warehouse
--> It repeats until user decides to quit
''' 
def displayResults(Warehouses):
      
      #displays until choice is N
      displayAnother ='Y'
      while displayAnother =='Y':
              displayWarehouses(Warehouses)#displays warehouses selection
              warehouseChoice = getValidInteger(1,5)
              if warehouseChoice == 5:
                 break
              else:
                 Warehouses[warehouseChoice-1].displayWarehouse()
                 print("\nDisplay another warehouse?(Y/N): ")
                 displayAnother = getValidYesOrNo()

'''
Function Name: getValidYesOrNo()
  --> Prompts user to input a choice which is either Y or N
  --> Display error message if incorrect character is inputted
'''
def getValidYesOrNo():

    flag =True
    while flag:
        #prompts user to input Y or N
        yes_or_no = input(" ")
        if yes_or_no.upper() == 'Y' or yes_or_no.upper() == 'N':
           return yes_or_no.upper()
        else:
          print("Wrong input,enter Y OR N: ")

'''
Function Name: getValidInteger(minimum,maximum)

  --> Prompts user to input a valid integer value.
  --> It then check the maximum and minimum values.
'''
def getValidInteger(minimum,maximum):

        flag =True
        while flag == True:
             number= input("")   
             try:
                  #checks if input is valid integer
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