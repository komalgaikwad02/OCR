import mysql.connector
from datetime import datetime
from datetime import date

today = date.today()
def Mysql_connection():
    try:
        mydb = mysql.connector.connect(
            host="LocalHost",
            user="root",
            password="komal2894",
            database="OCR_PAN"
        )
        mycursor = mydb.cursor()
        return mydb, mycursor
    except:
        print("Mysql Connection Error...!")

def PAN_DataUpdate(FullName,FatherName,DOB,PAN_no):
    # PAN_no = ABDCS5237Q"
    if PAN_no[3] == 'P':
        Remarks = "It's Personal PanCard"
    else:
        Remarks = "Possible Fraud or Corporate Pan Card"

    # print(PAN_no[3])
    mydb, mycursor = Mysql_connection()

    print("FullName : "+ FullName + " FatherName : " + FatherName + " DOB : " + DOB + " PAN_no : "+ PAN_no + " Remarks : "+ Remarks)
    if mydb:
        sql = 'INSERT INTO OCR_PAN_Details (Record_Insert_Date, FullName, FatherName, DOB, PAN_no,Remarks) VALUES (NOW(),"{1}", "{2}", "{3}","{4}","{5}");'.format(today,FullName, FatherName,datetime.strptime(DOB,'%d/%m/%Y') , PAN_no,Remarks)
        mycursor.execute(sql)
        mydb.commit()
        print(str(mycursor.rowcount) + " new Record Inserted! ")

def Adhar_DataUpdate(FullName,Gender,DOB,Adhar_no):
    Adhar_masking = Adhar_no[:2] + 'X' * 8 + Adhar_no[-2:]
    mydb, mycursor = Mysql_connection()
    print("FullName : "+ FullName + " Gender : " + Gender + " DOB : " + DOB + " Adhar_no : " + Adhar_no + " Adhar_masking : "+ Adhar_masking)
    if mydb:
        sql = 'INSERT INTO OCR_Adhar_Details (Record_Insert_Date, FullName, Gender, DOB, Adhar_no, Adhar_masking) VALUES (NOW(),"{1}", "{2}", "{3}","{4}","{5}");'.format(today,FullName, Gender, DOB , Adhar_no, Adhar_masking)
        mycursor.execute(sql)
        mydb.commit()
        print(str(mycursor.rowcount) + " new Feedbacks Inserted! ")


def Create_table_query_for_PAN():
    mydb, mycursor = Mysql_connection()
    if mycursor:
        create_table_query = "CREATE TABLE OCR_PAN_Details (Record_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,Record_Insert_Date TIMESTAMP,FullName VARCHAR(255) NOT NULL, FatherName VARCHAR(255) NOT NULL, DOB DATE NOT NULL, PAN_no VARCHAR(255) NOT NULL,Remarks VARCHAR(255) NOT NULL)"
        mycursor.execute(create_table_query)

def Create_table_query_for_Adhar():
    mydb, mycursor = Mysql_connection()
    if mycursor:
        create_table_query = "CREATE TABLE OCR_Adhar_Details (Record_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,Record_Insert_Date TIMESTAMP,FullName VARCHAR(255) NOT NULL, Gender VARCHAR(255) NOT NULL, DOB VARCHAR(255) NOT NULL, Adhar_no VARCHAR(255) NOT NULL,Adhar_masking VARCHAR(255)NOT NULL)"
        mycursor.execute(create_table_query)


def Show_OCR_table():
    mydb, mycursor = Mysql_connection()
    if mycursor:
        mycursor.execute("SELECT * FROM OCR_PAN_Details")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)

# Create_table_query_for_PAN()
# Create_table_query_for_Adhar()



# PAN_DataUpdate("GAIKWAD GANESH DHARMA","DHARMA SHRIPATI GAIKWAD","14/07/1988", "AYMPG6130B")
# Show_OCR_table()
