import psycopg2
import tkinter as tk
from tkinter import messagebox

window1 = tk.Tk()
window1.geometry("800x225")
window1.title('Pharmaceutical Store')

loginFrame = tk.Frame()
frameTransit = tk.Frame()
transactionFrame = tk.Frame()
billFrame = tk.Frame()
addEmplFrame = tk.Frame()
removeEmplFrame = tk.Frame()
inventoryFrame = tk.Frame()
checkoutFrame = tk.Frame()

conn = psycopg2.connect("dbname=pharma user=postgres password=tiger")
cur = conn.cursor()

emplID=None
emplType=None
####################### Login page ###################################################
tk.Label(loginFrame,text="Employee ID:").grid(row=0,column=0)
txtUsername = tk.Entry(loginFrame)
txtUsername.grid(row=0,column=1)

tk.Label(loginFrame,text="Password:").grid(row=1,column=0)

txtPassword = tk.Entry(loginFrame,show="*")
txtPassword.grid(row=1,column=1)

def login():
    global emplID
    emplID=str(txtUsername.get())
    cur.callproc('get_empl',[emplID,])
    row=cur.fetchone()
    if row is None:
        txtUsername.delete(0,20)
        txtPassword.delete(0,20)
        tk.messagebox.showwarning(message="Invalid Login ID/Password")
    global emplType    
    emplType=str(row[1]).lower()
    password=str(row[0])
    
    if password==txtPassword.get():
        txtUsername.delete(0,20)
        txtPassword.delete(0,20)
        if emplType=='manager':
            addEmplButton.pack()
            removeEmplButton.pack()
        loginFrame.pack_forget()
        frameTransit.pack()
        
    else:
        txtUsername.delete(0,20)
        txtPassword.delete(0,20)
        tk.messagebox.showwarning(message="Invalid LoginID/Password")

tk.Button(loginFrame,text="Login",command=login).grid(row=2,column=1)

loginFrame.pack()

#----------------------------- End login page ##############################################

############################## frameTransit page ###############################################
def logout():
    global emplID
    emplID=None
    global emplType
    emplType=None
    addEmplButton.pack_forget()
    removeEmplButton.pack_forget()
    frameTransit.pack_forget()
    loginFrame.pack()

def displayBillPage():
    addEmplButton.pack_forget()
    removeEmplButton.pack_forget()
    frameTransit.pack_forget()
    transactionFrame.pack()

def displayaddEmplButtonPage():
    addEmplButton.pack_forget()
    removeEmplButton.pack_forget()
    frameTransit.pack_forget()
    addEmplFrame.pack()

def displayremoveEmplButtonPage():
    addEmplButton.pack_forget()
    removeEmplButton.pack_forget()
    frameTransit.pack_forget()
    removeEmplFrame.pack()

def displayInventoryPage():
    addEmplButton.pack_forget()
    removeEmplButton.pack_forget()
    frameTransit.pack_forget()
    inventoryFrame.pack()

addEmplButton=tk.Button(text="Add an Employee",command=displayaddEmplButtonPage)
removeEmplButton=tk.Button(text="Remove an Employee",command=displayremoveEmplButtonPage)
tk.Button(frameTransit,text="Check Inventory/Add Stock",command=displayInventoryPage).grid(row=1,column=0)
buttNewPurchase= tk.Button(frameTransit,text="New Purchase",command=displayBillPage)
buttNewPurchase.grid(row=2,column=0)
buttLogout=tk.Button(frameTransit,text="Logout",command=logout)
buttLogout.grid(row=3,column=0)

#-------------------- end of frameTransit ##################################################

##################### Inventory page ######################################################
def goBackFromInventory():
    stockEntry.delete(0,'end')
    qtyEntry.delete(0,'end')
    inventoryFrame.pack_forget()
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()
def getQTY():
    drugID=stockEntry.get()
    cur.callproc('get_stock',[drugID,])
    qty=cur.fetchone()
    qtyEntry.delete(0,'end')
    qtyEntry.insert(0,str(qty[0]))
def addStock():
    drugID=addStockEntry.get()
    qty=int(addQtyEntry.get())
    cur.callproc('add_stock',[drugID,qty,])
    conn.commit()
    tk.messagebox.showwarning(message="Added successfully...")
    addStockEntry.delete(0,'end')
    addQtyEntry.delete(0,'end')

tk.Label(inventoryFrame,text='Check stock').grid(row=0,column=0)
tk.Label(inventoryFrame,text='Stock ID:').grid(row=1,column=0)
stockEntry=tk.Entry(inventoryFrame)
stockEntry.grid(row=1,column=1)
tk.Button(inventoryFrame,text='Check Quantity',command=getQTY).grid(row=1,column=2)
qtyEntry=tk.Entry(inventoryFrame)
qtyEntry.grid(row=1,column=3)

tk.Label(inventoryFrame,text='Add stock').grid(row=2,column=0)
tk.Label(inventoryFrame,text='Stock ID:').grid(row=3,column=0)
addStockEntry=tk.Entry(inventoryFrame)
addStockEntry.grid(row=3,column=1)
tk.Label(inventoryFrame,text='Enter quantity:').grid(row=4,column=0)
addQtyEntry=tk.Entry(inventoryFrame)
addQtyEntry.grid(row=4,column=1)
tk.Button(inventoryFrame,text="Add to Stock",command=addStock).grid(row=5,column=1)
tk.Button(inventoryFrame,text="Back",command=goBackFromInventory).grid(row=5,column=2)

#--------------------end of Inventory page ################################################

#################### billPage (transactionFrame) #########################################
transactionId=0
drug=['','','','']
drugName=['','','','']
qty=[0,0,0,0]
price=[0,0,0,0]
totalAmt=0
def displayTotalAmt():
    global price, totalAmt
    totalAmt=price[0]+price[1]+price[2]+price[3]
    amountEntry.delete(0,'end')
    amountEntry.insert(0,str(totalAmt))

def checkout():
    global drug,qty,price,transactionId,totalAmt  
    i=0
    purchaseId=0
    for i in range(4):
        if drug[i]=='':
            break

        cur.execute('select max(purchase_Id) from purchase')
        row=cur.fetchone()
        purchaseId=int(row[0])+1
        cur.callproc('insert_purchase',[purchaseId,transactionId,drug[i],qty[i],])
        conn.commit()
        
    cur.callproc('finish_transaction',[transactionId,totalAmt,])
    conn.commit()
    transactionFrame.pack_forget()
    billFrame.pack_forget()
    phoneEntry.delete(0,'end')
    rateEntry1.delete(0,'end')
    qtyEntry1.delete(0,'end')
    rateEntry2.delete(0,'end')
    qtyEntry2.delete(0,'end')
    rateEntry3.delete(0,'end')
    qtyEntry3.delete(0,'end')
    rateEntry4.delete(0,'end')
    qtyEntry4.delete(0,'end')
    checkoutFrame.pack()

def cancel():
    global transactionId, drug, drugName, qty, price, totalAmt 
    cur.callproc('terminate_transaction',[transactionId,])
    conn.commit()
    transactionId=0
    transactionFrame.pack_forget()
    billFrame.pack_forget()
    phoneEntry.delete(0,'end')
    rateEntry1.delete(0,'end')
    qtyEntry1.delete(0,'end')
    rateEntry2.delete(0,'end')
    qtyEntry2.delete(0,'end')
    rateEntry3.delete(0,'end')
    qtyEntry3.delete(0,'end')
    rateEntry4.delete(0,'end')
    qtyEntry4.delete(0,'end')
    transactionId=0
    drug=['','','','']
    drugName=['','','','']
    qty=[0,0,0,0]
    price=[0,0,0,0]
    totalAmt=0
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

def createBill():
    phoneNo=phoneEntry.get()
    global transactionId
    cur.execute('select max(transaction_id) from transaction')
    row=cur.fetchone()
    transactionId=int(row[0])+1
    global emplID
    if phoneNo=="":
        tk.messagebox.showwarning(message="Enter Valid Phone Number")
    else:
        billFrame.pack()
        cur.callproc('create_transaction',[transactionId,emplID,phoneNo,])
        conn.commit()
        amountEntry.delete(0,'end')
        amountEntry.insert(0,'0')

def add0():
    global drug, qty, price, drugName   
    drug[0]=drugEntry1.get()
    qty[0]=int(qtyEntry1.get())
    cur.callproc('get_stock',[drug[0],])
    row=cur.fetchone()
    if row[0]<qty[0]:          
        tk.messagebox.showwarning(message="Stock Unavailable")
    else:
        drugName[0]=row[2]
        price[0]=qty[0]*row[1]
        rateEntry1.delete(0,'end')
        rateEntry1.insert(0,str(row[1]))
        priceEntry1.delete(0,'end')
        priceEntry1.insert(0,str(price[0]))
        displayTotalAmt()
        
def remove0():
    global drug, qty, price 
    drug[0]=''
    drugName[0]=''
    qty[0]=0
    price[0]=0
    displayTotalAmt()
    rateEntry1.delete(0,'end')
    priceEntry1.delete(0,'end')

def add1():
    global drug, qty, price  
    drug[1]=drugEntry2.get()
    qty[1]=int(qtyEntry2.get())
    cur.callproc('get_stock',[drug[1],])
    row=cur.fetchone()
    if row[0]<qty[1]:          
        tk.messagebox.showwarning(message="Stock Unavailable")
    else:
        drugName[1]=row[2]
        price[1]=qty[1]*row[1]
        rateEntry2.delete(0,'end')
        rateEntry2.insert(0,str(row[1]))
        priceEntry2.delete(0,'end')
        priceEntry2.insert(0,str(price[1]))
        displayTotalAmt()
        
def remove1():
    global drug, qty, price 
    drug[1]=''
    drugName[1]=''
    qty[1]=0
    price[1]=0
    displayTotalAmt()
    rateEntry2.delete(0,'end')
    priceEntry2.delete(0,'end')

def add2():
    global drug, qty, price  
    drug[2]=drugEntry3.get()
    qty[2]=int(qtyEntry3.get())
    cur.callproc('get_stock',[drug[2],])
    row=cur.fetchone()
    if row[0]<qty[2]:          
        tk.messagebox.showwarning(message="Stock Unavailable")
    else:
        drugName[2]=row[2]
        price[2]=qty[2]*row[1]
        rateEntry3.delete(0,'end')
        rateEntry3.insert(0,str(row[1]))
        priceEntry3.delete(0,'end')
        priceEntry3.insert(0,str(price[2]))
        displayTotalAmt()
        
def remove2():
    global drug, qty, price 
    drug[2]=''
    drugName[2]=''
    qty[2]=0
    price[2]=0
    displayTotalAmt()
    rateEntry3.delete(0,'end')
    priceEntry3.delete(0,'end')

def add3():
    global drug, qty, price  
    drug[3]=drugEntry4.get()
    qty[3]=int(qtyEntry4.get())
    cur.callproc('get_stock',[drug[3],])
    row=cur.fetchone()
    if row[0]<qty[3]:          
        tk.messagebox.showwarning(message="Stock Unavailable")
    else:
        drugName[3]=row[2]
        price[3]=qty[3]*row[1]
        rateEntry4.delete(0,'end')
        rateEntry4.insert(0,str(row[1]))
        priceEntry4.delete(0,'end')
        priceEntry4.insert(0,str(price[3]))
        displayTotalAmt()
        
def remove3():
    global drug, qty, price 
    drug[3]=''
    drugName[3]=''
    qty[3]=0
    price[3]=0
    displayTotalAmt()
    rateEntry4.delete(0,'end')
    priceEntry4.delete(0,'end')
    

tk.Label(transactionFrame,text="Customer Phone Number").grid(row=0,column=0)
phoneEntry=tk.Entry(transactionFrame)
phoneEntry.grid(row=0,column=1)
tk.Button(transactionFrame,text="Create bill",command=createBill).grid(row=0,column=2)

tk.Label(billFrame,text="DrugID").grid(row=1,column=0)
tk.Label(billFrame,text="Quantity").grid(row=1,column=1)

tk.Label(billFrame,text="Rate").grid(row=1,column=3)
tk.Label(billFrame,text="Price").grid(row=1,column=4)

drugEntry1=tk.Entry(billFrame)
drugEntry1.grid(row=2,column=0)
qtyEntry1=tk.Entry(billFrame)
qtyEntry1.grid(row=2,column=1)
tk.Button(billFrame,text="Add to bill",command=add0).grid(row=2,column=2)
rateEntry1=tk.Entry(billFrame)
rateEntry1.grid(row=2,column=3)
priceEntry1=tk.Entry(billFrame)
priceEntry1.grid(row=2,column=4)
tk.Button(billFrame,text="Remove item",command=remove0).grid(row=2,column=5)

drugEntry2=tk.Entry(billFrame)
drugEntry2.grid(row=3,column=0)
qtyEntry2=tk.Entry(billFrame)
qtyEntry2.grid(row=3,column=1)
tk.Button(billFrame,text="Add to bill",command=add1).grid(row=3,column=2)
rateEntry2=tk.Entry(billFrame)
rateEntry2.grid(row=3,column=3)
priceEntry2=tk.Entry(billFrame)
priceEntry2.grid(row=3,column=4)
tk.Button(billFrame,text="Remove item",command=remove1).grid(row=3,column=5)

drugEntry3=tk.Entry(billFrame)
drugEntry3.grid(row=4,column=0)
qtyEntry3=tk.Entry(billFrame)
qtyEntry3.grid(row=4,column=1)
tk.Button(billFrame,text="Add to bill",command=add2).grid(row=4,column=2)
rateEntry3=tk.Entry(billFrame)
rateEntry3.grid(row=4,column=3)
priceEntry3=tk.Entry(billFrame)
priceEntry3.grid(row=4,column=4)
tk.Button(billFrame,text="Remove item",command=remove2).grid(row=4,column=5)

drugEntry4=tk.Entry(billFrame)
drugEntry4.grid(row=5,column=0)
qtyEntry4=tk.Entry(billFrame)
qtyEntry4.grid(row=5,column=1)
tk.Button(billFrame,text="Add to bill",command=add3).grid(row=5,column=2)
rateEntry4=tk.Entry(billFrame)
rateEntry4.grid(row=5,column=3)
priceEntry4=tk.Entry(billFrame)
priceEntry4.grid(row=5,column=4)
tk.Button(billFrame,text="Remove item",command=remove3).grid(row=5,column=5)

tk.Label(billFrame,text="Total bill").grid(row=6,column=2)
amountEntry=tk.Entry(billFrame)
amountEntry.grid(row=6,column=3)

tk.Button(billFrame,text="Checkout",command=checkout).grid(row=7,column=1)
tk.Button(billFrame,text="Cancel",command=cancel).grid(row=7,column=3)

#------------------------- end bill page ############################################################

######################### checkout page #############################################################
def dispBill():
    textArea.pack()
    backButton.pack()
    for i in range(4):
        if drug[i]=='':
            break
        item='\n'+drugName[i]+'\t QTY: '+str(qty[i])+'\t Price: '+str(price[i])
        textArea.insert(tk.END, item)
    amountLine='\n'+'Total amount: '+str(totalAmt)     
    textArea.insert(tk.END, amountLine) 

def backToMenu():
    global transactionId,drug,drugName,qty,price,totalAmt
    textArea.pack_forget()
    checkoutFrame.pack_forget()
    backButton.pack_forget()
    transactionId=0
    drug=['','','','']
    drugName=['','','','']
    qty=[0,0,0,0]
    price=[0,0,0,0]
    totalAmt=0
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

tk.Button(checkoutFrame,text="Generate Reciept",command=dispBill).grid(row=0,column=0)
textArea=tk.Text(height=10,width=75)
backButton=tk.Button(text="Back to menu",command=backToMenu)

#-------------------- end checkout page #############################################################

######################### add empl page ############################################################
def goBackFromaddEmplButton():
    addEmplFrame.pack_forget()
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

def addEmpl():
    try:
        cur.callproc('add_empl',[loginId.get(),fname.get(),lname.get(),phNo.get(),job.get(),int(salary.get()),loginPassword.get(),])
        conn.commit()
        tk.messagebox.showwarning(message="Success!")
        fname.delete(0,20)
        lname.delete(0,20)
        phNo.delete(0,20)
        job.delete(0,20)
        salary.delete(0,20)
        loginId.delete(0,20)
        loginPassword.delete(0,20)
        
    except:
        for notice in conn.notices:
            tk.messagebox.showwarning(message=notice)
        conn.commit()
        

tk.Label(addEmplFrame,text="Enter First Name:").grid(row=1,column=0)
fname = tk.Entry(addEmplFrame)
fname.grid(row=1,column=1)

tk.Label(addEmplFrame,text="Enter Last Name:").grid(row=2,column=0)
lname = tk.Entry(addEmplFrame)
lname.grid(row=2,column=1)


tk.Label(addEmplFrame,text="Enter Phone Number:").grid(row=3,column=0)
phNo = tk.Entry(addEmplFrame)
phNo.grid(row=3,column=1)

tk.Label(addEmplFrame,text="Enter Job Type:").grid(row=4,column=0)
job = tk.Entry(addEmplFrame)
job.grid(row=4,column=1)

tk.Label(addEmplFrame,text="Enter Salary:").grid(row=5,column=0)
salary = tk.Entry(addEmplFrame)
salary.grid(row=5,column=1)

tk.Label(addEmplFrame,text="Enter Login ID:").grid(row=6,column=0)          #LoginID == EmployeeId
loginId = tk.Entry(addEmplFrame)
loginId.grid(row=6,column=1)

tk.Label(addEmplFrame,text="Enter Password for access:").grid(row=7,column=0)
loginPassword = tk.Entry(addEmplFrame,show="*")
loginPassword.grid(row=7,column=1)

tk.Button(addEmplFrame,text="Add Employee",command=addEmpl).grid(row=9,column=0)
tk.Button(addEmplFrame,text="Back",command=goBackFromaddEmplButton).grid(row=9,column=1)

#------------------------ end add empl page ########################################################

######################### remove empl page #########################################################
def goBackFromRemoveEmplPage():
    removeEmplFrame.pack_forget()
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

def removeEmpl():
    cur.callproc('get_empl',[removalID.get(),])
    row=cur.fetchone()
    if row is None:
        tk.messagebox.showwarning(message="No such Employee exists!")
        removalID.delete(0,20)
    else:
        cur.callproc('remove_empl',[removalID.get(),])
        conn.commit()
        tk.messagebox.showwarning(message="Success!")
        removalID.delete(0,20)

tk.Label(removeEmplFrame,text="Enter Employee ID:").grid(row=1,column=0)
removalID = tk.Entry(removeEmplFrame)
removalID.grid(row=1,column=1)
tk.Button(removeEmplFrame,text="Remove Employee",command=removeEmpl).grid(row=2,column=0)
tk.Button(removeEmplFrame,text="Back",command=goBackFromRemoveEmplPage).grid(row=2,column=1)

#------------------------ end remove empl page ####################################################


window1.mainloop()

cur.close()
conn.close()

