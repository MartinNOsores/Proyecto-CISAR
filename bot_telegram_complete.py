import logging
import os
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, ConversationHandler, Filters
from decouple import config
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import sqlite3
from sqlite3 import Error
from datetime import date
import requests
import time

numero_tarjeta_rfid = int()
fechahoy = date.today()
fecha_hora = time.ctime()
edad = 0
check = 0
nombre_apellido = ""
fechanac= ""
curso = ""
division = ""
especialidad = ""
numero_tarjeta_rfid = ""
nombreuser = ""

DATABOT = "update: Update, context: CallbackContext"

datatuple = []

situacion = "Temperatura elevada"

replies = {
            "curso" : ["1ero", "2do", "3ero", "4to", "5to", "6to", "7mo"],
            "division" : ["1era", "2da", "3era", "4ta", "5ta"],
            "especialidad" : ["Avionica", "Aeronautica"]
                }

class CisarAPP(DATABOT):
    def __init__(self) -> None:
        reader = SimpleMFRC522()
        GPIO.setwarnings(False)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        logger = logging.getLogger(__name__)

    def crearBasedeDatos():
        sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/CISAR_DB.db')
        cursor = sqliteConnection.cursor()

        cursor.execute("""CREATE TABLE usuarios (    
                                nombre text,
                                curso integer,
                                division integer,
                                especialidad integer,
                                numero_tarjeta_rfid integer
                                )""");
    def subirBasedeDatos(update: Update, context: CallbackContext):
        sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/CISAR_DB.db')
        cursor = sqliteConnection.cursor()
        
        datatuple[0] = nombre_apellido
        datatuple[1] = curso
        datatuple[2] = division
        datatuple[3] = especialidad

        cursor.execute("INSERT INTO usuarios VALUES (?,?,?,?,?)", (nombre_apellido, curso, division, especialidad, numero_tarjeta_rfid))
        update.message.reply_text("Datos cargados satisfactoriamente!" + " \\U0002705")
        sqliteConnection.commit()
        sqliteConnection.close()

    def start(update: Update, context: CallbackContext) -> None:
        user = update.effective_user
    
        update.message.reply_markdown_v2(
        f"Buenas {user.mention_markdown_v2()}\! el bot de Cisar te saluda, en que puedo ayudarte? para desplegar mi lista de comandos haz clic en /ayuda \U0001F605",
        reply_markup=ForceReply(selective=True)
    )


    pass

    def voy_command(update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        update.message.reply_markdown_v2(
        fr'''Usted {user.mention_markdown_v2()}\! se está comprometiendo con proceder con el posible sospechoso, tenga cuidado''',
        reply_markup=ForceReply(selective=True)
    )

    def help_command(update: Update, context: CallbackContext) -> None:
        htext = "Mi lista de comandos: \n\n\t/Registro (Le permite registarse como alumno)\n\n\t/check (comprobar)\n\n\t/voy"
        update.message.reply_text(htext)

    def calcularEdad(fechanac):

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


class RegistrarAlumnos(CisarAPP):
    
    def echo(update: Update, context: CallbackContext) -> None:
        
        def registrarNombreApellido(update: Update, context: CallbackContext) -> int:
            global nombre_apellido
            user = update.effective_user
            update.message.reply_markdown_v2(
            fr'Hola {user.mention_markdown_v2()}\! le solicito que me mande su nombre y apellido completo por escrito'
            + '\n\nAsegurese de colocar su nombre y apellido correctamente, por favor ', reply_markup=ForceReply(selective=True), nombre_apellido = (update.message.text))
            nombre_apellido = (update.message.text)
            update.message.reply_text("Tu nombre y apellido completo es: \n\n" + nombre_apellido + "\n\npor favor haga clic en /continuar")
            print("nombre y apellido: " + nombre_apellido)
            datatuple.append(nombre_apellido)
            
        def registrarCurso(update: Update, context: CallbackContext) -> int:
            global curso
            reply_keyboard = [replies["curso"]]                
            update.message.reply_text('Indique su curso',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)
            curso = (update.message.text)
            print("Año: "+ curso)
            datatuple.append(curso)
            update.message.reply_text("Presione /division para continuar")

        def registrarDivision(update: Update, context: CallbackContext) -> int:
            global division
            
            if curso =='1ero' or curso =='2do' or curso =='3ero' :
                reply_keyboard = [replies["division"]]
            elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':
                reply_keyboard = [replies["division"][0:2]]

            update.message.reply_text( "Seleccione su division",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)
            division = (update.message.text)
            print("Division: " + division)
            datatuple.append(division)
            update.message.reply_text("Presione /especialidad para continuar")
            
        def registrarEspecialidad(update: Update, context: CallbackContext) -> int:
            global especialidad

            if curso =='1ero' or curso =='2do' or curso =='3ero' :
                especialidad = "S/N"

            elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':     
                reply_keyboard = [replies["especialidad"]]

            update.message.reply_text('Seleccione su especialidad', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'),)
            especialidad = (update.message.text)
            print("Especialidad: " + especialidad)
            datatuple.append(especialidad)
            update.message.reply_text("Presione /RFID para registar su tarjeta de identificacion. Luego apoyela sobre el sensor ")
        def registarTarjetaRfid(update: Update, context: CallbackContext) -> int:
            global numero_tarjeta_rfid 
            try:
                id, text = reader.read()
                print("Numero de identificacion:", id) 
                numero_tarjeta_rfid = id
            finally:
                GPIO.cleanup()

                CisarAPP.subirBasedeDatos()

                print("Datos cargados satisfactoriamente")



def ingreso_exitoso(update: Update, context: CallbackContext, nombreuser) -> None:
   htext = '''Bienvenido/a ''' + nombreuser + ''' puede ingresar a la cabina\n'''
   Htext = f"Fecha y Hora de ingreso: {fecha_hora}"
   update.message.reply_text(htext + Htext)

def ingreso_no_exitoso(update: Update, context: CallbackContext) -> None:
   htext = ''' Usted no se encuentra registrado, \n /Registro para registarse'''
   update.message.reply_text(htext)

def chequearUsuarios(update, context, numero_tarjeta_rfid):
    #CONEXION Y CHEQUEO BASE DE DATOS
    sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/CISAR_DB.db')
    sqlite_select_query = """SELECT numero_tarjeta_rfid, nombre, curso, division, especialidad from Usuarios"""
    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    check = 0
    
    for row in records:
        print(row)
        sleep(.5)
            
        if row[0] == numero_tarjeta_rfid:
            nombreuser = row[1]
            cursouser =  row[2]
            divisionuser = row[3]
            especialidaduser = row[4]
            check =+ 1
            break

    if check > 0:    
        print("Se encuentra en la base de datos:", row)
            
        r = requests.get("https://api.telegram.org/bot1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY/sendMessage?chat_id=-1001507958281&text=El%20sujeto%20"+ nombreuser + "%20presenta%20%20sintomas%0A%0ACurso: " + cursouser + "%0A%0ADivision: " +  divisionuser + "%0A%0AEspecialidad: " + especialidaduser + "%0A%0A/voy"  )
        with open("index.html", "wb") as f:   
            f.write(r.content)
            r.close()
            
        ingreso_exitoso(update, context, nombreuser)
        
    elif check == 0:
        print("NO se encuentra en la base de datos")
        ingreso_no_exitoso(update, context)

def corroborar_number_RFID (update: Update, context: CallbackContext):
    
    reader = SimpleMFRC522()
    
    htext = "Apoye la tarjeta sobre el sensor"
    update.message.reply_text(htext)
    try:
            global numero_tarjeta_rfid
            id, text = reader.read()
            numero_tarjeta_rfid = id
    finally:
            GPIO.cleanup()
            chequearUsuarios(update, context, numero_tarjeta_rfid)

def main() -> None:
    TOKEN = config('TOKEN')
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("Ayuda", help_command))
    dispatcher.add_handler(CommandHandler("Voy", voy_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(CommandHandler("Registro", registrar))
    dispatcher.add_handler(CommandHandler("division", registro_dos))
    dispatcher.add_handler(CommandHandler('continuar', registro_uno))
    dispatcher.add_handler(CommandHandler('especialidad', registro_tres))
    dispatcher.add_handler(CommandHandler('RFID', registro_cuatro))
    dispatcher.add_handler(CommandHandler("check", corroborar_number_RFID))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
   main()


CisarAPP.