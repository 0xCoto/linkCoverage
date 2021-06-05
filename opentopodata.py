import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import random
from time import sleep

# Tx location [lat, long]
Tx = [39.140043817693154, 21.658209430289556]

# Rx location [lat, long]
#Rx = [39.169868047238076, 21.61960477652405]

### ^ subtract 1 for ...

# Radius [deg]
radius = 0.5

# Resolution (step) [deg]
resolution = 0.1

# Parse dict to json
#data = json.dumps(data)

url = "https://api.opentopodata.org/v1/eudem25m?"

#heatmap = np.empty(shape=[0, 3])
heatmap = np.array([]) #np.empty(shape=[0, 1])

#url = "https://api.opentopodata.org/v1/eudem25m?locations=-43.5,172.5|27.6,1.98&interpolation=cubic"
for lat in np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution):
        for long in np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution):
                print('Fetching: '+str(lat)+','+str(long))
                data = "locations="+str(lat)+","+str(long)
                response = requests.get(url, data, headers={'content-type': 'application/json'})
                elevation = response.text.split('"elevation": ')[1].split(',')[0]
                if elevation == 'null':
                        elevation = 0
                else:
                        elevation = float(elevation)
                #elevation = float(np.random.randint(100))
                #print(lat, long, elevation)
                heatmap = np.append(heatmap, elevation)
                sleep(1.3)
                #heatmap = np.vstack((heatmap, np.array([lat, long, elevation])))
heatmap = heatmap.reshape(-1, len(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution)))
print(heatmap)
plt.imshow(heatmap, interpolation='gaussian', extent=[np.min(np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution)), np.max(np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution)), np.min(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution)), np.max(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution))])
plt.show()
