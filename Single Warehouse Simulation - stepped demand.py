import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class warehouse:
    def __init__(self, inventory_level):
        self.i = inventory_level
        self.review_inventory(0)

#this function executes the ordering process to fulfilling the demand, received at the beginning of the period

    def order(self, Q, time):
        self.review_inventory(time)
        self.i += Q
        self.review_inventory(time)

    def on_hand_inventory(self):
        return max(0, self.i)

    def issue(self, demand, time):
        self.review_inventory(time)
        self.i = self.i - demand
        self.review_inventory(time+1) #demand os realized at the end of the period

    def review_inventory(self, time):
        try:
            self.levels.append([time, self.i])
            self.on_hand.append([time, self.on_hand_inventory()])
        except AttributeError:
            self.levels, self.on_hand = [[0, self.i]], [[0, self.on_hand_inventory()]]

def plot_inventory(values, label):

    #data
    df = pd.DataFrame({'x': np.array(values)[:,0], 'fx': np.array(values)[:,1]})

    #plot
    plt.xticks(range(len(values)), range(1, len(values)+1))
    plt.xlabel("$t")
    plt.ylabel("items")
    plt.plot('x', 'fx', data = df, linestyle = '-', marker ='o',label = label)

initial_inventory = 50 #Declaration of new Stock Level at the start of period 1

w = warehouse(initial_inventory)

demand_rate = 5 #The periodic demand of the items

N = 20

for t in range(N):
    if(t==10):
        w.order(50, t) # This conditional statement ensures to place an order of size 50, in the 10th period
    w.issue(demand_rate,t)

plot_inventory(w.levels, "Inventory Level")
plt.legend()
plt.show()



    
