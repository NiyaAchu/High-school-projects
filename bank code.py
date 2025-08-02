import mysql
import mysql.connector as cnctr
import datetime
import csv
import random
import os
def init():
    global conn, crsr
    conn=cnctr.connect(host='localhost',
                       user='root',
                       password='niya15',
                       database='xiib')
    crsr=conn.cursor()
init()

def create_table():
    qry="create table if not exists Account_File(Account_number int primary key, Name varchar(50), Address varchar(50), Date date, Telephone_number int, mobile_number int, Fax_number int, DOB date, Interest_Rate float, Current_balance float)"
    crsr.execute(qry)
create_table()

def tday():
    today=datetime.date.today()
    return today

#validate date
def validate_date():
    while True:
        dateofbirth=input('Enter date of birth (dd/mm/yyyy): ')
        try:
            dateobj=datetime.datetime.strptime(dateofbirth,'%d/%m/%Y')
            return dateobj
        except ValueError:
            print('Invalid date :(')

def account_number():
    while True:
        try:
            n=int(input('Enter Account number(only digits): '))
            return n
        except ValueError:
            print('Invalid input')
            
def generate_account():
    acc=random.randint(10000,99999)
    qry='select account_number from account_file'
    crsr.execute(qry)
    see=crsr.fetchall()
    for i in see:
        if acc==i:
            acc=random.randint(10000,99999)
    return acc

def telephone_number():
    while True:
        try:
            n=int(input('Enter telephone number #1: '))
            return n
        except ValueError:
            print('Invalid input')
def mobile_number():
    while True:
        try:
            n=int(input('Enter moblie number #2: '))
            return n
        except ValueError:
            print('Invalid input')
def fax_number():
    while True:
        try:
            n=int(input('Enter fax number: '))
            return n
        except ValueError:
            print('Invalid input')
      
def open_account():
    global an,tdate,tdesc,amt
    an=generate_account()
    name=input('Enter name: ')
    address=input('Enter address: ')
    tdate=tday()
    tn=telephone_number()
    mob=mobile_number()
    fax=fax_number()
    dob=validate_date()
    rateint=3.5
    amt=float(input('Enter the amount you would like to deposit: '))
    data=(an,name,address,tdate,tn,mob,fax,dob,rateint,amt)
    qry=("insert into account_file values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    crsr.execute(qry,data)
    conn.commit()
    print('Account created!')
    print('Your account number is ',an)
    tdesc='DEPOSIT'
    create_transaction()

def deposit():
    global tdesc,amt,an
    tdesc='DEPOSIT'
    an=account_number()
    amt=float(input('Enter the amount you would like to deposit: '))
    data=(amt,an)
    qry=("update account_file set current_balance=current_balance + %s where account_number=%s")
    crsr.execute(qry,data)
    conn.commit()
    print('Succesfully deposited')
    create_transaction()
    interest()
    create_passbook()


def withdrawal():
    global tdesc,amt,an
    tdesc='WITHDRAWN'
    an=account_number()
    amt=float(input('Enter the amount you would like to withdraw: '))
    data=(amt,an)
    qry=("update account_file set current_balance=current_balance - %s where account_number=%s")
    crsr.execute(qry,data)
    conn.commit()
    print('Succesfully withdrawn')
    create_transaction()
    interest()
    create_passbook()
def balance():
    qry=('select current_balance from account_file where account_number=%s')
    data=(an,)
    crsr.execute(qry,data)
    result=crsr.fetchone()
    if result:
        # Extract the balance from the tuple (result[0] is the balance)
        balance = result[0]
        
        return balance
    else:
        print("No account found")
        return None
def create_transaction():
    global tdesc,amt,an,tid,tdate,bal
    fn=f'{an}.csv'
    i=0
    try:
        with open(fn,'r') as f:
            r=csv.reader(f)
            for rec in r:
                i+=1
    except FileNotFoundError:
        pass
    with open(fn,'a',newline='') as f:
        tid=10000+i
        tdate=tday()
        tkind=tdesc
        amount=amt
        bal=balance()
        rec=[tid,tdate,tkind,amount,bal]
        w=csv.writer(f)
        w.writerow(rec)
def interest():
    global inte,an #later remember to add inte in a new table....maybe transaction table
    inte=0
    qry=("select current_balance, date from account_file where account_number=%s")
    data=(an,)
    crsr.execute(qry,data)
    row=crsr.fetchone()
    if row:
        balance,od=row
        tdy=datetime.date.today()
        diff=tdy-od
        if (od.year%400==0) or (od.year%100!=0 and od.year%4==0):
            t=diff.days/366
        else: t=diff.days/365
        if (diff.days%366==0) or (diff.days%365==0):
            inte+=balance*0.035*t
    else: print('No account found')

def update_personal():
    
   details='''
1. Name
2. Address
3. Telephone number
4. Mobile number
5. Fax number
6. Date of birth
0. Exit'''
   print(details)
   op=int(input('Which of the following personal details would you like to change? '))
   
   if op==1:
       an=account_number()
       na=input("Enter the name you would like to change to: ")
       data=(na,an)
       qry=("update account_file set Name=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
    
   elif op==2:
       an=account_number()
       ad=input("Enter the address you would like to change to: ")
       data=(ad,an)
       qry=("update account_file set address=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
   elif op==3:
       an=account_number()
       tn=int(input("Enter the telephone number you would like to change to: "))
       data=(tn,an)
       qry=("update account_file set telephone_number=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
   elif op==4:
       an=account_number()
       mn=int(input("Enter the mobile number you would like to change to: "))
       data=(mn,an)
       qry=("update account_file set mobile_number=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
   elif op==5:
       an=account_number()
       fn=int(input("Enter the fax number you would like to change to: "))
       data=(fn,an)
       qry=("update account_file set fax_number=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
   elif op==6:
       an=account_number()
       dd=validate_date()
       data=(dd,an)
       qry=("update account_file set dob=%s where account_number=%s")
       crsr.execute(qry,data)
       conn.commit()
       print("Updated!")
   elif op==0:
       print("Exit..")

def format_date(date_obj):
    if isinstance(date_obj, datetime.date):
        return date_obj.strftime('%Y-%m-%d')  
    return date_obj
def display_details():
    an=account_number()
    qry=('select * from account_file where account_number=%s')
    data=(an,)
    crsr.execute(qry,data)
    det=crsr.fetchall()
    print('='*200)
    print(f'''{'Account_Number':15s} {'Name':<20} {'Address':<25} {'Date':<25} {'Mobile_Number':<25} {'Telephone_Number':<25}\
{'Fax_number':<25} {'DOB':<25} {'Interest_Rate':<25} {'Current_balance':<25}''')
    for row in det:
        formatted_date = format_date(row[3])  # Assuming row[3] is a date
        formatted_dob = format_date(row[7])  # Assuming row[7] is DOB
        formatted_interest_rate = f'{row[8]:.2f}'  # Format interest rate to 2 decimal places
        formatted_balance = f'{row[9]:,.2f}'  # Format balance with commas and 2 decimal places
        
    print(f'{row[0]:<15} {row[1]:<20} {row[2]:<25} {formatted_date:<25} {row[4]:<25} {row[5]:<25} {row[6]:<25} {formatted_dob:<25} \
{formatted_interest_rate:<25} {formatted_balance:<25}')
    print('-'*200)

def create_passbook():
    global an,tid,tdate,amt,bal, tdesc, inte
    table_name = f"{an}_passbook"
    qry=f'''create table if not exists {table_name}(Transaction_ID int primary key, Date date, Credit float, Debit float, Interest float, Balance float)'''
    crsr.execute(qry)
    if tdesc=='DEPOSIT':
        data=(tid,tdate,amt,None,inte,bal)
        qry=(f''' insert into {table_name} values(%s,%s,%s,%s,%s,%s)''')
        crsr.execute(qry,data)
    elif tdesc=='WITHDRAWN':
        data=(tid,tdate,None,amt,inte,bal)
        qry=(f''' insert into {table_name} values(%s,%s,%s,%s,%s,%s)''')
        crsr.execute(qry,data)
    conn.commit()

def cheque():
    chqacc=int(input('Enter the account number(only digits) from where you are getting the cheque: '))
    wdd=float(input('Enter the amount: '))
    data=(wdd,chqacc)
    qry=("update account_file set current_balance=current_balance - %s where account_number=%s")
    crsr.execute(qry,data)
    conn.commit()
    acc=int(input('Enter your account number: '))
    data=(wdd,acc)
    qry=("update account_file set current_balance=current_balance + %s where account_number=%s")
    crsr.execute(qry,data)
    conn.commit()
    print('Cheque clearance')

def bank_statement():
    an=account_number()
    try:
        z=0
        fn=f'{an}.csv'
        with open (fn,'r') as f:
            r=list(csv.reader(f))
            print('-'*70)
            print(f'''{'Tran_ID'}    {'Date'}          {'Type'}         {'Amount'}         {'Current_Balance'}''')
            print('-'*70)
            for rec in r[::-1]:
                ttid,dda,ty,am,b=int(rec[0]), rec[1], rec[2], float(rec[3]), float(rec[4])
                print(f'''{ttid}    {dda}      {ty:9s} {am:10.2f}  {b:15.2f}''')
                z+=1
                if z==30: break
    except FileNotFoundError:
        print('File is not found:(')

def close_account():
    confirm=input('Are you sure you want to delete your account(Y/N)? ')
    if confirm in 'Yy':
        an=account_number()
        data=(an,)
        qry=('delete from account_file where account_number=%s')
        crsr.execute(qry,data)
        conn.commit()
        table_name = f"{an}_passbook"
        qry=f'''drop table {table_name}'''
        crsr.execute(qry)
        fn=f'{an}.csv'
        os.remove(fn)
        print('Your account has been deleted')
    else:
        print('Exit...')
        
# def weekly_balance()
def daily_balance():
    an=account_number()
    table_name = f"{an}_passbook"
    qry = f"SELECT date, balance FROM {table_name} ORDER BY Date"
    crsr.execute(qry)
    week=crsr.fetchall()
    print('-'*70)
    print(f'''{'Date'}         {'Balance':<20}''')
    for row in week:
        formatted_date = format_date(row[0])  
        formatted_balance = f'{row[1]:,.2f}'  # Format balance with commas and 2 decimal places
        print(f'{formatted_date:<13} {formatted_balance:<25}')
    print('-'*70)
        
print('Welcome to Niya Bank =D')
while True:
    menu='''
1. Open an account
2. Deposit
3. Withdraw
4. Modification of personal details
5. Display information of an account
6. Cheque
7. Bank Statement
8. Daily balance
9. Close an account
0. Exit'''
    
    print(menu)
    op=int(input('Enter option: '))
    if op==1: open_account()
    elif op==2: deposit()
    elif op==3: withdrawal()
    elif op==4: update_personal()
    elif op==5: display_details()
    elif op==6: cheque()
    elif op==7: bank_statement()
    elif op==8: daily_balance()
    elif op==9: close_account()
    elif op==0:
        print('Thank you for visiting my bank :D')
        break
    
    
    
    
    
    
    
    
    
