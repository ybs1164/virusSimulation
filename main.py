import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import objects.map as map

m = map.Map()
fig = m.GetFigure()

anime = FuncAnimation(fig, m.update, interval=100, init_func=m.init)
plt.show()

