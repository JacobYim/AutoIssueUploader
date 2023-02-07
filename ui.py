import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile, askdirectory
import os
from validation import login_test
import threading 
import time
import logging
import tkinter.scrolledtext as ScrolledText
import pandas as pd
from upload import UploadManager

stop_threads = False
works = []
UploadMgr = None

def quit() :
    '''
        a method acting at closing button
    '''
    global root
    global stop_threads
    stop_threads = True
    root.quit()

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

id = tk.StringVar() #Password variable
pw = tk.StringVar() #Password variable
dirpath = None
filepath = None


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class myGUI(tk.Frame):

    # This class defines the graphical user interface 

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def build_gui(self):                    
        # Build GUI
        self.root.title('Proceeding Logs')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='disabled')
        st.configure(
            width = 200, 
            height = 200,    
            font='TkFixedFont'
        )
       
        st.grid(column = 0, pady = 10, padx = 10)
        text_handler = TextHandler(st)

        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

def worker():
    '''
    function for
    '''
    cur_works = []
    while True:
        global stop_threads, works, UploadMgr
        if stop_threads:
            break
        time.sleep(2)
        timeStr = time.asctime()
        msg = 'Current time: ' + timeStr
        logging.info(msg) 
        if len(works) > 0 :
            logging.info(len(works)) 
            cur_works += works
            works = []
            UploadMgr.run(cur_works, 3)

def hello ():  
    t1 = threading.Thread(target=worker, args=[])
    t1.start()

    top= Toplevel(root)
    top.geometry("750x250")
    top.title("Child Window")
    myGUI(top)
    
    print(dirpath,filepath )
    # file_testS
    if not dirpath and not filepath :
        label1 = tk.Label(root, text= 'Please check your file path or directory', fg='red', font=('helvetica', 8, 'bold'))
        canvas1.create_window(150, 210, window=label1)
        return

    # login test
    if not id and not pw :
        label1 = tk.Label(root, text= 'Please check your id and pw or \n Network VPN Status', fg='red', font=('helvetica', 8, 'bold'))
        canvas1.create_window(150, 210, window=label1)
        return

    else : 
        global UploadMgr
        s, p =str(id.get()), str(pw.get())
        UploadMgr = UploadManager(s, p)

    global works
    df = pd.read_excel(filepath, header=0, index_col=0)
    data = list(df[0:100].to_dict('series').values())
    data = list(filter(lambda x : str(x['Uploaded']) == '0', data))
    for i in range(len(data)) :
        data[i]['dirpath'] = dirpath
    # data = list(map(lambda x : x['dirpath'] = dirpath, data))
    works += data

    
    # t1.join()

def open_file():
    file = askopenfile(mode='r', filetypes=[('Excel Files', '*.xlsx')])
    if file:
        global filepath 
        filepath = os.path.abspath(file.name)
        print(filepath)
        path_label = tk.Label(root, text = str(filepath), font=('helvetica', 8))
        canvas1.create_window(150, 125, window=path_label)

def open_dir():
    path = askdirectory(title='Select Folder')  
    if path:
        global dirpath
        dirpath = os.path.abspath(path)
        print(dirpath)
        path_label = tk.Label(root, text = str(dirpath), font=('helvetica', 8))
        canvas1.create_window(150, 175, window=path_label)

label1 = tk.Label(root, text= 'Issue Auto Uploader', fg='blue', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 20, window=label1)

id_label = tk.Label(root, text= 'ID', fg='black', font=('helvetica', 8))
id_txt = tk.Entry(root, width = 25, textvariable=id)
canvas1.create_window(50, 50, window=id_label)
canvas1.create_window(150, 50, window=id_txt)

pw_label = tk.Label(root, text= 'PW', fg='black', font=('helvetica', 8))
pw_txt = tk.Entry(root, width = 25, textvariable=pw, show='*')
canvas1.create_window(50, 75, window=pw_label)
canvas1.create_window(150, 75, window=pw_txt)

issue_file_label = tk.Label(root,  width = 25, text='ISSUE', fg='black', font=('helvetica', 8))
file_browser = tk.Button(root, width = 22, text="Browse", command=open_file)
canvas1.create_window(50, 100, window=issue_file_label)
canvas1.create_window(150, 100, window=file_browser)

video_dir_label = tk.Label(root,  width = 25, text='Video', fg='black', font=('helvetica', 8))
video_dir_browser = tk.Button(root, width = 22, text="Browse", command=open_dir)
canvas1.create_window(50, 150, window=video_dir_label)
canvas1.create_window(150, 150, window=video_dir_browser)

button1 = tk.Button(text='Upload', command=hello, bg='brown',fg='white')
canvas1.create_window(150, 250, window=button1) 

root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()
