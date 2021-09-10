import logging
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
from time import sleep
from sqlite3 import Error
from datetime import date
import RPi.GPIO as GPIO

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

edad = 0
nombre_apellido = ""
fechanac = ""
curso = ""
division = ""
division_superior = ""
especialidad = ""
numero_tarjeta_rfid = ""

reader = SimpleMFRC522()

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



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

GENDER, DIVISION, PHOTO, LOCATION, BIO, USERNAME = range(6)


replies = [
    ['1ero', '2do', '3ero','4to', '5to', '6to','7mo'],
    ['1era', '2da', '3era','4ta', '5ta'],
    ['1°', '2°'], #lista para el caso en que el curso sea > 3ero
    ['Avionica', 'Aeronautica']
]

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! yo soy el CisarBot encargado del registro'+ ' \n\nle solicito me mande su nombre y apellido completo por escrito'
        + '\n\nAsegurese de colocar su nombre y apellido correctamente, por favor ',
        reply_markup=ForceReply(selective=True),
    )
    
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    
    text = update.message.text
    
    for reply in replies:
        if text in replies[0]:
            global curso
            update.message.reply_text("/division para continuar")
            curso=(update.message.text)
            print("Año: "+ curso)
            return 
        
        elif text in replies[1]:
            global division
            division=(update.message.text)
            print("Division: "+ division)
            update.message.reply_text("Seleccione /RFID para registar su identificacion")
            return
        
        elif text in replies[2]:
            global division_superior
            division_superior=(update.message.text)
            print("Division: "+ division_superior)
            update.message.reply_text("ahora digame su /especialidad")
            return
        
        elif text in replies[3]:
            global especialidad
            especialidad=(update.message.text)
            print("Especialidad: "+ especialidad)
            update.message.reply_text("Seleccione /RFID para registar su identificacion")
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
        especialidad = "-"
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
        print(id)
        #print(text)
    finally:
        GPIO.cleanup()
        update.message.reply_text("Datos cargados satisfactoriamente! ")
        
        c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", (nombre_apellido, curso, division, especialidad, numero_tarjeta_rfid))
    
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1900533604:AAHWB8F_p37NkvNgrpvTyA_6iMVonp1UpU0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("division", registro_dos))
    dispatcher.add_handler(CommandHandler('continuar', registro_uno))
    dispatcher.add_handler(CommandHandler('especialidad', registro_tres))
    dispatcher.add_handler(CommandHandler('RFID', registro_cuatro))
        #     cargarDatos()
 
    updater.start_polling()
    updater.idle()
    
    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()

