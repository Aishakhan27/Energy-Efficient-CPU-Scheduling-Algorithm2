# The code is divided into three modules: Algorithm Design, Simulation Environment, and Performance Analysis. 
# The implementation uses pyhton for the scheduling algorithm and Python for simulation and visualization.



# Module 1: Algorithm Design and Implementation (Python)
# This module implements the Energy-Efficient Round Robin (EE-RR) algorithm with Dynamic Frequency Scaling (DVFS) and Idle State Optimization.


# scheduler.py
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        """
        Initialize a process with:
        - pid: Process ID
        - arrival_time: Time when process arrives in the system
        - burst_time: Total CPU time required by the process
        - priority: Process priority (lower value = higher priority)
        """
        self.pid = pid       
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # Tracks remaining execution time
        self.priority = priority
        self.start_time = None  # Will be set when process starts executing
        self.finish_time = None  # Will be set when process completes
        self.execution_history = []  # Tracks execution intervals

    def __str__(self):
        return f"Process {self.pid}: Arrival={self.arrival_time}, Burst={self.burst_time}, Priority={self.priority}"

    def add_execution_interval(self, start, end):
        """Record an execution interval for this process"""
        self.execution_history.append((start, end))


class CPU:
    def __init__(self, base_power, max_frequency, min_frequency):
        """
        Initialize CPU with:
        - base_power: Base power consumption in Watts at max frequency
        - max_frequency: Maximum CPU frequency in GHz
        - min_frequency: Minimum CPU frequency in GHz
        """
        self.base_power = base_power
        self.max_frequency = max_frequency
        self.min_frequency = min_frequency
        self.current_frequency = max_frequency  # Start at max frequency
        self.power_consumption = 0  # Total power consumed in Joules
        self.idle_time = 0  # Total time spent idle
        self.frequency_history = []  # Tracks frequency changes over time
        self.power_history = []  # Tracks power consumption over time

    def execute(self, process, time_quantum, current_time):
        """
        Execute a process for a given time quantum and update power consumption
        Returns the actual execution time (may be less than quantum if process finishes)
        """
        execution_time = min(time_quantum, process.remaining_time)
        process.remaining_time -= execution_time

        # Record execution interval
        process.add_execution_interval(current_time, current_time + execution_time)

        # Adjust frequency based on priority (DVFS)
        new_frequency = self.min_frequency if process.priority > 1 else self.max_frequency
        if new_frequency != self.current_frequency:
            self.current_frequency = new_frequency
            self.frequency_history.append((current_time, self.current_frequency))

        # Calculate power consumption (simplified model: Power = Base Power * Frequency Ratio)
        power = self.base_power * (self.current_frequency / self.max_frequency)
        energy_consumed = power * execution_time
        self.power_consumption += energy_consumed
        self.power_history.append((current_time, power))

        return execution_time

    def idle(self, time, current_time):
        """Simulate CPU idle state (low power mode)"""
        self.idle_time += time
        idle_power = 0.1 * self.base_power  # 10% of base power during idle
        self.power_consumption += idle_power * time
        self.current_frequency = 0  # No frequency during idle
        self.frequency_history.append((current_time, 0))
        self.power_history.append((current_time, idle_power))


def round_robin_scheduling(processes, time_quantum, cpu):
    """
    Simulates Round Robin scheduling with energy efficiency features
    Returns list of completed processes and the CPU object with consumption data
    """
    current_time = 0
    ready_queue = []  # Processes ready to execute
    completed_processes = []  # Finished processes
    processes = sorted(processes, key=lambda p: p.arrival_time)  # Sort by arrival time
    
    while processes or ready_queue:
        # Add arrived processes to ready queue
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))
        
        if not ready_queue:
            # No processes ready - CPU idle
            cpu.idle(1, current_time)
            current_time += 1
            continue
        
        # Get next process from ready queue
        current_process = ready_queue.pop(0)
        
        # Record start time if not already set
        if current_process.start_time is None:
            current_process.start_time = current_time
        
        # Execute the process
        execution_time = cpu.execute(current_process, time_quantum, current_time)
        current_time += execution_time
        
        # Check if process completed
        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            completed_processes.append(current_process)
        else:
            # Re-add to ready queue if not finished
            ready_queue.append(current_process)
    
    return completed_processes
