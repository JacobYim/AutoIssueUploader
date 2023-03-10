import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pickle
from issue_excel_generator import project_excel_download
from issue_uploader import upload_multithread
import threading


class Uploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Uploader")

        # Variables for user input
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.auto_upload = tk.BooleanVar()
        self.show_browser = tk.BooleanVar()
        self.save_credentials = tk.BooleanVar()
        self.num_threads = tk.StringVar(value="1")
        self.project_name = tk.StringVar()
        self.issue_type = tk.StringVar()

        # Load saved credentials if file exists
        try:
            with open(".credentials.pickle", "rb") as f:
                saved_credentials = pickle.load(f)
                if saved_credentials.get('save_credentials') :
                    self.username.set(saved_credentials.get("username"))
                    self.password.set(saved_credentials.get("password"))
                    self.auto_upload.set(saved_credentials.get("auto_upload"))
                    self.show_browser.set(saved_credentials.get("show_browser"))
                    self.save_credentials.set(saved_credentials.get("save_credentials"))
                    self.num_threads.set(saved_credentials.get("num_threads"))
                    self.project_name.set(saved_credentials.get("project_name"))
                    self.issue_type.set(saved_credentials.get("issue_type"))
        except FileNotFoundError:
            pass

        # Group 1: User ID, Password, Save ID Password, and Show Browser
        group1_frame = tk.LabelFrame(root, text="User Info")
        group1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        tk.Label(group1_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(group1_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(group1_frame, textvariable=self.username).grid(row=0, column=1, padx=10, pady=5)
        tk.Entry(group1_frame, textvariable=self.password, show="*").grid(row=1, column=1, padx=10, pady=5)
        tk.Checkbutton(group1_frame, text="Save credentials", variable=self.save_credentials).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        tk.Checkbutton(group1_frame, text="Show browser", variable=self.show_browser).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Group 2: Select Excel File, Upload, and Number of Threads
        group2_frame = tk.LabelFrame(root, text="Excel Upload")
        group2_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        tk.Button(group2_frame, text="Select Excel file", command=self.select_file).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(group2_frame, text="Number of threads:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(group2_frame, textvariable=self.num_threads).grid(row=1, column=1, padx=10, pady=5)
        tk.Checkbutton(group2_frame, text="auto upload", variable=self.auto_upload).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Upload button
        tk.Button(group2_frame, text="Upload", command=self.upload).grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Group 3: Project Name, Issue Type, and Download Excel Form
        group3_frame = tk.LabelFrame(root, text="Project Info")
        group3_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        tk.Label(group3_frame, text="Project name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(group3_frame, textvariable=self.project_name).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(group3_frame, text="Issue type:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(group3_frame, textvariable=self.issue_type).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(group3_frame, text="Download Excel form", command=self.download_form).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Group 4: Log Message Window
        group4_frame = tk.LabelFrame(root, text="Log Messages")
        group4_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.log = scrolledtext.ScrolledText(group4_frame, height=10, width=50)
        self.log.pack(fill=tk.BOTH, expand=True)

        # Configure rows and columns to stretch
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

    def select_file(self):
        """Open a file dialog to select an Excel file."""
        filetypes = [("Excel files", "*.xlsx"), ("All files", "*.*")]
        self.filename = filedialog.askopenfilename(filetypes=filetypes)

    def upload(self):
        """Start the upload process."""
        # Get user input
        username = self.username.get()
        password = self.password.get()
        auto_upload = self.auto_upload.get()
        show_browser = self.show_browser.get()
        save_credentials = self.save_credentials.get()
        num_threads = int(self.num_threads.get())
        project_name = self.project_name.get()
        issue_type = self.issue_type.get()

        # Save credentials if requested
        if save_credentials:
            with open(".credentials.pickle", "wb") as f:
                pickle.dump({
                    "username": username, 
                    "password": password, 
                    "save_credentials": save_credentials, 
                    "auto_upload" : auto_upload,
                    "show_browser" : show_browser,
                    "num_threads" : num_threads,
                    "project_name" : project_name,
                    "issue_type" : issue_type
                    },
                    f
                )

        # Perform upload
        try :
            t = threading.Thread(target=upload_multithread, args=(username, password, self.filename, num_threads, auto_upload, show_browser, self.log))
            t.start()
        except Exception as e :
            self.log.insert(tk.END,"Downloader Fail with Error : {}\n".format(e))

    def download_form(self):
        """Download an Excel form."""
        # TODO: Implement download form process
        username = self.username.get()
        password = self.password.get()
        auto_upload = self.auto_upload.get()
        show_browser = self.show_browser.get()
        save_credentials = self.save_credentials.get()
        num_threads = int(self.num_threads.get())
        project_name = self.project_name.get()
        issue_type = self.issue_type.get()

        # Save credentials if requested
        if save_credentials:
            with open(".credentials.pickle", "wb") as f:
                pickle.dump({
                    "username": username, 
                    "password": password, 
                    "save_credentials": save_credentials, 
                    "auto_upload" : auto_upload,
                    "show_browser" : show_browser,
                    "num_threads" : num_threads,
                    "project_name" : project_name,
                    "issue_type" : issue_type
                    },
                    f
                )
        try :
            t = threading.Thread(target=project_excel_download, args=(username, password, project_name, issue_type, show_browser, False, self.log))
            t.start()
        except Exception as e :
            self.log.insert(tk.END,"Downloader Fail with Error : {}\n".format(e))
            
if __name__ == "__main__":
    root = tk.Tk()
    uploader = Uploader(root)
    root.mainloop()
