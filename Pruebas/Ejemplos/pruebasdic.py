s = "44419783"
lenght = len(s) 

if s.isnumeric() == True and lenght < 9:
    print("valor correcto")
else:
    print("valor incorrecto")