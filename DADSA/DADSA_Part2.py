import csv
import os
import pickle
import copy

class Item():


    #default constructor
    def __init__(self,item_number=None,itemDescription=None,
                  item_price=None,itemShape = None,itemWeigth =None):

        self.itemNumber = item_number
        self.itemDescription =itemDescription
        self.itemPrice = item_price
        self.itemShape = itemShape
        self.itemWeigth = itemWeigth
 
   
    def __str__(self):
        return "%-8s  %-45s £%-10s %-10s %s "%(self.itemNumber,self.itemDescription,self.itemPrice,
                                          self.itemShape,self.itemWeigth)
    
    def __repr__(self):
        return "%s %s %s %s %s"%(self.itemNumber,self.itemDescription,self.itemPrice,
                                         self.itemShape,self.itemWeigth)

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
                  if i.storageQuantity > 0 and i.storageWeigth >= warehouseItem.itemWeigth:
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

    def addShape(self,shapeName,weigth,quantity):
        temp = storageShapes(shapeName,weigth,quantity) 
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
    
    def __init__(self,shapeName=None,storageWeigth=None,storageQuantity=None):
        self.shapeName = shapeName
        self.storageWeigth = storageWeigth
        self.storageQuantity = storageQuantity
    
    def decreaseStorageWeigth(self):
        self.storageQuantity-=1

    def increaseStorageWeigth(self):
        self.storageQuantity+=1
        
    def __str__(self):
         return "%s %s %s"%(self.shapeName,self.storageWeigth,self.storageQuantity)

    def __repr__(self):
        return "%s %s %s"%(self.shapeName,self.storageWeigth,self.storageQuantity)

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
    warehouseShapes.append([['Rectangle',500,10],['Sphere',2000,2],['Pyramid',250,10]])
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
    Warehouses = createWarehouses()
    readcsvFiletoWarehouse(Warehouses)
    Warehouses[0].displayWarehouse()

  
    return

def readcsvFiletoWarehouse(Warehouses):

    tempWarehouse = Warehouse("temp",2000000000)
    createTempWarehouse(tempWarehouse)

    loadcsv('Warehouse A.csv',Warehouses[0])
    loadcsv('Warehouse B.csv',Warehouses[1])
    loadcsv('Warehouse C.csv',Warehouses[2])
    loadcsv('Warehouse D.csv',Warehouses[3])
    loadcsv('DATA TO INSERT INTO WAREHOUSE A.csv',tempWarehouse)
    
    loadItemsToWarehouseA(tempWarehouse,Warehouses)
    input()

def createTempWarehouse(tempWarehouse):

    tempWarehouse.addShape('Rectangle',2000,10)
    tempWarehouse.addShape('Square',2000,10)
    tempWarehouse.addShape('Sphere',2000,10)
    tempWarehouse.addShape('Pyramid',2000,10)

def loadItemsToWarehouseA(tempWarehouse,Warehouses):

    itemAdded = True

    os.system('cls')
    print("\n")
    print("    TASK A 'Load Items through Warehouse A'")
    print("    ---------------------------------------\n")

    for i in range(0,len(tempWarehouse.warehouseItems)):
        for j in range(0,4):
            itemAdded = Warehouses[j].addItem(tempWarehouse.warehouseItems[i],False)
            if itemAdded == True:                
                break        
    return

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

main()