from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import tkinter.font as tkFont

class Menuprincipal:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.frame = tk.Frame(self.master)
        self.fontStyle = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
        self.titulo = tk.Label(self.frame, text="¡ BIENVENIDO A CISAR™ !")
        self.titulo.configure(font=self.fontStyle)
        self.frame.pack()
        self.titulo.pack(side = TOP, ipady = 10, padx= 200)

        """ AGREGAR IMAGEN """

        self.image = Image.open("/Users/pedrogonzalez/Desktop/PROYECTO CISAR/Tkinter GIU/icono_cisar.JPG")
        self.image = self.image.resize((100,100))

        self.python_image = ImageTk.PhotoImage(self.image)
        
        self.label_imagen = tk.Label(self.master, image=self.python_image)
        
        self.label_imagen.pack(side = BOTTOM, pady=165)


    '''def agregarImagen(self):
        """ AGREGAR IMAGEN """
        self.image = Image.open("/Users/pedrogonzalez/Desktop/PROYECTO CISAR/Tkinter GIU/icono_cisar.JPG")
        self.image = self.image.resize((100,100))

        self.python_image = ImageTk.PhotoImage(self.image)
        
        self.label_imagen = tk.Label(self.master, image=self.python_image)
        
        self.python_image.pack()
        self.label_imagen.pack()'''

    def newWindow(self):
        pass

class AddUser:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)


def main():
    rootPrincipal = tk.Tk()
    rootAddUser = tk.Tk()
    rootPrincipal.geometry("1000x500")
    rootPrincipal.config(bg="black")
    rootPrincipal.title("<-- CISAR -->")
    rootAddUser.title("<-- CONTROL DE USUARIOS -->")
    rootAddUser.geometry("1000x500")
    app = Menuprincipal(rootPrincipal)
    app1 = AddUser(rootAddUser)
    rootPrincipal.mainloop()
    rootAddUser.mainloop()
    #Menuprincipal.agregarImagen()

if __name__ == '__main__':
   main()