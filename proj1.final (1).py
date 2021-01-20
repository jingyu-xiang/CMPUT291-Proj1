import sqlite3
import getpass
import re
import time
import datetime
from datetime import datetime
import sys

connection = None
cursor = None
userName = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    connection.commit()
    return


def Login():
    global userName
    result = False
    Login_type = 0
    count = 0

    print("Please enter username and password, you can try at most 3 times:")

    # check validity of username and passWord to counter command line injection
    while True:
        while (count < 3):
            print("%d tries remain" %(3 - count))
            count += 1

            userName = input("User ID:")
            if not re.match("^[A-Za-z0-9_]*$", userName):
                print("Error: Username is not in valid format!")
                continue

            passWord = getpass.getpass()
            if not re.match("^[A-Za-z0-9_]*$", passWord):
                print("Error: Password is not in valid format!")
                continue
            else:
                result = True
                break

        if (result == False or count  >= 3):
            print('Access denied')
            sys.exit()

        cursor.execute("Select * From users Where uid=:uid collate nocase And pwd=:pwd;",{"uid":userName, "pwd":passWord} )
        user = cursor.fetchone()
        if not user:
            print("Access denied")
            # sys.exit()
        else:
            if 'a' in user:
                Login_type = 1
                return Login_type
            if 'o' in user:
                Login_type = 2
                return Login_type


def input_name():
    fname = ''
    lname = ''
    while True:
        if len(fname)==0:
            fname = input("Enter the first name: ")
            continue
        elif not re.match("^[A-Za-z0-9_]*$", fname):
            fname = input("Name in invalid format!\nEnter the first name: ")
            continue
        if len(lname)==0:
            lname = input("Enter the last name: ")
            continue
        if not re.match("^[A-Za-z0-9_]*$", lname):
            lname = input("Name in invalid format!\nEnter the last name: ")
            continue

        break

    return fname, lname

def input_person_info(type):

    while True:
        birthDate = input("Enter birth date in the format YYYY-MM-DD: ")
        if len(birthDate) != 0 and not re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", birthDate):
            print("Error: Birthdate is not in valid format!")
            continue
        if len(birthDate) == 0:
            birthDate = None
            break
        break

    while True:
        birthPlace = input('Enter the birthplace of the newborn: ')
        if len(birthPlace) == 0:
            birthPlace = None
            break
        elif len(birthPlace) > 20:
            print("Length of birth place exceed 20!")
            continue
        break

    if type == 'child':
        return birthDate, birthPlace

    if type == 'adult':
        while True:
            PhoneNum = input("Enter the phone number: ")
            if len(PhoneNum) == 0:
                PhoneNum = None
                break;
            elif len(PhoneNum) > 12:
                print("Length  of phone number exceed 12!")
                continue
            break
        while True:
            address = input("Enter address: ")
            if len(address) == 0:
                address = None
                break
            elif len(address) > 30:
                print("Length  of address exceed 30!")
                continue
            break


    return birthDate, birthPlace, PhoneNum, address



# q1
def input_birth_info(uid):
    global connection, cursor
    have_mom = True
    have_dad = True

    print('***Information of the newborn will be entered in this section***')

    fname, lname = input_name()
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

        birthDate, birthPlace, = input_person_info('child')

        # assign new registration number
        now = datetime.now()
        regDate = now. strftime("%Y-%m-%d")
        cursor.execute("Select city From users Where uid=:uid;",{"uid":uid})
        regPlace = cursor.fetchone()[0]
        #print(regPlace)
        cursor.execute("Select Max(regno) From births")
        maxRegno = cursor.fetchone()[0]
        regNo = int(maxRegno + 10)
        #print(regNo)


        #**info of the father
        print('***Information of the father will be entered in this section***')

        f_fname, f_lname = input_name()
        cursor.execute("Select * From persons Where UPPER(fname)=:f_fname And UPPER(lname)=:f_lname ",{"f_fname":f_fname.upper(), "f_lname":f_lname.upper()})
        rows1 = cursor.fetchall()

        #print(rows1)
        if len(rows1) == 0:#No father info
            have_dad = False

            f_birthDate, f_birthPlace, f_PhoneNum, f_address = input_person_info('adult')
            insertion_f = [f_fname, f_lname, f_birthDate, f_birthPlace, f_address, f_PhoneNum]
            #print(insertion_f)
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_f);
            connection.commit()


        #**info of the mother
        print('***Information of the mother will be entered in this section***')

        m_fname, m_lname = input_name()
        cursor.execute("Select * From persons Where UPPER(fname)=:m_fname And UPPER(lname)=:m_lname",{"m_fname":m_fname.upper(), "m_lname":m_lname.upper()})
        rows2 = cursor.fetchall()
        #print(rows2)
        if len(rows2) == 0:#No mother info
            have_mom = False

            m_birthDate, m_birthPlace, m_PhoneNum, m_address = input_person_info('adult')

            insertion_m = [m_fname, m_lname, m_birthDate, m_birthPlace, m_address, m_PhoneNum]
            #print(insertion_m)
            cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_m);
            connection.commit()


        # if mom and dad are the same person
        if (m_fname.upper() == f_fname.upper()) and (m_lname.upper() == f_lname.upper()):
            print("Father and mother can not be the same person!, now return to the operation menu")
            return

        #**Insertion part
        if have_mom == True:
            cursor.execute("Select * From persons Where UPPER(fname)=:m_fname And UPPER(lname)=:m_lname",{"m_fname":m_fname.upper(), "m_lname":m_lname.upper()})
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

        return

# q2
def input_marriage_info(uid):
    global connection, cursor
    p1_exist = True
    p2_exist = True

    #**get partner1's information
    print(" information about the partner1 will be entered in this section")

    p1_fname, p1_lname = input_name()
    cursor.execute("Select * From persons Where UPPER(fname)=:p1_fname And UPPER(lname)=:p1_lname;",{"p1_fname":p1_fname.upper(), "p1_lname":p1_lname.upper()})
    p1_name = cursor.fetchall()
    if len(p1_name) ==1:#exist in persons
        pass
        #print(p1_name[0][0])
        #print(p1_name[0][1])
    elif len(p1_name) == 0:
        p1_exist = False

        p1_Birthdate, p1_birthPlace, p1_PhoneNum, p1_address = input_person_info('adult')

        insertion_p1 = [p1_fname,  p1_lname, p1_Birthdate, p1_birthPlace,  p1_PhoneNum,  p1_address]
        #print(insertion_p1)
        cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_p1);
        connection.commit()

    #**get partner2's information
    print(" information about the partner2 will be entered in this section")

    p2_fname, p2_lname = input_name()

    cursor.execute("Select * From persons Where fname=:p2_fname collate nocase And lname=:p2_lname collate nocase;",{"p2_fname":p2_fname, "p2_lname":p2_lname})
    p2_name = cursor.fetchall()
    if len(p2_name) ==1:#exist in persons
        pass
    elif len(p2_name) == 0:
        p2_exist = False

        p2_Birthdate, p2_birthPlace, p2_PhoneNum, p2_address = input_person_info('adult')
        insertion_p2 = [p2_fname,  p2_lname, p2_Birthdate, p2_birthPlace,  p2_PhoneNum,  p2_address]
        #print(insertion_p2)
        cursor.execute("Insert into persons VALUES(?,?,?,?,?,?)",insertion_p2);
        connection.commit()


    # if partner 1 and 2 are the same person
    if (p1_fname.upper() == p2_fname.upper()) and (p1_lname.upper() == p2_lname.upper()):
        print("partner1 and partner2 can not be the same person! Now return to the operation menu")
        return

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
    connection.commit()
    return


# q3
def renew_registration(user_regno):
    regno = (user_regno,)
    current_date = time.strftime("%Y-%m-%d")
    cursor.execute(' SELECT expiry FROM registrations WHERE regno =?;', regno)
    old_expiry = cursor.fetchone()
    if not old_expiry:
        print("Registration doesn't exist!")
        return

    # if expired
    if (old_expiry[0] <= current_date):
        year=int(current_date[0:4])
        new_expiry_year= year + 1
        new_date = str(new_expiry_year)+current_date[4:10]
        data1 = ((new_date), user_regno)
        cursor.execute('UPDATE registrations SET expiry =? WHERE regno =?;', data1)

    # if not expired
    elif (old_expiry[0] > current_date):
        year=int(old_expiry[0][0:4])
        new_expiry_year= year + 1
        new_date=str(new_expiry_year)+old_expiry[0][4:10]
        data1 = ((new_date),user_regno)
        cursor.execute('UPDATE registrations SET expiry =? WHERE regno =?;', data1)

    print("*"*8+"finish renewing"+"*"*8+"\n")

    connection.commit()
    return



#q4
def process_bill(vin, oldfname, oldlname, newfname, newlname, newplate):
    # check if the car exisits in the system
    cursor.execute("SELECT vin FROM registrations WHERE vin =:user_vin COLLATE NOCASE;", {"user_vin": vin})
    result = cursor.fetchone()
    if not result:
        print("Error: Car doesn't exisit in the system")
        return
    else:
        correct_vin = result[0]
    # check if the seller is the latest owner
    data = (vin, oldfname, oldlname)
    sql = ''' SELECT * FROM registrations AS r
            WHERE r.vin =? COLLATE NOCASE
            AND r.fname =?  COLLATE NOCASE AND r.lname =? COLLATE NOCASE
            AND r.expiry = (SELECT MAX(expiry) FROM registrations AS r1 GROUP BY r1.vin COLLATE NOCASE HAVING r1.vin = r.vin COLLATE NOCASE); '''
    cursor.execute(sql, data)
    result = cursor.fetchall()

    if not len(result):
        print("Error: Seller is not the latest owner!")
        return

    # update/invalid seller's registration
    current_date = time.strftime("%Y-%m-%d")
    data = (current_date, oldfname, oldlname)
    cursor.execute('''UPDATE registrations SET expiry =?
                    WHERE fname =? COLLATE NOCASE AND lname =? COLLATE NOCASE;''', data)

    # assign new registration to buyer
    newname = (newfname, newlname)
    cursor.execute("SELECT fname, lname FROM persons WHERE fname =? COLLATE NOCASE AND lname =? COLLATE NOCASE;", newname)
    result = cursor.fetchone()
    if not result:
        print( "Error: Buyer doesn't exist in persons table")
        return
    else:
        correct_fname = result[0]
        correct_lname = result[1]

    # assign a new latest regno, and double check if it regno is indeed unique
    while True:
        cursor.execute('SELECT * FROM registrations ORDER BY regno DESC LIMIT 1; ')
        latest_regno = cursor.fetchone()['regno'] + 1

        cursor.execute('SELECT * FROM registrations WHERE regno = :new', {"new": latest_regno})
        if cursor.fetchone() == None:
            break

    year=int(current_date[0:4])
    new_expiry_year= year + 1
    new_date = str(new_expiry_year)+current_date[4:10]

    data = (latest_regno, current_date, new_date, newplate, correct_vin, correct_fname, correct_lname)
    cursor.execute( "INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?);", data)

    print("*"*8+"finish processing bill"+"*"*8+"\n")

    connection.commit()
    return



# q5
def process_payment(tno, amount):
    # check if payment amount is an integer
    try:
        val = int(amount)
    except ValueError:
        print("Error: Payment amount is not an integer!")
        return

        # check if tno is correct, i.e. indeed exisit
    cursor.execute('SELECT * FROM tickets WHERE tno = :given;', {"given": tno})
    result = cursor.fetchone()
    if result == None:
        print("Error: ticket number doesn't exist!")
        return
    fine_amount = result['fine']


    current_date = time.strftime("%Y-%m-%d")
    data = (tno, current_date)
    cursor.execute('SELECT * FROM payments WHERE tno =? AND pdate =?;', data)
    if cursor.fetchone():
        print("Error: ticket already been paid on %s" %current_date)
        return

    cursor.execute('SELECT SUM(amount) FROM payments WHERE tno =:given;', {"given": tno})
    paid_amount = cursor.fetchone()[0]
    if paid_amount != None:
        if (paid_amount + amount > fine_amount):
            print("Error: Payment amount exceeding fine amount")

    data = (tno, current_date, amount)
    cursor.execute('INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?);', data)

    print("*"*8+"finish processing payment"+"*"*8+"\n")
    connection.commit()
    return



# q6
def get_driver_abstract(fname, lname):
    name = (fname, lname)
    cursor.execute("SELECT * FROM persons WHERE fname =? COLLATE NOCASE AND lname =? COLLATE NOCASE;", name)
    if not cursor.fetchone():
        print("Error: Person doesn't exist in the system!")
        return

    # find total number of tickets, dnotices, dpoints within life time
    cursor.execute("SELECT COUNT(t.tno) FROM registrations AS r, tickets AS t WHERE r.regno = t.regno AND r.fname =? COLLATE NOCASE AND r.lname =? COLLATE NOCASE GROUP BY r.regno;", name)
    result = cursor.fetchone()
    if not result:
        ltotal_ticket = 0
    else:
        ltotal_ticket = result[0]

    cursor.execute("SELECT COUNT(ddate), SUM(points) FROM demeritNotices WHERE fname =? COLLATE NOCASE AND lname =? COLLATE NOCASE", name)
    result = cursor.fetchone()
    if not result:
        ltotal_dpoint = 0
        ltotal_dnotice = 0
    else:
        ltotal_dnotice = result[0]
        ltotal_dpoint = result[1]

    print("-"*15)
    print("Number of total ticket within lifetime: ",ltotal_ticket)
    print("Number of total demerit notices within lifetime: ", ltotal_dnotice)
    print("Number of total demerit points within lifetime: ", ltotal_dpoint)

    # find total number of tickets, dnotices, dpoints within past 2 years
    current_date = time.strftime("%Y-%m-%d")
    year=int(current_date[0:4])
    threshold_year= year - 2
    threshold = str(threshold_year)+current_date[4:10]
    data = (fname, lname, threshold)

    cursor.execute("SELECT COUNT(t.tno) FROM registrations AS r, tickets AS t WHERE r.regno = t.regno AND r.fname =? COLLATE NOCASE AND r.lname =? COLLATE NOCASE AND t.vdate >=? GROUP BY r.regno;", data)
    result = cursor.fetchone()
    if not result:
        stotal_ticket = 0
    else:
        stotal_ticket = result[0]

    cursor.execute("SELECT COUNT(ddate), SUM(points) FROM demeritNotices WHERE fname =? COLLATE NOCASE AND lname =? COLLATE NOCASE AND ddate >=?", data)
    result = cursor.fetchone()
    if not result:
        stotal_dnotice = 0
        stotal_dpoint = 0
    else:
        stotal_dnotice = result[0]
        stotal_dpoint = result[1]
    print("-"*15)
    print("Number of total ticket within 2 years: ",stotal_ticket)
    print("Number of total demerit notices within 2 years: ", stotal_dnotice)
    print("Number of total demerit points within 2 years: ", stotal_dpoint)
    print( "-"*15)

    # find total number of tickets, dnotices, dpoints within past 2 years
    if ltotal_ticket == 0:
        print("No ticket in past years!")
        return
    if input("Enter y/Y to see past tickets, otherwise return to the main menu: ").lower() != 'y':
        return

    sql = '''
            SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
            FROM registrations AS r, tickets AS t, vehicles AS v
            WHERE r.fname =? COLLATE NOCASE AND r.lname =? COLLATE NOCASE
            AND r.regno = t.regno AND r.vin = v.vin
            ORDER BY t.vdate DESC;
            '''
    cursor.execute(sql, name)
    rows = cursor.fetchall()
    nameList = ["----------\nticket number:", "violation date:", "violation description:", "fine amount:", "registration number:", "vehicle make:", "vehicle model:"]

    if ltotal_ticket > 5:
        for i in range(5):
            temp = "\n".join("{} {}".format(x, y) for x, y in zip(nameList, rows[i]))
            print(temp)

        if input("Enter y/Y to see more ticket, otherwise return to the main menu: ").lower() == 'y':
            for i in range(5, len(rows)):
                temp = "\n".join("{} {}".format(x, y) for x, y in zip(nameList, rows[i]))
                print(temp)
    else:
        for i in range(ltotal_ticket):
            temp = "\n".join("{} {}".format(x, y) for x, y in zip(nameList, rows[i]))
            print(temp)
        print("*****All ticket records has been shown!*****")

    return



#7
def issue_ticket(registrations_regno):
    regno = (registrations_regno,)
    current_date = time.strftime("%Y-%m-%d")
    cursor.execute(' SELECT fname,lname, make, model, year, color FROM registrations left outer join vehicles WHERE regno =? AND registrations.vin=vehicles.vin;', regno)
    result = cursor.fetchone()
    if not result:
        print( '\n'+'*****registrations number is not found*****'+'\n')
        return
    print('person name: ',result[0],result[1])
    print('make: ',result[2])
    print('model: ',result[3])
    print('year: ',result[4])
    print('color: ',result[5])

    #choose proceed or not
    while True:
        answer = input("Proceed and ticket?(yes/no): ")
        if answer.lower() == "no":
            return;
        elif answer.lower() == "yes":
            break;

    #enter details
    else:
        vdate = input("violation date YYYY-MM-DD:")
        if vdate == "":
            vdate = current_date
        vtext = input("violation description:")
        while True:
            try:
                fine  = int(input("fine amout:"))
            except ValueError:
                print("Error: Fine amount is not an integer!")
                continue
            else:
                break

    #give a ticket_no
    cursor.execute('SELECT * FROM tickets ORDER BY tno DESC LIMIT 1; ')
    new_ticket_no = cursor.fetchone()['tno'] + 1

    #insert
    insertion = [new_ticket_no,registrations_regno,fine,vtext,vdate]
    cursor.execute('Insert into tickets VALUES (?,?,?,?,?);',insertion)
    print('\n'+'*****The ticket has successfully recorded*****'+'\n')
    connection.commit()
    return


#8
def find_car_owner(make,model,year,color,plate):

    if make=='':
        make='%%'
    if model=='':
        model='%%'
    if year=='':
        year='%%'
    if color=='':
        color='%%'
    if plate=='':
        plate='%%'

    data = [make,model,year,color,plate]

    cursor.execute(' SELECT  COUNT(DISTINCT vin) FROM vehicles left OUTER join registrations  using (vin) WHERE UPPER(make) LIKE UPPER(?) AND UPPER(model) LIKE UPPER(?) AND UPPER(year) LIKE UPPER(?) AND UPPER(color) LIKE UPPER(?) AND UPPER(plate) LIKE UPPER(?) ;',data)
    result_no = cursor.fetchone()

    if  result_no[0]==0:
        print('\n'+'*****Cannot find this car in the system******'+'\n')
        return

    print('\n*************************')
    print('There are',result_no[0],'matches founded')

    cursor.execute(' SELECT  * FROM vehicles left OUTER join registrations  using (vin) WHERE UPPER(make) LIKE UPPER(?) AND UPPER(model) LIKE UPPER(?) AND UPPER(year) LIKE UPPER(?) AND UPPER(color) LIKE UPPER(?) AND UPPER(plate) LIKE UPPER(?) GROUP BY VIN HAVING regdate=max(regdate) ;',data)
    result_11 = cursor.fetchall()
    if result_no[0]<4:
        for row in result_11:
            print('\n*************************')
            print('vin:',row[0])
            print('make:',row[1])
            print('model:',row[2])
            print('year:',row[3])
            print('color:',row[4])
            print('plate:',row[8])
            print('the latest registration date:',row[6])
            print('the expiry date:',row[7])
            print('the name of the person:',row[9],row[10])
        return

    else :
        for row in result_11:
            print('\n*************************')
            print('vin:',row[0])
            print('make:',row[1])
            print('model:',row[2])
            print('year:',row[3])
            print('color:',row[4])
            print('plate:',row[8])
        print('\n*************************')
        ans=input('enter a vin number to see details or enter exit:')
        if ans == '':
            return
        elif ans == 'exit':
            return
        vin=(ans,)
        data = [make,model,year,color,plate,vin]
        cursor.execute(' SELECT  * FROM vehicles left OUTER join registrations  using (vin) WHERE vehicles.vin=? ORDER BY regdate DESC limit 1;',vin)
        row = cursor.fetchone()

        print('\n*************************')
        print('vin:',row[0])
        print('make:',row[1])
        print('model:',row[2])
        print('year:',row[3])
        print('color:',row[4])
        print('plate:',row[8])
        print('the latest registration date:',row[6])
        print('the expiry date:',row[7])
        print('the name of the person:',row[9],row[10])
        print('\n')

        return




def main():

    path = input("Please enter name of the database: ")
    # path="./proj1.db"
    connect(path)
    Login_type = Login()

    while True:
        print("*****Please choose from functions bellow*****")
        if (Login_type == 1):#agent
            op_list = ['* press 1 to Register_birth', '* press 2 to Register_marriage', '* press 3 to Renew_vehicle_registration', '* press 4 to Process_bill', '* press 5 to Process_payment', '* press 6 to Get_driver_abstract', '* press 0 to Logout']
            for op in op_list:
                print(op)

        elif (Login_type == 2):#officier
            op1_list = ['* press 7 to issue_ticket', '* press 8 to find_car_owner', '* press 0 to Logout']
            for op in op1_list:
                print(op)

        op = input('choose an operation: ')
        if op == '0':
            break;
        elif op == '1' and Login_type == 1:#Register_birth
            input_birth_info(userName)

        elif op == '2' and Login_type == 1:#Register_marriage
            input_marriage_info(userName)

        elif op == '3' and Login_type == 1:#Renew_vehicle_registration
            while True:
                user_regno = input("Please enter registration number: ")
                if user_regno != '':
                    break
            renew_registration(user_regno)

        elif op == '4' and Login_type == 1:#Process_bill
            vin = oldfname = oldlname = newfname = newlname = newplate = ''
            while True:
                if (vin == ''):
                    vin = input("Enter vehicle's vin number: ")
                    continue
                if (oldfname == '' or oldlname == ''):
                    oldfname = input("Enter seller's first name: ")
                    oldlname = input("Enter seller's last name: ")
                    continue
                if (newfname == '' or newlname == ''):
                    newfname = input("Enter buyer's first name: ")
                    newlname = input("Enter buyer's last name: ")
                    continue
                if (newplate == '' or len(newplate) > 7):
                    newplate = input("Enter the new plate number: ")
                else:
                    break
            process_bill(vin, oldfname, oldlname, newfname, newlname, newplate)

        elif op == '5' and Login_type == 1:#Process_payment
            tno = amount = ''
            while True:
                if (tno == ''):
                    tno = input("Enter ticket number: ")
                    continue
                if (amount == ''):
                    amount = input("Enter payment amount: ")
                else:
                    break
            process_payment(tno, amount)

        elif op == '6' and Login_type == 1:#Get_driver_abstract
            fname = lname = ''
            while True:
                if fname == '':
                    fname = input("Enter the first name: ")
                    continue
                if lname == '':
                    lname = input("Enter the last name: ")
                else:
                    break
            get_driver_abstract(fname, lname)

        elif op == '7' and Login_type == 2:#issue_ticket
            regno = ''
            while regno == '':
                regno = input("Please enter registration number: ")
            issue_ticket(regno)

        elif op == '8' and Login_type == 2:#find_car_owner
            make = model = year = color = plate = ''
            while make == '' and model == '' and year == '' and color == '' and plate == '':
                make = input('make: ')
                model = input('model: ')
                year = input('year: ')
                color = input('color: ')
                plate = input('plate: ')
            find_car_owner(make,model,year,color,plate)


    # cursor.execute("SELECT * FROM marriages;")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row['p1_fname'], row['p1_lname'],row['p2_fname'], row['p2_lname'], row['regplace'], row['regno'])

    connection.commit()
    connection.close()
    return



if __name__ == "__main__":
    main()
