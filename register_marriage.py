import sqlite3
from datetime import datetime
import sys
connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def input_marriage_info(uid):
    global connection, cursor
    p1_exist = True
    p2_exist = True

    #**get partner1's information
    print(" information about the partner1 will be entered in this section")
    p1_fname = ''
    p1_lname = ''
    while True:
            if (len(p1_fname)==0 ):
                p1_fname = input("Enter partner1's first name: ")
                continue
            elif(len(p1_lname)==0):
                p1_lname = input("Enter partner1's last name: ")
                continue
            elif(len(p1_fname) !=0 and len(p1_lname) != 0):
                break
    cursor.execute("Select * From persons Where UPPER(fname)=:p1_fname And UPPER(lname)=:p1_lname;",{"p1_fname":p1_fname.upper(), "p1_lname":p1_lname.upper()})
    p1_name = cursor.fetchall()
    if len(p1_name) ==1:#exist in persons
        pass
        #print(p1_name[0][0])
        #print(p1_name[0][1])
    elif len(p1_name) == 0:
        p1_exist = False
        p1_Birthdate = input("Enter partner1's birth date in the format YYYY-MM-DD: ")
        if len(p1_Birthdate) == 0:
            p1_Birthdate = None
        p1_birthPlace = input('Enter the birthplace of partner1: ')
        if len(p1_birthPlace) == 0:
            p1_birthPlace = None
        p1_PhoneNum = input("Enter partner1's phone number: ")
        if len(p1_PhoneNum) == 0:
            p1_PhoneNum = None
        p1_address = input("Enter partner1's address: ")
        if len(p1_address) == 0:
            p1_address = None
        insertion_p1 = [p1_fname,  p1_lname, p1_Birthdate, p1_birthPlace,  p1_PhoneNum,  p1_address]
        #print(insertion_p1)
        cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_p1);
        connection.commit()

    #**get partner2's information
    print(" information about the partner2 will be entered in this section")
    p2_fname = ''
    p2_lname = ''
    while True:
            if (len(p2_fname)==0 ):
                p2_fname = input("Enter partner2's first name: ")
                continue
            elif(len(p2_lname)==0):
                p2_lname = input("Enter partner2's last name: ")
                continue
            elif(len(p2_fname) !=0 and len(p2_lname) != 0):
                break
    cursor.execute("Select * From persons Where fname=:p2_fname collate nocase And lname=:p2_lname collate nocase;",{"p2_fname":p2_fname, "p2_lname":p2_lname})
    p2_name = cursor.fetchall()
    if len(p2_name) ==1:#exist in persons
        pass
    elif len(p2_name) == 0:
        p2_exist = False
        p2_Birthdate = input("Enter partner2's birth date in the format YYYY-MM-DD: ")
        if len(p2_Birthdate) == 0:
            p2_Birthdate = None        
        p2_birthPlace = input('Enter the birthplace of partner2: ')
        if len(p2_birthPlace) == 0:
            p2_birthPlace = None        
        p2_PhoneNum = input("Enter partner2's phone number: ")
        if len(p2_PhoneNum) == 0:
            p2_PhoneNum = None        
        p2_address = input("Enter partner2's address: ")
        if len(p2_address) == 0:
            p2_address = None        
        insertion_p2 = [p2_fname,  p2_lname, p2_Birthdate, p2_birthPlace,  p2_PhoneNum,  p2_address]
        #print(insertion_p2)
        cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_p2);
        # connection.commit()


    #**generate RegPlace and RegNo and Insertion
    cursor.execute("Select city From users Where uid=:uid;",{"uid":uid})
    regPlace = cursor.fetchone()[0]
    cursor.execute("Select Max(regno) From marriages")
    maxRegno = cursor.fetchone()[0]
    regNo = int(maxRegno + 10)
    now = datetime.now()
    regDate = now.strftime("%Y-%m-%d")

    if p1_exist == False and p2_exist == False:
        insertion_mrg = [regNo, regDate, regPlace, p1_fname, p1_lname, p2_fname, p2_lname]
        #print(insertion_mrg)
        cursor.execute("Insert into marriages VALUES(?,?,?,?,?,?,?)",insertion_mrg);
        # connection.commit()
        print("registration complete")
    elif p1_exist == True and p2_exist == False:
        insertion_mrg = [regNo, regDate, regPlace, p1_name[0][0], p1_name[0][1], p2_fname, p2_lname]
        #print(insertion_mrg)
        cursor.execute("Insert into marriages VALUES(?,?,?,?,?,?,?)",insertion_mrg);
        # connection.commit()
        print("registration complete")
    elif p1_exist == False and p2_exist == True:
        insertion_mrg = [regNo, regDate, regPlace, p1_fname, p1_lname, p2_name[0][0], p2_name[0][1]]
        #print(insertion_mrg)
        cursor.execute("Insert into marriages VALUES(?,?,?,?,?,?,?)",insertion_mrg);
        # connection.commit()
        print("registration complete")
    else:
        insertion_mrg = [regNo, regDate, regPlace, p1_name[0][0], p1_name[0][1], p2_name[0][0], p2_name[0][1]]
        #print(insertion_mrg)
        cursor.execute("Insert into marriages VALUES(?,?,?,?,?,?,?)",insertion_mrg);
        # connection.commit()
        print("registration complete")    



def main():
    global connection, cursor

    path="./Pro1.db"
    connect(path)
    uid = '1'
    input_marriage_info(uid)
    connection.commit()
    connection.close()
    return    
    
    
if __name__ == "__main__":
    main()