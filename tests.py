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


import asyncio
import requests
from tkinter import *
from tkinter import ttk
import threading


async def get_page(url):

    resp = requests.get(url)
    return resp.status_code


class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self)
        self.master = master
        self.loop = asyncio.get_event_loop()
        Button(self.master, text='get', command=lambda: self.thread_worker(self.loop)).pack()
        self.progress = ttk.Progressbar(self.master, orient='horizontal', mode='indeterminate')
        self.progress.pack(side=BOTTOM, fill=X, expand=1, anchor='s')

    def start_asyn_loop(self, loop):
        items = self.master.winfo_children()
        # print(items)
        if len(items) > 3:
            items[3].destroy()

        result = loop.run_until_complete(get_page('http://www.python.org'))
        Label(self.master, text=result).pack()
        self.progress.stop()
        loop.stop()

    def thread_worker(self, loop):
        self.progress.start()
        threading.Thread(target=self.start_asyn_loop, args=(loop,)).start()


root = Tk()
app = Application(root)
root.mainloop()
