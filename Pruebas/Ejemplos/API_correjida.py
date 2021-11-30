API

import requests
import time
n = 1

while n>0:

  r = requests.get("https://api.telegram.org/bot1611398547:AAG9YCiIxoW1SrGpsSHzDj1vSXMlqLf5kEY/sendMessage?chat_id=-1001507958281&text=El%20sospechoso%20est%C3%A1%20tratando%20de%20violar%20el%20sistema%0A%0A/situation")
  with open("index.html", "wb") as f:
    f.write(r.content)
    r.close()
  time.sleep(10)
