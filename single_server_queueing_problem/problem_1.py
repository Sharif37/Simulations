"""
Write a program in any computer programming language
for the grocery checkout counter (single server queueing model)
simulation as detailed in Table 2.10 in the textbook. The total
number of customers to be served should be input from the user of this program.

"""



import random

def simulate_queue(num_customers):
    interarrival_times = []
    arrival_times = []
    service_times = []
    start_times = []
    waiting_times = []
    end_times = []
    total_times_in_system = []
    idle_times = []

    # Initializing first customer
    interarrival_times.append(0)  # First customer arrives at time 0
    arrival_times.append(0)
    service_times.append(random.randint(1, 10)) 
    start_times.append(0)
    waiting_times.append(0)
    end_times.append(start_times[0] + service_times[0])
    total_times_in_system.append(end_times[0] - arrival_times[0])
    idle_times.append(0)

    # Simulate for the rest of the customers
    for i in range(1, num_customers):
        interarrival_times.append(random.randint(1, 9)) 
        arrival_times.append(arrival_times[i-1] + interarrival_times[i])
        service_times.append(random.randint(1, 10)) 

        start_times.append(max(arrival_times[i], end_times[i-1]))
        waiting_times.append(start_times[i] - arrival_times[i])
        end_times.append(start_times[i] + service_times[i])
        total_times_in_system.append(end_times[i] - arrival_times[i])
        idle_times.append(start_times[i] - end_times[i-1])

    # Display the table 
    print(f"{'Customer':<10}{'Interarrival Time':<20}{'Arrival Time':<15}{'Service Time':<15}"
          f"{'Start Time':<15}{'Waiting Time':<15}{'End Time':<15}{'Time in System':<15}{'Idle Time':<15}")
    
    for i in range(num_customers):
        print(f"{i+1:<10}{interarrival_times[i]:<20}{arrival_times[i]:<15}{service_times[i]:<15}"
              f"{start_times[i]:<15}{waiting_times[i]:<15}{end_times[i]:<15}{total_times_in_system[i]:<15}"
              f"{idle_times[i]:<15}")
    
    print("\nTotal:")
    print(f"Total Interarrival Time: {sum(interarrival_times)}")
    print(f"Total Service Time: {sum(service_times)}")
    print(f"Total Waiting Time: {sum(waiting_times)}")
    print(f"Total Time in System: {sum(total_times_in_system)}")
    print(f"Total Idle Time: {sum(idle_times)}")

# Input the number of customers
num_customers = int(input("Enter the total number of customers: "))
simulate_queue(num_customers)
