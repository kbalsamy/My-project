from tkinter import *
import Pmw
from tkinter import ttk
from constants import *
import sqlite3
import Create_table_widget as Table
import file_creator


def get_table_name():

    options = []
    con = sqlite3.connect('ReadingsV1onAPP.db')
    cursor = con.cursor()
    args = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(args)
    table_list = cursor.fetchall()
    if len(table_list) == 0:
        # print('no values')
        return ('Not available',)
    else:
        t, _ = (table_list)
        return t


class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self)
        self.databasetable_name = StringVar(self)
        self.pack()
        self.opt = Pmw.OptionMenu(self, labelpos='w', label_text='Choose available database here',
                                  menubutton_textvariable=self.databasetable_name, items=get_table_name())
        self.opt.pack()
        Button(self, text='Display', command=self.show_db_table).pack()

    def show_db_table(self):
        results = file_creator.downloadvalues(self.databasetable_name.get())
        manager = Table.Table_creator(self)
        manager.exim_table('Service Number')
        manager.exim_table('Import Units', single_header=False)
        manager.exim_table('Export Units', single_header=False)
        manager.exim_table('Difference', single_header=False)
        manager.add_row(results)


root = Tk()
app = Application(root)
root.mainloop()
