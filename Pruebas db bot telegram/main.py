import sqlite3
from time import sleep

tarjeta_july = 97700326497
tarjeta_drope = 261631149373
a = 0

sqliteConnection = sqlite3.connect('/Users/pedrogonzalez/Desktop/Pruebas db bot telegram/SQLite_Python.db')
cursor = sqliteConnection.cursor()

def insertVaribleIntoTable(nombre, curso, division, especialidad, numero_tarjeta_rfid):

    def crearTablaUsuarios():
        cursor.execute("""CREATE TABLE Usuarios ( 
            nombre text, 
            curso integer,
            division integer,
            especialidad integer,
            numero_tarjeta_rfid integer
            )""")

    try:
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Usuarios
                          (nombre, curso, division, especialidad, numero_tarjeta_rfid) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (nombre, curso, division, especialidad, numero_tarjeta_rfid)
        
        cursor.execute(sqlite_insert_with_param, data_tuple)
        
        sqliteConnection.commit()

        print("Python Variables inserted successfully into Usuarios table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def chequearUsuarios(numero_tarjeta_rfid):

    sqlite_select_query = """SELECT numero_tarjeta_rfid from Usuarios"""

    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    for row in records:
        print(row[0])
        if row[0] == tarjeta_july:
            print("YES, esta en la db", row)
            
        cursor.close()


chequearUsuarios(tarjeta_july)

#insertVaribleIntoTable("Pedro", "7mo", "2da", "AVC", "261631149373")
#insertVaribleIntoTable("July", "7mo", "2da", "AVC", "97700326497")


        
       
