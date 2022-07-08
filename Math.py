import pandas as pd
import numpy as np

atm = pd.read_csv("atmdata.csv")
thrust = pd.read_csv("thrust.csv")
Cd = pd.read_csv("RASaero.csv")


def Thrust(time):

    return thrust[thrust["Time"] <= time].iloc[-1]["Corrected Thrust"]


def air_density(altitude):
    return atm[atm["Altitude[m]"] <= altitude].iloc[-1]["Density[kg/m3]"]

def CD(mach):
    return Cd[Cd["Mach"] <= mach].iloc[-1]["CD"]

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
# Pretty sure that this is wrong. 3.5" is 0.0889 m, so area should be closer to 0.025
# area = 0.0081
area = 0.025
parea = 3.57
pCd = 2.2
altitude = 0
density = air_density(altitude)
mach = velocity/density
D = CD(mach)
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
thr = []
alt = []
vel = []
net = []
mac = []

while time < 10000:
    density = air_density(altitude)
    avg = Thrust(time)
    thr.append(avg)
    tim.append(time)
    alt.append(altitude)
    vel.append(velocity)
    net.append(net_force)
    den.append(density)
    mac.append(velocity/density)
    if thrustactive(burn_time) is True:
        wet = wet - (gradient*inc)
        drag = 1/2*area*D*density*velocity**2
        net_force = avg - wet*gravity - drag
        acceleration = net_force/wet
        velocity = velocity + acceleration*inc
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        mach = velocity/density
        time += inc
        # print(altitude, velocity, net_force)
    elif time >= burn_time and parachute(altitude) is False:
        avg = 0
        drag = 1 / 2 * area * D * density * velocity ** 2
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



import matplotlib.pyplot as plt

def show_density():
    x = tim
    y = den
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Density (kg/m^3)")
    plt.show()

def show_altitude():
    x = tim
    y = alt
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.show()

def show_thrust():
    x = tim
    y = thr
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.show()  

def print_maxes():
    print("--- Maxes ---")
    print(f"Max Altitude: {max(alt):.0f} m")
    print(f"Max Velocity: {max(vel):.0f} m/s")
    print(f"Max Net Force: {max(net):.0f} N")
    print(f"Min Density: {min(den):.4f} kg/m^3")


print_maxes()
# show_density()
# show_thrust()
show_altitude()
show_density()
