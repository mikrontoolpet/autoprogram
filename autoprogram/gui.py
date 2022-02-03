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

from autoprogram.config import Config
from autoprogram import tools


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

        # canvas = Canvas(self, width=2000, height=2000)
        # canvas.place(x = -100, y = 220)
        # blackLine = canvas.create_line(0,2,2000,2)
        # canvas.configure(background='gray')
        
        # canvas_id = canvas.create_text(432,25)
        # canvas.itemconfig(canvas_id, text = "akselov@stud.ntnu.no")
        # canvas.insert(canvas_id, 12, "")

        self.frames = {}

        for F in (InitializingPage, SelectFamilyPage, SelectModePage, InsertArgumentsPage):
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
        for T in (tools.drills.drills.titaniumg5.Tool, tools.drills.drills.ic.Tool): # new tool classes must be added here
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
                            command=lambda: threading.Thread(target=self.set_family).start())
        next_button.place(x=40,y=300)
        # Close Button
        close_button = ttk.Button(self, text="Close",command=self.quit)
        close_button.place(x=200,y=300)

    def run(self):
        pass

    def browse_family(self):
        family_dir = Path(filedialog.askdirectory(initialdir=Config.MASTER_PROGS_BASE_DIR))
        family_address_temp = family_dir.relative_to(Config.MASTER_PROGS_BASE_DIR)
        family_address_temp = family_address_temp.as_posix() # convert backslashes to forward slashes, to match hardcoded family addresses
        self.family_entry.delete(0, END)
        self.family_entry.insert(0, family_address_temp)

    def set_family(self):
        SelectFamilyPage.tool_family = InitializingPage.family_dict[self.family_address.get()]
        self.controller.show_frame(SelectModePage)


class SelectModePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Header
        label = tk.Label(self, text="Select Mode", font=LARGE_FONT)
        label.place(x=44,y=10)
        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.set_mode).start())
        next_button.place(x=65,y=300)
        # Back Button
        back_button = ttk.Button(self, text="Back",command=self.controller.show_frame(SelectFamilyPage))
        back_button.place(x=200,y=300)
        # Modes listbox
        modes = Config.MODES
        self.listbox = Listbox(self, height=2, width=35)
        for mode in modes:
            self.listbox.insert(END, str(mode))
        self.listbox.place(x=65,y=65)

    def run(self):
        pass

    def set_mode(self):
        try:
            SelectModePage.mode = self.listbox.get(self.listbox.curselection())
            self.controller.show_frame(InsertArgumentsPage)
        except TclError:
            messagebox.showwarning(title="No choice error", message="Please select mode")


class InsertArgumentsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Arguments", font=LARGE_FONT)
        label.place(x=110,y=10)
        self.rowconfigure(0, minsize=45)

        # Next Button
        next_button = ttk.Button(self, text="Next",
                            command=lambda: threading.Thread(target=self.set_mode).start())
        next_button.place(x=65,y=300)

        # button0 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button0.place(x=65,y=50)

        # button1 = ttk.Button(self, text="Display Motor Speed monitor",
        #                     command= motor_speed_monitor)
        # button1.place(x=65,y=80)

        # button2 = ttk.Button(self, text="Display Motor Torque monitor",
        #                     command= motor_torque_monitor)
        # button2.place(x=65,y=110)

        # button3 = ttk.Button(self, text="Display Motor Current monitor",
        #                     command= motor_current_monitor)
        # button3.place(x=65,y=140)

        # button4 = ttk.Button(self, text="Display Motor Temperature monitor",
        #                     command= motor_temp_monitor)
        # button4.place(x=65,y=170)

    def run(self):
        if SelectModePage.mode == Config.MODES[0]: # manual
            self.grid_ui_entries()
        elif SelectModePage.mode == Config.MODES[1]: # auto
            pass


    def grid_ui_entries(self):
        # Inspect tool class input arguments
        self.tool_cls_args = inspect.getargspec(SelectFamilyPage.tool_family.__init__).args[3::] # get selected tool class arguments
        # Grid corrsponding data entries
        for idx, arg in enumerate(self.tool_cls_args):
            arg_entry = tk.Entry(self, width=20, name=arg)
            arg_label = tk.Label(self, width=20, text=arg)
            arg_entry.grid(row=1+idx, column=1, padx=4, pady=4)
            arg_label.grid(row=1+idx, column=0, padx=4, pady=4)

    def read_ui_entries(self):
        self.str_arg_list = []
        for arg in self.tool_cls_args:
            arg_entry = self.nametowidget(arg)
            str_arg = arg_entry.get()
            self.str_arg_list.append(raw_inp_data_i)

    def next_button_method(self):
        if SelectModePage.mode == Config.MODES[0]: # manual
            self.read_ui_entries()
        self.controller.show_frame(InsertArgumentsPage)

# def motor_current_monitor():
#     messagebox.showinfo("Display sensor data", "Motor Current data will be displayed in a new window")
#     subprocess.call([sys.executable, 'server_gui_motorCurrent.py', 'argument1', 'argument2'])

# def motor_temp_monitor():
#     messagebox.showinfo("Display sensor data", "Motor Temperature data will be displayed in a new window")
#     subprocess.call([sys.executable, 'server_gui_motorTemperature.py', 'argument1', 'argument2'])

# def write_motorSpeed_to_file():
#     messagebox.showinfo("Data to file", "Motor Speed data will be written to file KUKA_KR16_2_motorSpeed.csv")
#     subprocess.call([sys.executable, 'server_gui_write_motorSpeed.py', 'argument1', 'argument2'])
#     messagebox.showinfo("Data to file", "Motor Speed data was successfully written to file KUKA_KR16_2_motorSpeed.csv")

# def write_motorTorque_to_file():
#     messagebox.showinfo("Data to file", "Motor Torque data will be written to file KUKA_KR16_2_motorTorque.csv")
#     subprocess.call([sys.executable, 'server_gui_write_motorTorque.py', 'argument1', 'argument2'])
#     messagebox.showinfo("Data to file", "Motor Torque data was successfully written to file KUKA_KR16_2_motorTorque.csv")

# def write_motorCurrent_to_file():
#     messagebox.showinfo("Data to file", "Motor Current data will be written to file KUKA_KR16_2_motorCurrent.csv")
#     subprocess.call([sys.executable, 'server_gui_write_motorCurrent.py', 'argument1', 'argument2'])
#     messagebox.showinfo("Data to file", "Motor Current data was successfully written to file KUKA_KR16_2_motorCurrent.csv")

# def write_motorTemp_to_file():
#     messagebox.showinfo("Data to file", "Motor Temperature data will be written to file KUKA_KR16_2_motorTemp.csv")
#     subprocess.call([sys.executable, 'server_gui_write_motorTemperature.py', 'argument1', 'argument2'])
#     messagebox.showinfo("Data to file", "Motor Temperature data was successfully written to file KUKA_KR16_2_motorTemp.csv")