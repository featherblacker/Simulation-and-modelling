import numpy as np
import pandas as pd

ws1 = np.loadtxt('ws1.dat')
ws2 = np.loadtxt('ws2.dat')
ws3 = np.loadtxt('ws3.dat')
sp1 = np.loadtxt('servinsp1.dat')
sp22 = np.loadtxt('servinsp22.dat')
sp23 = np.loadtxt('servinsp23.dat')

class Simulation:
    def __init__(self, ws):
        self.clock = 0.0
        self.t_arrival = self.generate_interarrival()
        self.t_departure = float('inf')
        self.num_in_system = 0
        self.ws = ws
        self.times = 0

        self.num_arrivals = 0
        self.num_depart = 0
        self.total_wait = 0.0

    def advance_time(self):
        t_event = min(self.t_arrival, self.t_departure)
        self.total_wait += self.num_in_system * (t_event - self.clock)
        self.clock = t_event

        if self.t_arrival <= self.t_departure:
            self.handle_arrival_event()
        else:
            self.handle_depart_event()

    def handle_arrival_event(self):
        self.num_in_system += 1
        self.num_arrivals += 1
        if self.num_in_system <= 1:
            self.t_departure = self.clock + self.generate_service(self.times)
            self.times+=1
        self.t_arrival = self.clock + self.generate_interarrival()

    def handle_depart_event(self):
        self.num_in_system -= 1
        self.num_depart += 1
        if self.num_in_system > 0:
            self.t_departure = self.clock + self.generate_service(self.times)
            self.times+=1
        else:
            self.t_departure = float('inf')

    def generate_interarrival(self):
        return np.random.exponential(1. / 3)

    def generate_service(self, times):
        return self.ws[times]

    def get_departs(self):
        return self.num_depart




np.random.seed(0)
s = Simulation(ws1)

for _ in range(100):
    s.advance_time()
