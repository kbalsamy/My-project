# modules
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import Pmw
import Create_table_widget as Table
import extractor
import batch_extractor as downloader
from queue import Queue
import queue
import threading
import time
# global data
from constants import *
import asyncio
import log
import logging
import file_creator as excel


# Helper classes and functions


def get_uname(file):
    if file:
        with open(file, 'r') as file:
            return [uname.strip() for uname in file]
    else:
        pass


def frame(window, side, bg=None):
    "Frames are returned here"
    view = Frame(window)
    view.pack(side=side, expand=1, fill=BOTH)
    return view


def button(window, name, command, side=None):
    "Buttons are returned here"
    b = Button(window, text=name, command=command)
    b.pack(side=side, fill=BOTH, expand=1)
    return b
    # main Application


class Application(Frame):

    def __init__(self, title, height, width, parent=None):
        Frame.__init__(self)
        self.title = title
        self.height = height
        self.width = width
        self.service_number = StringVar()
        self.service_password = StringVar()
        self.month = StringVar()
        self.year = IntVar()
        self.master.title(self.title)
        self.master.geometry('{}x{}'.format(self.height, self.width))
        self.master.grab_set()
        self.service_list = None
        self.progress = 0
        self.squeue = Queue()
        self.bqueue = Queue()
        self.loop = asyncio.get_event_loop()
        self.build_gui()
        self.progressbar = ttk.Progressbar(self.master, orient='horizontal', mode='indeterminate')
        self.progressbar.pack(side=BOTTOM, fill=X, expand=1, anchor='s')
        self.working_frame = Frame(self.master, height=180)
        self.working_frame.pack(side=TOP, fill=X)
        self.log_window = ScrolledText.ScrolledText(self.master, state='disabled')
        self.log_window.pack(side=BOTTOM, fill=X)
        self.log_handler = log.TextHandler(self.log_window)
        logging.basicConfig(filename='AMRapplication.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.addHandler(self.log_handler)

    def search_pane_gui(self):

        pass

    def move_window_pos(self, x, y):
        self.master.geometry('+{}+{}'.format(x, y))

    def move_frame_pos(self, frame, x, y):
        frame.geometry('+{}+{}'.format(x, y))

    def clear_mainwindow(self):
        children = self.working_frame.winfo_children()
        for wid in children:
            wid.destroy()
        self.menubar.entryconfig('Single Download', state='active')

    def upload_file(self):

        file = filedialog.askopenfilename()
        service_list = get_uname(file)
        self.service_list = service_list

    def show_progresss(self, max):

        self.progressbar = ttk.Progressbar(self.master, orient='horizontal', mode='indeterminate')
        self.progressbar.pack(side=BOTTOM, fill=X, expand=1, anchor='s')

    def db_spread_display(self, button):
        if button == 'Display':
            Message(self.master, text='Download is completed').pack()
        else:
            self.messbox.deactivate()
            self.menubar.entryconfig('Batch Download', state='active')
# -------------------------------------------------------------------------------------------------------

    def file_to_save(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                filetypes=(("Excel workbook", "*.xlsx"), ("all files", "*.*")))
        # print(filename)
        if filename is None:
            return
        tablename = self.month.get() + str(self.year.get())
        d = excel.xldownloader("{}.xlsx".format(filename), tablename)
        dialog = Pmw.MessageDialog(self.master, title='Download status', defaultbutton=0, buttons=('OK',),
                                   message_text='Excel file download completed')

    def get_batch_results(self, queue):
        results = downloader.main(self.service_list, self.pword_dialog.get(), self.month.get(), self.year.get())
        queue.put(results)

    def show_batch_results(self):
        self.menubar.entryconfig('Batch Download', state='disabled')
        try:
            results = self.bqueue.get(0)
            self.progressbar.stop()
            self.messbox = Pmw.MessageDialog(self.master, title='Batch download status', message_text=results, buttons=('Display', 'OK'), command=self.db_spread_display)
            self.messbox.activate(geometry='centerscreenfirst')
            timestr = time.asctime()
            logging.info('{} Batch download is completed'.format(timestr))
            b = Button(self.working_frame, text='Download', command=self.file_to_save)
            b.pack()

        except queue.Empty:
            self.master.after(100, self.show_batch_results)

    def execute_bdownload(self, button):

        if button == 'Download':
            self.pword_dialog = Pmw.PromptDialog(self.master, title='Password', label_text='Password:', entryfield_labelpos='n', entry_show='*', defaultbutton=0, buttons=('OK', 'Cancel'))
            self.pword_dialog.activate(geometry='centerscreenfirst')
            self.bdownload.deactivate()
            self.progressbar.start()
            # place thread here
            threading.Thread(target=self.get_batch_results, args=(self.bqueue,)).start()
            self.master.after(100, self.show_batch_results)
        else:
            self.bdownload.deactivate()

    def batch_download_dialog(self):

        self.bdownload = Pmw.Dialog(self.master, title='Batch Service Download', buttons=('Download', 'Cancel'), defaultbutton='Search', command=self.execute_bdownload)
        Message(self.bdownload.interior(), text='*This Option will work only, \n if password is same for all service', justify=LEFT, width=350).pack(side=TOP, fill=X, expand=1)
        Label(self.bdownload.interior(), text='Upload .txt file here').pack()
        Button(self.bdownload.interior(), text='upload', command=self.upload_file).pack()
        self.month.set('January')
        OptionMenu(self.bdownload.interior(), self.month, *months).pack()
        self.year.set(2019)
        OptionMenu(self.bdownload.interior(), self.year, *years).pack()
        self.bdownload.activate(geometry='centerscreenfirst')
# ------------------------------------------------------------------------------------------------------

    def get_results(self, queue=None):
        results = extractor.scrape(self.service_number.get(), self.service_password.get(), self.month.get(), self.year.get())
        queue.put(results)

    def show_results(self):
        self.menubar.entryconfig('Single Download', state='disabled')
        try:
            results = self.squeue.get(0)
            self.progressbar.stop()
            Button(self.working_frame, text='Clear', command=self.clear_mainwindow).pack()
            manager = Table.Table_creator(self.working_frame)
            manager.exim_table('Service Number')
            manager.exim_table('Import Units', single_header=False)
            manager.exim_table('Export Units', single_header=False)
            manager.exim_table('Difference', single_header=False)
            manager.add_row(results)
        except queue.Empty:
            self.master.after(100, self.show_results)

    def execute_sdownload(self, button):
        if button == 'Search':
            self.sdownload.deactivate()
            self.progressbar.start()
            # add scroll text window here to display log messages
            self.t1 = threading.Thread(target=self.get_results, kwargs={'queue': self.squeue})
            self.t1.start()
            self.master.after(100, self.show_results)
        else:
            self.sdownload.deactivate()
            self.sdownload.withdraw()

    def show_sdownload_dialog(self):
        self.sdownload = Pmw.Dialog(self.master, title='Single Service Download', buttons=('Search', 'Cancel'), defaultbutton='Search', command=self.execute_sdownload)
        Label(self.sdownload.interior(), text='Enter Service number').pack(side=TOP)
        sNumber = Entry(self.sdownload.interior(), width=30, textvariable=self.service_number)
        sNumber.pack(side=TOP)
        Label(self.sdownload.interior(), text='Enter Password').pack(side=TOP)
        pword = Entry(self.sdownload.interior(), width=30, show='*', textvariable=self.service_password)
        pword.pack(side=TOP)
        self.month.set('January')
        OptionMenu(self.sdownload.interior(), self.month, *months).pack(side=TOP, pady=10)
        self.year.set(2019)
        OptionMenu(self.sdownload.interior(), self.year, *years).pack(side=TOP, pady=10)
        self.sdownload.activate(geometry='centerscreenfirst')

    def show_about_dialog(self):
        Pmw.aboutversion('1.0')
        Pmw.aboutcopyright('Copyright Thiran Softwares 2019\nAll rights reserved')
        Pmw.aboutcontact(
            'For information about this application contact:\n' +
            '  My Help Desk\n' +
            '  Phone: +91 9176961009\n' +
            '  email: help@thiransoftwares.com'
        )
        about = Pmw.AboutDialog(self.master, title='About AMR Extractor', buttons=('OK',))
        self.move_frame_pos(about, 550, 150)
        about.activate(globalMode=1)


# Gui initilisation
    def build_gui(self):

        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.menubar.add_command(label='Single Download', command=self.show_sdownload_dialog)
        self.menubar.add_command(label='Batch Download', command=self.batch_download_dialog)
        self.menubar.add_command(label='About', command=self.show_about_dialog)


# Application instatiation
if __name__ == '__main__':
    app = Application('AMR extractor', 800, 250)
    app.move_window_pos(500, 150)
    app.mainloop()
