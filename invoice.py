
# constants
VAT_RATE = 0.22
DISCOUNT1 = 0.1
DISCOUNT_THRESHOLD1 = 20
DISCOUNT2 = 0.2
DISCOUNT_THRESHOLD2 = 50
RATES = {'EUR':1.0, 'GBP':0.88, 'USD':1.09}


def loadStock(stockFile):
    '''
    Load data from stock file into data list.
    Each line of the file holds name and price
    This information is loaded into a list which holds a list of id, name and price for each item.
    data = [ [id, name, price], ... ]
    '''
    data = []
    with open(stockFile) as f:
        for line in f:
            if line.strip() == "": continue
            ls = line.split(',')
            data.append([ls[0].strip(), float(ls[1].strip()), int(ls[2].strip()) ])
    return data


def itemList(stock):
    '''
    This prints out the list of items, prefixed with each item id
    The item id can be used to select the required item
    '''
    fItemList = []
    for idx, item in enumerate(stock):
        fItemList.append( f"{idx+1} : {item[0]}\n" )
    return fItemList


def getItemName(stock, selectedItem):
    '''
    Returns the item name from the stock data structure for the selected line.
    '''
    return stock[selectedItem][0]

def getItemNumber(stock, itemName):
    for idx, n in enumerate(stock):
        if n[0] == itemName:
            return idx
            break
    return -1


def getPrice(stock, selectedItem):
    '''
    Returns the price for the given item from the stock data structure. 
    '''
    price = stock[selectedItem][1]
    return price

def availableQuantity(stock, selectedItem):
    '''
    Returns the available quantity for the selected stock
    '''
    quantity = stock[selectedItem][2]
    return quantity

def getCurrencyValue(amount, ccy, dp=2):
    '''
    Takes the currency code (EUR, GBP, USD and looks up the rate for the ccy)
    The ccy amount is rounded according to the number of decimal points defined in dp (defaults to 2)
    '''
    rate = RATES[ccy]
    return round( amount*rate, dp)


def adjustStockQuantity(stock, selectedItem, changeInQuantity):
    '''
    update the value of the stock for the selected item
    '''
    stock[selectedItem][2] += changeInQuantity
    

def saveStockData(filename, stock):
    '''
    stores the stock data back to disk.
    This will store the updated stock quantities
    '''
    with open(filename, 'w') as f:
        for line in stock:
            f.writelines( f"{line[0]},{line[1]},{line[2]}\n" )


def saveOrderToFile(filename, orderDetails):
    '''
    Save the invoice data in the order file - append to end of file
    '''
    with open(filename,'r+') as f:
        content = f.read()
        f.seek(0)
        f.write( ','.join([str(i) for i in orderDetails])+'\n' + content )
    #with open(filename, 'r') as f:
    #    no_lines = len(f.readlines())
    #return no_lines
    return 0

def loadOrders(filename):
    '''
    '''
    orders = []
    with open(filename, 'r') as f:
        for line in f:
            orders.append(line.strip().split(','))
    return orders
        

def checkStock(stock, selectedItem, quantity):
    '''
    Check to see if there is enough stock for the selected item
    '''
    if availableQuantity(stock, selectedItem) < quantity:
        return False
    return True


def calculateVAT(amount):
    '''
    Calculates the VAT to be paid on an amount.
    '''
    return amount * VAT_RATE

def discount(amount, dp=2):
    '''
    Calculates the amount of discount to apply.
    Amound over discount threshold has the discount amount applied
    '''
    if amount > DISCOUNT_THRESHOLD2:
        return round(amount * DISCOUNT2,dp)
    elif amount > DISCOUNT_THRESHOLD1:
        return round(amount * DISCOUNT1,dp) 
    return 0.0  


def createInvoiceData(stock, selectedItem, quantity, ccy):
    '''
    Produce all the calculated values using the above functions.
    Returns the multiple calculated values in a list, in the currency ccy selected
    '''
    price = getPrice(stock, selectedItem)
    total_before_discount = price*quantity
    dis = discount(total_before_discount)
    total_gross = total_before_discount - dis
    vat = calculateVAT(total_gross)
    total_net = total_gross + vat
    # adjust stock quantity
    adjustStockQuantity(stock, selectedItem, -quantity)
    # return invoice values, converted to the selected ccy
    return [ getCurrencyValue(price, ccy),
            getCurrencyValue(total_before_discount,ccy), 
           getCurrencyValue(dis,ccy), 
           getCurrencyValue(vat,ccy), 
           getCurrencyValue(total_net,ccy)]


def generateInvoice(item, quantity, ccy, price, total_before_discount, discount, vat, total_net):
    '''
    Print out the invoice on the console given stock, selected item and quantity
    '''
    # check stock is avaiable
    invoice = []
    #invoice.append("             INVOICE\n")
    #invoice.append("=================================\n")
    invoice.append(f"Item:\t\t|  {item}\n")
    invoice.append(f"Item Price:\t|  {price}\n")
    invoice.append(f"Quantity:\t|  {quantity}\n")
    invoice.append(f"Total:\t\t|  {total_before_discount}\n")
    invoice.append(f"Discount:\t|  {discount}\n")
    invoice.append(f"VAT:\t\t|  {vat}\n")
    invoice.append(f"Net Total:\t|  {total_net}\n")
    invoice.append(f"Currency:\t|  {ccy}\n")
    return invoice

def display_invoice_list(item, quantity, ccy, price, total_before_discount, discount, vat, total_net):
    invoice = []
    invoice.append( ("Item",item) )
    invoice.append( ("Item Price",price) )
    invoice.append( ("Quantity",  quantity) )
    invoice.append( ("Total",  total_before_discount) )
    invoice.append( ("Discount", discount) )
    invoice.append( ("VAT", vat) )
    invoice.append( ("Net Total", total_net) )
    invoice.append( ("Currency", ccy) )
    return invoice



'''
Main program asks user to select item and quantity and prints the invoice
Only runs if this file is the first to be loaded ("__main__").
This means the code will not be run when the file is imported into the test scripts.
'''
if __name__ =="__main__":
    stockFileName = "stock.txt"
    stock = loadStock(stockFileName)
    print( ''.join(itemList(stock)) )
    selectedItem = int(input("Enter Item:")) - 1
    itemName = getItemName(stock, selectedItem)
    print(f"Item Selected: {itemName}")
    quantity = int(input("Enter Amount:"))

    # check if stock is available, if not then report issue and exist
    if checkStock(stock, selectedItem, quantity) == False:
        print("Not enough quanity in stock to complete order")
        exit()

    # get currency and check a valid value has been entereed
    ccy = input("Enter Currency (EUR, GBP, USD):")
    if ccy not in ['EUR','GBP','USD']:
        print("Invalid currency entered")
        exit()
    print()
    # get data
    price, total_before_discount, discnt, vat, total_net = createInvoiceData(stock, selectedItem, quantity, ccy)
    # print output to the command line
    print(''.join(generateInvoice(itemName, quantity, ccy, price, total_before_discount, discnt, vat, total_net)))
    # store result in the order file.
    saveStockData(stockFileName, stock)
    # write invoice information to order file.
    saveOrderToFile("orders.txt", (itemName, quantity, ccy, price, total_before_discount, discnt, vat, total_net))

