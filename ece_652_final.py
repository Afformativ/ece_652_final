import sys 
from fractions import Fraction

# function to calculate the greatest common divisor
def gcd(a,b):
    if(b==0):
        return(abs(a))
    else:
        return(gcd(b,a % b))

# function to calculate the least common multiple
def lcm(a,b):
    return abs(a*b)// gcd(a,b)

# function to calculate hyperperiod
def calculate_hyperperiod(periods):
    current_lcm=periods[0]
    for period in periods[1:]:
        current_lcm=lcm(current_lcm,period)
    return current_lcm

# function to calculate the GCD of multiple numbers
def multiple_gcd(numbers):
    current_gcd=numbers[0]
    for number in numbers[1:]:
        current_gcd=gcd(current_gcd,number)
    return current_gcd

#class representing a task
class Task:
    def __init__(self,execution_time,period,deadline):
        self.execution_time=execution_time
        self.period=period
        self.deadline=deadline
        self.remaining_time=0
        self.preemptions=0
        self.next_arrival_time=0
        self.absolute_deadline=0

#function to read tasks from a file
def read_task(filename):
    tasks=[]
    try:
        with open(filename,'r') as file:
            for line in file:
                try:
                    parts=line.strip().split(',')

                    #exception if it is not exactly 3 elements in an input line
                    if len(parts) !=3:
                        raise ValueError("Line does not contain exactly three values")
                    execution_time, period, deadline=map(Fraction, parts)

                    #exception if something is lower or equal to zero
                    if execution_time <=0 or period <=0 or deadline <=0:
                        raise ValueError("Execution time, period and deadline must be positive integers")
                    
                    #exception if execution time is more than deadline/period
                    if execution_time > min(period, deadline):
                        raise ValueError("execution time must be less than or equal to period and deadline")
                    tasks.append(Task(execution_time,period,deadline))
                except ValueError as e:
                    continue
    # error if such file not found            
    except FileNotFoundError:
        sys.exit(1)
    return tasks

#function to perform deadline monotonic scheduling
def deadline_monotonic_scheduling(tasks,hyperperiod,precision):
    sorted_tasks=sorted(tasks,key=lambda x: x.deadline)
    time=Fraction(0)
    previous_task=None

    while time < hyperperiod:
        # update task states at the start of each period
        for task in sorted_tasks:
            if time % task.period==0:
                task.remaining_time=task.execution_time
                task.next_arrival_time=time + task.period
                task.absolute_deadline=time + task.deadline
        
        # get all runnable tasks
        runnable_tasks=[t for t in sorted_tasks if t.remaining_time > 0  and time < t.absolute_deadline]
        if not runnable_tasks:
            time += precision
            continue
        
        # select the highest priority task
        highest_priority_task=min(runnable_tasks,key=lambda t: t.deadline)

        # handle preemptions
        if previous_task and previous_task != highest_priority_task:
            previous_task.preemptions += 1
        
        #execute the highest priority task
        highest_priority_task.remaining_time -= precision
        previous_task = highest_priority_task

        # check if the task has finished
        if highest_priority_task.remaining_time <= 0:
            highest_priority_task.remaining_time = 0
            previous_task=None
        
        time += precision
    
    #check if all tasks completed successfully
    for task in sorted_tasks:
        if task.remaining_time > 0:
            return 0, []
    
    return 1, [task.preemptions for task in tasks]

def main(filename):
    tasks = read_task(filename)

    #exception if it is not any task in the input file
    if not tasks:
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

    #exception if it is not file name in the terminal line
    if len(sys.argv)!=2:
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
