from tkinter import *
import tkinter as ttk
import tkinter as tk
from tkinter import font
from tkinter.constants import LEFT, TOP
from PIL import Image, ImageTk
import tkinter.font as tkFont

class App(tk.Tk): 

    def agregar_imagen(self):
        """AGREGAR IMAGEN"""
        self.image = Image.open("/Users/pedrogonzalez/Desktop/PROYECTO CISAR/Tkinter GIU/icono_cisar.JPG")
        self.image = self.image.resize((100,100))
 
        self.python_image = ImageTk.PhotoImage(self.image)
        
        self.label_imagen = ttk.Label(image=self.python_image)
        
        self.label_imagen.place(x = 450,y = 170)

    def agregar_titulo(self):

        self.titulo = ttk.Label(text=" BIENVENIDO A CISAR™")
        self.titulo.configure(font=self.fontStyle)
        self.titulo.place(x = 410,y = 100)
    
    def etiqueta_temperatura(self):

        #self.etiqueta = ttk.Label(text="La temperatura esta bien: ",background="#37DC30")
        #self.etiqueta.place(x = 500,y = 900)
        pass

    def agregar_boton(self):
        self.boton = ttk.Button(text="prueba de boton 01", background="white")
        self.boton.place(x = 500,y = 400)
        pass

    def __init__(self):  
        super().__init__()  
        """CONFIGURACION TK"""
        self.geometry("1000x500")
        self.config(bg="black")
        self.resizable(False, False)
        self.title("interfaz_cisar")
        self.fontStyle = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
        """WIDGETS"""
        self.agregar_imagen()
        self.agregar_titulo()
        #etiqueta_temperatura() 

app = App()
app.mainloop()

# if __name__ == "__main__": 

"""self.frame1 = tk.Frame()
        self.frame1.place(x=0, y= 0)
        self.frame1.config(bg="red")
        self.frame1.pack()
        self.frame2 = tk.Frame()
        self.frame2.place(x=150, y=150)
        self.frame2.config(bg="green")
        self.frame2.pack()"""