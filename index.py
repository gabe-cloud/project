from tkinter import *
from tkinter import ttk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile


import sqlite3

class Registration:

    db_name = 'database.db'
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('UNEG Project')
    
        #Creo contenedor
        frame = LabelFrame(self.wind, text= 'Registrar nuevo archivo de actas')
        frame.grid(row=0, column= 0, columnspan= 3, pady= 20)
        SecondFrame = LabelFrame(self.wind, text= 'Filtro de busqueda')
        SecondFrame.grid(row=1, column= 1, pady= 10, padx= 10)

        #File ID Input
        Label(frame, text='ID: ').grid(row=1, column= 0)
        self.id = Entry(frame)
        self.id.focus()
        self.id.grid(row=1,column=1)

        #Title Input
        Label(frame, text='Titulo: ').grid(row=2, column= 0)
        self.title = Entry(frame)
        self.title.grid(row=2,column=1, pady=10)
        
        #Descripcion Input
        Label(frame, text='Descripción: ').grid(row=3, column= 0)
        self.description = Entry(frame)
        self.description.grid(row=3,column=1, pady=10)

        ttk.Button(frame, text="Buscar Archivo", command=self.open_file).grid(row=4, columnspan=2, sticky= W + E)

        #Button Add new file
        ttk.Button(frame, text="Save", command= self.add_file).grid(row=5, columnspan=2, sticky= W + E)
        
        #Descripcion Filter
        Label(SecondFrame, text='Número ID: ').grid(row=1, column= 0)
        self.description = Entry(SecondFrame)
        self.description.grid(row=1,column=1, pady=10)

        #Button Search new file
        ttk.Button(SecondFrame, text="Buscar", command= self.add_file).grid(row=2, columnspan=2, sticky= W + E)

        #Output Messages
        self.message = Label(text='', fg ='red')
        self.message.grid(row=5, column=0, columnspan= 3, sticky= W + E)

        #Table
        self.tree = ttk.Treeview(height = 20, column = ("c1", "c2"))
        self.tree.grid(row=6, columnspan=3)
        self.tree.heading("# 0", text="ID", anchor=CENTER)
        self.tree.heading("# 1", text="Title", anchor=CENTER)
        self.tree.heading("# 2", text="Description", anchor=CENTER)

        #Buttons
        ttk.Button(text= 'BORRAR', command = self.delete_file).grid(row=7,column=0, sticky = W + E)
        ttk.Button(text= 'EDITAR', command = self.edit_file).grid(row=7,column=2, sticky = W + E)
        
        #Filling the Row

        self.get_files()


    #Database connection
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #Select db
    def get_files(self):
        
        records = self.tree.get_children()
        #Limpia el tree
        for element in records:
            self.tree.delete(element)
        #Consulta de datos
        query = 'SELECT * FROM file'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0 , text=row[0], values=(row[1],row[2]))

    def validation(self):
        return len(self.id.get()) != 0 and len(self.title.get()) != 0 and len(self.description.get()) != 0

    def add_file(self):
        if self.validation():
            query = 'INSERT INTO file VALUES(?,?,?,?)'
            parameters =(self.id.get(), self.title.get(), self.description.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Archivo {} añadido exitosamente'.format(self.title.get())
            self.id.delete(0,END)
            self.title.delete(0,END)
            self.description.delete(0,END)
        else:
            self.message['text'] = 'Rellene las casillas'.format(self.title.get())
        self.get_files()

    def delete_file(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un dato'
            return
        self.message['text']=''
        id =self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM file WHERE id = ?'
        self.run_query(query, (id, ))
        self.message['text'] = 'Archivo {} a sido eliminado exitosamente'.format(id)
        self.get_files()
    
    def edit_file(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un dato'
            return
        id = self.tree.item(self.tree.selection())['text']
        old_title = self.tree.item(self.tree.selection())['values'][0]
        old_description = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editando File'

        #Old id
        Label(self.edit_wind, text = 'ID antigua: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value = id), state = 'readonly').grid(row=0, column=2)      
        #New id
        Label(self.edit_wind, text = 'ID nuevo: ').grid(row=1, column=1)
        new_id = Entry(self.edit_wind)
        new_id.grid(row=1, column=2)

        #Old title
        Label(self.edit_wind, text = 'Titulo antiguo').grid(row=2, column= 1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value= old_title), state= 'readonly').grid(row=2, column=2)
        #New title
        Label(self.edit_wind, text = 'Titulo nuevo').grid(row=3,column=1)
        new_title = Entry(self.edit_wind)
        new_title.grid(row=3, column=2)

        #Old description
        Label(self.edit_wind, text = 'Descripción antigua').grid(row=4, column= 1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value= old_description), state= 'readonly').grid(row=4, column=2)
         #New description
        Label(self.edit_wind, text = 'Descripción nueva').grid(row=5,column=1)
        new_description = Entry(self.edit_wind)
        new_description.grid(row=5, column=2)

        Button(self.edit_wind, text='Actualizar', command = lambda: self.edit_records(new_id.get(), id, new_title.get(), new_description.get())).grid(row=6, column=2, sticky= W)

    def edit_records(self, new_id, id, new_title, new_description):
        query= 'UPDATE file SET id = ?, title = ?, description = ? WHERE id = ?'
        parameters = (new_id, new_title, new_description, id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Archivo {} actualizado exitosamente'.format(id)
        self.get_files()

    def open_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Python Files', '*.pdf')])
        if file:
            content = file.read()
            file.close()
            print("%d characters in this file" % len(content))

if __name__=='__main__':
    window = Tk()
    application = Registration(window)
    window.iconbitmap('C:\\Users\\gjrzr\\Desktop\\TRY\\uneg-logo-2D2635F1F5-seeklogo.com.ico')
    window.mainloop()

