nombretemp = "hola buenas tardes"
nombre_apellido = ""

nombretemp = nombretemp.title()

for i in nombretemp:
    if i == " ":
        i = ""
        nombre_apellido += i

    else:
        nombre_apellido += i

if nombre_apellido.isalpha() == True:
    print("nombre_apellido: ", nombre_apellido)



