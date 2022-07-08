from scipy import rand, signal
from matplotlib import pyplot as plt
import numpy as np

number = 10
density = 10
period = 10
amplitude = 50

noiseAmpl = .01
noise = list(abs(np.random.normal(1, noiseAmpl * amplitude,  (number+1)*density)))

x = list((np.array(range(0, (number+1)*density))-.5)/density)
y = (-signal.sawtooth(list(np.array(x)*6/period)) + 1) * amplitude - noise

plt.plot(x, y)
plt.show()
