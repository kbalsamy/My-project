# from tkinter import *
# import api
# import constants


# class App(Frame):

#     def __init__(self, master):
#         Frame.__init__(self)
#         self.pack()
#         self.master = master
#         self.results = None
#         Button(self, text='get', command=self.get_val).pack()

#     def get_val(self):

#         self.results = api.scrape('079204720584', 'tneb', 'January', 2019)
#         Label(self, text=self.results).pack()

#     def get_from_func(self):

#         pass


# root = Tk()
# a = App(root)
# root.mainloop()

# from tkinter import *

# class Application():

#     def __init__(self):
#         self.title = title


# import asyncio
# import requests
# from tkinter import *
# from tkinter import ttk
# import threading


# async def get_page(url):

#     resp = requests.get(url)
#     return resp.status_code


# class Application(Frame):

#     def __init__(self, master):
#         Frame.__init__(self)
#         self.master = master
#         self.loop = asyncio.get_event_loop()
#         Button(self.master, text='get', command=lambda: self.thread_worker(self.loop)).pack()
#         self.progress = ttk.Progressbar(self.master, orient='horizontal', mode='indeterminate')
#         self.progress.pack(side=BOTTOM, fill=X, expand=1, anchor='s')

#     def start_asyn_loop(self, loop):
#         items = self.master.winfo_children()
#         # print(items)
#         if len(items) > 3:
#             items[3].destroy()

#         result = loop.run_until_complete(get_page('http://www.python.org'))
#         Label(self.master, text=result).pack()
#         self.progress.stop()
#         loop.stop()

#     def thread_worker(self, loop):
#         self.progress.start()
#         threading.Thread(target=self.start_asyn_loop, args=(loop,)).start()


# root = Tk()
# app = Application(root)
# root.mainloop()

# import time
# import threading
# import logging
# try:
#     import tkinter as tk  # Python 3.x
#     import tkinter.scrolledtext as ScrolledText
# except ImportError:
#     import Tkinter as tk  # Python 2.x
#     import ScrolledText


# class TextHandler(logging.Handler):
#     # This class allows you to log to a Tkinter Text or ScrolledText widget
#     # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

#     def __init__(self, text):
#         # run the regular Handler __init__
#         logging.Handler.__init__(self)
#         # Store a reference to the Text it will log to
#         self.text = text

#     def emit(self, record):
#         msg = self.format(record)

#         def append():
#             self.text.configure(state='normal')
#             self.text.insert(tk.END, msg + '\n')
#             self.text.configure(state='disabled')
#             # Autoscroll to the bottom
#             self.text.yview(tk.END)
#         # This is necessary because we can't modify the Text from other threads
#         self.text.after(0, append)


# class myGUI(tk.Frame):

#     # This class defines the graphical user interface

#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.root = parent
#         self.build_gui()

#     def build_gui(self):
#         # Build GUI
#         self.root.title('TEST')
#         self.root.option_add('*tearOff', 'FALSE')
#         self.grid(column=0, row=0, sticky='ew')
#         self.grid_columnconfigure(0, weight=1, uniform='a')
#         self.grid_columnconfigure(1, weight=1, uniform='a')
#         self.grid_columnconfigure(2, weight=1, uniform='a')
#         self.grid_columnconfigure(3, weight=1, uniform='a')

#         # Add text widget to display logging info
#         st = ScrolledText.ScrolledText(self, state='disabled')
#         st.configure(font='TkFixedFont')
#         st.grid(column=0, row=1, sticky='w', columnspan=4)

#         # Create textLogger
#         text_handler = TextHandler(st)

#         # Logging configuration
#         logging.basicConfig(filename='test.log',
#                             level=logging.INFO,
#                             format='%(asctime)s - %(levelname)s - %(message)s')

#         # Add the handler to logger
#         logger = logging.getLogger()
#         logger.addHandler(text_handler)


# def worker():
#     # Skeleton worker function, runs in separate thread (see below)
#     while True:
#         # Report time / date at 2-second intervals
#         time.sleep(2)
#         timeStr = time.asctime()
#         msg = 'Current time: ' + timeStr
#         logging.info(msg)


# def main():

#     root = tk.Tk()
#     myGUI(root)
#     t1 = threading.Thread(target=worker, args=[])
#     t1.start()

#     root.mainloop()
#     t1.join()


# main()


# main()
from tkinter import filedialog
from tkinter import *
from xlsxwriter import Workbook


def downloadfile(filename):
    wb = Workbook("{}.xlsx".format(filename))
    ws = wb.add_worksheet('one')

    ws.write(0, 0, 'karthik')
    wb.close()


root = Tk()

frame = Frame(root).pack()
filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                        filetypes=(("Excel workbook", "*.xlsx"), ("all files", "*.*")))
print(filename)
Button(frame, text='get', command=lambda: downloadfile(filename)).pack()
print(filename)


root.mainloop()

# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.options import Options

# options = Options()
# options.headless = False
# binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
# driver = webdriver.Firefox(options=options, firefox_binary=binary)
# driver.get('http://www.python.org')
