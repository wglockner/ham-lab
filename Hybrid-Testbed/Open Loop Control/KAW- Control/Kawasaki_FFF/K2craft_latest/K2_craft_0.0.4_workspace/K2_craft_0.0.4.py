import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pypylon import pylon
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
import selectors
import types
import threading
import time

# Initialize Server Socket
sel = selectors.DefaultSelector()
host, port = '192.168.1.1', 10000

class Kaw2FFFControl:
    def __init__(self, root):
        print("Initializing...")
        self.root = root
        self.root.title("Kaw2 FFF Control")

        # Initialize IO state dictionaries
        self.input_states = {}
        self.output_states = {}
        self.connection_state = False

        # Initialize display variable after creating the root window
        self.display_var = tk.StringVar(value="both")

        # Initialize camera variable
        self.camera = None

        # Initialize GUI elements
        self.initialize_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Bind closing event

        # Initialize camera
        print("Setting up camera...")
        self.setup_camera()

        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.setup_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def setup_server(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
        self.connection_state = True  # Set connection state to True when a connection is accepted

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
                self.process_received_data(recv_data.decode())
            else:
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
                self.connection_state = False  # Set connection state to False when connection is closed
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                try:
                    sent = sock.send(data.outb)
                    data.outb = data.outb[sent:]
                except Exception as e:
                    print(f"Error sending data to {data.addr}: {e}")
                    self.connection_state = False

    def send_data(self, message):
        if self.connection_state:
            for key in sel.get_map().values():
                if key.data is not None:
                    conn = key.fileobj
                    try:
                        conn.send(message.encode())
                        print(f"Sent data: {message} to {key.data.addr}")
                    except Exception as e:
                        print(f"Error sending data to {key.data.addr}: {e}")
                        self.connection_state = False
        else:
            print("Cannot send data. No active connection.")

    def update_io_label(self, pin, state):
        pin_label = self.channel_1_pin_labels.get(pin) or self.channel_2_pin_labels.get(pin)
        if pin_label:
            pin_label.config(text=f"Pin {pin}: {'High' if state else 'Low'}", background="green" if state else "red")

    def process_received_data(self, data):
        data_str = data.strip()
        print(f"Received data: {data_str}")
        if "channel_1_states:" in data_str:
            states = data_str.split('channel_1_states:')[1].split(',')
            for pin, state in enumerate(states, start=1):
                state = (state == '1')
                if pin <= 16:
                    self.update_input_indicator(1, pin, state)
        if "channel_2_states:" in data_str:
            states = data_str.split('channel_2_states:')[1].split(',')
            for pin, state in enumerate(states, start=1):
                state = (state == '1')
                if pin <= 16:
                    self.update_input_indicator(2, pin, state)

    def initialize_gui(self):
        # Using grid for the entire layout
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tab_control = ttk.Notebook(self.main_frame)
        self.IO_control_tab = ttk.Frame(self.tab_control)
        self.camera_tab = ttk.Frame(self.tab_control)
        self.motor_control_tab = ttk.Frame(self.tab_control)

        self.start_video_button = ttk.Button(self.camera_tab, text="Start Video Feed", command=self.start_video_feed)
        self.start_video_button.grid(row=1, column=0, pady=10, sticky=tk.W)

        self.stop_video_button = ttk.Button(self.camera_tab, text="Stop Video Feed", command=self.stop_video_feed)
        self.stop_video_button.grid(row=1, column=1, pady=10, sticky=tk.W)

        # Styling for radio buttons
        style = ttk.Style()
        style.configure('Big.TRadiobutton', font=('Helvetica', 12))

        # Adding a frame to group the radio buttons
        self.radio_button_frame = ttk.LabelFrame(self.camera_tab, text="Display Options", padding=(10, 5))
        self.radio_button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)

        ttk.Radiobutton(self.radio_button_frame, text="Lines", variable=self.display_var, value="lines", style='Big.TRadiobutton').grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Blobs", variable=self.display_var, value="blobs", style='Big.TRadiobutton').grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Colors", variable=self.display_var, value="color", style='Big.TRadiobutton').grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Edges", variable=self.display_var, value="edges", style='Big.TRadiobutton').grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Contours", variable=self.display_var, value="contours", style='Big.TRadiobutton').grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Shapes", variable=self.display_var, value="shapes", style='Big.TRadiobutton').grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(self.radio_button_frame, text="Both", variable=self.display_var, value="both", style='Big.TRadiobutton').grid(row=6, column=0, sticky=tk.W, pady=2)

        # Adding frames for Edge and Color Segmentation Parameters
        self.edge_param_frame = ttk.LabelFrame(self.camera_tab, text="Edge Detection Parameters", padding=(10, 5))
        self.edge_param_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)

        self.edge_low_threshold_label = ttk.Label(self.edge_param_frame, text="Low Threshold:")
        self.edge_low_threshold_label.grid(row=0, column=0, sticky=tk.W)
        self.edge_low_threshold_var = tk.IntVar(value=100)
        self.edge_low_threshold_scale = ttk.Scale(self.edge_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.edge_low_threshold_var)
        self.edge_low_threshold_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.edge_high_threshold_label = ttk.Label(self.edge_param_frame, text="High Threshold:")
        self.edge_high_threshold_label.grid(row=1, column=0, sticky=tk.W)
        self.edge_high_threshold_var = tk.IntVar(value=200)
        self.edge_high_threshold_scale = ttk.Scale(self.edge_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.edge_high_threshold_var)
        self.edge_high_threshold_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.color_param_frame = ttk.LabelFrame(self.camera_tab, text="Color Segmentation Parameters", padding=(10, 5))
        self.color_param_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)

        self.lower_hue_label = ttk.Label(self.color_param_frame, text="Lower Hue:")
        self.lower_hue_label.grid(row=0, column=0, sticky=tk.W)
        self.lower_hue_var = tk.IntVar(value=0)
        self.lower_hue_scale = ttk.Scale(self.color_param_frame, from_=0, to=180, orient=tk.HORIZONTAL, variable=self.lower_hue_var)
        self.lower_hue_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.upper_hue_label = ttk.Label(self.color_param_frame, text="Upper Hue:")
        self.upper_hue_label.grid(row=1, column=0, sticky=tk.W)
        self.upper_hue_var = tk.IntVar(value=180)
        self.upper_hue_scale = ttk.Scale(self.color_param_frame, from_=0, to=180, orient=tk.HORIZONTAL, variable=self.upper_hue_var)
        self.upper_hue_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.lower_saturation_label = ttk.Label(self.color_param_frame, text="Lower Saturation:")
        self.lower_saturation_label.grid(row=2, column=0, sticky=tk.W)
        self.lower_saturation_var = tk.IntVar(value=120)
        self.lower_saturation_scale = ttk.Scale(self.color_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.lower_saturation_var)
        self.lower_saturation_scale.grid(row=2, column=1, sticky=(tk.W, tk.E))

        self.upper_saturation_label = ttk.Label(self.color_param_frame, text="Upper Saturation:")
        self.upper_saturation_label.grid(row=3, column=0, sticky=tk.W)
        self.upper_saturation_var = tk.IntVar(value=255)
        self.upper_saturation_scale = ttk.Scale(self.color_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.upper_saturation_var)
        self.upper_saturation_scale.grid(row=3, column=1, sticky=(tk.W, tk.E))

        self.lower_value_label = ttk.Label(self.color_param_frame, text="Lower Value:")
        self.lower_value_label.grid(row=4, column=0, sticky=tk.W)
        self.lower_value_var = tk.IntVar(value=70)
        self.lower_value_scale = ttk.Scale(self.color_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.lower_value_var)
        self.lower_value_scale.grid(row=4, column=1, sticky=(tk.W, tk.E))

        self.upper_value_label = ttk.Label(self.color_param_frame, text="Upper Value:")
        self.upper_value_label.grid(row=5, column=0, sticky=tk.W)
        self.upper_value_var = tk.IntVar(value=255)
        self.upper_value_scale = ttk.Scale(self.color_param_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.upper_value_var)
        self.upper_value_scale.grid(row=5, column=1, sticky=(tk.W, tk.E))

        # Initialize channel labels for inputs and outputs side by side
        self.create_io_controls(self.IO_control_tab, 1, 16, 0)
        self.create_io_controls(self.IO_control_tab, 2, 16, 1)
        self.create_io_controls(self.IO_control_tab, 3, 15, 2)
        self.create_io_controls(self.IO_control_tab, 4, 15, 3)

        self.tab_control.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set up the camera display label
        self.video_label = ttk.Label(self.camera_tab)
        self.video_label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set up the matplotlib graph
        self.fig, self.ax = plt.subplots(2, 1, figsize=(5, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.camera_tab)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=7, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialize states
        self.control_state = False
        self.extrusion_state = False
        self.retraction_state = False
        self.printer_state = False
        self.printer_paused = False
        self.air_state = False
        self.automated_state = False
        self.rumbler_state = False
        self.connection_state = False
        self.print_error_once = True
        self.disconnect_state = False

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

        Extruder_tab = ttk.Frame(self.tab_control)
        quality_tab = ttk.Frame(self.tab_control)
        other_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(Extruder_tab, text ='Extruder Control')
        self.tab_control.add(self.IO_control_tab, text='IO Control')
        self.tab_control.add(self.camera_tab, text='Camera View')
        self.tab_control.add(quality_tab, text ='Quality')
        self.tab_control.add(self.motor_control_tab, text='Motor Control')
        self.tab_control.add(other_tab, text ='Other')
        self.tab_control.grid(row=10, column=0, columnspan=10, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Printer status indicator
        self.status_label = ttk.Label(Extruder_tab, text="Printer Stopped", background="red", foreground="white")
        self.status_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.setup_motor_control_ui()

        # Connection status control
        self.connection_status_label = ttk.Label(Extruder_tab, text="Not Connected", background="red", foreground="white")
        self.connection_status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Speed control frame
        speed_frame = ttk.LabelFrame(Extruder_tab, text="Speed Control", padding="10")
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
        temp_frame = ttk.LabelFrame(Extruder_tab, text="Temperature Control", padding="10")
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
        control_frame = ttk.Frame(Extruder_tab, padding="10")
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
        self.author_label.grid(row=1, column=0, columnspan=5, padx=0, pady=0, sticky=tk.E+tk.S)

        # Control Tab
        # Layer_tab
        # Layer height frame
        layer_height_frame = ttk.LabelFrame(quality_tab, text="Layer height (mm)", padding="10")
        layer_height_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        layer_height_frame.columnconfigure([0, 1, 2, 3], weight=1)

        # Layer height
        self.layer_height_var = tk.DoubleVar()

        self.layer_height_label = ttk.Label(layer_height_frame, text="Layer height: ", font=('Arial', 10))
        self.layer_height_label.grid(row=0, column=0, padx=15, pady=15, sticky=(tk.W))

        self.layer_height_entry = ttk.Entry(layer_height_frame, textvariable=self.layer_height_var, width=10)
        self.layer_height_entry.grid(row=0, column=1, padx=0, sticky=(tk.W))
        self.layer_height_entry.bind('<Return>', self.update_layer_height_entry)

        # Initial layer height
        self.first_layer_height_var = tk.DoubleVar()

        self.first_layer_height_label = ttk.Label(layer_height_frame, text="First layer height: ", font=('Arial', 10))
        self.first_layer_height_label.grid(row=1, column=0, padx=15, pady=0, sticky=(tk.E))

        self.first_layer_height_entry = ttk.Entry(layer_height_frame, textvariable=self.first_layer_height_var, width=10)
        self.first_layer_height_entry.grid(row=1, column=1, padx=0, sticky=(tk.W))
        self.first_layer_height_entry.bind('<Return>', self.update_first_layer_height_entry)

        # Line width frame
        line_width_frame = ttk.LabelFrame(quality_tab, text="Line width (mm)", padding="10")
        line_width_frame.grid(row=5, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        line_width_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)

        # Default line width
        self.default_line_width_var = tk.DoubleVar()

        self.default_line_width_label = ttk.Label(line_width_frame, text="Default: ", font=('Arial', 10))
        self.default_line_width_label.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W))

        self.default_line_width_entry = ttk.Entry(line_width_frame, textvariable=self.default_line_width_var, width=10)
        self.default_line_width_entry.grid(row=0, column=1, padx=0, sticky=(tk.E))
        self.default_line_width_entry.bind('<Return>', self.update_default_line_width_entry)

        # First layer line width
        self.first_layer_line_width_var = tk.DoubleVar()

        self.first_layer_line_width_label = ttk.Label(line_width_frame, text="First Layer: ", font=('Arial', 10))
        self.first_layer_line_width_label.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W))

        self.first_layer_line_width_entry = ttk.Entry(line_width_frame, textvariable=self.first_layer_line_width_var, width=10)
        self.first_layer_line_width_entry.grid(row=1, column=1, padx=0, sticky=(tk.E))
        self.first_layer_line_width_entry.bind('<Return>', self.update_first_layer_line_width_entry)

        # IO control tab
        Kawasaki_IO_control_frame = ttk.LabelFrame(self.IO_control_tab, text="Kawasaki IO", padding="10")
        Kawasaki_IO_control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
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

    def create_io_controls(self, parent, channel, num_pins, column):
        frame = ttk.LabelFrame(parent, text=f"Channel {channel} Controls", padding="10")
        frame.grid(row=0, column=column, sticky='nsew', padx=5, pady=5)

        for pin in range(1, num_pins + 1):
            pin_label = ttk.Label(frame, text=f"Pin {pin}: Low", background="red", width=15)
            pin_label.grid(row=pin-1, column=0, sticky='ew')

            if channel in [1, 2]:
                self.input_states[(channel, pin)] = pin_label
            else:
                if not (channel == 3 and pin == 9):
                    button = ttk.Button(frame, text="Toggle", command=lambda ch=channel, p=pin: self.toggle_output(ch, p))
                    button.grid(row=pin-1, column=1, padx=5, pady=2)
                    self.output_states[(channel, pin)] = (pin_label, button)
                else:
                    pin_label.config(text="Pin 9: High", background="green")
                    self.set_output(channel, pin, True)

    def update_input_indicator(self, channel, pin, state):
        try:
            label = self.input_states[(channel, pin)]
            label.config(text=f"Pin {pin}: {'High' if state else 'Low'}", background="green" if state else "red")
        except KeyError:
            print(f"No label defined for Channel {channel} Pin {pin}.")

    def toggle_output(self, channel, pin):
        label, button = self.output_states[(channel, pin)]
        current_state = label.cget("text").endswith("High")
        new_state = not current_state
        self.set_output(channel, pin, new_state)
        label.config(text=f"Pin {pin}: {'High' if new_state else 'Low'}", background="green" if new_state else "red")
        button.config(text="Toggle Off" if new_state else "Toggle On")

    def set_output(self, channel, pin, state):
        command = f"SET_OUTPUT:{channel}:{pin}:{1 if state else 0}"
        self.send_data(command + "\n")
        print(f"Command sent: {command}")

    def get_output_state(self, pin):
        return self.output_states.get(pin, False)

    def update_connection_status(self, is_connected):
        self.connection_state = is_connected
        if is_connected:
            self.connection_status_label.config(text="Connected", background="green")
        else:
            self.connection_status_label.config(text="Not Connected", background="red")

    def request_io_update(self):
        if self.connection_state:
            self.send_data("REQUEST_IO_UPDATE")

    def auto_request_io_update(self):
        while not self.stop_threads:
            if self.root.winfo_exists():
                self.request_io_update()
            time.sleep(0.5)

    def monitor_connection(self):
        def run():
            while True:
                time.sleep(1)
                if self.connection_state:
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
        if self.connection_state:
            message = f"{variable_name}:{value}\n"
            self.send_data(message)
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
        print(f"Setting speed to {value} RPM\n")

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
        print(f"Setting first layer height to {value} mm")

    def update_line_width_entry(self, entry, variable, command_name, min_value, max_value):
        value = self.default_line_width_var.get()
        print(f"Setting default line width to {value} mm")

    def update_default_line_width_entry(self, event):
        value = self.default_line_width_var.get()
        print(f"Setting default line width to {value} mm")

    def update_first_layer_line_width_entry(self, event):
        value = self.first_layer_line_width_var.get()
        print(f"Setting first layer line width to {value} mm")

    def toggle_extrusion(self):
        if not self.retraction_state:
            self.extrusion_state = not self.extrusion_state
            self.send_variable_update("command", "extrude\n" if self.extrusion_state else "stop_print\n")
            self.extrusion_button.config(text="Stop Extrusion" if self.extrusion_state else "Start Extrusion")
            print("Extrusion started" if self.extrusion_state else "Extrusion stopped")

    def toggle_retraction(self):
        if not self.extrusion_state:
            self.retraction_state = not self.retraction_state
            self.send_variable_update("command", "retract\n" if self.retraction_state else "stop_retract\n")
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
            self.send_variable_update("command", "stop_print\n")
            self.status_label.config(text="Printer Stopped", background="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
            print("Printer stopped")

    def pause_printer(self):
        self.printer_paused = not self.printer_paused
        command = "pause_print" if self.printer_paused else "resume_print"
        self.send_variable_update("command", command)
        self.pause_button.config(text="Resume" if self.printer_paused else "Pause")
        self.status_label.config(text="Printer Paused", background="yellow" if self.printer_paused else "green")
        print("Printer paused" if self.printer_paused else "Printing resumed")

    def toggle_air(self):
        self.air_state = not self.air_state
        action = "on\n" if self.air_state else "off\n"
        self.send_variable_update("air", action)
        self.air_button.config(text="Stop Air" if self.air_state else "Start Air")
        print("Air toggled:", "on" if self.air_state else "off")

    def toggle_automated(self):
        self.automated_state = not self.automated_state
        action = "on\n" if self.automated_state else "off\n"
        self.send_variable_update("automated", action)
        self.automated_button.config(text="Stop Automated" if self.automated_state else "Start automated")
        print("Automated toggled:", "on" if self.automated_state else "off")

    def toggle_rumbler(self):
        self.rumbler_state = not self.rumbler_state
        action = "on\n" if self.rumbler_state else "off\n"
        self.send_variable_update("rumbler", action)
        self.rumbler_button.config(text="Stop Rumbler" if self.rumbler_state else "Start Rumbler")
        print("Rumbler toggled:", "on" if self.rumbler_state else "off")

    def toggle_disconnect(self):
        if self.connection_state:
            self.send_variable_update("command", "stop_client")
            self.disconnect_socket()
        else:
            self.create_socket()
            self.connect_to_plc()

    def read_channel_states(self):
        while self.connection_state:
            data = self.receive_data()
            if data:
                self.root.after(0, lambda d=data: self.update_io_indicators(d))
            time.sleep(0.25)

    def start_video_feed(self):
        if self.camera and not self.camera.IsGrabbing():
            try:
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImages)
                self.update_camera_feed()
                print("Video feed started.")
            except Exception as e:
                print(f"Failed to start video feed: {e}")

    def stop_video_feed(self):
        if self.camera and self.camera.IsGrabbing():
            self.camera.StopGrabbing()
            print("Video feed stopped.")

    def setup_camera(self):
        self.release_camera()
        self.line_counts = []
        self.blob_counts = []
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.blob_detector = self.setup_blob_detector()
        self.update_camera_feed()

    def release_camera(self):
        if self.camera is not None:
            if (self.camera.IsGrabbing()):
                self.camera.StopGrabbing()
            self.camera.Close()
            self.camera = None

    def setup_blob_detector(self):
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 150
        params.filterByCircularity = True
        params.minCircularity = 0.1
        params.filterByConvexity = True
        params.minConvexity = 0.5
        params.filterByInertia = True
        params.minInertiaRatio = 0.01
        return cv2.SimpleBlobDetector_create(params)

    def update_camera_feed(self):
        if self.camera and self.camera.IsGrabbing() and self.root.winfo_exists():
            try:
                grabResult = self.camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    image = self.converter.Convert(grabResult).GetArray()
                    self.process_image(image)
                grabResult.Release()
                if self.root.winfo_exists():
                    self.root.after(10, self.update_camera_feed)
            except Exception as e:
                print(f"Error during camera feed update: {e}")
        else:
            print("Camera not grabbing or window closed, stopping updates.")

    def process_image(self, image):
        display_image = image
        if self.display_var.get() == "lines":
            display_image, _ = self.detect_lines(image)
        elif self.display_var.get() == "blobs":
            display_image, _ = self.detect_blobs(image)
        elif self.display_var.get() == "color":
            display_image = self.color_segmentation(image)
        elif self.display_var.get() == "edges":
            display_image = self.edge_detection(image)
        elif self.display_var.get() == "contours":
            display_image = self.contour_detection(image)
        elif self.display_var.get() == "shapes":
            display_image = self.shape_detection(image)
        else:
            line_image, line_count = self.detect_lines(image)
            blob_image, blob_count = self.detect_blobs(image)
            display_image = cv2.addWeighted(line_image, 0.5, blob_image, 0.5, 0)
            self.line_counts.append(line_count)
            self.blob_counts.append(blob_count)

        display_image = self.resize_image(display_image, 770, 400)
        self.update_image(self.video_label, display_image)
        self.update_graphs()

    def update_image(self, label, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        label.config(image=image)
        label.image = image

    def update_graphs(self):
        self.ax[0].clear()
        self.ax[0].plot(self.line_counts, 'r-')
        self.ax[0].set_title('Line Detection Count')
        self.ax[1].clear()
        self.ax[1].plot(self.blob_counts, 'b-')
        self.ax[1].set_title('Blob Detection Count')
        self.canvas.draw()
        self.canvas.flush_events()

    def detect_lines(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred_gray, self.edge_low_threshold_var.get(), self.edge_high_threshold_var.get(), apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=20)
        line_image = image.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return line_image, len(lines) if lines is not None else 0

    def detect_blobs(self, image):
        keypoints = self.blob_detector.detect(image)
        blob_image = cv2.drawKeypoints(image, keypoints, None, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return blob_image, len(keypoints)

    def color_segmentation(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([self.lower_hue_var.get(), self.lower_saturation_var.get(), self.lower_value_var.get()])
        upper_bound = np.array([self.upper_hue_var.get(), self.upper_saturation_var.get(), self.upper_value_var.get()])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        segmented_image = cv2.bitwise_and(image, image, mask=mask)
        return segmented_image

    def edge_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.edge_low_threshold_var.get(), self.edge_high_threshold_var.get())
        edge_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edge_image

    def contour_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = image.copy()
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        return contour_image

    def shape_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shape_image = image.copy()
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
            if len(approx) == 3:
                shape = "Triangle"
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                shape = "Square" if 0.95 <= ar <= 1.05 else "Rectangle"
            elif len(approx) == 5:
                shape = "Pentagon"
            else:
                shape = "Circle"
            cv2.drawContours(shape_image, [approx], -1, (0, 255, 0), 2)
            x, y = approx[0][0]
            cv2.putText(shape_image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        return shape_image

    def resize_image(self, image, width, height):
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    def update_image_display(self, image):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = ImageTk.PhotoImage(image)
        self.video_label.config(image=image)
        self.video_label.image = image

    def setup_motor_control_ui(self):
        motor_frame = ttk.LabelFrame(self.motor_control_tab, text="Motor Commands", padding="10")
        motor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(motor_frame, text="Start Motor", command=self.start_motor).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(motor_frame, text="Stop Motor", command=self.stop_motor).grid(row=0, column=1, padx=5, pady=5)

        self.motor_speed_var = tk.DoubleVar(value=0)
        ttk.Label(motor_frame, text="Speed:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(motor_frame, from_=0, to=100, variable=self.motor_speed_var, orient="horizontal", command=self.update_motor_speed).grid(row=1, column=1, sticky="ew")

    def start_motor(self):
        print("This button has not yet been implemented.")

    def stop_motor(self):
        print("Stopping motor...")
        print("This button has not yet been implemented.")

    def update_motor_speed(self, event):
        speed = self.motor_speed_var.get()
        print(f"Setting motor speed to {speed}")

    def on_closing(self):
        print("Shutting down server...")
        self.is_running = False
        sel.close()
        self.root.destroy()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = Kaw2FFFControl(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
