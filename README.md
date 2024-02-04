# Multi-Processor Scheduler
## Overview
This project implements a multi-processor scheduler that supports different scheduling algorithms such as First-Come-First-Serve (FCFS), Shortest Job First (SJF), and Round Robin (RR). The scheduler assigns tasks to multiple processor cores based on their arrival time, priority, and resource requirements.

## Prerequisites
Python 3
Matplotlib library (install using pip install matplotlib)

## Usage
Run the script in a Python environment.
``` python
python scheduler.py
```

Follow the on-screen instructions to input the number of resources, tasks, and their specifications.

Choose a scheduling algorithm (FCFS, SJF, RR) when prompted.

The scheduler will simulate the execution of tasks on multiple processor cores, and a Gantt chart will be generated as "ganttchart.png" to visualize the task scheduling.

# Code Structure
scheduler.py: Main script containing the scheduler implementation.

The implementation is made of Creating four threads for every code and a main thread for ready and waiting queue.Then in each slice of time The algorithm asks a task for every ready processor and assign a proper task (which resources are available) and decrease it's remaining time by 1.


draw_gantt(data): Function to create a Gantt chart based on the task execution data.
Resource class: Represents a resource with a name, capacity, and a mutex for thread safety.
Task class: Represents a task with an ID, type, duration, arrival time, required resources, priority, state, execution time, and a mutex for thread safety.
process_execution(task): Function to simulate task execution.
# Scheduling Algorithms
## First-Come-First-Serve (FCFS):

Tasks are scheduled in the order of their arrival time and priority.
Waiting tasks are considered if their priority is higher and required resources are available.
## Shortest Job First (SJF):

Tasks are scheduled based on their remaining execution time and priority.
Waiting tasks are considered if their priority is higher and required resources are available.
## Round Robin (RR):

Tasks are scheduled in a circular manner, and each task gets a fixed time slice.
Tasks are sorted by priority.
Waiting tasks are considered if their priority is higher and required resources are available.
# Input Format
Input the number of resources (R1, R2, R3).
Input the number of tasks.
For each task, input the task ID, type (X, Y, Z), duration, and priority.
Input the algorithm

# Output Format
Display the current status of the ready and waiting queue.
Print the task execution details for each core (Core, Time, Task).
Generate a Gantt chart as "ganttchart.png" to visualize task scheduling.
