import psycopg2
import tkinter as tk
from tkinter import messagebox

window1 = tk.Tk()
window1.geometry("800x225")

loginFrame = tk.Frame()
frameTransit = tk.Frame()
transactionFrame = tk.Frame()
addEmplFrame = tk.Frame()
removeEmplFrame = tk.Frame()
inventoryFrame = tk.Frame()

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
    emplID=str(txtUsername.get())
    sql="SELECT*FROM employee where employee_id=%s;"
    cur.execute(sql,(str(emplID),))
    row=cur.fetchone()
    if row is None:
        txtUsername.delete(0,20)
        txtPassword.delete(0,20)
        tk.messagebox.showwarning(message="Invalid LoginID/Password")
    global emplType    
    emplType=str(row[4]).lower()
    password=str(row[6])
    
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

addEmplButton=tk.Button(text="Add an Employee",command=displayaddEmplButtonPage)
removeEmplButton=tk.Button(text="Remove an Employee",command=displayremoveEmplButtonPage)
tk.Button(frameTransit,text="Check Inventory/Add Stock").grid(row=1,column=0)
buttNewPurchase= tk.Button(frameTransit,text="New Purchase",command=displayBillPage)
buttNewPurchase.grid(row=2,column=0)
buttLogout=tk.Button(frameTransit,text="Logout",command=logout)
buttLogout.grid(row=3,column=0)

#-------------------- end of framTransit ##################################################

##################### Inventory page ######################################################


#--------------------end of Inventory page ################################################

#################### billPage (transactionFrame) #########################################
def cancel():
    transactionFrame.pack_forget()
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

tk.Label(transactionFrame,text="Customer Phone Number").grid(row=0,column=0)
phoneEntry=tk.Entry(transactionFrame)
phoneEntry.grid(row=0,column=1)

tk.Label(transactionFrame,text="DrugID").grid(row=1,column=0)
tk.Label(transactionFrame,text="Quantity").grid(row=1,column=1)

tk.Label(transactionFrame,text="Rate").grid(row=1,column=3)
tk.Label(transactionFrame,text="Price").grid(row=1,column=4)

drugEntry1=tk.Entry(transactionFrame)
drugEntry1.grid(row=2,column=0)
qtyEntry1=tk.Entry(transactionFrame)
qtyEntry1.grid(row=2,column=1)
tk.Button(transactionFrame,text="Add to bill").grid(row=2,column=2)
rateEntry1=tk.Entry(transactionFrame)
rateEntry1.grid(row=2,column=3)
priceEntry1=tk.Entry(transactionFrame)
priceEntry1.grid(row=2,column=4)
tk.Button(transactionFrame,text="Remove item").grid(row=2,column=5)

drugEntry2=tk.Entry(transactionFrame)
drugEntry2.grid(row=3,column=0)
qtyEntry2=tk.Entry(transactionFrame)
qtyEntry2.grid(row=3,column=1)
tk.Button(transactionFrame,text="Add to bill").grid(row=3,column=2)
rateEntry2=tk.Entry(transactionFrame)
rateEntry2.grid(row=3,column=3)
priceEntry2=tk.Entry(transactionFrame)
priceEntry2.grid(row=3,column=4)
tk.Button(transactionFrame,text="Remove item").grid(row=3,column=5)

drugEntry3=tk.Entry(transactionFrame)
drugEntry3.grid(row=4,column=0)
qtyEntry3=tk.Entry(transactionFrame)
qtyEntry3.grid(row=4,column=1)
tk.Button(transactionFrame,text="Add to bill").grid(row=4,column=2)
rateEntry3=tk.Entry(transactionFrame)
rateEntry3.grid(row=4,column=3)
priceEntry3=tk.Entry(transactionFrame)
priceEntry3.grid(row=4,column=4)
tk.Button(transactionFrame,text="Remove item").grid(row=4,column=5)

drugEntry4=tk.Entry(transactionFrame)
drugEntry4.grid(row=5,column=0)
qtyEntry4=tk.Entry(transactionFrame)
qtyEntry4.grid(row=5,column=1)
tk.Button(transactionFrame,text="Add to bill").grid(row=5,column=2)
rateEntry4=tk.Entry(transactionFrame)
rateEntry4.grid(row=5,column=3)
priceEntry4=tk.Entry(transactionFrame)
priceEntry4.grid(row=5,column=4)
tk.Button(transactionFrame,text="Remove item").grid(row=5,column=5)

tk.Label(transactionFrame,text="Total bill").grid(row=6,column=2)
amountEntry=tk.Entry(transactionFrame)
amountEntry.grid(row=6,column=3)

tk.Button(transactionFrame,text="Checkout").grid(row=7,column=1)
tk.Button(transactionFrame,text="Cancel",command=cancel).grid(row=7,column=3)

#------------------------- end bill page ############################################################


######################### add empl page ############################################################
def goBackFromaddEmplButton():
    addEmplFrame.pack_forget()
    if emplType=='manager':
        addEmplButton.pack()
        removeEmplButton.pack()
    frameTransit.pack()

def addEmpl():
    try:
        data=(loginId.get(),fname.get(),lname.get(),phNo.get(),job.get(),salary.get(),loginPassword.get())
        sql="insert into employee values(%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(sql,data)
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
        tk.messagebox.showwarning(message="Error!")
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
    sql="SELECT*FROM employee where employee_id=%s"
    cur.execute(sql,(str(removalID.get()),))
    row=cur.fetchone()
    if row is None:
        tk.messagebox.showwarning(message="No such Employee exists!")
        removalID.delete(0,20)
    else:
        sql="DELETE FROM employee where employee_id=%s"
        cur.execute(sql,(str(removalID.get()),))
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

