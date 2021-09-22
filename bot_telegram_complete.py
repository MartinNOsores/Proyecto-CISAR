import logging
import os
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext
from decouple import config
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import sqlite3
from sqlite3 import Error
from datetime import date
import requests
import time

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

##############################
numero_tarjeta_rfid = int()

##############################

###Datos a pasar/obtener de la DataBase###
edad = 0
check = 0
nombre_apellido = ""
fechanac= ""
curso = ""
division = ""
division_superior = ""
especialidad = ""
numero_tarjeta_rfid = ""
nombreuser = ""
###Datos a pasar/obtener de la DataBase###

reader = SimpleMFRC522()

GPIO.setwarnings(False)

#Para crear la base de datos:
#cursor.execute("""CREATE TABLE usuarios (    
                        #nombre text,
                        #curso integer,
                        #division integer,
                        #especialidad integer,
                        #numero_tarjeta_rfid integer
                        
                        #)""");

# Enable logging
logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO)


logger = logging.getLogger(__name__)

situacion = "Temperatura elevada"

####CAMBIAR POR LAS VARIABLES DEL OTRO PROGRAMA####
alumnoe = "Montoni Juan Manuel"
cursoe= "7to 2da"
comisione= "B"
procedimientoe= "Debe retirarse por protocolo"
####CAMBIAR POR LAS VARIABLES DEL OTRO PROGRAMA####


"""
Las siguientes lineas son las que establecen la conexión
con la base de datos.
"""



#Conexión con base de datos establecida

def start(update: Update, context: CallbackContext) -> None:
   user = update.effective_user
   update.message.reply_markdown_v2(
       fr'''Buenas {user.mention_markdown_v2()}\! el bot de Cisar te saluda, en que puedo ayudarte? para desplegar mi lista de comandos haz clic en /ayuda''',
       reply_markup=ForceReply(selective=True)
   )


def alarm(update: Update, context: CallbackContext) -> None:
     update.message.reply_text("\nSituacion: " + situacion + "\n\nAlumno: " + alumnoe + "\n\nCurso: " + cursoe +
                                "\tComision: " + comisione + "\n\nProcedimiento: " + procedimientoe + "\n\n/voy")
   #Send the Covid suspicius


def voy_command(update: Update, context: CallbackContext) -> None:
   user = update.effective_user
   update.message.reply_markdown_v2(
       fr'''Usted {user.mention_markdown_v2()}\! se está comprometiendo con proceder con el posible sospechoso, tenga cuidado''',
       reply_markup=ForceReply(selective=True)
   )
   
def mastic_command(update: Update, context: CallbackContext) -> None:
   htext = '''
Bien por vos
'''
   update.message.reply_text(htext)


def bicho_command(update: Update, context: CallbackContext) -> None:
   htext = '''
https://www.youtube.com/watch?v=3muyI-uGhHY
'''
   update.message.reply_text(htext)


def help_command(update: Update, context: CallbackContext) -> None:
   htext = '''
Mi lista de comandos:


/Registro (Le permite registarse como alumno)


/situation (muestra la situacion de un caso positivo)


/check (comprobar)


/siu (siu)


/elbicho (ay mi madre)


'''
   update.message.reply_text(htext)


def siu_command(update: Update, context: CallbackContext) -> None:
   htext = ''' https://www.youtube.com/watch?v=3zuGXcy1d7I
'''
   update.message.reply_text(htext)

###Programa *registro&DB* ###
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


GENDER, DIVISION, PHOTO, LOCATION, BIO, USERNAME = range(6)


replies = [
    ['1ero', '2do', '3ero','4to', '5to', '6to','7mo'],
    ['1era', '2da', '3era','4ta', '5ta'],
    ['1°', '2°'], #lista para el caso en que el curso sea > 3ero
    ['Avionica', 'Aeronautica']
]

def registrar(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! le solicito que me mande su nombre y apellido completo por escrito'
        + '\n\nAsegurese de colocar su nombre y apellido correctamente, por favor ',
        reply_markup=ForceReply(selective=True),
    )
    
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    
    text = update.message.text
    
    for reply in replies:
        global division
        if text in replies[0]:
            global curso
            update.message.reply_text("/division para continuar")
            curso=(update.message.text)
            print("Año: "+ curso)
            return 
        
        elif text in replies[2]:
            division=(update.message.text)
            print("Division: "+ division)
            update.message.reply_text("ahora digame su /especialidad")
            return
        
        elif text in replies[1]:
            division=(update.message.text)
            print("Division: "+ division)
            update.message.reply_text("Seleccione /RFID para registar su identificacion. Luego apoye su tarjeta en el detector")
            return
        
        elif text in replies[3]:
            global especialidad
            especialidad=(update.message.text)
            print("Especialidad: "+ especialidad)
            update.message.reply_text("Seleccione /RFID para registar su identificacion. Luego apoye su tarjeta en el detector ")
            return
    
    global nombre_apellido
    update.message.reply_text("Tu nombre y apellido completo es: \n\n" + update.message.text + "\n\npor favor haga clic en /continuar")
    nombre_apellido=(update.message.text)
    print("nombre y apellido: " + nombre_apellido)
    

def registro_uno(update: Update, context: CallbackContext) -> int:
    """busca obtener a que curso pertenece."""
    reply_keyboard = [replies[0]]

    #user = update.message.from_user
    #logger.info("Nombre y apellido: %s", update.message.text)

    update.message.reply_text(
        #'Send /cancel to stop talking to me.\n\n'
        'Indique su curso',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )
    return GENDER

def registro_dos(update: Update, context: CallbackContext) -> int:
    """busca obtener a que division pertenece."""
    if curso =='1ero' or curso =='2do' or curso =='3ero' :
      reply_keyboard = [replies[1]]
    elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':
      reply_keyboard = [replies[2]]
    
    #user = update.message.from_user
    #logger.info("Año of %s: %s", user.first_name, update.message.text)
    
    update.message.reply_text(
        #'Send /cancel to stop talking to me.\n\n'
        'Seleccione su division',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Escribi bien'
        ),
    )
    return DIVISION

def registro_tres(update: Update, context: CallbackContext) -> int:
    """busca obtener a que especialidad pertenece."""
    if curso =='1ero' or curso =='2do' or curso =='3ero' :
        especialidad = " - "
        return
        
    elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':     
        reply_keyboard = [replies[3]]
    
    update.message.reply_text(
        #'Send /cancel to stop talking to me.\n\n'
        'Seleccione su especialidad',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )
    
    return

def registro_cuatro(update: Update, context: CallbackContext) -> int:
    """busca registrar la tarjeta/llavero RFID."""
    
    try:
        

        id, text = reader.read()
        print("Numero de identificacion:", id)
        numero_tarjeta_rfid = id
        #print(text)
    finally:
        GPIO.cleanup()
        
        sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/CISAR_DB.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO usuarios VALUES (?,?,?,?,?)", (nombre_apellido, curso, division, especialidad, numero_tarjeta_rfid))
        update.message.reply_text("Datos cargados satisfactoriamente! ")
        sqliteConnection.commit()
        sqliteConnection.close()
        
###FIN del Programa *registro&DB* ### 

def ingreso_exitoso(update: Update, context: CallbackContext, nombreuser) -> None:
   htext = ''' Bienvenido/a ''' + nombreuser + ''' puede ingresar a la cabina'''
   update.message.reply_text(htext)

def ingreso_no_exitoso(update: Update, context: CallbackContext) -> None:
   htext = ''' Usted no se encuentra registrado, \n /Registro para registarse'''
   update.message.reply_text(htext)

def chequearUsuarios(update, context, numero_tarjeta_rfid):
    
    sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/CISAR_DB.db')
    sqlite_select_query = """SELECT numero_tarjeta_rfid, nombre from Usuarios"""
    
    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    
    check = 0
    
    for row in records:
        print(row)
        sleep(.5)
            
        if row[0] == numero_tarjeta_rfid:
            nombreuser = row[1]
            check =+ 1
            break
    
    if check > 0:
        
        print("Se encuentra en la base de datos:", row)
            
        r = requests.get("https://api.telegram.org/bot1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY/sendMessage?chat_id=-1001507958281&text=El%20sospechoso%20est%C3%A1%20tratando%20de%20violar%20el%20sistema%0A%0A/situation")
        with open("index.html", "wb") as f:    #Ejecuta la url
            f.write(r.content)
            r.close()
            
        ingreso_exitoso(update, context, nombreuser)
        
    elif check == 0:
        print("NO se encuentra en la base de datos")
        ingreso_no_exitoso(update, context)
            
    #temperature por aca
    

def corroborar_number_RFID (update: Update, context: CallbackContext):
    
    reader = SimpleMFRC522()

    try:
            global numero_tarjeta_rfid
            id, text = reader.read()
            numero_tarjeta_rfid = id
    finally:
            GPIO.cleanup()
            #update.message.reply_text("Seleccione /buscar ")
            chequearUsuarios(update, context, numero_tarjeta_rfid)
#------------------------------------------------------------------------------------------------
def main() -> None:
    """Runing bot."""
    TOKEN = config('TOKEN')
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    #updater = Updater("1611398547:AAEOgMyfYm-5U1j03oqvFtg-I7VpN7d9Eg")


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("siu", siu_command))
          
    #old commands:
    dispatcher.add_handler(CommandHandler("melamastico", mastic_command))
    dispatcher.add_handler(CommandHandler("Ayuda", help_command))
    dispatcher.add_handler(CommandHandler("situation", alarm))
    dispatcher.add_handler(CommandHandler("Voy", voy_command))
    dispatcher.add_handler(CommandHandler("elbicho", bicho_command))
            
    ###New commands from registro&DB
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(CommandHandler("Registro", registrar))
    dispatcher.add_handler(CommandHandler("division", registro_dos))
    dispatcher.add_handler(CommandHandler('continuar', registro_uno))
    dispatcher.add_handler(CommandHandler('especialidad', registro_tres))
    dispatcher.add_handler(CommandHandler('RFID', registro_cuatro))
    dispatcher.add_handler(CommandHandler("check", corroborar_number_RFID))

    # Start the Bot
    updater.start_polling()


    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
   main()
