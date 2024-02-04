import threading
import time
from queue import Queue
from queue import PriorityQueue

import matplotlib.pyplot as plt
import numpy as np

def draw_gantt(data):
    plot_data = []
    for i, core in enumerate(data):
        for task in core:
            for time, task_id in task.items():
                plot_data.append((i, time, task_id))

    # Sort the data by time
    plot_data.sort(key=lambda x: x[1])

    # Create the figure and the axes
    fig, ax = plt.subplots()

    # The labels for the tasks
    labels = sorted(list(set([task for _, _, task in plot_data])))

    # The colors for the tasks
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))

    # Plot the data
    for i, (core, time, task) in enumerate(plot_data):
        ax.broken_barh([(time, 1)], (core, 1), facecolors=colors[labels.index(task)])

    # Set the yticks to the core indices
    ax.set_yticks(range(len(data)))

    # Set the ytick labels to the core names
    ax.set_yticklabels(['Core '+str(i+1) for i in range(len(data))])

    # Set the xticks to the time values
    ax.set_xticks(range(plot_data[-1][1] + 2))

    # Set the xlabel
    ax.set_xlabel('Time')

    # Set the ylabel
    ax.set_ylabel('Core')

    # Set the title
    ax.set_title('Gantt Chart')
    ax.legend([plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(labels))], labels)
    ax.grid(True)
    ax.set_yticks(range(len(data)))
    plt.savefig("ganttchart.png")


tasks = []
waiting = []
resource_pool = []

class Resource:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.mutex = threading.Lock()

class Task:
    def __init__(self, task_id, task_type, duration, arrival_time,required_resources, priority):
        self.task_id = task_id
        self.task_type = task_type
        self.duration = duration
        self.arrival_time = arrival_time
        self.required_resources = required_resources
        self.priority = priority
        self.state = "Ready"
        self.execution_time = 0.0
        self.mutex = threading.Lock()

    def set_state(self, state):
        with self.mutex:
            self.state = state

    def set_execution_time(self, execution_time):
        with self.mutex:
            self.execution_time = execution_time





cores = [[],[],[],[]]


def fcfs_scheduler(core_num,tasks,resource_pool,lock,ctime):
    if len(tasks)>0:
        lock.acquire() 
        tasks.sort(key=lambda x: (x.arrival_time , x.priority))  # Sort processes based on arrival time
        task = tasks.pop(0)
        if len(waiting) > 0 and waiting[0].priority > task.priority and waiting[0].required_resources[0] <= resource_pool[0].capacity and waiting[0].required_resources[1] <= resource_pool[1].capacity and waiting[0].required_resources[2] <= resource_pool[2].capacity:
            tasks.insert(0,waiting.pop(0))
        while task.required_resources[0] > resource_pool[0].capacity or task.required_resources[1] > resource_pool[1].capacity or task.required_resources[2] > resource_pool[2].capacity:
            waiting.append(task)
            if len(tasks)>0:
                task = tasks.pop(0)
            else:
                break
        resource_pool[0].capacity -= task.required_resources[0]
        resource_pool[1].capacity -= task.required_resources[1]
        resource_pool[2].capacity -= task.required_resources[2]
        cores[core_num-1].append({ctime : task.task_id})
        lock.release()

        print(f"Core: {core_num}, Time: {ctime}, Task: {task.task_id}")
        # print("Resource 1:",resource_pool[0].capacity," Resource 2:",resource_pool[1].capacity," Resource 3:",resource_pool[2].capacity)

        process_execution(task)
        time.sleep(1)
        lock.acquire()
        if task.duration > 0:
            tasks.insert(0,task)
        resource_pool[0].capacity += task.required_resources[0]
        resource_pool[1].capacity += task.required_resources[1]
        resource_pool[2].capacity += task.required_resources[2]
        lock.release()
    else: 
        print(f"Core: {core_num}, Time: {ctime}, Task: Idle")


def sjf_scheduler(core_num,tasks,resource_pool,lock,ctime):
    if len(tasks)>0:
        lock.acquire()
        tasks.sort(key=lambda x: (x.duration , x.priority))  # Sort processes based on shortest remaining time
        task = tasks.pop(0)
        if len(waiting) > 0 and waiting[0].priority > task.priority and waiting[0].required_resources[0] <= resource_pool[0].capacity and waiting[0].required_resources[0] <= resource_pool[1].capacity and waiting[0].required_resources[2] <= resource_pool[2].capacity:
            tasks.insert(0,waiting.pop(0))
        while task.required_resources[0] > resource_pool[0].capacity or task.required_resources[1] > resource_pool[1].capacity or task.required_resources[2] > resource_pool[2].capacity:
            waiting.append(task)
            if len(tasks)>0:
                task = tasks.pop(0)
            else:
                break
        resource_pool[0].capacity -= task.required_resources[0]
        resource_pool[1].capacity -= task.required_resources[1]
        resource_pool[2].capacity -= task.required_resources[2]
        cores[core_num-1].append({ctime : task.task_id})

        lock.release()

        print(f"Core: {core_num}, Time: {ctime}, Task: {task.task_id}")
        # print("Resource 1:",resource_pool[0].capacity," Resource 2:",resource_pool[1].capacity," Resource 3:",resource_pool[2].capacity)
        process_execution(task)
        time.sleep(1)
        lock.acquire()
        if task.duration > 0:
            tasks.insert(0,task)
        resource_pool[0].capacity += task.required_resources[0]
        resource_pool[1].capacity += task.required_resources[1]
        resource_pool[2].capacity += task.required_resources[2]
        lock.release()
    else: 
        print(f"Core: {core_num}, Time: {ctime}, Task: Idle")


def RR_scheduler(core_num,tasks,resource_pool,lock,ctime):
    if len(tasks)>0:
        lock.acquire()
        task = tasks.pop(0)
        if len(waiting) > 0 and waiting[0].priority > task.priority and waiting[0].required_resources[0] <= resource_pool[0].capacity and waiting[0].required_resources[0] <= resource_pool[1].capacity and waiting[0].required_resources[2] <= resource_pool[2].capacity:
            tasks.insert(0,waiting.pop(0))
        while task.required_resources[0] > resource_pool[0].capacity or task.required_resources[1] > resource_pool[1].capacity or task.required_resources[2] > resource_pool[2].capacity:
            waiting.append(task)
            if len(tasks)>0:
                task = tasks.pop(0)
            else:
                break
        resource_pool[0].capacity -= task.required_resources[0]
        resource_pool[1].capacity -= task.required_resources[1]
        resource_pool[2].capacity -= task.required_resources[2]
        cores[core_num-1].append({ctime : task.task_id})

        lock.release()

        print(f"Core: {core_num}, Time: {ctime}, Task: {task.task_id}")
        # print("Resource 1:",resource_pool[0].capacity," Resource 2:",resource_pool[1].capacity," Resource 3:",resource_pool[2].capacity)

        process_execution(task)
        time.sleep(1)
        lock.acquire()
        if task.duration > 0:
            tasks.insert(0,task)
        resource_pool[0].capacity += task.required_resources[0]
        resource_pool[1].capacity += task.required_resources[1]
        resource_pool[2].capacity += task.required_resources[2]
        lock.release()
    else: 
        print(f"Core: {core_num}, Time: {ctime}, Task: Idle")


def process_execution(task):
    task.duration -= 1
    
     
def read_input():
    # Reading the number of resources
    num_resources = list(map(int, input("Enter resources , tasks and their specifications:\n").split()))
    # Creating resource objects
    resource_r1 = Resource("R1", capacity=num_resources[0])
    resource_r2 = Resource("R2", capacity=num_resources[1])
    resource_r3 = Resource("R3", capacity=num_resources[2])
    # Reading the number of tasks
    num_tasks = int(input())

    # Reading task details
    arrival = 0
    tasks = []
    for i in range(num_tasks):
        task_info = input().split()
        task_id = task_info[0]
        task_type = task_info[1]
        task_duration = int(task_info[2])
        required_resources = []
        if task_type == 'X':
            required_resources = [1, 1,0]
            task_priority = 3
        elif task_type == 'Y':
            required_resources = [0,1,1]
            task_priority = 2
        elif task_type == 'Z':
            required_resources = [1,0,1]
            task_priority = 1
          # Priority is set based on the order of tasks
        arrival += 1
        tasks.append(Task(task_id, task_type, task_duration, arrival,required_resources, task_priority))
    algo = input("Which Algorithm(FSFC, SJF, RR): ")
    return resource_r1,resource_r2,resource_r3, tasks , algo

if __name__ == "__main__":
    # Reading input
    resource_r1, resource_r2, resource_r3, tasks , algo = read_input()
    orgres1 = resource_r1
    orgres2 = resource_r2
    orgres3 = resource_r3


    resource_pool = [resource_r1, resource_r2, resource_r3]


    shared_output_lock = threading.Lock()
    print(f"\n(({algo}))")
    print ("============================")
    ctime = 0
    while len(tasks) > 0 or len(waiting)>0:
        ctime += 1
        threads = []
        task_ids=[]
        waiting_ids=[]
        for thistask in tasks:
            task_ids.append(thistask.task_id)
        for thiswait in waiting:
            waiting_ids.append(thiswait.task_id)
        print("Ready Queue: ",task_ids)
        print("Waiting Queue: ",waiting_ids)
        for i in range(4):
            if algo.lower() == "fcfs":
                t = threading.Thread(target=fcfs_scheduler , args=(i+1,tasks,resource_pool,shared_output_lock,ctime))
            elif algo.lower() == "sjf":
                t = threading.Thread(target=sjf_scheduler , args=(i+1,tasks,resource_pool,shared_output_lock,ctime))
            elif algo.lower() == "RR":
                tasks.sort(key=lambda x: x.priority)  # priority sort for RR
                t = threading.Thread(target=RR_scheduler , args=(i+1,tasks,resource_pool,shared_output_lock,ctime))
            else:
                print("Wrong Algorithm, please try again")


            threads.append(t)

        for i in range(4):
            threads[i].start()

        for i in range(4):
            threads[i].join()

        print("============================")
    print(cores)
    draw_gantt(cores)


