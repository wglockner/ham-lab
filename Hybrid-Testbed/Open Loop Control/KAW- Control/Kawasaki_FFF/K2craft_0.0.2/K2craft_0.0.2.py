# Author: Walter W Glockner
# GUI for adjusting parameters of FFF process for 
# Kawasaki GUI


import tkinter as tk
from tkinter import ttk
import socket
import select
import threading
import time
import queue


class Kaw2FFFControl:
    def __init__(self, root):

        print("Initializing...")
        self.root = root
        self.root.title("Kaw2 FFF Control")
        self.output_states = {}
        self.input_states = {}
        print("Setting connection state...")
        self.connection_state = False
        print("Initializing GUI...")
        self.initialize_gui()
        self.s = None
        
        self.plc_ip = '192.168.1.2'
        self.plc_port = 10000
        print("Connecting to PLC...")
        self.connect_to_plc()
        print("Initialization complete.")
        

    def create_socket(self):
        if self.s is not None:
            try:
                self.s.close()
            except OSError as e:
                print(f"Error closing existing socket: {e}")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)


    def connect_to_plc(self):
        self.create_socket()
        try:
            self.s.connect((self.plc_ip, self.plc_port))
            print("Connected to PLC")
            self.connection_state = True
            self.update_connection_status(True)
            self.send_data("GUI_CONNECTED")  # Sending a message to the PLC
        except (OSError, TimeoutError) as e:
            print(f"Connection to PLC failed: {e}")
            self.update_connection_status(False)

    def disconnect_socket(self):
        if self.s:
            try:
                self.s.close()
                print("Disconnected from PLC")
            except OSError as e:
                print(f"Error disconnecting from PLC: {e}")
            finally:
                self.s = None
                self.connection_state = False
                self.update_connection_status(False)

    def send_data(self, data):
        if self.connection_state and self.s:
            try:
                self.s.sendall(data.encode('utf-8'))
                print(f"Data sent: {data}")
            except OSError as e:
                print(f"Error sending data: {e}")
                self.disconnect_socket()

    def receive_data(self):
        buffer = ''
        if self.connection_state and self.s:
            try:
                self.s.setblocking(0)  # Set the socket to non-blocking mode
                ready = select.select([self.s], [], [], 1.0)
                if ready[0]:
                    while True:
                        try:
                            chunk = self.s.recv(1024).decode('utf-8')  # Try to read data
                            if chunk:
                                buffer += chunk
                            else:
                                break  # No more data, exit the loop
                        except BlockingIOError:
                            break  # No more data available at the moment
                    if '\n' in buffer:
                        complete_message = buffer.strip()
                        print("Received Data:", complete_message)  # Debugging statement
                        buffer = ''
                        return complete_message
            except OSError as e:
                print(f"Error receiving data: {e}")
                self.disconnect_socket()
            finally:
                if self.s:
                    self.s.setblocking(1)
        return None
    
    def update_io_label(self, pin, state):
        pin_label = self.channel_1_pin_labels.get(pin) or self.channel_2_pin_labels.get(pin)
        if pin_label:
            pin_label.config(text=f"Pin {pin}: {'High' if state else 'Low'}", background="green" if state else "red")


    def process_received_data(self, data):
        
        if "channel_1_states:" in data:
            states = data.split('channel_1_states:')[1].split(',')
            for pin, state in enumerate(states, start=1):
                state = (state == '1')
                if pin <= 16:
                    #print(f"Updating Channel 1, Pin {pin}, State {state}")  # Debug print
                    self.update_input_indicator(1, pin, state)
        if "channel_2_states:" in data:
            states = data.split('channel_2_states:')[1].split(',')
            for pin, state in enumerate(states, start=1):
                state = (state == '1')
                if pin <= 16:
                    #print(f"Updating Channel 2, Pin {pin}, State {state}")  # Debug print
                    self.update_input_indicator(2, pin, state)



    def toggle_disconnect(self):
        if self.connection_state:
            self.send_data("command:stop_client")
            self.disconnect_socket()
            self.disconnect_button.config(text="Connect Server")
        else:
            self.connect_to_plc()
            self.disconnect_button.config(text="Disconnect Server" if self.connection_state else "Connect Server")

    def update_connection_status(self, is_connected):
        self.connection_state = is_connected
        status_text = "Connected" if is_connected else "Not Connected"
        status_color = "green" if is_connected else "red"
        self.connection_status_label.config(text=status_text, background=status_color)

    def initialize_gui(self):
        
        # Using grid for the entire layout
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tab_control = ttk.Notebook(self.main_frame)
        self.IO_control_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.IO_control_tab, text='IO Control')
        self.create_io_controls(self.IO_control_tab, 1, 16, 0)  # Channel 1 inputs
        self.create_io_controls(self.IO_control_tab, 2, 16, 1)  # Channel 2 inputs

        # Initialize channel labels for inputs and outputs side by side
        self.create_io_controls(self.IO_control_tab, 1, 16, 0)  # Column 0 for channel 1
        self.create_io_controls(self.IO_control_tab, 2, 16, 1)  # Column 1 for channel 2
        self.create_io_controls(self.IO_control_tab, 3, 15, 2)  # Column 2 for channel 3
        self.create_io_controls(self.IO_control_tab, 4, 15, 3)  # Column 3 for channel 4

        # Initialize states
        self.control_state = False
        self.extrusion_state = False
        self.retraction_state = False
        self.printer_state = False  # False means stopped, True means started
        self.printer_paused = False  # Track the paused state
        self.air_state = False # False means off
        self.automated_state = False # False means manual
        self.rumbler_state = False # False means rumbler is off
        self.connection_state = False
        self.print_error_once = True
        self.disconnect_state = False
        threading.Thread(target=self.auto_request_io_update, daemon=True).start()

        # Main frame to contain all widgets
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        

        
        # Tab control
        quality_tab = ttk.Frame(self.tab_control) 
        IO_control_tab = ttk.Frame(self.tab_control)
        other_tab = ttk.Frame(self.tab_control) 
        
        self.tab_control.add(quality_tab, text ='Quality') 
        self.tab_control.add(other_tab, text ='Other') 
        self.tab_control.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E)) 

        # Printer status indicator
        self.status_label = ttk.Label(main_frame, text="Printer Stopped", background="red", foreground="white")
        self.status_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Connection status control
        self.connection_status_label = ttk.Label(main_frame, text="Not Connected", background="red", foreground="white")
        self.connection_status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

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

        self.rumbler_button = ttk.Button(control_frame, text="Start Rumbler", command=self.toggle_rumbler)
        self.rumbler_button.grid(row=0, column=7, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.disconnect_button = ttk.Button(control_frame, text="Disconnect server", command=self.toggle_disconnect)
        self.disconnect_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))



        # Author label
        self.author_label = ttk.Label(main_frame, text="Author: Walter W Glockner", font=('Bold', 5, 'bold'))
        self.author_label.grid(row=5, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)

        # Control Tab
        # Layer_tab
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

        # IO control tab
        Kawasaki_IO_control_frame = ttk.LabelFrame(IO_control_tab, text="Kawasaki IO", padding="10")
        Kawasaki_IO_control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Adjust column configuration for a single column layout
        Kawasaki_IO_control_frame.columnconfigure(0, weight=1)
        
        
        
        
       
        self.channel_3_pin_labels = {}
        self.channel_4_pin_labels = {}
        self.channel_5_pin_labels = {}
        self.channel_6_pin_labels = {}
        self.channel_7_pin_labels = {}
        self.channel_8_pin_labels = {}
        self.channel_labels = {}
        self.output_buttons = {}


        
        


       

        
















        

        
        

        # Other Label
        self.other_label = ttk.Label(other_tab, text="I know, I'll get to it...", font=('Arial', 20, 'italic'))
        self.other_label.grid(row=0, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)


        # Author label
        self.author_label = ttk.Label(main_frame, text="Author: Walter W Glockner", font=('Bold', 5, 'bold'))
        self.author_label.grid(row=5, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)

        pass

    def create_io_controls(self, parent, channel, num_pins, column):
        frame = ttk.LabelFrame(parent, text=f"Channel {channel} Controls", padding="10")
        frame.grid(row=0, column=column, sticky='nsew', padx=5, pady=5)
        
        
        for pin in range(1, num_pins + 1):
            pin_label = ttk.Label(frame, text=f"Pin {pin}: Low", background="red", width=15)
            pin_label.grid(row=pin-1, column=0, sticky='ew')
            
            if channel in [1, 2]:  # Inputs, no buttons
                self.input_states[(channel, pin)] = pin_label
            else:  # Outputs, add buttons
                if not (channel == 3 and pin == 9):  # Add button for all but Channel 3, Pin 9
                    button = ttk.Button(frame, text="Toggle", command=lambda ch=channel, p=pin: self.toggle_output(ch, p))
                    button.grid(row=pin-1, column=1, padx=5, pady=2)
                    self.output_states[(channel, pin)] = (pin_label, button)
                else:
                    # Set Channel 3, Pin 9 to high and do not create a button
                    pin_label.config(text="Pin 9: High", background="green")
                    self.set_output(channel, pin, True)  # Send command to set pin high initially
        

    def update_input_indicator(self, channel, pin, state):
        try:
            label = self.input_states[(channel, pin)]
            label.config(text=f"Pin {pin}: {'High' if state else 'Low'}", background="green" if state else "red")
        except KeyError:
            print(f"No label defined for Channel {channel} Pin {pin}.")
        
    def toggle_output(self, channel, pin):
        # Get the current state from the label
        label, button = self.output_states[(channel, pin)]
        current_state = label.cget("text").endswith("High")
        new_state = not current_state  # Toggle state
        self.set_output(channel, pin, new_state)
        # Update the label and button text based on the new state
        label.config(text=f"Pin {pin}: {'High' if new_state else 'Low'}", background="green" if new_state else "red")
        button.config(text="Toggle Off" if new_state else "Toggle On")


    def set_output(self, channel, pin, state):
        # Command to send the new state to the PLC
        command = f"SET_OUTPUT:{channel}:{pin}:{1 if state else 0}"
        self.send_data(command + "\n")
        print(f"Command sent: {command}")

    def get_output_state(self, pin):
        return self.output_states.get(pin, False)  # Return the state, default to False if not set
        
        

        

    def attempt_connection(self):
       try:
            plc_ip = "192.168.0.1"  # Replace with the actual IP address of the PLC
            plc_port = 10000  # Replace with the actual port number of the PLC
            self.s.connect((plc_ip, plc_port))
            print("Connected to PLC")
            return True
       except (OSError, TimeoutError) as e:
            print(f"Connection to PLC failed: {e}")
            return False

    def update_connection_status(self, is_connected):
        self.connection_state = is_connected
        if is_connected:
            self.connection_status_label.config(text="Connected", background="green")
        else:
            self.connection_status_label.config(text="Not Connected", background="red")

    def request_io_update(self):
        if self.connection_state and self.s:
            # Send a command to request IO states from the PLC
            # Assuming the PLC has an existing command to send back IO states when it receives this message
            self.send_data("REQUEST_IO_UPDATE\n")
    def auto_request_io_update(self):
        while True:
            self.request_io_update()
            data = self.receive_data()
            if data:
                
                self.process_received_data(data)
                #self.root.after(0, lambda d=data: self.update_input_indicator(d))

            time.sleep(2)

    def monitor_connection(self):
        def run():
            while True:
                time.sleep(5)
                if self.connection_state:
                    # Check if the connection is still alive
                    try:
                        self.s.setblocking(0)
                        ready = select.select([self.s], [], [], 0.1)
                        if not ready[0]:
                            self.update_connection_status(False)
                    except OSError:
                        self.update_connection_status(False)
                    finally:
                        self.s.setblocking(1)
        threading.Thread(target=run, daemon=True).start()


    


    def send_variable_update(self, variable_name, value):
        # Check if the connection is established before sending data
        if self.connection_state and self.s is not None:
            message = f"{variable_name}:{value}\n"
            try:
                self.s.sendall(message.encode())
                print(f"Sent update: {message}")
            except OSError as e:
                print(f"Error sending data: {e}")
                self.update_connection_status(False)  # Update the connection status if sending fails
        else:
            print("Cannot send data. No active connection.")



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


    def update_first_layer_height_entry(self, event):
        value = self.first_layer_height_var.get()
        #send_data(s, "FLH")
        #send_data(s, value)
        #send_data(s, '\n')
        print(f"Setting first layer height to {value} mm")

    def update_line_width_entry(self, entry, variable, command_name, min_value, max_value):
        value = self.default_line_width_var.get()
        #send_data(s, "DLW")
        #send_data(s, value)
        #send_data(s, '\n')
        print(f"Setting defualt line width to {value} mm")

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

    def toggle_rumbler(self):
        self.rumbler_state = not self.rumbler_state
        action = "on" if self.rumbler_state else "off"
        self.send_variable_update("rumbler", action)
        self.rumbler_button.config(text="Stop Rumbler" if self.rumbler_state else "Start Rumbler")
        print("Rumbler toggled:", "on" if self.rumbler_state else "off")

    def toggle_disconnect(self):
         if self.connection_state:
            # If connected, send the disconnect command to the PLC and close the socket
            self.send_variable_update("command", "stop_client")
            self.disconnect_socket()
         else:
            # If disconnected, create a new socket and attempt to reconnect
            self.create_socket()
            self.connect_to_plc()

  
    #def update_io_indicators(self, data):
        


        
    def monitor_connection(self):
        # Existing monitoring connection logic...
        def run():
            while True:
                # Check the connection status periodically.
                time.sleep(5)
                if not self.connection_state:
                    # If not connected, attempt to reconnect and update the GUI.
                    if self.attempt_connection():
                        self.root.after(0, lambda: self.update_connection_status(True))
                    else:
                        self.root.after(0, lambda: self.update_connection_status(False))
                else:
                    # If already connected, verify the connection is still alive.
                    current_state = check_connection(self.s)
                    if not current_state:
                        self.root.after(0, lambda: self.update_connection_status(False))
        threading.Thread(target=run, daemon=True).start()

        # Monitor IO states in the same thread or a separate thread
        
        def monitor_io():
            
            while True:
                if self.connection_state:
                    self.update_io_indicators()
                time.sleep(1)  # Update every second or choose appropriate timing

        io_thread = threading.Thread(target=monitor_io, daemon=True)
        io_thread.start()

    def read_channel_states(self):
        while self.connection_state:
            data = self.receive_data()
            if data:
                self.root.after(0, lambda d=data: self.update_io_indicators(d))
            time.sleep(1)  # Polling interval
    

    


    


# Main program
if __name__ == "__main__":
    root = tk.Tk()

    app = Kaw2FFFControl(root)

    root.mainloop()