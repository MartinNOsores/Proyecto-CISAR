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
nombre_apellido = fechanac = curso = division = especialidad = dni = numero_tarjeta_rfid = numero_tarjeta_rfid2 = rando = ""
GPIO.setwarnings(False)

#---------------------------IMPORTANTE---------------------------------
contador = -1000
#---------------------------IMPORTANTE---------------------------------

datatuple = []
replies = {
    "curso" : ["1ero", "2do", "3ero", "4to", "5to", "6to", "7mo"],
    "division" : ["1era", "2da", "3era", "4ta", "5ta"],
    "especialidad" : ["Avionica", "Aeronautica"],
    "procedimiento": ["SI", "Reingresar datos"]
}

logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO)
logger = logging.getLogger(__name__)

def ingreso_exitoso(update: Update, context: CallbackContext, nombreuser) -> None:
    htext = '''Bienvenido/a ''' + nombreuser + ''' puede ingresar a la cabina\n'''
    Htext = f"Fecha y Hora de ingreso: {fecha_hora}"
    update.message.reply_text(htext + Htext)

def ingreso_no_exitoso(update: Update, context: CallbackContext) -> None:
    htext = ''' Usted no se encuentra registrado, \n /Registro para registarse'''
    update.message.reply_text(htext)
    
def crearBasedeDatos():
    sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/BASE_DE_DATOS_CISAR.db')
    cursor = sqliteConnection.cursor()

    cursor.execute("""CREATE TABLE usuarios (    
                            nombre text,
                            curso integer,
                            division integer,
                            especialidad integer,
                            dni integer,
                            numero_tarjeta_rfid integer
                            )""");

def subirBasedeDatos(update, context):
    sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/BASE_DE_DATOS_CISAR.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", (nombre_apellido, curso, division, especialidad, dni, numero_tarjeta_rfid))
    emoji = "\N{flexed biceps}"
    update.message.reply_text(f"Datos cargados satisfactoriamente! {emoji} ")
    
    sqliteConnection.commit()
    sqliteConnection.close()

def leerRfid():
    try:
        global numero_tarjeta_rfid
        reader = SimpleMFRC522()
        id, text = reader.read()
        print("Numero de identificacion:", id)
    finally:
        GPIO.cleanup()
        numero_tarjeta_rfid = id
    return

def start(update: Update, context: CallbackContext) -> None:
   user = update.effective_user
   emoji = "\N{raised hand}"
   update.message.reply_markdown_v2(
       fr'''Buenas {user.mention_markdown_v2()}\! {emoji} El bot de Cisar te saluda, en que puedo ayudarte? Para desplegar mi lista de comandos haz clic en /ayuda''',
       reply_markup=ForceReply(selective=True)
   )

def voy_command(update: Update, context: CallbackContext) -> None:
   htext = '''Usted se está comprometiendo con proceder con el posible sospechoso, tenga cuidado.'''
   update.message.reply_text(htext)

def help_command(update: Update, context: CallbackContext) -> None:
    htext = "Mi lista de comandos: \n\n --> \t/Registro (Le permite registarse como alumno)\n\n --> \t/Ingresar (busca iniciar el protocolo de ingreso)\n\n --> \t/voy (usted se ocupa del sospechoso)"
    update.message.reply_text(htext)

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
    
def echo(update: Update, context: CallbackContext) -> None:
    'cada vez que mandemos un string al bot el contador = contador + 1'
    global division
    global contador
    global especialidad
    global dni
    contador = contador + 1 #el contador está global por lo que despues de todo el proceso lo voy a tener que resetear

    if contador == 1:
        global nombre_apellido
        nombre_apellido=(update.message.text)
        nombre_temp = nombre_apellido.replace(" ", "")
        if nombre_apellido.isalpha() == True :
            print("nombre y apellido: " + nombre_apellido)
            #datatuple.append(nombre_apellido)
            registro_uno(update, context)
        else:
            contador = 0
            emoji = "\N{cross mark}" 
            update.message.reply_text(f"Por favor ingrese un nombre valido {emoji}")
            update.message.reply_text(f"Ingrese su nombre nuevamente")
        
    elif contador == 2:
        global curso
        curso=(update.message.text)
        print("Año: "+ curso)
        #datatuple.append(curso)
        registro_dos(update, context)
    
    elif contador == 3:
        division=(update.message.text)
        if curso =='1ero' or curso =='2do' or curso =='3ero' :
            reply_keyboard = [replies["division"]]
            print("Division: "+ division)
            #datatuple.append(division)
            especialidad = "-"
            print("Especialidad: "+ especialidad)
            registro_cuatro(update, context)
            
        elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':
            reply_keyboard = [replies["division"][0:2]]
            print("Division: "+ division)
            #datatuple.append(division)
            registro_tres(update, context)
    
    elif contador == 4:
        especialidad=(update.message.text)
        print("Especialidad: "+ especialidad)
        registro_cuatro(update, context)
        
    #elif contador == 6:
        #datatuple.append(especialidad)
        #registro_cuatro(update, context)

    elif contador == 5:
        dni = (update.message.text)
        lenght = len(dni)
        if dni.isnumeric() == True and lenght <9:
            print("DNI: " + dni)
            #datatuple.append(dni)
            chequeoDeDatos(update, context)
        else:
            contador = 4
            emoji = "\N{cross mark}" 
            update.message.reply_text(f"Por favor ingrese un DNI valido {emoji}")
            registro_seis(update, context)
            
    elif contador == 6:
        procedimiento = (update.message.text)
        if procedimiento =='SI' :
            registro_cinco(update, context)  #luego de dos segundos buscamos que vaya directamente a la funcion de registro de RFID
            
        elif procedimiento == "Reingresar datos":
            contador == -1000 #seteamos el contador porque tiene que volver a empezar de cero el proceso
            registrar(update, context)  #luego de dos segundos buscamos que vuelva  a la funcion de registro de usuario

def registrar(update: Update, context: CallbackContext) -> None:
    """1er función de la etapa de registro"""
    global contador
    contador = 0  #seteamos el contador en 0 para asegurarnos que no tome el nombre del usuario en cualquier string que le mandemos
    user = update.effective_user
    emoji = "\N{grinning face with smiling eyes}"
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! {emoji} Yo soy el CisarBot encargado del registro\.'+ ' \n\nLe solicito me mande su nombre y apellido completo por escrito, por favor\. ',
        reply_markup=ForceReply(selective=True),
    )

def registro_uno(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [replies["curso"]] 

    update.message.reply_text(
        ' --> Indique su curso',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )

def registro_dos(update: Update, context: CallbackContext) -> int:
    if curso =='1ero' or curso =='2do' or curso =='3ero' :
      reply_keyboard = [replies["division"]]
    elif curso == '4to' or curso == '5to' or curso =='6to' or curso =='7mo':
      reply_keyboard = [replies["division"][0:2]]

    update.message.reply_text(
        ' --> Seleccione su division',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Escribi bien'
        ),
    )

def registro_tres(update: Update, context: CallbackContext) -> int:
    """busca obtener a que especialidad pertenece.""" 
    reply_keyboard = [replies["especialidad"]]
    
    update.message.reply_text(
        ' --> Seleccione su especialidad',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )

def registro_cuatro(update: Update, context: CallbackContext) -> int:
    global contador
    contador = 4 #coloco al contador en 4 para que luego cuando entre en echo se saltee la especialidad en caso de ser necesario
    user = update.effective_user
    update.message.reply_markdown_v2 (fr''' \-\-\> Ahora {user.mention_markdown_v2()}\! Le voy a solicitar que ingrese el numero de DNI''',
       reply_markup=ForceReply(selective=True)
    )
def registro_seis(update: Update, context: CallbackContext) -> int:
    global contador
    user = update.effective_user
    update.message.reply_markdown_v2 (fr''' \-\-\> {user.mention_markdown_v2()}\! Por favor ingrese el numero de DNI nuevamente''',
       reply_markup=ForceReply(selective=True)
    )
        

def chequeoDeDatos(update: Update, context: CallbackContext) -> int:
    global contador
    print (contador)
    #Para confirmar los datos ingresados:
    procedimiento = ""
    emoji = "\N{white small square}"
    reply_keyboard = [replies["procedimiento"]] 
    
    update.message.reply_text(
    f"Su datos ingresados son: \n\n {emoji} Nombre y apellido: " + nombre_apellido + f"\n\n {emoji} Año: " + curso +
    f"\n\n {emoji} Division: " + division + f"\n\n {emoji} Especialidad: " + especialidad + f"\n\n {emoji} DNI: " + dni + f"\n\nSon datos sus correctos? ",
    reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Elegi bien'
        ),
    )

def registro_cinco(update: Update, context: CallbackContext) -> int:
    """busca registrar la tarjeta/llavero RFID."""
    global contador
    
    contador = -1000 #reseteo el contador para que la proxima persona que quiera registrase lo haga
    update.message.reply_text("Apoye la tarjeta sobre el sensor: ")
    
    leerRfid()
    
    #rando = numero_tarjeta_rfid[0]
    #numero_tarjeta_rfid = rando(str)
    #datatuple.append(numero_tarjeta_rfid)
    subirBasedeDatos(update, context)
            
def chequearUsuarios(update, context): 
    update.message.reply_text("Apoye la tarjeta sobre el sensor")

    leerRfid()
    
    sqliteConnection = sqlite3.connect('/home/pi/Desktop/Principal/BASE_DE_DATOS_CISAR.db')
    sqlite_select_query = """SELECT numero_tarjeta_rfid, nombre, curso, division, especialidad, dni from Usuarios"""
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
            dniuser = row[5]
            check =+ 1
            break

    if check > 0:
        emoji = "\N{raised hand}"
        
        print("Se encuentra en la base de datos: ", row)
        
        r = requests.get("https://api.telegram.org/bot1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY/sendMessage?chat_id=-1001507958281&text=El%20sujeto%20&"
            + nombreuser + "%20presenta%20%20sintomas%0A%0ACurso: " + cursouser + "%0A%0ADivision: " +  divisionuser + "%0A%0AEspecialidad: " + especialidaduser + "%0A%0ADNI:" + dniuser + "%0A%0A/voy"  )
        with open("index.html", "wb") as f:   
            f.write(r.content)
            r.close()

        ingreso_exitoso(update, context, nombreuser)
        
    else:
        print("No se encuentra en la base de datos")
        ingreso_no_exitoso(update, context)


def main() -> None:
    TOKEN = config('TOKEN')
    updater = Updater(TOKEN)
    #updater = Updater("1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("Ayuda", help_command))
    dispatcher.add_handler(CommandHandler("Voy", voy_command))
    dispatcher.add_handler(CommandHandler("Registro", registrar))
    dispatcher.add_handler(CommandHandler("Ingresar", chequearUsuarios))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
#     crearBasedeDatos()
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
   main()
