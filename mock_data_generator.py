from datetime import date, datetime, timedelta
import math
import numpy as np
import random as r
import matplotlib.pyplot as plt
from UliEngineering.SignalProcessing.Simulation import inverse_sawtooth
from server.plants import read_all
from server.water_values import add_new_value, delete_all

time_delta = 14     # Amount of days that the history goes back
measure_period = 3  # Period of water level measurements in hours
sine_weight = 8     # Sets the weight of the sine curve in the data (bigger value -> more curvy)

def generate(time_delta, measure_period, sine_weight):
    sample_rate = int(24 / measure_period * time_delta)
    a = r.uniform(.8, 1.6)
    date_time = [datetime.now() - timedelta(hours=time_delta*24)]
    noise = np.random.normal(0, r.uniform(.6, 1.9), sample_rate)
    data = inverse_sawtooth(frequency=a, samplerate=sample_rate, amplitude=40, phaseshift=r.random()*1e6)
    sin = [(sine_weight*math.sin(i*(a/20))) for i in range(sample_rate)]
    for i in range(len(data)):
        data[i] += 50+noise[i]+sin[i]
        if data[i] < 0:
            data[i] = 0
        if data[i] > 100:
            data[i] = 100
        date_time.append(date_time[i]+timedelta(hours=measure_period))
    del date_time[-1]

    return data, date_time

# plt.plot(date_time, data)
# plt.xlabel('Time')
# plt.ylabel('Water Level')
# plt.title('reversed Sawtooth ')
# plt.show()

plants = read_all()
for j in plants:
    data, date_time = generate(time_delta, measure_period, sine_weight)
    for i in range(len(data)):
        add_new_value({"plant_id":j.get("id"),"value":int(data[i]),"report_time":date_time[i].strftime("%Y-%m-%d %H:%M:%S.%f")})