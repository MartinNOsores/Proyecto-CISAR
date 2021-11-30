import sqlite3
from time import sleep
from sqlite3 import Error
from datetime import date
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
edad = 0
nombre_apellido = ""
fechanac = ""
curso = ""
division = ""
especialidad = ""
numero_tarjeta_rfid = ""

GPIO.setwarnings(False)

conn = sqlite3.connect("/home/pi/Desktop/CISAR_DB.db")
c = conn.cursor()

#c.execute("""CREATE TABLE usuarios (
                    #nombre text,
                     #edad integer,
                     #curso integer,
                     #division integer,
                     #especialidad integer,
                     #numero_tarjeta_rfid integer
                     #)""");

def tomarValores(c):

    '''NOMBRE & APELLIDO --> nombre_apellido ''' 

    print("-> Ingrese su nombre y apellido: \n")
    nombre_apellido = input()
    
    for char in nombre_apellido:
        if char.isalpha() or char == " " and not char.isnumeric():
            continue
        else:
            print("\n [!] Ingrese un nombre y apellido valido [!]")
            exit()
            

    '''FECHA NACIMIENTO'''

    print("\n-> Ingrese su fecha de nacimiento con el siguiente formato: ")
    sleep(.5)
    print("-> EJEMPLO: DD/MM/AAAA \n")
    
    fechanac = input()
    sleep(.5)

    edad = calcularEdad(fechanac)

    '''CURSO y DIVISION --> curso_division '''
    sleep(.5)
    print("\n-> Seleccione su curso: \n")
    sleep(.5)
    print("[1] 1er año")
    sleep(.5)
    print("[2] 2do año")
    sleep(.5)
    print("[3] 3er año")
    sleep(.5)
    print("[4] 4to año")
    sleep(.5)
    print("[5] 5to año")
    sleep(.5)
    print("[6] 6to año")
    sleep(.5)
    print("[7] 7mo año\n")

    token = input()

    if token == "1":
        curso = "1ero"
    elif token == "2":
        curso = "2do"
    elif token == "3":
        curso = "3ero"
    elif token == "4":
        curso = "4to"
    elif token == "5":
        curso = "5to"
    elif token == "6":
        curso = "6to"
    elif token == "7":
        curso = "7mo"
    elif token != "1" or "2" or "3" or "4" or "5" or "6" or "7":
        print("Seleccione un curso disponible")
        exit()
    print("\n######################")

    '''DIVISION --> division '''
    sleep(.5)
    print("\n-> Seleccione su division: \n")
    sleep(.5)
    print("[1] Primera")
    sleep(.5)
    print("[2] Segunda")
    if (curso == "1ero" or curso == "2do" or curso == "3ero"):
        sleep(.5)
        print("[3] Tercera")
        sleep(.5)
        print("[4] Cuarta")
        sleep(.5)
        print("[5] Quinta")
        sleep(.5)
    else:
#     (curso == "4to" or "5to" or "6to" or "7mo"):
        pass

    print("\n") 
    token = input()
    
    if token == "1":
        division = "1era"
    elif token == "2":
        division = "2da"
    elif token == "3":
        division = "3era"
    elif token == "4":
        division = "4ta"
    elif token == "5":
        division = "5ta"
    elif token != ("1" and "2" and "3" and "4" and "5"):
        print("\nElija una division disponible")
        exit()
    print("\n######################")
    
    if curso == "4to" or curso == "5to" or curso == "6to" or curso == "7mo":
        print("\n-> Elija su especialidad: ")
        sleep(.5)
        print("[1] AVIONICA")
        sleep(.5)
        print("[2] AERONAUTICA\n")
        sleep(.5)
        
        token = input()

        if token == "1":
            especialidad = "AVC" 
        elif token == "2":
            especialidad = "AERO"  
        elif token != "1" or "2":
            print("Elija una especialidad disponible")
    
    elif("1ero" or "2do" or "3ero"):
        especialidad = " - "
        pass
            
    
        print("\n######################")

    '''NACIONALIDAD'''

    #print("\n-> Ingrese su nacionalidad: \n")
    #nacionalidad = input()
    #sleep(.5)
    
    '''TARJETA'''
    print("-> Apoye la tarjeta sobre el sensor")
    try:
        id, text = reader.read()
        numero_tarjeta_rfid = id
        
    finally:
        GPIO.cleanup()

    c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", (nombre_apellido, edad, curso, division, especialidad, numero_tarjeta_rfid))

    print("\n###########################################")
    print("\n   [!] Datos cargados correctamente [!]  \n")
    print("###########################################\n")

def calcularEdad(fechanac):
    
    fechahoy = date.today()
    day = int((fechanac[0:2]))
    month = int((fechanac[3:5]))
    year = int((fechanac[6:]))
    
    #if (year > fechahoy.year): #or month > fechahoy.month or day > fechahoy.day:
        #print("\n [!] Ingrese una fecha de nacimiento valida [!]")
        #exit()
    #else:
        #pass
    
    edad = fechahoy.year - year - ((fechahoy.month, fechahoy.day) < (month, day))

    return edad

tomarValores(c)

conn.commit()

conn.close()
             
#c.execute("INSERT INTO usuarios VALUES ('Pedro', '21', 'Chileno')")
#id INTEGER PRIMARY KEY AUTOINCREMENT,

#fetchone, fetchall (11)

