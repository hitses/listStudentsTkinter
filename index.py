from tkinter import ttk
from tkinter import *

import sqlite3

class Student:
  db_name = 'database.db'


  def __init__(self, window):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups(
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name  TEXT
    )''')
    conn.commit()
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
    id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_class	INTEGER,
    name	TEXT,
    points	INTEGER,
    FOREIGN KEY(id_class) REFERENCES groups(id)
    )''')
    conn.commit()


    self.wind = window
    self.wind.title('Lista de estudiantes')

    # Creando marco
    classes = LabelFrame(self.wind, text='Cursos')
    classes.grid(row=0, column=0, pady=5)

    # Options menu
    listOfClasses = self.get_classes('groups')
    self.option = StringVar()
    self.option.set(listOfClasses[0])


    """ def callback(*args):
      selectedClass = option.get()
      return selectedClass """


    self.option.trace("w", self.callback)

    OptionMenu(classes, self.option, *listOfClasses, command=self.get_students).grid(row = 0, column = 0)

    # Creando marco
    frame = LabelFrame(self.wind, text='Añadir estudiante')
    frame.grid(row=0, column=1, columnspan=3, pady=20)

    # Name Input
    Label(frame, text='Nombre: ').grid(row=1, column=0)
    self.name = Entry(frame)
    self.name.grid(row=1, column=1)

    # Points input
    Label(frame, text='Puntos: ').grid(row=2, column=0)
    self.points = Entry(frame)
    self.points.grid(row=2, column=1)

    # Button add student
    ttk.Button(frame, text='Añadir estudiante', command=lambda: self.add_students(self.get_classes('ids', self.callback()))).grid(row=3, columnspan=2, sticky=W+E)

    # Output messages
    self.message = Label(text='', fg='red')
    self.message.grid(row=3, column=0, columnspan=4, sticky=W+E)

    # Table
    self.tree = ttk.Treeview(height=10, columns=2)
    self.tree.grid(row=4, column=0, columnspan=4)
    self.tree.heading('#0', text='Nombre', anchor=CENTER)
    self.tree.heading('#1', text='Puntos', anchor=CENTER)

    # Table's buttons
    ttk.Button(text='Eliminar', command=self.delete_student).grid(row=5, column=0, sticky=W+E)
    ttk.Button(text='Editar', command=self.edit_student).grid(row=5, column=1, sticky=W)
    ttk.Button(text='+1 Punto', command=self.plus_points).grid(row=5, column=2, sticky=W+E)
    ttk.Button(text='-1 Punto', command=self.minus_points).grid(row=5, column=3, sticky=W+E)


    self.get_students(self.get_classes('group', self.callback()))
  
  def callback(self, *args):
      selectedClass = self.option.get()
      return selectedClass


  def run_query(self, query, params = ()):
      conn = sqlite3.connect(self.db_name)
      cursor = conn.cursor()
      result = cursor.execute(query, params)
      conn.commit()
      
      return result
    

  def get_students(self, group = ('1º')):
    # Cleaning table
    records = self.tree.get_children()
    for element in records:
      self.tree.delete(element)

    query = f'''
    SELECT s.name, s.points, g.name
    FROM students s
    INNER JOIN groups g
    ON s.id_class = g.id
    WHERE g.name = "{group}"
    ORDER BY points ASC'''
    print(query)
    db_rows = self.run_query(query)

    for row in db_rows:
      self.tree.insert('', 0, text=row[0], values=row[1])


  def get_classes(self, selection, name = ''):
    if selection == 'ids':
      idGroup = None
      query = f'SELECT id FROM groups WHERE name = "{name}" LIMIT 1'
      ids = self.run_query(query)
      for row in ids:
        idGroup = row[0]

      return idGroup

    elif selection == 'group':
      query = f'SELECT name FROM groups WHERE name = "{name}" LIMIT 1'
      db_rows = self.run_query(query)
      group = None
      for row in db_rows:
        group = row[0]

      return group

    elif selection == 'groups':
      query = 'SELECT name FROM groups'
      db_rows = self.run_query(query)

      groups = []
      for row in db_rows:
        groups.append(row[0])

      return groups


  def validation(self):
    return len(self.name.get()) != 0 and len(self.points.get()) != 0


  def add_students(self, group):
    self.message['text'] = ''
    self.message['fg'] = 'green'
    group
    if self.validation():
      query = 'INSERT INTO students VALUES(NULL, ?, ?, ?)'
      params = (group, self.name.get(), self.points.get())
      self.run_query(query, params)
      self.message['text'] = f'Estudiante {self.name.get()} añadido correctamente.'
      self.name.delete(0, END)
      self.points.delete(0, END)
    else:
      self.message['fg'] = 'blue'
      self.message['text'] = 'Se deben introducir el nombre y los puntos.'
    
    self.get_students(self.get_classes('group', self.callback()))
  
  def delete_student(self):
    self.message['text'] = ''
    self.message['fg'] = 'blue'
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError:
      self.message['text'] = 'Debes seleccionar un estudiante para eliminarlo.'
      return
    self.message['text'] = ''
    self.message['fg'] = 'red'
    name = self.tree.item(self.tree.selection())['text']
    query = 'DELETE FROM students WHERE name = ?'
    self.run_query(query, (name, ))
    self.message['text'] = f'Estudiante {name} se ha eliminado correctamente.'
    self.get_students(self.get_classes('group', self.callback()))

  def edit_student(self):
    self.message['text'] = ''
    self.message['fg'] = 'blue'
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError:
      self.message['text'] = 'Debes seleccionar un estudiante para editarlo.'
      return
    old_name = self.tree.item(self.tree.selection())['text']
    old_points = self.tree.item(self.tree.selection())['values'][0]
    self.edit_wind = Toplevel()
    self.edit_wind.title = 'Editar estudiante'

    # Old name
    Label(self.edit_wind, text='Nombre actual: ').grid(row=0, column=1)
    Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_name), state = 'readonly').grid(row=0, column=2)

    #New name
    Label(self.edit_wind, text='Nombre nuevo: ').grid(row=1, column=1)
    new_name = Entry(self.edit_wind)
    new_name.grid(row=1, column=2)

    # Old points
    Label(self.edit_wind, text='Puntuación actual: ').grid(row=2, column=1)
    Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_points), state = 'readonly').grid(row=2, column=2)

    #New points
    Label(self.edit_wind, text='Puntuación nueva: ').grid(row=3, column=1)
    new_points = Entry(self.edit_wind)
    new_points.grid(row=3, column=2)

    Button(self.edit_wind, text='Actualizar', command=lambda: self.edit_records(new_name.get(), new_points.get(), old_name, old_points)).grid(row=4, column=0, columnspan=3, sticky=W+E)
  
  def edit_records(self, new_name, new_points, old_name, old_points):
    if len(new_name) <= 0 and len(new_points) <= 0:
      self.message['text'] = ''
      self.message['fg'] = 'green'
      self.message['text'] = 'No se han añadido datos nuevos.'
      self.edit_wind.destroy()
    else:
      self.message['text'] = ''
      self.message['fg'] = 'green'
      query = 'UPDATE students SET name = ?, points = ? WHERE name = ? AND points = ?'
      params = (new_name, new_points, old_name, old_points)
      self.run_query(query, params)
      self.edit_wind.destroy()
      self.message['text'] = f'Estudiante {new_name} se ha actualizado correctamente.'
      self.get_students(self.get_classes('group', self.callback()))
  
  def plus_points(self):
    self.message['text'] = ''
    self.message['fg'] = 'blue'
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError:
      self.message['text'] = 'Debes seleccionar un estudiante para aumentar sus puntos.'
      return
    name = self.tree.item(self.tree.selection())['text']
    points = self.tree.item(self.tree.selection())['values'][0]
    self.message['text'] = ''
    self.message['fg'] = 'green'
    query = 'UPDATE students SET points = ? WHERE name = ? AND points = ?'
    params = (points + 1, name, points)
    self.run_query(query, params)
    self.message['text'] = f'{name} ha ganado un punto.'
    self.get_students(self.get_classes('group', self.callback()))

  def minus_points(self):
    self.message['text'] = ''
    self.message['fg'] = 'blue'
    try:
      self.tree.item(self.tree.selection())['text'][0]
    except IndexError:
      self.message['text'] = 'Debes seleccionar un estudiante para aumentar sus puntos.'
      return
    name = self.tree.item(self.tree.selection())['text']
    points = self.tree.item(self.tree.selection())['values'][0]
    self.message['text'] = ''
    self.message['fg'] = 'green'
    query = 'UPDATE students SET points = ? WHERE name = ? AND points = ?'
    params = (points - 1, name, points)
    self.run_query(query, params)
    self.message['text'] = f'{name} ha perdido un punto.'
    self.get_students(self.get_classes('group', self.callback()))


if __name__ == '__main__':
  window = Tk()
  Student(window)
  aplication = Student(window)
  window.mainloop()