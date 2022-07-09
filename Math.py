import pandas as pd
import numpy as np

atm = pd.read_csv("atmdata.csv")
thrust = pd.read_csv("thrust.csv")
Coefficient = pd.read_csv("RASaero.csv")



def air_density(altitude):
    return atm[atm["Altitude[m]"] <= altitude].iloc[-1]["Density[kg/m3]"]


def Thrust(time):
    return thrust[thrust["Time"] <= time].iloc[-1]["Corrected Thrust"]

def CD(mach):
    return Coefficient[Coefficient["Mach"] <= mach].iloc[-1]["CD"]

def SOS(altitude):
    return atm[atm["Altitude[m]"] <= altitude].iloc[-1]["Speed of sound[m/s]"]

# Initial Condiitons
time = 0
inc = 0.5
wet = 120
fuel = 60
gravity = -9.81
net_force = wet*gravity
burn_time = 19.43
gradient = fuel/burn_time
velocity = 0
drag = 0
area = 0.025
parea = 3.57
pCd = 2.2
altitude = 400
density = air_density(altitude)
Cd = 1.236
avg = Thrust(time)
sps = SOS(altitude)
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
CDD = []
ss = []

while time < 10000:
    density = air_density(altitude)
    avg = Thrust(time)
    sps = SOS(altitude)
    mach = velocity/sps
    Cd = CD(mach)
    thr.append(avg)
    tim.append(time)
    alt.append(altitude)
    vel.append(velocity)
    net.append(net_force)
    den.append(density)
    CDD.append(Cd)
    ss.append(sps)
    mac.append(mach)
    if thrustactive(burn_time) is True:
        wet = wet - (gradient*inc)
        drag = 1/2*area*Cd*density*velocity**2
        net_force = avg - wet*gravity - drag
        acceleration = net_force/wet
        velocity = velocity + acceleration*inc
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        time += inc

    elif time >= burn_time and parachute(altitude) is False:
        avg = 0
        drag = 1 / 2 * area * Cd * density * velocity ** 2
        net_force = wet*gravity - drag
        acceleration = net_force / wet
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        velocity = velocity + (acceleration * inc)
        time += inc

    else:
        avg = 0
        drag = 1 / 2 * parea * pCd * density * (velocity ** 2)
        net_force = wet*gravity + drag
        acceleration = net_force / wet
        altitude = (velocity * inc + (1 / 2 * acceleration * inc ** 2)) + altitude
        velocity = velocity + (acceleration * inc)
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

def show_CD():
    x = tim
    y = CDD
    plt.plot(x,y)
    plt.show()


def print_maxes():
    print("--- Maxes ---")
    print(f"Max Altitude: {max(alt):.0f} m")
    print(f"Min Velocity: {min(vel):.0f} m/s")
    print(f"Max Velocity: {max(vel):.0f} m/s")
    print(f"Max Net Force: {max(net):.0f} N")
    print(f"Min Density: {min(den):.4f} kg/m^3")
    print(f"Min CD: {min(CDD):.4f}")
    print(f"Max mach: {max(mac):.4f}")

print_maxes()
