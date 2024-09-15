"""
Make the necessary modifications to 
the above computer program of the model
of the checkout counter (Example 4.2) so
that the simulation will run for exactly 60 hours.

The termination conditions are set in two parts:
1. If the simulation reaches 3600 minutes (60 hours).
2. If all customers are processed.

The simulation will terminate if either condition is met.

"""

import random
import math
from queue import Queue


class Event:
    def __init__(self, event_type, event_time):
        self.event_type = event_type
        self.event_time = event_time

    def get_type(self):
        return self.event_type

    def get_time(self):
        return self.event_time


class EventList:
    def __init__(self):
        self.events = []

    def enqueue(self, event):
        self.events.append(event)
        self.events.sort(key=lambda e: e.get_time())

    def get_min(self):
        return self.events[0]

    def dequeue(self):
        self.events.pop(0)


class Sim:
    def __init__(self, total_customers, mean_interarrival_time, mean_service_time, sigma):
        # Simulation variables
        self.Clock = 0.0
        self.MeanInterArrivalTime = mean_interarrival_time
        self.MeanServiceTime = mean_service_time
        self.SIGMA = sigma
        self.LastEventTime = 0.0
        self.TotalBusy = 0.0
        self.MaxQueueLength = 0
        self.SumResponseTime = 0.0
        self.QueueLength = 0
        self.NumberInService = 0
        self.TotalCustomers = total_customers
        self.NumberOfDepartures = 0
        self.LongService = 0
       

        # Event list and queue
        self.FutureEventList = EventList()
        self.Customers = Queue()

        # Simulation time limit (60 hours = 3600 minutes)
        self.SimulationTimeLimit = 3600.0

    def exponential(self, mean):
        return -mean * math.log(random.random())

    def normal(self, mean, sigma):
        return mean + sigma * random.gauss(0, 1)

    def schedule_departure(self):
        service_time = self.normal(self.MeanServiceTime, self.SIGMA)
        while service_time < 0:
            service_time = self.normal(self.MeanServiceTime, self.SIGMA)

        departure_time = self.Clock + service_time
        self.FutureEventList.enqueue(Event('departure', departure_time))
        self.NumberInService = 1 #single server
        self.QueueLength -= 1

    def process_departure(self, event):
        # Get the customer from the queue
        finished = self.Customers.get()

        # If there are customers in the queue, schedule the next departure
        if self.QueueLength > 0:
            self.schedule_departure()
        else:
            self.NumberInService = 0

        
        response = self.Clock - finished.get_time()
        self.SumResponseTime += response

        # Record long service time
        if response > 4.0:
            self.LongService += 1

        self.TotalBusy += (self.Clock - self.LastEventTime)
        self.NumberOfDepartures += 1
        self.LastEventTime = self.Clock

    def process_arrival(self, event):
        # Add the customer to the queue
        self.Customers.put(event)
        self.QueueLength += 1

        # If the server is idle, schedule a departure
        if self.NumberInService == 0:
            self.schedule_departure()
        else:
            self.TotalBusy += (self.Clock - self.LastEventTime)

        # Adjust max queue length statistics
        if self.MaxQueueLength < self.QueueLength:
            self.MaxQueueLength = self.QueueLength

        # Schedule the next arrival
        next_arrival_time = self.Clock + self.exponential(self.MeanInterArrivalTime)
        self.FutureEventList.enqueue(Event('arrival', next_arrival_time))
        self.LastEventTime = self.Clock

    def report_generation(self):
        rho = self.TotalBusy / self.Clock
        avg_response = self.SumResponseTime / self.TotalCustomers
        proportion_long_service = self.LongService / self.TotalCustomers

        print("SINGLE SERVER QUEUE SIMULATION")
        print("GROCERY STORE CHECKOUT COUNTER")
        print(f"\tMEAN INTERARRIVAL TIME: {self.MeanInterArrivalTime}")
        print(f"\tMEAN SERVICE TIME: {self.MeanServiceTime}")
        print(f"\tSTANDARD DEVIATION OF SERVICE TIMES: {self.SIGMA}")
        print(f"\tNUMBER OF CUSTOMERS SERVED: {self.TotalCustomers}")
        print()
        print(f"\tSERVER UTILIZATION: {rho:.2f}")
        print(f"\tMAXIMUM LINE LENGTH: {self.MaxQueueLength}")
        print(f"\tAVERAGE RESPONSE TIME: {avg_response:.2f} MINUTES")
        print(f"\tPROPORTION WHO SPEND FOUR MINUTES OR MORE IN SYSTEM: {proportion_long_service:.2f}")
        print(f"\tSIMULATION RUN LENGTH: {self.Clock:.2f} MINUTES")
        print(f"\tNUMBER OF DEPARTURES: {self.NumberOfDepartures}")
      

    def run_simulation(self):
        # Initialize the simulation
        first_arrival_time = self.exponential(self.MeanInterArrivalTime)
        self.FutureEventList.enqueue(Event('arrival', first_arrival_time))

        # Run the simulation until either all customers are served or time limit is reached
        while self.NumberOfDepartures < self.TotalCustomers and self.Clock <= self.SimulationTimeLimit:
            event = self.FutureEventList.get_min()
            self.FutureEventList.dequeue()
            self.Clock = event.get_time()

            if event.get_type() == 'arrival':
                self.process_arrival(event)
            else:
                self.process_departure(event)

        # Generate the final report
        self.report_generation()


# Run the simulation
if __name__ == "__main__":
    total_customers = 1000  # total customer limit
    mean_interarrival_time = 4.5
    mean_service_time = 3.2
    sigma = 0.6

    sim = Sim(total_customers, mean_interarrival_time, mean_service_time, sigma)
    sim.run_simulation()
