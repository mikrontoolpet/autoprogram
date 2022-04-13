'''
Source code for a GUI able to run an OPC-UA client connected
to an OPC-UA Server to input data in a Virtual Grind Pro file.
Author: Alessandro Guglielmina
NTNU 2022
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
LARGE_FONT= ("Verdana", 12)
import threading
from pathlib import Path
import inspect
import asyncio
import logging

from autoprogram.errors import *
from autoprogram.config import Config
from autoprogram.vgpro import VgpWrapper
from autoprogram.common import try_more_times
try:
    from autoprogram import tools
except WrongCreateFileName:
    messagebox.showerror("Worksheet Error", "Wrong create file name.")

# Set gui logging level to INFO
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

CREATE_TOOL_TIMEOUT = 600
CREATE_TOOL_MAX_TRY_ATTEMPTS = 5


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, "robot-16.ico")
        tk.Tk.wm_title(self, "Autoprogram")
        tk.Tk.geometry(self,'400x400')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Pages initialization
        for F in (InitializingPage, SelectFamilyPage, SelectModePage, InsertArgumentsPage, CreatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(InitializingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.run() # runtime method
        
class InitializingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Initializing Page", font=LARGE_FONT)
        label.place(x=44,y=10)
        # Label
        self.init_label_text = "Tool families initialization..."
        self.init_label = tk.Label(self, text=self.init_label_text)
        self.init_label.place(x=100, y=100)
        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=self.next_button_method)
        next_button.place(x=40,y=300)
        # Close Button
        close_button = ttk.Button(self, text="Close",command=self.quit)
        close_button.place(x=200,y=300)

    def run(self):
        InitializingPage.family_dict = {}
        for T in (tools.drills.drills.atc.Tool,): # new tool classes must be added here
            InitializingPage.family_dict[T.family_address] = T
        self.init_label.config(text="Tool families initialized!")

    def next_button_method(self):
        self.controller.show_frame(SelectFamilyPage)
        self.init_label.config(text=self.init_label_text)

class SelectFamilyPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Select Family", font=LARGE_FONT)
        label.place(x=44,y=10)
        # Family entry
        self.family_address = tk.StringVar(self)
        self.family_entry = ttk.Entry(self, textvariable=self.family_address, width=30)
        self.family_entry.place(x=65,y=60)
        # Browse button
        browse_button = ttk.Button(self, text="Browse",
                            command=lambda: threading.Thread(target=self.browse_family).start())
        browse_button.place(x=260,y=60)
        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.next_button_method).start())
        next_button.place(x=65,y=300)
        # Back Button
        next_button = ttk.Button(self, text="Back",
                            command=lambda: threading.Thread(target=self.back_button_method).start())
        next_button.place(x=200,y=300)

    def run(self):
        pass

    def browse_family(self):
        family_dir = Path(filedialog.askdirectory(initialdir=Config.MASTER_PROGS_BASE_DIR))
        family_address_temp = family_dir.relative_to(Config.MASTER_PROGS_BASE_DIR)
        family_address_temp = family_address_temp.as_posix() # convert backslashes to forward slashes, to match hardcoded family addresses
        self.family_entry.delete(0, END)
        self.family_entry.insert(0, family_address_temp)

    def next_button_method(self):
        # Set the selected tool class
        try:
            family_address_var = self.family_address.get()
            SelectFamilyPage.ToolClass = InitializingPage.family_dict[family_address_var]
            self.controller.show_frame(SelectModePage)
        except KeyError:
            messagebox.showerror("User Entry Error", f"No such a tool family: {family_address_var}")

    def back_button_method(self):
        self.controller.show_frame(InitializingPage)


class SelectModePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Select Mode", font=LARGE_FONT)
        label.place(x=44,y=10)
        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.next_button_method).start())
        next_button.place(x=65,y=300)
        # Back Button
        back_button = ttk.Button(self, text="Back",
                            command=lambda: threading.Thread(target=self.back_button_method).start())
        back_button.place(x=200,y=300)
        # Modes listbox
        modes = Config.MODES
        self.listbox = Listbox(self, height=2, width=35)
        for mode in modes:
            self.listbox.insert(END, str(mode))
        self.listbox.place(x=65,y=65)

    def run(self):
        pass

    def next_button_method(self):
        try:
            SelectModePage.mode = self.listbox.get(self.listbox.curselection())
            if SelectModePage.mode == Config.MODES[0]: # manual
                self.controller.show_frame(InsertArgumentsPage)
            elif SelectModePage.mode == Config.MODES[1]: # auto
                self.controller.show_frame(CreatePage)
        except TclError:
            messagebox.showwarning(title="No choice error", message="Please select mode") 

    def back_button_method(self):
        self.controller.show_frame(SelectFamilyPage)


class InsertArgumentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Insert Arguments", font=LARGE_FONT)
        label.place(x=110,y=10)
        self.rowconfigure(0, minsize=45)
        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.next_button_method).start())
        next_button.place(x=65,y=300)
        # Back Button
        back_button = ttk.Button(self, text="Back",
                            command=lambda: threading.Thread(target=self.back_button_method).start())
        back_button.place(x=200,y=300)

    def run(self):
        if SelectModePage.mode == Config.MODES[0]: # manual
            self.grid_ui_entries()
        elif SelectModePage.mode == Config.MODES[1]: # auto
            pass

    def grid_ui_entries(self):
        # Tool name label
        tool_name_label = tk.Label(self, width=20, text="tool_name")
        tool_name_label.grid(row=1, column=0, padx=4, pady=4)
        # Tool name entry
        self.ui_name = tk.StringVar(self)
        tool_name_entry = ttk.Entry(self, textvariable=self.ui_name, width=20)
        tool_name_entry.grid(row=1, column=1, padx=4, pady=4)
        # Inspect tool class input arguments
        self.tool_cls_args = inspect.getargspec(SelectFamilyPage.ToolClass.__init__).args[3::] # get selected tool class arguments
        # Grid corrsponding labels and entries
        for idx, arg in enumerate(self.tool_cls_args):
            arg_label = tk.Label(self, width=20, text=arg)
            arg_entry = tk.Entry(self, width=20, name=arg)
            arg_label.grid(row=2+idx, column=0, padx=4, pady=4)
            arg_entry.grid(row=2+idx, column=1, padx=4, pady=4)

    def get_ui_entries(self):
        # Tool name
        InsertArgumentsPage.tool_name = self.ui_name.get()
        # Argument entries
        InsertArgumentsPage.ui_entries_list = []
        for arg in self.tool_cls_args:
            arg_entry = self.nametowidget(arg)
            str_arg = arg_entry.get()
            InsertArgumentsPage.ui_entries_list.append(str_arg)

    def next_button_method(self):
        self.get_ui_entries()
        self.controller.show_frame(CreatePage)

    def back_button_method(self):
        self.controller.show_frame(SelectModePage)


class CreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Create Programs", font=LARGE_FONT)
        label.place(x=150,y=30)
        self.rowconfigure(0, minsize=45)
        # Emergency Stop
        self.loadimage = tk.PhotoImage(file="autoprogram/icons/emergency_stop.png")
        self.emergency_stop = tk.Button(self, image=self.loadimage, command=lambda: threading.Thread(target=self.emergency_stop_method).start())
        self.emergency_stop["bg"] = "white"
        self.emergency_stop["border"] = "0"
        self.emergency_stop.place(x=120,y=100)

        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.next_button_method).start())
        next_button.place(x=65,y=300)
        # Back Button
        back_button = ttk.Button(self, text="Back",
                            command=lambda: threading.Thread(target=self.back_button_method).start())
        back_button.place(x=200,y=300)

    def run(self):
        asyncio.run(self.run_coroutine())

    def emergency_stop_method(self):
        asyncio.run(self.vgpw.__aexit__(None, None, None))

    async def run_coroutine(self):
        try:
            if SelectModePage.mode == Config.MODES[0]: # manual
                await self.create_one_tool(InsertArgumentsPage.tool_name, InsertArgumentsPage.ui_entries_list)
            elif SelectModePage.mode == Config.MODES[1]: # auto
                await self.create_many_tools()
        except TryMoreTimesFailed:
            messagebox.showerror("Autoprogram Error", "Try more times failed")
            _logger.error("Unhandled exception occurred.")

    @try_more_times(max_attempts=5, timeout=800, wait_period=1, retry_exception=AutoprogramError)
    async def create_one_tool(self, name, params_list):
        async with VgpWrapper(SelectFamilyPage.ToolClass.machine) as self.vgpw:
            async with SelectFamilyPage.ToolClass(self.vgpw.vgp_client, name, *params_list) as tool: # tool is an instance of the ToolFamily class
                await tool.create()
            
    async def create_many_tools(self):
        df = SelectFamilyPage.ToolClass.create_wb
        for idx, row in df.iterrows():
            name = row.loc["name"]
            params_list = row.filter(like="params").tolist()
            await self.create_one_tool(name, params_list)

    def next_button_method(self):
        self.controller.show_frame(SelectModePage)

    def back_button_method(self):
        self.controller.show_frame(InsertArgumentsPage)

