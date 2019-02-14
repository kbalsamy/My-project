from tkinter import *
import tkinter.ttk as ttk
import sys
import Create_table_widget as twidget

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = [2018, 2019]
# for testing the values
values = ['079204720584', 171, 333, 153, 648, 828, 46962, 15246, 5130, 163125, 57006, 46791, 14913, 4977, 162477, 56178]


def show_about():

    about_win = Toplevel(main_window)
    about_win.transient(main_window)
    about_win.geometry('150x100+600+250')
    about_win.title('About')
    about_win.grab_set()

    Message(about_win, text="""Thiran Softwares \nVersion 1.1""", bg='#b1d7ef').pack(fill=BOTH, expand=1)


def open_tabone():
    menubar.entryconfig('Single Download', state='active')
    pane1.pack_forget()
    manager.pack_forget()
    tabOne(main_window)


def display_results(window, subwindow):
    global manager
    global pane1

    subwindow.destroy()
    menubar.entryconfig('Single Download', state='disabled')
    pane1 = Frame(main_window, height=200, bg='gray')
    pane1.pack(side=TOP, fill=BOTH)
    Button(pane1, text='Search', command=open_tabone).pack()
    manager = twidget.Table_creator(main_window)
    manager.exim_table('Service Number')
    manager.exim_table('Import Units', single_header=False)
    manager.exim_table('Export Units', single_header=False)
    manager.exim_table('Difference', single_header=False)
    manager.add_row(values)


def make_center():

    display_width = main_window.winfo_screenwidth()
    display_height = main_window.winfo_screenheight()
    frame_width = main_window.winfo_reqwidth()
    frame_height = main_window.winfo_reqheight()
    Pos_right = int((display_width / 2) - (frame_width / 2))
    pos_down = int((display_height / 2) - (frame_height / 2))
    return str(Pos_right) + "+" + str(pos_down)


def service_num_validate(num):

    pass


def tabOne(window):

    global service_num
    global service_pass
    global service_month
    global service_year
    global tabOneButton

    tabOne = Toplevel(window)
    tabOne.title('Single Service download')
    tabOne.geometry('200x300+550+140')
    tabOne.attributes('-toolwindow', 1)
    tabOne.grab_set()
    service_num = StringVar(tabOne)
    service_pass = StringVar(tabOne)
    service_month = StringVar(tabOne)
    service_year = IntVar(tabOne)

    Label(tabOne, text='Enter Service number').pack(side=TOP)
    sNumber = Entry(tabOne, width=30, textvariable=service_num)
    sNumber.pack(side=TOP)
    Label(tabOne, text='Enter Password', textvariable=service_pass).pack(side=TOP)
    pword = Entry(tabOne, width=30, show='*')
    pword.pack(side=TOP)
    service_month.set('January')
    OptionMenu(tabOne, service_month, *months).pack(side=TOP, pady=10)
    service_year.set(2019)
    OptionMenu(tabOne, service_year, *years).pack(side=TOP, pady=10)
    tabOneButton = Button(tabOne, text='Get', height=1, width=10, command=lambda: display_results(main_window, tabOne))
    tabOneButton.pack(side=TOP, pady=10)


def application():

    global main_window
    global menubar

    main_window = Tk()
    main_window.title('Welcome')  # {}'.format(login_username.get()))
    main_window.geometry('800x550')
    main_window.geometry('+330+106')

    menubar = Menu(main_window)
    main_window.config(menu=menubar)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='Save', command=lambda: print('save'))
    filemenu.add_command(label='Print', command=lambda: print('print'))
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=lambda: print('Exit'))
    menubar.add_cascade(label='File', menu=filemenu)

    menubar.add_command(label='Single Download', command=lambda: tabOne(main_window))
    menubar.add_command(label='Batch Download')
    menubar.add_command(label='Show')
    menubar.add_command(label='About', command=show_about)

    main_window.mainloop()


def del_frame(frame):
    frame.destroy()
    login_window.deiconify()


def __CancelCommand():
    pass


def authenticate():

    if login_username.get() == 'user' and login_password.get() == 'pass':
        login_window.destroy()
        application()

    else:
        login_window.withdraw()
        user_entry.delete(0, 'end')
        pass_entry.delete(0, 'end')
        failed_frame = Tk()
        failed_frame.title('AMR Extractor')
        failed_frame.geometry('150x50+475+325')
        failed_frame.attributes('-toolwindow', 1)
        # failed_frame.resizable(0, 0)
        failed_frame.protocol('WM_DELETE_WINDOW', __CancelCommand)
        Label(failed_frame, text='Invalid account').pack()
        Button(failed_frame, text='Try Again', command=lambda: del_frame(failed_frame)).pack()


def login_frame():

    global login_window
    global login_username
    global login_password
    global user_entry
    global pass_entry

    login_window = Tk()
    login_window.title('AMR Extractor')
    login_window.geometry('450x250+250+200')
    login_username = StringVar()
    login_password = StringVar()
    Label(login_window, text='UserName').pack(pady=10)
    user_entry = Entry(login_window, textvariable=login_username, width=30)
    user_entry.pack(pady=10)
    Label(login_window, text='Password').pack(pady=10)
    pass_entry = Entry(login_window, show='*', textvariable=login_password, width=30)
    pass_entry.pack(pady=10)
    Button(login_window, text='Login', command=authenticate).pack(pady=10)

    login_window.mainloop()


# login_frame()
application()
