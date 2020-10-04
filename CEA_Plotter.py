import matplotlib.pyplot as plt
import matplotlib as mpl
from math import *
from prop_calc import a_chamber,exhaust_vel,R,molecular_wht,mdot_tot,a_throat
mpl.use('Qt5Agg')
with open("OF_1point5") as f:
    lines = f.readlines()

    p = [line.split()[0] for line in lines]
    del p[0]

    rho = [line.split()[1] for line in lines]
    del rho[0]
    h = [line.split()[2] for line in lines]
    del h[0]
    isp = [line.split()[3] for line in lines]
    del isp[0]
    gam = [line.split()[4] for line in lines]
    del gam[0]
    m =[line.split()[5] for line in lines]
    del m[0]
    cp = [line.split()[6] for line in lines]
    del cp[0]
    t = [line.split()[7] for line in lines]
    del t[0]

p = [float(i) for i in p]
rho = [float(i) for i in rho]
h = [float(i) for i in h]
isp = [float(i) for i in isp]
gam = [float(i) for i in gam]
m = [float(i) for i in m]
cp = [float(i) for i in cp]
t = [float(i) for i in t]

chamber_pressures = p[::2]
throat_pressures = p[1::2]

chamber_densities = rho[::2]
throat_densities = rho[1::2]

chamber_temp = t[::2]
throat_temp = t[1::2]

chamber_gamma = gam[::2]
throat_gamma = gam[1::2]


exhaust_vels = []
mdot_tot_vals = []
a_throat_vals = []
r_throat_vals = []
a_chamber_vals = []
r_chamber_vals = []

#Lower OF ratio, lower burn temperature in the chamber
#L* is the characteristic length of the combustion chamber and for LOX/ethanol is between 2.5m-3m
l_star = 2.5
len_chamber = 0.1
for i in range(len(chamber_gamma)):
    calc_exhaust_vel = exhaust_vel(R/molecular_wht,chamber_gamma[i],chamber_temp[i],101325.,chamber_pressures[i]*100000)

    exhaust_vels.append(calc_exhaust_vel)
    calc_mdot_tot = mdot_tot(1500,calc_exhaust_vel)

    mdot_tot_vals.append(calc_mdot_tot)

    calc_a_throat = a_throat(calc_mdot_tot,chamber_pressures[i]*100000,chamber_gamma[i],chamber_temp[i])

    a_throat_vals.append(calc_a_throat)
    r_throat_vals.append(sqrt(calc_a_throat/pi))

    a_chamber_val = a_chamber(calc_a_throat)
    r_chamber_vals.append(sqrt(a_chamber_val/pi))

    a_chamber_vals.append(a_chamber_val)
fig,axs = plt.subplots(2,3)
axs[0,0].plot(chamber_pressures,r_throat_vals,'o')
axs[0,0].set_title('Chamber Pressure vs. Radius of Throat')

axs[0,1].plot(chamber_pressures,mdot_tot_vals,'o')
axs[0,1].set_title('Chamber Pressure vs. Total Mass Flow Rate')

axs[0,2].plot(chamber_pressures,chamber_gamma,'o')
axs[0,2].set_title('Chamber Pressure vs. Chamber gamma')
axs[1,0].plot(chamber_pressures,chamber_temp,'o')
axs[1,0].set_title('Chamber Pressure vs. Chamber Temperature')

axs[1,1].plot(chamber_pressures,r_chamber_vals,'o')
axs[1,1].set_title('Chamber Pressure vs. Radius of Chamber')

axs[1,2].plot(chamber_pressures,exhaust_vels,'o')
axs[1,2].set_title('Chamber Pressure vs. Exhaust Velocities')

plt.show()



# fig = plt.figure()
#
# ax = fig.gca(projection = '3d')
#
# ax.plot(chamber_pressures,chamber_temp,chamber_gamma,'o')
# ax.set_xlabel('Pressure')
# ax.set_ylabel('Temp')
# ax.set_zlabel('gamma')
# plt.show()


