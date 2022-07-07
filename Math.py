path = r'C: > Users > tanne > Documents >VScode > atmdata.csv'
import pandas as pd
atm = pd.read_csv("atmdata.csv")
thrust = pd.read_csv("thrust.csv")
import numpy as np
print(thrust)

def Thrust(time):
    return thrust[thrust["Time"] <= time].loc[-1]["Corrected Thrust"]


def air_density(altitude):
    return atm[atm["Altitude[m]"] <= altitude].iloc[-1]["Density[kg/m3]"]



time = 0
inc = 0.25
wet = 120
fuel = 60
gravity = -9.81
net_force = wet*gravity
burn_time = 31
gradient = fuel/burn_time
velocity = 0
drag = 0
area = 0.0081
parea = 3.57
pCd = 2.2
Cd = 0.75
altitude = 0
density = air_density(altitude)
avg = Thrust(time)

if net_force == 0:
    acceleration = gravity


def parachute(altitude):
    if velocity < 0:
        return True
    else:
        return False


def thrustactive(burn_time):
    if time < burn_time:
        return True
    else:
        return False


tim = []
den = []
alt = []
vel = []
net = []

while time < 10000:
    density = air_density(altitude)
    tim.append(time)
    alt.append(altitude)
    vel.append(velocity)
    net.append(net_force)
    den.append(density)
    if thrustactive(burn_time) is True:
        wet = wet - (gradient*inc)
        drag = 1/2*area*Cd*density*velocity**2
        net_force = avg - wet*gravity - drag
        acceleration = net_force/wet
        velocity = velocity + acceleration*inc
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        time += inc
        # print(altitude, velocity, net_force)
    elif time >= burn_time and parachute(altitude) is False:
        avg = 0
        drag = 1 / 2 * area * Cd * density * velocity ** 2
        net_force = wet*gravity - drag
        acceleration = net_force / wet
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        velocity = velocity + (acceleration * inc)
        # print(altitude, velocity, net_force)
        time += inc
    else:
        avg = 0
        drag = 1 / 2 * parea * pCd * density * (velocity ** 2)
        net_force = wet*gravity + drag
        acceleration = net_force / wet
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        velocity = velocity + (acceleration * inc)
        # print(altitude, velocity, net_force)
        time += inc
        if altitude <= 0:
            break
print(max(alt), max(vel), max(net), min(den))


import matplotlib.pyplot as plt
x= tim
y= den
plt.plot(x, y)
plt.show()
