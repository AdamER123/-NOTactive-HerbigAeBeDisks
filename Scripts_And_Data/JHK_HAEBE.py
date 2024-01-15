# JHK color-color diagram of HAEBE stars

#imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import scipy as sp


#initializing arrays used for taking data from files

#arrays for Bessel and Brett colors of dwarfs
dwarf_JH_arr = []
dwarf_HK_arr = []

#arrays for Bessel and Brett colors of giants
giant_JH_arr = []
giant_HK_arr = []

#arrays for Bessel and Brett colors of HAEBE stars
HAEBE_HK_set1 = []
HAEBE_JH_set1 = []

HAEBE_HK_set2 = []
HAEBE_JH_set2 = []

#arrays for reddening lines
r_linex_A7 = [0.025]
r_liney_A7 = [0.09]
r_linex_B8 = [-0.035]
r_liney_B8 = [-0.09]

#Arrays for CTTS Locus
CTTS_JH = []
CTTS_HK = np.arange(0.2, 1, 0.1)

#vertices for HAEBE box
verts = [
	(0.27, 0.35), # P0
	(0.55, 0.1), # P1
	(1.10, 0.8),  # P2
    (0.8, 1.00),  # P3
    (0.27, 0.35)  # IGNORE
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY
         ]        # controlling path of box to close it in

path = Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='none', lw=2)      
x_box, y_box = zip(*verts) #creating x- and y-values for box that goes along with path and patch to form box

#getting JHK data for Bessel and Brett colors of dwarfs
with open('bessell_brett.dwarf', 'r') as f:
	i = 0
	table = f.readlines()
	for line in table:
		if i != 0:
			#specifying data in column to put into array
			dwarf_JH_arr.append(float(line[23:30]))
			dwarf_HK_arr.append(float(line[30:39]))
		i += 1 

#getting JHK data for Bessel and Brett colors of giants
with open('bessell_brett.giant', 'r') as f:
	table = f.readlines()
	i = 0
	for line in table:
		if i != 0:
			#specifying data in column to put into array
			giant_JH_arr.append(float(line[23:30]))
			giant_HK_arr.append(float(line[30:39]))
		i += 1 

#getting JHK data for Bessel and Brett colors of HAEBE stars from tables containing 2MASS data
with open('HAEBEdata_2MASS.txt', 'r') as f:
	table = f.readlines()
	line_data = table[103:]
	i = 0
	err = 0 #number of times cannot find 2MASS data for a star
	for line in line_data:
		if i >= 0 and i <= 94 and i != 15 and i != 87 and i != 88 and i != 92 and line[-21:-11] != '        - ' and line[-31:-21] != '        - ':
			#specifying data in column to put into array
			HAEBE_HK_set1.append(float(line[-21:-11]))
			HAEBE_JH_set1.append(float(line[-31:-21]))
			print i
		elif i >= 94 and line[-21:-11] != '        - ' and line[-31:-21] != '        - ':
			#specifying data in column to put into array
			HAEBE_HK_set2.append(float(line[-21:-11]))
			HAEBE_JH_set2.append(float(line[-31:-21]))
			print i
		else:
			err += 1
		i += 1


#creating data for reddening lines
i = 0
for Av in range(0, 15, 5):
	r_linex_A7.append(r_linex_A7[i] + 0.068*Av)
	r_liney_A7.append(r_liney_A7[i] + 0.106*Av)

	r_linex_B8.append(r_linex_B8[i] + 0.068*Av)
	r_liney_B8.append(r_liney_B8[i] + 0.106*Av)
	i += 1


#creating data for CTTS Locus
for HK in CTTS_HK:
	CTTS_JH.append(0.5*HK + 0.52)


#plotting JHK data from Bessel and Brett colors and HAEBE stars 
plt.plot(dwarf_HK_arr, dwarf_JH_arr)
plt.plot(giant_HK_arr, giant_JH_arr)

#plotting reddening lines for A7 and B8 stars
plt.plot(r_linex_A7, r_liney_A7, color = 'r', linestyle = '--', label = 'Reddening Lines')
plt.plot(r_linex_B8, r_liney_B8, color = 'r', linestyle = '--')

#plotting CTTS Locus line
plt.plot(CTTS_HK, CTTS_JH, color = 'black', label = 'CTTS Locus')

#plotting approximate box surrounding likely HAEBE stars
plt.plot(x_box, y_box, color = 'brown', linestyle = ':')

#plotting stars from catalogs
plt.scatter(HAEBE_HK_set1, HAEBE_JH_set1, color = 'indigo', marker = "+", label = 'HAEBE Stars, Herbst Catalog')
plt.scatter(HAEBE_HK_set2, HAEBE_JH_set2, color = 'orange', marker = "*", label = 'HAEBE Stars, The Catalog')

plt.ylabel('J - H')        #y-axis title, color made from 2MASS J-H
plt.xlabel('H - K')        #x-axis title, color made from 2MASS H-K
plt.title('JHK Diagram for HAEBE Star Determination')    #title of plot

#legend of the plot, based on labels
plt.legend() 

#display plot with minor ticks
plt.minorticks_on()
plt.show()


print "done", err  #printing number of times cannot find 2MASS data for a star