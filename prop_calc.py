#This file will house the calculations needed in order to check how the oxidizer and propellant will work together
#Liquid oxygen and ethanol were chosen to be the oxidizer and the propellant respectively

from math import *
import numpy as np
force = 1500 #N
g0 = 9.80665 #m/s^2
loxps = 1. #kg/s
fuelps = 1. #kg/s
R = 8.3145 #J/mol/K
molecular_wht = 27.592/1000 #kg/mol
of_ratio = lambda loxps, fuelps:loxps/fuelps

press_throat = lambda chamber_press,gamma: chamber_press*(1+(gamma-1)/2)**(-gamma/(gamma-1))

isp = lambda mdot_tot: force/mdot_tot

mdot_lox = lambda mdot_tot: mdot_tot*of_ratio/(of_ratio+1) #kg/s

mdot_fuel = lambda mdot_lox,of_ratio: mdot_lox/of_ratio

a_throat = lambda mdot_tot,chamber_press,gamma, chamber_temp: (mdot_tot/chamber_press)*sqrt((R/molecular_wht)*chamber_temp/gamma)*(1+(gamma-1)/2)**((gamma+1)/(2*(gamma-1)))

temp_throat = lambda temp_combustion,gamma: temp_combustion*(1/(1+(gamma-1)/2))

exhaust_vel = lambda r_val,gamma,chamber_temp,exit_press,chamber_press: sqrt(2.*(r_val*gamma*chamber_temp/(gamma-1))*(1-(exit_press/chamber_press)**((gamma-1)/gamma)))

mdot_tot = lambda force,exhaust_vel: force/exhaust_vel

a_chamber = lambda a_throat: a_throat*6
vol_frustum = lambda r_throat,r_chamber,len_frust: (1/3)*pi*len_frust*(r_throat**2 + r_chamber**2 + (r_throat+r_chamber))
#a_chamber = lambda a_throat,l_star,len_chamber: (l_star*a_throat)/(1.1*len_chamber)
vol_chamber = lambda char_len,a_throat: char_len*a_throat
def diameter_c(diameter_t, theta,vol_c,diam_c,len_c):

    pass