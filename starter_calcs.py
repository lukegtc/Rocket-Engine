import numpy as np
import scipy as sp
from scipy.optimize import fsolve
from math import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import openpyxl as op

mpl.use('Qt5Agg')
p1 = 100000*5#Chamber pressure (Pa) (Before throat) MUST BE LARGER THAN p0
p0 = 101325 #outside pressure (Pa)
T1 = 3066 #chamber temp (K)
thrust_goal = 1500 #Thrust desired (N)
gamma = 1.19

r = 301.337 #gas constant
radius_throat = 0.029650 #meters
thetas = []
press_ratio = p0/p1

critical_temp_ratio = (2*gamma*r)/(gamma-1)

critical_press_ratio = ((2/(gamma+1))**(gamma/(gamma-1)))

critical_throat_vel = sqrt((2*gamma*r*T1)/(gamma+1))

exit_vel = sqrt(critical_temp_ratio*T1*(1-(press_ratio**((gamma-1)/gamma))))

temp_exit = T1*press_ratio**((gamma-1)/gamma)
a_exit = sqrt(gamma*r*temp_exit)
mach_exit = exit_vel/a_exit

prandtl_eq = lambda mach_num: sqrt((gamma+1)/(gamma-1)) * atan(sqrt((gamma-1)/(gamma+1)*(mach_num**2-1))) - atan(sqrt(mach_num**2-1))

max_theta = 0.5*prandtl_eq(mach_exit)

dtheta = abs((pi/2-max_theta)-round(pi/2-max_theta,1))


n = max_theta*2

mach_nums = []
points = []
line_slopesR = []
line_slopesL = []
LR = []
for i in np.arange(dtheta,n,dtheta):
    thetas.append(i)

    func = lambda x : i-prandtl_eq(x)
    x_vals = [1,1.01*mach_exit]
    mach_nums.append(sp.optimize.bisect(func,x_vals[0],x_vals[1]))
    points.append(radius_throat*tan(i))
    line_slopesR.append(-1/tan(i))
    LR.append(tan(i+asin(1/sp.optimize.bisect(func,x_vals[0],x_vals[1]))))
    line_slopesL.append(1/tan(i))


for j in range(len(points)):
    P1 = [0,radius_throat]
    P2 = [points[j],0]

    plt.plot(P2,P1,'r')
x_points = []
y_points = []
for c in range(len(points)):

    x_p = [points[c], (radius_throat+line_slopesL[c]*points[c])/(line_slopesL[c]-line_slopesR[-1])]
    y_p = [0,line_slopesR[-1]*(radius_throat+line_slopesL[c]*points[c])/(line_slopesL[c]-line_slopesR[-1]) + radius_throat]

    plt.plot(x_p,y_p,'b')

xw1 = (radius_throat+line_slopesL[0]*points[0])/(line_slopesL[0]-tan(max_theta))
yw1 = (tan(radius_throat)*xw1 + radius_throat)
DTW = tan(max_theta)/(len(points)-1)
xw = [xw1]
yw = [yw1]
for k in range(1,len(points)):
    s = tan(max_theta)-(k-1)*DTW
    b = yw[k-1]-s*xw[k-1]
    xw.append((b+line_slopesL[k]*points[k])/(line_slopesL[k]-s))
    yw.append(s*xw[k]+b)
    xp3 = [(radius_throat+line_slopesL[k]*points[k])/(line_slopesL[k]-line_slopesR[-1]),xw[k]]
    yp3 = [line_slopesR[-1]*(radius_throat+line_slopesL[k]*points[k])/(line_slopesL[k]-line_slopesR[-1]) + radius_throat,yw[k]]
    plt.plot(xp3,yp3,'g')
xw.insert(0,0)
yw.insert(0,radius_throat)

new_set = np.transpose([xw,yw])


new_set = new_set.tolist()
wb = op.Workbook()
ws = wb.active
for i in new_set:

    ws.append(i)

wb.save(filename="nozzle_points.xlsx")
wb.close()
plt.plot(xw,yw)

radius_exit = max(yw)
print(yw[-1])
ar = (radius_throat/radius_exit)**2
print(radius_exit)
plt.show()
