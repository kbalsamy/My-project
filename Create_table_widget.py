from tkinter import *


class Table_creator(Frame):

    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.is_row = False
        # self.window.geometry('800x100')
        self.config(bg='red')
        self.pack(fill=X)
        self.header = Frame(self, height=20, bg='red')
        self.header.pack(side=TOP, fill=BOTH, expand=1)
        self.row = Frame(self, height=20, bg='blue')
        self.row.pack(side=TOP, fill=BOTH, expand=1)

    def exim_table(self, name, single_header=True):

        if single_header:
            h = Frame(self.header, relief=SOLID, bd=1, bg='#a0beef')
            h.pack(side=LEFT, fill=BOTH, expand=1)
            Label(h, text=name, height=2, bg='#a0beef').pack()
        else:

            exim_frame = Frame(self.header, relief=SOLID, bd=1, bg='#a0beef')
            exim_frame.pack(side=LEFT, fill=BOTH, expand=1)
            Label(exim_frame, text=name, bg='#a0beef').pack()

            con_frame = Frame(exim_frame, relief=SOLID, bd=0, bg='#a0beef')
            con_frame.pack(side=TOP, fill=BOTH, expand=1)
            c = ['C1', 'C2', 'C3', 'C4', 'C5']
            for i in c:
                Label(con_frame, text=i, bd=1, relief=SOLID, bg='#a0beef').pack(side=LEFT, fill=BOTH, expand=1)

    def add_row(self, values):

        s = StringVar()
        s.set(values[0])
        Entry(self.row, textvariable=s, state='readonly', bd=1, relief=SOLID, width=32).pack(side=LEFT, fill=BOTH, expand=1)
        for val in values[1]:
            v = IntVar()
            v.set(val)
            Entry(self.row, textvariable=v, state='readonly', bd=1, relief=SOLID, width=5).pack(side=LEFT, fill=BOTH, expand=1)
        self.is_row = True


def main():
    values = ['079204720584', 171, 333, 153, 648, 828, 46962, 15246, 5130, 163125, 57006, 46791, 14913, 4977, 162477, 56178]

    root = Tk()
    manger = Table_creator(root)
    manger.exim_table('Service Number')
    manger.exim_table('Import Units', single_header=False)
    manger.exim_table('Export Units', single_header=False)
    manger.exim_table('Difference', single_header=False)
    manger.add_row(values)
    root.mainloop()


# main()
