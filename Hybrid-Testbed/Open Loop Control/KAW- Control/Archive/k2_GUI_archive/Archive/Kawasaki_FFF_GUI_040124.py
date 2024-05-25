# Author: Walter W Glockner
# GUI for adjusting parameters of FFF process for 
# Kawasaki GUI


import tkinter as tk
from tkinter import ttk
import socket
import select

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_to_plc(socket, plc_ip, plc_port):
    socket.connect((plc_ip, plc_port))
    print("Connected to PLC")

def send_data(socket, data):
    socket.sendall(data.encode())

def receive_data(socket):
    received_data = ''
    socket.setblocking(0)  # Set the socket to non-blocking mode

    while True:
        ready = select.select([socket], [], [], 1.0)  # Wait for 1 second
        if ready[0]:
            chunk = socket.recv(1024).decode()
            if not chunk:
                break
            received_data += chunk
        else:
            # No data available within 1 second
            break

    socket.setblocking(1)  # Set the socket back to blocking mode
    return received_data

# Usage
plc_ip = '192.168.1.2'  # PLC's static IP address
plc_port = 10000        # Port that the PLC is listening on
s = create_socket()
connect_to_plc(s, plc_ip, plc_port)


print(receive_data(s))

class Kaw2FFFControl:
    def __init__(self, root):
        self.root = root
        root.title("Kaw2 FFF Control")
        tab_control = ttk.Notebook(root) 

        # Initialize states
        self.extrusion_state = False
        self.retraction_state = False
        self.printer_state = False  # False means stopped, True means started
        self.printer_paused = False  # Track the paused state
        self.air_state = False # False means off
        self.automated_state = False # False means manual

        # Main frame to contain all widgets
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        
        # Tab control
        quality_tab = ttk.Frame(tab_control) 
        other_tab = ttk.Frame(tab_control) 
        
        tab_control.add(quality_tab, text ='Quality') 
        tab_control.add(other_tab, text ='Other') 
        tab_control.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E)) 

        # Printer status indicator
        self.status_label = ttk.Label(main_frame, text="Printer Stopped", background="red", foreground="white")
        self.status_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Speed control frame
        speed_frame = ttk.LabelFrame(main_frame, text="Speed Control", padding="10")
        speed_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        speed_frame.columnconfigure(1, weight=1)

        self.speed_label = ttk.Label(speed_frame, text="Speed (RPM):")
        self.speed_label.grid(row=0, column=0, sticky=tk.W)

        self.speed_var = tk.DoubleVar()
        self.speed_scale = ttk.Scale(speed_frame, from_= -800, to = 800, orient='horizontal', variable=self.speed_var, command=self.update_speed_scale)
        self.speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        self.speed_entry = ttk.Entry(speed_frame, textvariable=self.speed_var, width=10)
        self.speed_entry.grid(row=0, column=2, padx=5)
        self.speed_entry.bind('<Return>', self.update_speed_entry)

        # Temperature control frame
        temp_frame = ttk.LabelFrame(main_frame, text="Temperature Control", padding="10")
        temp_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        temp_frame.columnconfigure(1, weight=1)

        self.temp_label = ttk.Label(temp_frame, text="Temperature (°C):")
        self.temp_label.grid(row=0, column=0, sticky=tk.W)

        self.temp_var = tk.DoubleVar()
        self.temp_scale = ttk.Scale(temp_frame, from_=0, to=300, orient='horizontal', variable=self.temp_var, command=self.update_temp_scale)
        self.temp_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        self.temp_entry = ttk.Entry(temp_frame, textvariable=self.temp_var, width=10)
        self.temp_entry.grid(row=0, column=2, padx=5)
        self.temp_entry.bind('<Return>', self.update_temp_entry)

        # Control buttons frame
        control_frame = ttk.Frame(main_frame, padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        control_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_printer)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_printer, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_printer, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.extrusion_button = ttk.Button(control_frame, text="Start Extrusion", command=self.toggle_extrusion)
        self.extrusion_button.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.retraction_button = ttk.Button(control_frame, text="Start Retraction", command=self.toggle_retraction)
        self.retraction_button.grid(row=0, column=4, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.air_button = ttk.Button(control_frame, text="Start Air", command=self.toggle_air)
        self.air_button.grid(row=0, column=5, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.automated_button = ttk.Button(control_frame, text="Start Automated", command=self.toggle_automated)
        self.automated_button.grid(row=0, column=6, padx=5, pady=5, sticky=(tk.W, tk.E))

        #self.rumble_button = ttk.Button(control_frame, text="Start Rumbler", command=self.toggle_rumble)
        #self.rumble_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))


        # Layer height frame
        layer_height_frame = ttk.LabelFrame(quality_tab, text="Layer height (mm)", padding="10")
        layer_height_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = (tk.W, tk.E))
        layer_height_frame.columnconfigure([0, 1, 2, 3], weight = 1)

        # Layer height
        self.layer_height_var = tk.DoubleVar()
        
        self.layer_height_label = ttk.Label(layer_height_frame, text = "Layer height: ", font = ('Arial', 10))
        self.layer_height_label.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = (tk.W))

        self.layer_height_entry = ttk.Entry(layer_height_frame, textvariable=self.layer_height_var, width=10)
        self.layer_height_entry.grid(row = 0, column = 1, padx = 0, sticky = (tk.W))
        self.layer_height_entry.bind('<Return>', self.update_layer_height_entry)

        # Inital layer height
        self.first_layer_height_var = tk.DoubleVar()
        
        self.first_layer_height_label = ttk.Label(layer_height_frame, text = "First layer height: ", font = ('Arial', 10))
        self.first_layer_height_label.grid(row = 1, column = 0, padx = 15, pady = 0, sticky = (tk.E))

        self.first_layer_height_entry = ttk.Entry(layer_height_frame, textvariable=self.first_layer_height_var, width=10)
        self.first_layer_height_entry.grid(row = 1, column = 1, padx = 0, sticky = (tk.W))
        self.first_layer_height_entry.bind('<Return>', self.update_first_layer_height_entry)

        # Line width frame
        line_width_frame = ttk.LabelFrame(quality_tab, text="Line width (mm)", padding="10")
        line_width_frame.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = (tk.W, tk.E))
        line_width_frame.columnconfigure([0, 1, 2, 3, 4], weight = 1)

        # Default line width
        self.default_line_width_var = tk.DoubleVar()
        
        self.default_line_width_label = ttk.Label(line_width_frame, text = "Default: ", font = ('Arial', 10))
        self.default_line_width_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = (tk.W))

        self.default_line_width_entry = ttk.Entry(line_width_frame, textvariable=self.default_line_width_var, width=10)
        self.default_line_width_entry.grid(row = 0, column = 1, padx = 0, sticky = (tk.E))
        self.default_line_width_entry.bind('<Return>', self.update_default_line_width_entry)

        # First layer line width
        self.first_layer_line_width_var = tk.DoubleVar()
        
        self.first_layer_line_width_label = ttk.Label(line_width_frame, text = "First Layer: ", font = ('Arial', 10))
        self.first_layer_line_width_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = (tk.W))

        self.first_layer_line_width_entry = ttk.Entry(line_width_frame, textvariable=self.default_line_width_var, width=10)
        self.first_layer_line_width_entry.grid(row = 1, column = 1, padx = 0, sticky = (tk.E))
        self.first_layer_line_width_entry.bind('<Return>', self.update_first_layer_line_width_entry)

        # Author label
        self.author_label = ttk.Label(other_tab, text="I know, I'll get to it...", font=('Arial', 20, 'italic'))
        self.author_label.grid(row=0, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)


        # Author label
        self.author_label = ttk.Label(main_frame, text="Author: Walter W Glockner", font=('Bold', 5, 'bold'))
        self.author_label.grid(row=5, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)


    

    def send_variable_update(self, variable_name, value):
        message = f"{variable_name}:{value}\n"
        send_data(s, message)
        print(f"Sent update: {message}")

    def update_speed_scale(self, value):
        self.speed_var.set(round(float(value), 1))
        self.send_variable_update("eMotorRPM", self.speed_var.get())
        self.send_variable_update("extrudeFlowrate", self.speed_var.get())
        print(f"Setting speed to {value} RPM")

    def update_speed_entry(self, event):
        value = self.speed_var.get()
        self.speed_scale.set(value)
        self.send_variable_update("eMotorRPM", value)
        print(f"Setting speed to {value} RPM")

    def update_temp_scale(self, value):
        self.temp_var.set(round(float(value), 1))
        self.send_variable_update("temperature", self.temp_var.get())
        print(f"Setting temperature to {value} °C")

    def update_temp_entry(self, event):
        value = self.temp_var.get()
        self.temp_scale.set(value)
        self.send_variable_update("temperature", value)
        print(f"Setting temperature to {value} °C")

    def update_layer_height_entry(self, event):
        value = self.layer_height_var.get()
        self.send_variable_update("layer_height", value)
        print(f"Setting layer height to {value} mm")

    # Implement similar updates for other update methods...


    def update_first_layer_height_entry(self, event):
        value = self.first_layer_height_var.get()
        #send_data(s, "FLH")
        #send_data(s, value)
        #send_data(s, '\n')
        print(f"Setting first layer height to {value} mm")

    def update_default_line_width_entry(self, event):
        value = self.default_line_width_var.get()
        #send_data(s, "DLW")
        #send_data(s, value)
        #send_data(s, '\n')
        print(f"Setting defualt line width to {value} mm")

    def update_first_layer_line_width_entry(self, event):
        value = self.first_layer_line_width_var.get()
        #send_data(s, "LW")
        #send_data(s, value)
        #send_data(s, '\n')
        print(f"Setting defualt line width to {value} mm")

    def toggle_extrusion(self):
        if not self.retraction_state:
            self.extrusion_state = not self.extrusion_state
            self.send_variable_update("command", "extrude" if self.extrusion_state else "stop_print")
            self.extrusion_button.config(text="Stop Extrusion" if self.extrusion_state else "Start Extrusion")
            print("Extrusion started" if self.extrusion_state else "Extrusion stopped")

    def toggle_retraction(self):
        if not self.extrusion_state:
            self.retraction_state = not self.retraction_state
            self.send_variable_update("command", "retract" if self.retraction_state else "stop_retract")
            self.retraction_button.config(text="Stop Retraction" if self.retraction_state else "Start Retraction")
            print("Retraction started" if self.retraction_state else "Retraction stopped")

    def start_printer(self):
        if not self.printer_state:
            self.printer_state = True
            self.send_variable_update("command", "start_print")
            self.status_label.config(text="Printer Started", background="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            print("Printer started")

    def stop_printer(self):
        if self.printer_state:
            self.printer_state = False
            self.send_variable_update("command", "stop_print")
            self.status_label.config(text="Printer Stopped", background="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
            print("Printer stopped")

    def pause_printer(self):
        self.printer_paused = not self.printer_paused
        command = "pause_print" if self.printer_paused else "resume_print"
        self.pause_button.config(text="Resume" if self.printer_paused else "Pause")
        self.status_label.config(text="Printer Paused", background="yellow" if self.printer_paused else "green")
        print("Printer paused" if self.printer_paused else "Printing resumed")

    def toggle_air(self):
        self.air_state = not self.air_state
        action = "on" if self.air_state else "off"
        self.send_variable_update("air", action)
        self.air_button.config(text="Stop Air" if self.air_state else "Start Air")
        print("Air toggled:", "on" if self.air_state else "off")

    def toggle_automated(self):
        self.automated_state = not self.automated_state
        action = "on" if self.automated_state else "off"
        self.send_variable_update("automated", action)
        self.automated_button.config(text="Stop Automated" if self.automated_state else "Start automated")
        print("Automated toggled:", "on" if self.automated_state else "off")
        



# Main program
if __name__ == "__main__":
    root = tk.Tk()
    gui = Kaw2FFFControl(root)
    root.mainloop()

