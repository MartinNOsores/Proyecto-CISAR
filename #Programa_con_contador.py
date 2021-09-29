from _typeshed import Self
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

fechahoy = date.today()
fecha_hora = time.ctime()
edad = check = 0
nombre_apellido = fechanac = curso = division = especialidad = dni = numero_tarjeta_rfid = ""

#---------------------------IMPORTANTE---------------------------------
contador = 0
#---------------------------IMPORTANTE---------------------------------

datatuple = []
replies = {
    "curso" : ["1ero", "2do", "3ero", "4to", "5to", "6to", "7mo"],
    "division" : ["1era", "2da", "3era", "4ta", "5ta"],
    "especialidad" : ["Avionica", "Aeronautica"]
}

#-----FALTARIA LA FUNCION QUE PERMITE CREAR LA BASE DE DATOS, SUBIR LOS DATOS y LEER EL RFID 

reader = SimpleMFRC522()

GPIO.setwarnings(False)

#c.execute("""CREATE TABLE usuarios (
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

def start(update: Update, context: CallbackContext) -> None:
   user = update.effective_user
   update.message.reply_markdown_v2(
       fr'''Buenas {user.mention_markdown_v2()}\! el bot de Cisar te saluda, en que puedo ayudarte? para desplegar mi lista de comandos haz clic en /ayuda''',
       reply_markup=ForceReply(selective=True)
   )

def voy_command(update: Update, context: CallbackContext) -> None:
   htext = '''
Usted se está comprometiendo con proceder con el posible sospechoso, tenga cuidado.'''
   update.message.reply_text(htext)

def help_command(update: Update, context: CallbackContext) -> None:
   htext = "Mi lista de comandos: \n\n\t/Registro (Le permite registarse como alumno)\n\n\t/Ingresar (busca iniciar el protocolo de ingreso)\n\n\t/voy"
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


def registrar(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! yo soy el CisarBot encargado del registro'+ ' \n\nle solicito me mande su nombre y apellido completo por escrito'
        + '\n\nAsegurese de colocar su nombre y apellido correctamente, por favor ',
        reply_markup=ForceReply(selective=True),
    )
    
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global contador
    global division
    contador = contador + 1 #el contador está global por lo que despues de todo el proceso lo voy a tener que resetear

    #for reply in replies:

        if contador == 1:
            global nombre_apellido
            nombre_apellido=(update.message.text)
            print("nombre y apellido: " + nombre_apellido)
            update.message.reply_text("Tu nombre y apellido completo es: " + nombre_apellido + "\n\n es correcto?")
            registro_uno()
            break
        
        if contador == 2:
            global curso
            curso=(update.message.text)
            print("Año: "+ curso)
            update.message.reply_text("Su curso es: " + curso + "\n\n es correcto?")
            registro_dos()
            break
        
        elif contador == 2:
            division=(update.message.text)
            if division in replies[2]:
                print("Division: "+ division)
                update.message.reply_text("Su división es: " + division + "\n\n es correcto?")
                registro_tres()
                break
            
            elif division in replies[1]:
                print("Division: "+ division)
                 update.message.reply_text("Su división es: " + division + "\n\n es correcto?")
                registro_cuatro()
            break
        
        elif contador == 3:
            global especialidad
            especialidad=(update.message.text)
            print("Especialidad: "+ especialidad)
            update.message.reply_text("Su especialidad es: " + especialidad + "\n\n es correcto?")
            registro_cuatro()
            break

        elif contador == 4:
            global dni
            dni = (update.message.text)
            update.message.reply_text("Su DNI es: \n\n" + dni)
            print("DNI " + dni)
            datatuple.append(dni)
            update.message.reply_text("Su numero de DNI es: " + dni + "\n\n es correcto?")
            registro_cinco()
            break


def registro_uno(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [replies[0]]

    update.message.reply_text(
        'Indique su curso',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )

def registro_dos(update: Update, context: CallbackContext) -> int:
    if curso =='1ero' or curso =='2do' or curso =='3ero' :
      reply_keyboard = [replies[1]]
    elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':
      reply_keyboard = [replies[2]]
    
    #user = update.message.from_user
    #logger.info("Año of %s: %s", user.first_name, update.message.text)
    
    update.message.reply_text(
        'Seleccione su division',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Escribi bien'
        ),
    )

def registro_tres(update: Update, context: CallbackContext) -> int:
    """busca obtener a que especialidad pertenece."""
    if curso =='1ero' or curso =='2do' or curso =='3ero' : #esto tiene que estar en otro lugar, porque sino nunca entra
        especialidad = "-"
        break
        
    elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':     
        reply_keyboard = [replies[3]]
    
    update.message.reply_text(
        #'Send /cancel to stop talking to me.\n\n'
        'Seleccione su especialidad',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )

def registro_cuatro(update: Update, context: CallbackContext) -> int:
    contador = 3 #coloco al contador en 3 para que luego cuando entre en echo se saltee la especialidad en caso de ser necesario
    user = update.effective_user
    update.message.reply_text("Ingrese su numero de DNI")
    

def registro_cinco(update: Update, context: CallbackContext) -> int:
    """busca registrar la tarjeta/llavero RFID."""
    contador = 0 #reseteo el contador para que la proxima persona que quiera registrase lo haga correctamente
    
    try:
        id, text = reader.read()
        print("Numero de identificacion:", id)
        numero_tarjeta_rfid = id
        #print(text)
    finally:
        GPIO.cleanup()
        update.message.reply_text("Datos cargados satisfactoriamente! ")
                    
        conn = sqlite3.connect("/home/pi/Desktop/CISAR_DB.db")
        
        c = conn.cursor()
        
        c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?)", (nombre_apellido, curso, division, especialidad, numero_tarjeta_rfid))
        
        conn.commit()

        conn.close()

        contador == 0



def main() -> None:
    """Runing bot."""
    #TOKEN = config('TOKEN')
    #updater = Updater(TOKEN)
    updater = Updater("1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("Ayuda", help_command))
    dispatcher.add_handler(CommandHandler("Voy", voy_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    #dispatcher.add_handler(CommandHandler("Registro", registrar))
    #dispatcher.add_handler(CommandHandler("division", registro_dos))
    #dispatcher.add_handler(CommandHandler('continuar', registro_uno))
    #dispatcher.add_handler(CommandHandler('especialidad', registro_tres))
    #dispatcher.add_handler(CommandHandler('RFID', registro_cinco))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
   main()