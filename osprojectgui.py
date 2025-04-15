import tkinter as tk   
# Tkinter is Python's standard GUI (Graphical User Interface) package. 
# It's a thin object-oriented layer on top of Tcl/Tk that makes it easy to create desktop applications with Python.
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
# JSON (JavaScript Object Notation)
# JSON is a lightweight data interchange format that's easy for humans to read and write, and easy for machines to parse and generate.
import json
from scheduler import Process, CPU, round_robin_scheduling
from matplotlib.ticker import MaxNLocator

class EnergyEfficientSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduler")
        self.root.geometry("1400x900")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        self.setup_layout()
        
        # Initialize empty process list
        self.processes = []
        
    def configure_styles(self):
        """Configure custom styles for the GUI with modern aesthetics"""
        # Updated modern color scheme
        self.colors = {
            'primary': '#1a237e',    # Deep Blue
            'secondary': '#0d47a1',  # Rich Blue
            'accent': '#2962ff',     # Bright Blue
            'background': '#f5f6fa', # Light Gray-Blue
            'surface': '#ffffff',    # White
            'text': '#2c3e50',      # Dark Gray
            'success': '#00c853',    # Green
            'warning': '#ffd600',    # Yellow
            'error': '#d50000',     # Red
            'idle': '#ffecb3'       # Light Yellow
        }

        # Configure main styles with shadows and rounded corners
        self.style.configure('Custom.TFrame',
            background=self.colors['background'],
            relief='solid',
            borderwidth=1,
            bordercolor=self.colors['primary']
        )

        # Modern label style
        self.style.configure('Custom.TLabel',
            background=self.colors['background'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10),
            padding=5
        )

        # Enhanced button style
        self.style.configure('Custom.TButton',
            font=('Segoe UI Semibold', 10),
            padding=(15, 8),
            background=self.colors['accent'],
            foreground='white',
            borderwidth=0,
            relief='flat'
        )

        # Button hover effects
        self.style.map('Custom.TButton',
            background=[('active', self.colors['primary']), 
                       ('disabled', '#bdc3c7')],
            foreground=[('active', 'white'), 
                       ('disabled', '#95a5a6')]
        )

        # Modern header style
        self.style.configure('Header.TLabel',
            font=('Segoe UI', 14, 'bold'),
            foreground=self.colors['primary'],
            background=self.colors['background'],
            padding=10
        )

        # Enhanced Treeview style
        self.style.configure('Custom.Treeview',
            background=self.colors['surface'],
            fieldbackground=self.colors['surface'],
            foreground=self.colors['text'],
            rowheight=35,
            font=('Segoe UI', 10),
            borderwidth=0
        )
        
        self.style.configure('Custom.Treeview.Heading',
            font=('Segoe UI Semibold', 10),
            background=self.colors['primary'],
            foreground='white',
            padding=5
        )

        # Tab styling
        self.style.configure('Custom.TNotebook',
            background=self.colors['background'],
            tabmargins=[5, 5, 2, 0]
        )

        self.style.configure('Custom.TNotebook.Tab',
            font=('Segoe UI', 10),
            padding=[20, 8],
            background=self.colors['surface'],
            foreground=self.colors['text']
        )
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frames
        self.left_frame = ttk.Frame(self.root, padding=10)
        self.right_frame = ttk.Frame(self.root, padding=10)
        
        # Process input section
        self.input_frame = ttk.LabelFrame(self.left_frame, text="Process Input", padding=10)
        self.create_process_input_widgets()
        
        # Simulation controls
        self.control_frame = ttk.LabelFrame(self.left_frame, text="Simulation Controls", padding=10)
        self.create_control_widgets()
        
        # Results display
        self.result_frame = ttk.LabelFrame(self.right_frame, text="Results", padding=10)
        self.create_result_widgets()
        
        # Visualization frames
        self.visualization_frame = ttk.LabelFrame(self.right_frame, text="Visualizations", padding=10)
        self.create_visualization_widgets()
        


    
    def create_process_input_widgets(self):
        """Create widgets for process input"""
        # Process table
        columns = ("PID", "Arrival Time", "Burst Time", "Priority")
        self.process_table = ttk.Treeview(
            self.input_frame, 
            columns=columns, 
            show="headings", 
            height=8,
            selectmode='browse'
        )
        
        # Configure columns
        col_widths = [50, 90, 80, 70]
        for col, width in zip(columns, col_widths):
            self.process_table.heading(col, text=col)
            self.process_table.column(col, width=width, anchor=tk.CENTER)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(self.input_frame, orient=tk.VERTICAL, command=self.process_table.yview)
        self.process_table.configure(yscrollcommand=scrollbar.set)
        
        # Process entry fields
        self.pid_var = tk.IntVar()
        self.arrival_var = tk.IntVar()
        self.burst_var = tk.IntVar()
        self.priority_var = tk.IntVar(value=1)
        
        ttk.Label(self.input_frame, text="PID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.pid_var, width=8).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Arrival Time:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.arrival_var, width=8).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Burst Time:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.burst_var, width=8).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Priority:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        ttk.Entry(self.input_frame, textvariable=self.priority_var, width=8).grid(row=2, column=3, padx=5, pady=5)
        
        # Buttons for process management
        button_frame = ttk.Frame(self.input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add Process", command=self.add_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_processes).pack(side=tk.LEFT, padx=5)
        
        # Import/export buttons
        io_frame = ttk.Frame(self.input_frame)
        io_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        ttk.Button(io_frame, text="Import Processes", command=self.import_processes).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="Export Processes", command=self.export_processes).pack(side=tk.LEFT, padx=5)
        
        # Layout the table and scrollbar
        self.process_table.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        scrollbar.grid(row=0, column=4, sticky='ns')
    
    def add_process(self):
        """Add a new process to the table"""
        try:
            pid = self.pid_var.get()
            arrival = self.arrival_var.get()
            burst = self.burst_var.get()
            priority = self.priority_var.get()
            
            if pid <= 0 or arrival < 0 or burst <= 0 or priority <= 0:
                raise ValueError("All values must be positive integers")
            
            # Check for duplicate PID
            for item in self.process_table.get_children():
                if self.process_table.item(item)['values'][0] == pid:
                    raise ValueError(f"Process with PID {pid} already exists")
            
            self.process_table.insert("", "end", values=(pid, arrival, burst, priority))
            
            # Clear entry fields
            self.pid_var.set("")
            self.arrival_var.set("")
            self.burst_var.set("")
            
            # Auto-increment PID
            self.pid_var.set(pid + 1)
            


        
        except Exception as e:
            messagebox.showerror("Error", str(e))


    
    def remove_process(self):
        """Remove selected process from the table"""
        try:
            selected_item = self.process_table.selection()
            if not selected_item:
                raise ValueError("No process selected")
            
            pid = self.process_table.item(selected_item)['values'][0]
            self.process_table.delete(selected_item)


        
        except Exception as e:
            messagebox.showerror("Error", str(e))


    
    def clear_processes(self):
        """Clear all processes from the table"""
        for item in self.process_table.get_children():
            self.process_table.delete(item)


    
    def import_processes(self):
        """Import processes from a JSON file"""
        try:
            filepath = filedialog.askopenfilename(
                title="Import Processes",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
            
            if not filepath:
                return
                
            with open(filepath, 'r') as f:
                processes = json.load(f)
            
            self.clear_processes()
            for proc in processes:
                self.process_table.insert("", "end", values=(
                    proc['pid'], proc['arrival'], proc['burst'], proc['priority']
                ))
            


        
        except Exception as e:
            messagebox.showerror("Import Error", str(e))


    
    def export_processes(self):
        """Export processes to a JSON file"""
        try:
            processes = []
            for item in self.process_table.get_children():
                pid, arrival, burst, priority = self.process_table.item(item)['values']
                processes.append({
                    'pid': pid,
                    'arrival': arrival,
                    'burst': burst,
                    'priority': priority
                })
            
            if not processes:
                raise ValueError("No processes to export")
                
            filepath = filedialog.asksaveasfilename(
                title="Export Processes",
                defaultextension=".json",
                filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
            
            if not filepath:
                return
                
            with open(filepath, 'w') as f:
                json.dump(processes, f, indent=2)
            


        
        except Exception as e:
            messagebox.showerror("Export Error", str(e))



    def create_control_widgets(self):
        """Create widgets for simulation controls"""
        # Time quantum input
        ttk.Label(self.control_frame, text="Time Quantum:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.quantum_var = tk.IntVar(value=3)
        ttk.Entry(self.control_frame, textvariable=self.quantum_var, width=8).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # CPU parameters
        ttk.Label(self.control_frame, text="CPU Parameters", style='Header.TLabel').grid(row=1, column=0, columnspan=2, pady=10)
        
        """CPU Base Power refers to the minimum guaranteed power consumption (in watts) that a CPU is designed to use under typical workloads 
        when operating at its base clock speed. It is also sometimes called TDP (Thermal Design Power) or PL1 (Power Level 1) in Intel processors."""
        # Create CPU parameter variables
        self.base_power_var = tk.DoubleVar(value=125)   #Intel Core i9-13900K: 125W TDP
        self.max_freq_var = tk.DoubleVar(value=5.8)   # Intel Core i9-13900K: 5.8 GHz max turbo frequency
        self.min_freq_var = tk.DoubleVar(value=3.0)  # Intel Core i9-13900K: 3.0 GHz base frequency
        
        param_labels = ["Base Power (W):", "Max Freq (GHz):", "Min Freq (GHz):"]
        param_vars = [self.base_power_var, self.max_freq_var, self.min_freq_var]
        
        for i, (label, var) in enumerate(zip(param_labels, param_vars)):
            ttk.Label(self.control_frame, text=label).grid(row=i+2, column=0, padx=5, pady=2, sticky='e')
            ttk.Entry(self.control_frame, textvariable=var, width=8).grid(row=i+2, column=1, padx=5, pady=2, sticky='w')
        
        # Run button
        ttk.Button(self.control_frame, text="Run Simulation", command=self.run_simulation).grid(
            row=5, column=0, columnspan=2, pady=15, ipadx=20, ipady=5
        )
    
    def create_result_widgets(self):
        """Create widgets for results display"""
        # Result table
        columns = ("PID", "Start Time", "Finish Time", "Turnaround", "Waiting")
        self.result_table = ttk.Treeview(
            self.result_frame, 
            columns=columns, 
            show="headings", 
            height=8,
            selectmode='browse'
        )
        
        # Configure columns
        col_widths = [50, 80, 80, 80, 80]
        for col, width in zip(columns, col_widths):
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=width, anchor=tk.CENTER)
        
        # Scrollbar for result table
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscrollcommand=scrollbar.set)
        
        # Metrics display
        self.metrics_frame = ttk.Frame(self.result_frame)
        
        self.avg_turnaround_var = tk.StringVar(value="Average Turnaround Time: -")
        self.avg_waiting_var = tk.StringVar(value="Average Waiting Time: -")
        self.power_consumption_var = tk.StringVar(value="Total Power Consumption: - Joules")
        self.idle_time_var = tk.StringVar(value="CPU Idle Time: - units")
        self.energy_saving_var = tk.StringVar(value="Estimated Energy Savings: - %")
        
        metrics = [
            self.avg_turnaround_var, 
            self.avg_waiting_var,
            self.power_consumption_var,
            self.idle_time_var,
            self.energy_saving_var
        ]
        
        for metric in metrics:
            label = ttk.Label(self.metrics_frame, textvariable=metric, font=('Segoe UI', 9))
            label.pack(anchor=tk.W, pady=2)
        
        # Layout the widgets
        self.result_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.metrics_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)
    
    def create_visualization_widgets(self):
        """Create widgets for visualizations"""
        # Notebook for multiple tabs
        self.visualization_notebook = ttk.Notebook(self.visualization_frame)
        
        # Create tabs
        self.create_power_consumption_tab()
        self.create_gantt_chart_tab()
        self.create_frequency_usage_tab()
        
        # Pack the notebook
        self.visualization_notebook.pack(fill=tk.BOTH, expand=True)
    
    def create_power_consumption_tab(self):
        """Create power consumption visualization tab"""
        self.power_tab = ttk.Frame(self.visualization_notebook)
        self.power_fig, self.power_ax = plt.subplots(figsize=(10, 4), dpi=100)
        self.power_fig.patch.set_facecolor('#f5f5f5')
        
        # Configure plot
        self.power_ax.set_facecolor('#f5f5f5')
        self.power_ax.grid(True, linestyle='--', alpha=0.6)
        self.power_ax.set_xlabel("Time (units)", fontsize=10)
        self.power_ax.set_ylabel("Power (Watts)", fontsize=10)
        self.power_ax.set_title("CPU Power Consumption Over Time", fontsize=12, pad=10)
        
        # Create canvas and toolbar
        self.power_canvas = FigureCanvasTkAgg(self.power_fig, master=self.power_tab)
        self.power_toolbar = NavigationToolbar2Tk(self.power_canvas, self.power_tab)
        self.power_toolbar.update()
        
        # Layout
        self.power_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.visualization_notebook.add(self.power_tab, text="Power Consumption")
    
    def create_gantt_chart_tab(self):
        """Create Gantt chart visualization tab"""
        self.gantt_tab = ttk.Frame(self.visualization_notebook)
        self.gantt_fig, self.gantt_ax = plt.subplots(figsize=(10, 4), dpi=100)
        self.gantt_fig.patch.set_facecolor('#f5f5f5')
        
        # Configure plot
        self.gantt_ax.set_facecolor('#f5f5f5')
        self.gantt_ax.grid(True, axis='x', linestyle='--', alpha=0.6)
        self.gantt_ax.set_xlabel("Time (units)", fontsize=10)
        self.gantt_ax.set_ylabel("Processes", fontsize=10)
        self.gantt_ax.set_title("Process Execution Gantt Chart", fontsize=12, pad=10)
        
        # Create canvas and toolbar
        self.gantt_canvas = FigureCanvasTkAgg(self.gantt_fig, master=self.gantt_tab)
        self.gantt_toolbar = NavigationToolbar2Tk(self.gantt_canvas, self.gantt_tab)
        self.gantt_toolbar.update()
        
        # Layout
        self.gantt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.visualization_notebook.add(self.gantt_tab, text="Gantt Chart")
    
    def create_frequency_usage_tab(self):
        """Create CPU frequency usage visualization tab"""
        self.freq_tab = ttk.Frame(self.visualization_notebook)
        self.freq_fig, self.freq_ax = plt.subplots(figsize=(10, 4), dpi=100)
        self.freq_fig.patch.set_facecolor('#f5f5f5')
        
        # Configure plot
        self.freq_ax.set_facecolor('#f5f5f5')
        self.freq_ax.grid(True, linestyle='--', alpha=0.6)
        self.freq_ax.set_xlabel("Time (units)", fontsize=10)
        self.freq_ax.set_ylabel("Frequency (GHz)", fontsize=10)
        self.freq_ax.set_title("CPU Frequency Usage Over Time", fontsize=12, pad=10)
        
        # Create canvas and toolbar
        self.freq_canvas = FigureCanvasTkAgg(self.freq_fig, master=self.freq_tab)
        self.freq_toolbar = NavigationToolbar2Tk(self.freq_canvas, self.freq_tab)
        self.freq_toolbar.update()
        
        # Layout
        self.freq_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.visualization_notebook.add(self.freq_tab, text="Frequency Usage")
    
    def setup_layout(self):
        """Arrange widgets with proper spacing"""
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Add padding around main frames
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')
        
        # Left frame contents with spacing
        self.input_frame.pack(fill=tk.BOTH, padx=5, pady=10, expand=False)
        self.control_frame.pack(fill=tk.BOTH, padx=5, pady=10, expand=False)
        
        # Right frame contents with spacing
        self.result_frame.pack(fill=tk.BOTH, padx=5, pady=10, expand=False)
        self.visualization_frame.pack(fill=tk.BOTH, padx=5, pady=10, expand=True)
        


    
    def run_simulation(self):
        """Run the scheduling simulation"""
        try:
            # Get process details from the table
            processes = []
            for row in self.process_table.get_children():
                values = self.process_table.item(row)["values"]
                pid, arrival_time, burst_time, priority = map(int, values)
                processes.append(Process(pid, arrival_time, burst_time, priority))
            
            if not processes:
                raise ValueError("No processes to schedule")
            
            # Get simulation parameters
            time_quantum = self.quantum_var.get()
            base_power = self.base_power_var.get()
            max_freq = self.max_freq_var.get()
            min_freq = self.min_freq_var.get()
            
            if time_quantum <= 0 or base_power <= 0 or max_freq <= 0 or min_freq <= 0:
                raise ValueError("All parameters must be positive numbers")
            
            # Create CPU instance and run simulation
            cpu = CPU(base_power=base_power, max_frequency=max_freq, min_frequency=min_freq)
            completed_processes = round_robin_scheduling(processes.copy(), time_quantum, cpu)
            
            # Clear previous results
            for row in self.result_table.get_children():
                self.result_table.delete(row)
            
            # Display results
            for process in completed_processes:
                turnaround_time = process.finish_time - process.arrival_time
                waiting_time = turnaround_time - process.burst_time
                self.result_table.insert("", "end", values=(
                    process.pid, 
                    process.start_time, 
                    process.finish_time,
                    turnaround_time, 
                    waiting_time
                ))
            
            # Calculate and display metrics
            total_turnaround = sum(p.finish_time - p.arrival_time for p in completed_processes)
            total_waiting = sum((p.finish_time - p.arrival_time - p.burst_time) for p in completed_processes)
            
            self.avg_turnaround_var.set(f"Average Turnaround Time: {total_turnaround/len(completed_processes):.2f} units")
            self.avg_waiting_var.set(f"Average Waiting Time: {total_waiting/len(completed_processes):.2f} units")
            self.power_consumption_var.set(f"Total Power Consumption: {cpu.power_consumption:.2f} Joules")
            self.idle_time_var.set(f"CPU Idle Time: {cpu.idle_time} units")
            
            # Calculate energy savings
            baseline_power = base_power * sum(p.burst_time for p in processes)
            energy_saving = ((baseline_power - cpu.power_consumption) / baseline_power) * 100
            self.energy_saving_var.set(f"Estimated Energy Savings: {energy_saving:.1f}%")
            
            # Update visualizations
            self.update_visualizations(completed_processes, cpu)
            


        
        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))



    def update_visualizations(self, completed_processes, cpu):
        """Update all visualization tabs with simulation results"""
        if not completed_processes:
            return
            
        max_time = max(p.finish_time for p in completed_processes)
        time_points = np.arange(0, max_time + 1)
        
        # Update power consumption plot
        self.update_power_plot(cpu)
        
        # Update Gantt chart
        self.update_gantt_chart(completed_processes)
        
        # Update frequency usage plot
        self.update_frequency_plot(cpu)
    
    def update_power_plot(self, cpu):
        """Update the power consumption plot with enhanced styling"""
        self.power_ax.clear()
        
        if not cpu.power_history:
            return
        
        times, powers = zip(*cpu.power_history)
        
        # Plot with gradient fill
        self.power_ax.fill_between(
            times, 
            powers,
            alpha=0.3,
            color=self.colors['secondary']
        )
        
        self.power_ax.plot(
            times,
            powers,
            color=self.colors['secondary'],
            linewidth=2,
            label="Power Consumption"
        )
        
        # Style the plot
        self.power_ax.set_facecolor('white')
        self.power_ax.grid(True, linestyle='--', alpha=0.2, color='gray')
        self.power_ax.set_xlabel("Time (units)", fontsize=10, color=self.colors['text'])
        self.power_ax.set_ylabel("Power (Watts)", fontsize=10, color=self.colors['text'])
        self.power_ax.set_title(
            "CPU Power Consumption Over Time",
            fontsize=12,
            color=self.colors['primary'],
            pad=15,
            fontweight='bold'
        )
        
        # Style the spines
        for spine in self.power_ax.spines.values():
            spine.set_color(self.colors['text'])
            spine.set_linewidth(0.5)
        
        self.power_fig.patch.set_facecolor(self.colors['background'])
        self.power_canvas.draw()
    
    def update_gantt_chart(self, completed_processes):
        """Update the Gantt chart with process execution timeline"""
        self.gantt_ax.clear()
        
        # Prepare data
        pids = [f"P{p.pid}" for p in completed_processes]
        pids.append("CPU")  # Add a row for CPU utilization
        
        # Create color map based on priority
        colors = ['#2ecc71' if p.priority == 1 else '#f39c12' for p in completed_processes]
        
        # Plot each process's execution intervals
        for i, process in enumerate(completed_processes):
            for start, end in process.execution_history:
                self.gantt_ax.barh(
                    pids[i], 
                    end - start, 
                    left=start, 
                    color=colors[i],
                    edgecolor='#34495e',
                    height=0.6,
                    alpha=0.8
                )


        
        # Find and plot idle intervals
        if completed_processes:
            max_time = max(end for p in completed_processes for _, end in p.execution_history)
            busy_intervals = sorted([(start, end) for p in completed_processes for start, end in p.execution_history])
            current_time = 0
            
            # Plot idle intervals
            for start, end in busy_intervals:
                if start > current_time:
                    # There's an idle interval
                    self.gantt_ax.barh(
                        "CPU",
                        start - current_time,
                        left=current_time,
                        color='#e74c3c',  # Red for idle time
                        edgecolor='#34495e',
                        height=0.6,
                        alpha=0.4,
                        hatch='//'
                    )
                current_time = max(current_time, end)
            
            # Check for idle time after last process
            if current_time < max_time:
                self.gantt_ax.barh(
                    "CPU",
                    max_time - current_time,
                    left=current_time,
                    color='#e74c3c',  # Red for idle time
                    edgecolor='#34495e',
                    height=0.6,
                    alpha=0.4,
                    hatch='//'
                )
        
        # Configure plot
        self.gantt_ax.set_facecolor('#f5f5f5')
        self.gantt_ax.grid(True, axis='x', linestyle='--', alpha=0.6)
        self.gantt_ax.set_xlabel("Time (units)", fontsize=10)
        self.gantt_ax.set_ylabel("Processes", fontsize=10)
        self.gantt_ax.set_title("Process Execution Gantt Chart", fontsize=12, pad=10)
        self.gantt_ax.invert_yaxis()
        self.gantt_ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Adjust plot margins and layout
        if completed_processes:
            max_time = max(end for p in completed_processes for _, end in p.execution_history)
            self.gantt_ax.set_xlim(-0.5, max_time + 0.5)  # Set x-axis limits with small padding
        self.gantt_fig.tight_layout()  # Adjust layout to remove extra space
        
        # Create legend
        high_priority = plt.Rectangle((0,0), 1, 1, fc='#2ecc71', alpha=0.8)
        low_priority = plt.Rectangle((0,0), 1, 1, fc='#f39c12', alpha=0.8)
        cpu_idle = plt.Rectangle((0,0), 1, 1, fc='#e74c3c', alpha=0.4, hatch='//')
        
        self.gantt_ax.legend(
            [high_priority, low_priority, cpu_idle], 
            ['High Priority', 'Low Priority', 'CPU Idle'],
            loc='upper right'
        )
        
        # Redraw canvas
        self.gantt_canvas.draw()
    
    def update_frequency_plot(self, cpu):
        """Update the CPU frequency usage plot"""
        self.freq_ax.clear()
        
        if not cpu.frequency_history:
            return
            
        # Extract frequency history data
        times, freqs = zip(*cpu.frequency_history)
        
        # Plot frequency usage
        self.freq_ax.step(
            times, 
            freqs, 
            where='post',
            label="CPU Frequency",
            color='#9b59b6',
            linewidth=2
        )
        
        # Configure plot
        self.freq_ax.set_facecolor('#f5f5f5')
        self.freq_ax.grid(True, linestyle='--', alpha=0.6)
        self.freq_ax.set_xlabel("Time (units)", fontsize=10)
        self.freq_ax.set_ylabel("Frequency (GHz)", fontsize=10)
        self.freq_ax.set_title("CPU Frequency Usage Over Time", fontsize=12, pad=10)
        self.freq_ax.legend(loc='upper right')
        self.freq_ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.freq_ax.set_ylim(0, cpu.max_frequency * 1.1)
        
        # Redraw canvas
        self.freq_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyEfficientSchedulerGUI(root)
    root.mainloop()
    
