import numpy as np
import math

results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(0,100000):
    next = np.random.exponential(1)
    number = math.ceil(next)
    number = min(number, 10)
    results[number-1] = results[number-1]+1
print(results)