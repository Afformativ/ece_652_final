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

class Task:
    def __init__(self,execution_time,period,deadline):
        self.execution_time=execution_time
        self.period=period
        self.deadline=deadline
        self.remaining_time=0
        self.preemptions=0

def read_task(filename):
    tasks=[]
    with open(filename,'r') as file:
        for line in file:
            execution_time,period,deadline=map(float,line.strip().strip(','))
            tasks.append(Task(execution_time,period,deadline))
    return tasks
