import sys 
from fractions import Fraction

def gcd(a,b):
    if(b==0):
        return(abs(a))
    else:
        return(gcd(b,a % b))

def lcm(a,b):
    return abs(a*b)// gcd(a,b)

def calculate_hyperperiod(periods):
    current_lcm=periods[0]
    for period in periods[1:]:
        current_lcm=lcm(current_lcm,period)
    return current_lcm

def multiple_gcd(numbers):
    current_gcd=numbers[0]
    for number in numbers[1:]:
        current_gcd=gcd(current_gcd,number)
    return current_gcd

class Task:
    def __init__(self,execution_time,period,deadline):
        self.execution_time=execution_time
        self.period=period
        self.deadline=deadline
        self.remaining_time=0
        self.preemptions=0
        self.next_arrival_time=0
        self.absolute_deadline=0

def read_task(filename):
    tasks=[]
    try:
        with open(filename,'r') as file:
            for line in file:
                try:
                    parts=line.strip().split(',')
                    if len(parts) !=3:
                        raise ValueError(f"Line does not contain exactly three values: {line.strip()}")
                    execution_time, period, deadline=map(Fraction, parts)

                    if execution_time <=0 or period <=0 or deadline <=0:
                        raise ValueError(f"Execution time, period and deadline must be positive integers. Found: {execution_time}, {period}, {deadline}")
                    if execution_time > min(period, deadline):
                        raise ValueError(f"execution time must be less than or equal to period and deadline. Found: {execution_time} > {min(period, deadline)}")
                    tasks.append(Task(execution_time,period,deadline))
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)
    return tasks

def deadline_monotonic_scheduling(tasks,hyperperiod,precision):
    sorted_tasks=sorted(tasks,key=lambda x: x.deadline)
    time=Fraction(0)
    previous_task=None

    while time < hyperperiod:
        for task in sorted_tasks:
            if time % task.period==0:
                task.remaining_time=task.execution_time
                task.next_arrival_time=time + task.period
                task.absolute_deadline=time + task.deadline
        
        runnable_tasks=[t for t in sorted_tasks if t.remaining_time > 0  and time < t.absolute_deadline]
        if not runnable_tasks:
            time += precision
            continue
        
        highest_priority_task=min(runnable_tasks,key=lambda t: t.deadline)

        if previous_task and previous_task != highest_priority_task:
            previous_task.preemptions += 1
        
        highest_priority_task.remaining_time -= precision
        previous_task = highest_priority_task

        if highest_priority_task.remaining_time <= 0:
            highest_priority_task.remaining_time = 0
            previous_task=None
        
        time += precision

    for task in sorted_tasks:
        if task.remaining_time > 0:
            return 0, []
    
    return 1, [task.preemptions for task in tasks]

def main(filename):
    tasks = read_task(filename)
    if not tasks:
        print("Error: No valid tasks read from the file.")
        sys.exit(1)
    
    periods = [task.period for task in tasks]
    hyperperiod = calculate_hyperperiod(periods)

    all_inputs=[task.execution_time for task in tasks] + [task.period for task in tasks] + [task.deadline for task in tasks]
    precision=multiple_gcd(all_inputs)
    
    res, preemptions = deadline_monotonic_scheduling(tasks, hyperperiod,precision)

    print(res)
    if res:
        print(','.join(map(str,preemptions)))
    else:
        print()

if __name__=="__main__":
    if len(sys.argv)!=2:
        print('Error: wrong input, it should be: python ece_652_final <filename>')
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
