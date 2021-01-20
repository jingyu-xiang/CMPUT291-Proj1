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

def input_birth_info(uid):
    global connection, cursor
    have_mom = True
    have_dad = True
    
    print('***Information of the newborn will be entered in this section***')
    fname = ''
    lname = ''
    while True:
        if (len(fname)==0 ):
            fname = input("Enter the first name: ")
            continue
        elif(len(lname)==0):
            lname = input("Enter the last name: ")
            continue
        elif(len(fname) !=0 and len(lname) != 0):
            break 
    cursor.execute("Select * From persons Where UPPER(fname)=:fname And UPPER(lname)=:lname;",{"fname":fname.upper(), "lname":lname.upper()})
    rows = cursor.fetchall()
    #print(rows)
    if len(rows) > 0:
        print("the newborn's name is already existent in persons table. Now return to the operation menu page")
        return
    elif len(rows) == 0:
        
        #**info of the newborn
        gender = input('Enter the gender, "M" for male and "F" for female: ')
        while gender not in ('M', 'F', 'm', 'f'):
            print('Please enter a valid gender')  
            gender = input('Enter the gender, "M" for male and "F" for female: ')
        gender = gender.upper()
        birthDate = input('Enter the birthdate in the format YYYY-MM-DD: ')
        if len(birthDate) == 0:
            birthDate = None
        birthPlace = input('Enter the birthplace of the newborn: ')
        if len(birthPlace) == 0:
            birthPlace = None        
        now = datetime.now()
        regDate = now. strftime("%Y-%m-%d")
        #print(regDate)
        cursor.execute("Select city From users Where uid=:uid;",{"uid":uid})
        regPlace = cursor.fetchone()[0]
        #print(regPlace)
        cursor.execute("Select Max(regno) From births")
        maxRegno = cursor.fetchone()[0]
        regNo = int(maxRegno + 10)
        #print(regNo)
        
        
        #**info of the father
        print('***Information of the father will be entered in this section***')
        f_fname = ''
        f_lname = ''
        while True:
            if (len(f_fname)==0 ):
                f_fname = input("Enter the father's first name: ")
                continue
            elif(len(f_lname)==0):
                f_lname = input("Enter the father's last name: ")
                continue
            elif(len(f_fname) !=0 and len(f_lname) != 0):
                break
        cursor.execute("Select * From persons Where UPPER(fname)=:f_fname And UPPER(lname)=:f_lname ",{"f_fname":f_fname.upper(), "f_lname":f_lname.upper()})
        rows1 = cursor.fetchall()
        
        #print(rows1)
        if len(rows1) == 0:#No father info
            have_dad = False
            f_birthDate = input("Enter the father's birth date in the format YYYY-MM-DD: ")
            if len(f_birthDate) == 0:
                f_birthDate = None            
            f_birthPlace = input("Enter the father's birth place: ")
            if len(f_birthPlace) == 0:
                f_birthPlace = None            
            f_PhoneNum = input("Enter the father's phone number: ")
            if len(f_PhoneNum) == 0:
                f_PhoneNum = None            
            f_address = input("Enter the father's address: ")
            if len(f_address) == 0:
                f_address = None            
            insertion_f = [f_fname, f_lname, f_birthDate, f_birthPlace, f_address, f_PhoneNum]
            #print(insertion_f)
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_f);
            connection.commit()
            
        
        #**info of the mother
        print('***Information of the mother will be entered in this section***')     
        m_fname = ''
        m_lname = ''
        while True:
            if (len(m_fname)==0 ):
                m_fname = input("Enter the mother's first name: ")
                continue
            elif(len(m_lname)==0):
                m_lname = input("Enter the mother's last name: ")
                continue
            elif(len(m_fname) !=0 and len(m_lname) != 0):
                break
        cursor.execute("Select * From persons Where UPPER(fname)=:m_fname And UPPER(lname)=:m_lname",{"m_fname":m_fname.upper(), "m_lname":m_lname.upper()})
        rows2 = cursor.fetchall()
        #print(rows2)
        if len(rows2) == 0:#No mother info
            have_mom = False
            m_birthDate = input("Enter the mother's birth date in the format YYYY-MM-DD: ")
            if len(m_birthDate) == 0:
                m_birthDate = None
            m_birthPlace = input("Enter the mother's birth place: ")
            if len(m_birthPlace) == 0:
                m_birthPlace = None
            m_PhoneNum = input("Enter the mother's phone number: ")
            if len(m_PhoneNum) == 0:
                m_PhoneNum = None
            m_address = input("Enter the mother's address: ")
            if len(m_address) == 0:
                m_address = None
            insertion_m = [m_fname, m_lname, m_birthDate, m_birthPlace, m_address, m_PhoneNum]
            #print(insertion_m)
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_m);
            connection.commit()
         
        #**Insertion part   
        if have_mom == True:
            cursor.execute("Select * From persons Where fname=:m_fname And lname=:m_lname",{"m_fname":m_fname, "m_lname":m_lname})
            result = cursor.fetchone() 
            #print(result)
            addr = result[4]
            phone = result[5]
            insertion_nbp = [fname, lname, birthDate,  birthPlace, addr, phone]
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_nbp);
            connection.commit()
        else:
            insertion_nbp = [fname, lname, birthDate,  birthPlace, m_address, m_PhoneNum]
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_nbp);
            connection.commit() 
            
        if have_dad == False and have_mom == False:    
            insertion_nb = [regNo, fname, lname, regDate, regPlace, gender, f_fname, f_lname, m_fname, m_lname]
            cursor.execute("Insert into births VALUES(?,?,?,?,?,?,?,?,?,?)",insertion_nb);
            connection.commit()
        elif have_dad == True and have_mom == False:
            insertion_nb = [regNo, fname, lname, regDate, regPlace, gender, rows1[0][0], rows1[0][1], m_fname, m_lname]
            cursor.execute("Insert into births VALUES(?,?,?,?,?,?,?,?,?,?)",insertion_nb);
            connection.commit()            
        elif have_dad == False and have_mom == True:
            insertion_nb = [regNo, fname, lname, regDate, regPlace, gender, f_fname, f_lname, rows2[0][0], rows2[0][1]]
            cursor.execute("Insert into births VALUES(?,?,?,?,?,?,?,?,?,?)",insertion_nb);
            connection.commit()
        else:
            insertion_nb = [regNo, fname, lname, regDate, regPlace, gender, rows1[0][0], rows1[0][1], rows2[0][0], rows2[0][1]]
            cursor.execute("Insert into births VALUES(?,?,?,?,?,?,?,?,?,?)",insertion_nb);
            connection.commit()
        
        print("registration complete")
        

        
        
        
            
def main():
    global connection, cursor

    path="./Pro1.db"
    connect(path)
    uid = '1'
    input_birth_info(uid)
    connection.commit()
    connection.close()
    return    
    
    
if __name__ == "__main__":
    main()
