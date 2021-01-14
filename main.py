import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class agentModel:
    def __init__(self,nConsumers=10, nProducers = 4,producerMin=5, producerS=1, consumerMax=4, consumerS=1, slope = .1, stepSize = .2):
        
        #make variable available to entire class

        self.nConsumers = nConsumers
        self.nProducers = nProducers
        self.producerMin = producerMin
        self.producerS = producerS
        self.consumerMax = consumerMax
        self.consumerS = consumerS
        self.stepSize = stepSize

        #Create empty dataframes
        self.consumers = pd.DataFrame()
        self.producers = pd.DataFrame()
        
        #Fill dataframe with random values
        self.consumers["maxPrice"] = np.random.normal(loc=consumerMax, scale = consumerS, size = nConsumers)
        self.producers["minPrice"] = np.random.normal(loc=producerMin, scale = producerS, size = nProducers)
        self.producers["price"] = self.producers["minPrice"] + 1

        #good to record at least one metric
        self.surplus = []
    
    def cycle(self):
        consumerSample = self.consumers.sample(n=min(self.nProducers, self.nConsumers))
        producerSample = self.producers.sample(n=min(self.nProducers, self.nConsumers))

        #this step makes a lot of the rest easier but it is only reasonable when we treat consumers as immutable.
        consumerSample.index = producerSample.index


        #makes sale if the amount the consumer is willing to pay us greater than or equal to the price
        s = consumerSample["maxPrice"].ge(producerSample["price"])

        #calculate surplus
        ps = (producerSample["price"][s] - producerSample["minPrice"][s]).sum()
        cs = (consumerSample["maxPrice"][s] - producerSample["price"][s]).sum()
        self.surplus.append(ps+cs)

        #adjust price based on the sale
        producerSample["price"] = np.where(s, producerSample["price"] + self.stepSize, producerSample["price"] - self.stepSize)

        #make sure no one dips below their minimum sell price
        l = producerSample["price"] < producerSample["minPrice"]
        producerSample["price"][l] = producerSample["minPrice"][l]

        
        #update values
        self.producers.update(producerSample)
    
    def sale(self, row):
        print(row)



model = agentModel(nConsumers = 1000, nProducers = 500, stepSize = .01)

print(model.producers)

for i in range(1000):
    model.cycle()

print(model.producers)

#smooth that shit out with a moving average
plt.plot(pd.Series(model.surplus).rolling(20).mean())
plt.show()