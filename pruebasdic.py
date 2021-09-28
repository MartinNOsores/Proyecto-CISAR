replies = {
    "curso" : ["1ero", "2do", "3ero", "4to", "5to", "6to", "7mo"],
    "division" : ["1era", "2da", "3era", "4ta", "5ta"],
    "especialidad" : ["Avionica", "Aeronautica"]
}
reply_keyboard = [replies["division"][:2]]
#print(reply_keyboard)

datatuple = []

datatuple.append("pedro gonzalez")
datatuple.append("7mo")
datatuple.append("2da")

for i in datatuple:

    nombre_apellido = datatuple[i] 
    curso = datatuple[i]
    division = datatuple[i]

    print(i)

nombre = curso = apellido = "primer valor"

for i in range(0,2):
    #print(nombre)
    #print(apellido)

    nombre = "segundo valor" 
    apellido = "2do valor"

