import pandas as pd
import numpy as np
from collections import defaultdict
import scipy
from queue import PriorityQueue
import matplotlib.pyplot as plt

class Warehouse:
    def __init__(self, inventory_level, fixed_ordering_cost, holding_cost):
        self.i, self.k, self.h = inventory_level, fixed_ordering_cost, holding_cost
        self.o = 0 #It indicates the set of outstanding orders
        self.period_costs = defaultdict(int) #A python dictionary to record the costs of the inventory across each period

    def receive_order(self, Q , time):
        self.review_inventory(time)
        self.i, self.o = self.i + Q, self.o - Q # Updation of Inventory stock levels and outstanding orders by EOQ
        self.review_inventory(time)

    def order(self, Q, time):
        self.review_inventory(time)
        self.period_costs[time] += self.K #incur the ordering costs and store it in the period_costs dictionary
        self.o += Q
        self.review_inventory(time)

    def on_hand_inventory(self):
        return max(0, self.i)

    def issue(self, demand, time):
        self.review_inventory(time)
        self.i = self.i - demand

    def inventory_position(self):
        return self.o + self.i

    def review_inventory(self, time):
        try:
            self.levels.append([time, self.i])
            self.on_hand.append([time, self.on_hand_inventory()])
            self.positions.append([time, self.inventory_position()])
        except AttributeError:
            self.levels, self.on_hand = [[0, self.i]], [[0, self.on_hand_inventory()]]
            self.positions = [[0, self.inventory_position()]]

    def incur_holding_cost(self, time): #incur holding cost and store it in a dictionary
        self.period_costs[time] += self.on_hand_inventory()*self.h


#The following code encompasses the definition of the Discrete Event Simulation approach for simulating the Inventory

class EventWrapper():
    def __init__(self, event):
        self.event = event

    def __lt__(self, other):
        return self.event.priority < other.event.priority

class DES():
    def __init__(self, end):
        self.events, self.end, self.time = PriorityQueue(), end, 0

    def start(self):
        while True:
            event = self.events.get()
            self.time = event[0]
            if self.time<self.end:
                event[1].event.end()
            else:
                break

    def schedule(self, event: EventWrapper, time_lag: int):
        self.events.put((self.time +time.lag, event))

class CustomerDemand:
    def __init__(self, des:DES, demand_rate: float, warehouse: Warehouse):
        self.d = demand_rate
        self.w = warehouse
        self.des = des
        self.priority = 1                                    

class Order:
    def __init__(self, des: DES, Q:float, warehouse: Warehouse, lead_time: float):
        self.Q = Q
        self.w = warehouse
        self.des = des
        self.lead_time = lead_time
        self.priority = 0



#The EndofPeriod class is for recording the overall inventory costs at the end of the review period

class EndOfPeriod:
    def __init__(self, des: DES, warehouse: Warehouse):
        self.w = warehouse
        self.des = des
        self.priority = 2 #denotes a low priority

    def end(self):
        self.w.incur_holding_cost(self.des.time)
        self.des.schedule(EventWrapper(EndOfPeriod(self.des, self.w)), 1)

sample = {"inventory_level": 0, "fixed_ordering_cost": 100, "holding_cost": 1}

w = Warehouse(**sample)

N = 20 #Taking a horizon length of 20 periods

des = DES(N)

d = CustomerDemand(des, 10, w)
des.schedule(EventWrapper(d), 0) #scheduling a demand immediately

lead_time = 0
o = Order(des, 50, w, lead_time)

for t in range(0, 20, 5):
    des.schedule((EventWrapper(EndOfPeriods, w)), 0) #schedule End of the period

des.start()

print("Period costs : " +str([w.period_costs[e] for e in w.period_costs]))
print("Average cost per period:" + '%.2f' % (sum([w.period_costs[e] for e in w.period_costs])/ len(w.period_costs)))

plot.inventory(w.positions, "Inventory Position")
plot_inventory(w.levels, "Inventory level" )
plt.legend
plt.show()








