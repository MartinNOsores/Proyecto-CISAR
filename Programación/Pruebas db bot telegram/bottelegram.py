
import logging
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext
from decouple import config



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






situacione = "Temperatura elevada"
alumnoe = "Montoni Juan Manuel"
cursoe= "7to 2da"
comisione= "B"
procedimientoe= "Debe retirarse por protocolo"


def alarm(update: Update, context: CallbackContext) -> None:
     update.message.reply_text("\nSituacion: " + situacione + "\n\nAlumno: " + alumnoe + "\n\nCurso: " + cursoe + "\tComision: " + comisione + "\n\nProcedimiento: " + procedimientoe + "\n\n/voy")
   #Send the Covid suspicius




def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
   """Remove job with given name. Returns whether job was removed."""
   current_jobs = context.job_queue.get_jobs_by_name(name)
   if not current_jobs:
       return False
   for job in current_jobs:
       job.schedule_removal()
   return True




def set_timer(update: Update, context: CallbackContext) -> None:
   """Add a job to the queue."""
   chat_id = update.message.chat_id
   try:
       # args[0] should contain the time for the timer in seconds
       due = int(context.args[0])
       if due < 0:
           update.message.reply_text('No puedo viajar al pasado, jaja!')
           return


       job_removed = remove_job_if_exists(str(chat_id), context)
       context.job_queue.run_once(alarm,
                                  due,
                                  context=chat_id,
                                  name=str(chat_id))


       text = 'Temporizador agregado!'
       if job_removed:
           text += ' El temporizador ha sido eliminado exitosamente.'
       update.message.reply_text(text)


   except (IndexError, ValueError):
       update.message.reply_text('Debes usar /set <segundos>')




def unset(update: Update, context: CallbackContext) -> None:
   """Remove the job if the user changed their mind."""
   chat_id = update.message.chat_id
   job_removed = remove_job_if_exists(str(chat_id), context)
   text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
   update.message.reply_text(text)


#old commands
def voy_command(update: Update, context: CallbackContext) -> None:
   htext = '''
Usted se está comprometiendo con proceder con el posible sospechoso, tenga cuidado.


'''
   update.message.reply_text(htext)


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




def log(update: Update, context: CallbackContext) -> None:
   db[str(latest_key() + 1)] = update.message.text




def fetch(update: Update, context: CallbackContext) -> None:
   update.message.reply_text(db.get(str(latest_key()), 'No Messages Yet.'))


situacion = "Temperatura normal"
alumno = "Bourlot David"
curso= "7to 2da"
comision= "B"
procedimiento= "Puede ingresar al establecimiento"


def noinfectatres_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("\nSituacion: " + situacion + "\n\nAlumno: " + alumno + "\n\nCurso: " + curso + "\tComision: " + comision + "\n\nProcedimiento: " + procedimiento)


usuario_nuevo = ''


def cargar_usuario(update: Update, context: CallbackContext):
   print ("ingrese su nombre y apellido")
   input(usuario_nuevo)


   print ("su nombre y apellido es: ", usuario_nuevo)




def help_command(update: Update, context: CallbackContext) -> None:
   htext = '''
Mi lista de comandos:


/start (Lista de comandos)


/situation (muestra la situacion de un caso positivo)


/situation2 (muestra la situacion de un caso negativo)


/voy (le da un aviso a la persona que va)


/set <tiempo> para ingresar el temporizador


/cargar (le permite cargar un nuevo usuario)
'''
   update.message.reply_text(htext)


def siu_command(update: Update, context: CallbackContext) -> None:
   htext = ''' https://www.youtube.com/watch?v=3zuGXcy1d7I
'''
   update.message.reply_text(htext)




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
   dispatcher.add_handler(CommandHandler("set", set_timer))
   dispatcher.add_handler(CommandHandler("unset", unset))
   dispatcher.add_handler(CommandHandler("cargar", cargar_usuario))
  
   #old commands:
   dispatcher.add_handler(CommandHandler("melamastico", mastic_command))
   dispatcher.add_handler(CommandHandler("Ayuda", help_command))
   dispatcher.add_handler(CommandHandler("fetch", fetch))
   dispatcher.add_handler(CommandHandler("situation", alarm))
   dispatcher.add_handler(CommandHandler("situation2", noinfectatres_command))
   dispatcher.add_handler(CommandHandler("Voy", voy_command))
   dispatcher.add_handler(CommandHandler("elbicho", bicho_command))


   # Start the Bot
   updater.start_polling()


   # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
   # SIGABRT. This should be used most of the time, since start_polling() is
   # non-blocking and will stop the bot gracefully.
   updater.idle()




if __name__ == '__main__':
   main()