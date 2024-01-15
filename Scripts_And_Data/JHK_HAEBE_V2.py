#program that creates color-color diagrams to make checks on stars

#imports
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from numpy import nan
import numpy as np
import pandas as pd
import sys

#initialization
total 			= 0
JHK_arr 		= ['J', 'H', 'K']
redden2MASS_arr	= ['A_J', 'A_H', 'A_K']
WISE_arr		= ['W1','W2','W3','W4']
reddenWISE_arr	= ['A_W1','A_W2','A_W3','A_W4']

f1 = plt.figure()
f2 = plt.figure()
ax1 = f1.add_subplot(111)
ax2 = f2.add_subplot(111)

#NEED TO CHECK: WHETHER BV DATA IS AVAILABLE FOR REDDENING, WHETHER FLAGS ARE OK, WHETHER DATA IS MISSING, AND WHETHER FITS WITHIN HERNANDEZ BOX
#function to get and initially process data from CSV file using pandas
def dataGetter(x_obj):
	mag_list = []
	with open('MAIN_DATA.csv', 'rb') as csvfile:
		mycsv = pd.read_csv(csvfile)

		#2MASS magnitudes
    	spot = mycsv['2MASS_FLAG'][x_obj]
    	for i in xrange(0, len(JHK_arr)):
    		if spot[i] == ('0' or 'H'):
    			mag_list.append(float(mycsv[JHK_arr[i]][x_obj]) - float(mycsv[redden2MASS_arr[i]][x_obj]))
    		else: 
    			mag_list.append(float(nan))

    	#WISE magnitudes
    	spot = mycsv['WISE_FLAG'][x_obj]
    	for i in xrange(0, len(WISE_arr)):
    		if spot[i] == ('0' or 'H'):
    			mag_list.append(float(mycsv[WISE_arr[i]][x_obj]) - float(mycsv[reddenWISE_arr[i]][x_obj]))
    		else: 
    			mag_list.append(float(nan))

 	mag_list.append(mycsv['MAIN_ID'][x_obj])
	mag_tup = tuple(mag_list)
	return mag_tup


#Need to switch to do 136, 137...also need to switch i range to from 0 to 2
#for z in [132]:
for z in xrange(0, 144, 4):
	for i in xrange(0, 4):
		x_obj = z + i
		#using function call to output data needed
		J,H,K, W1,W2,W3,W4, ID = dataGetter(x_obj)
		#creating colors to act as check from Hernandez et al.
		JH = J - H
		HK = H - K

		#for setting up flux data, dereddened flux conversion from magnitudes, note the conversion factors change
		if ( (HK) < -3.0/2.0*( (JH) - 23.0/15.0) and (HK) > ((JH) - (331.0/560.0))*-28.0/25.0 and (JH) > (14.0/11.0*(HK) - 3.0/5.0) and (JH) < (65.0/53.0*(HK) + 1.0/53.0) ):
			ax1.scatter(HK, JH, color = 'orange')
			ax1.annotate(ID, xy = (HK, JH), xytext = (HK - 0.009, JH + 0.005), fontsize = 5)
			if (W3-W4) >= 1.8:
				print 'I'
				ax2.scatter(J - W4, J - W1, color = 'orange', marker = "o", linewidths = 1.3, s = 60)
				ax2.scatter(J - W4, J - W1, edgecolor = 'red', marker = "o", linewidths = 13, s = 1.4, facecolor = 'none')
				ax2.annotate(ID, xy = (J - W4, J - W1), xytext = (J - W4, J - W1 + 0.01), fontsize = 6.5)	
			elif math.isnan(W3) == False and math.isnan(W4) == False:
				print 'II'
				ax2.scatter(J - W4, J - W1, color = 'orange', marker = "o", linewidths = 1.3, s = 60)
				ax2.annotate(ID, xy = (J - W4, J - W1), xytext = (J - W4, J - W1 + 0.01), fontsize = 6.5)
			total += 1
			#print 'a', x_obj, HK, JH

		elif ((HK) < -0.890065348664074 * ((JH) - 0.57184917296716) and (HK) > -0.861286747696601 * ((JH) + 0.0147349830253168) and \
			(JH) > 1.62175790018995*(HK)-0.424174147193922 and (JH) < 1.31575306101884*(HK)-0.00950529799682048):
			ax1.scatter(HK, JH, color = 'purple')
			ax1.annotate(ID, xy = (HK, JH), xytext = (HK + 0.008, JH + 0.005), fontsize = 5)
			if (W3-W4) >= 1.8:
				print 'I'
				ax2.scatter(J - W4, J - W1, color = 'purple', marker = "o", linewidths = 1.3, s = 60)
				ax2.scatter(J - W4, J - W1, edgecolor = 'red', marker = "o", linewidths = 13, s = 1.4, facecolor = 'none')
				ax2.annotate(ID, xy = (J - W4, J - W1), xytext = (J - W4, J - W1 + 0.01), fontsize = 6.5)
			elif math.isnan(W3) == False and math.isnan(W4) == False:
				print 'II'
				ax2.scatter(J - W4, J - W1, color = 'purple', marker = "o", linewidths = 1.3, s = 60)
				ax2.annotate(ID, xy = (J - W4, J - W1), xytext = (J - W4, J - W1 + 0.01), fontsize = 6.5)
				ax2.annotate(ID, xy = (J - W4, J - W1), xytext = (J - W4, J - W1 + 0.01), fontsize = 6.5)
			total += 1
		else:
			ax1.scatter(HK, JH, color = 'pink')
			ax1.annotate(ID, xy = (HK, JH), xytext = (HK + 0.005, JH + 0.005), fontsize = 5)
			total += 1
			# print 'c', x_obj, HK, JH, ID


A_VperJ = 3.55
A_HperJ = 0.624
A_KperJ = 0.382

dwarf_JH_arr = []		#arrays for Bessel and Brett colors of dwarfs
dwarf_HK_arr = []

giant_JH_arr = []		#arrays for Bessel and Brett colors of giants
giant_HK_arr = []

r_linex_A7 = [0.025]	#arrays for reddening lines
r_liney_A7 = [0.09]
r_linex_B8 = [-0.035]
r_liney_B8 = [-0.09]

CTTS_JH = []			#Arrays for CTTS Locus
CTTS_HK = np.arange(0.2, 1, 0.1)

#getting JHK data for Bessel and Brett colors of dwarfs
with open('bessell_brett.dwarf', 'r') as f:
	i = 0
	lines = f.readlines()
	for line in lines:
		if i != 0:
			#specifying data in column to put into array
			dwarf_JH_arr.append(float(line[23:30]))
			dwarf_HK_arr.append(float(line[30:39]))
		i += 1 

#getting JHK data for Bessel and Brett colors of giants
with open('bessell_brett.giant', 'r') as f:
	lines = f.readlines()
	i = 0
	for line in lines:
		if i != 0:
			#specifying data in column to put into array
			giant_JH_arr.append(float(line[23:30]))
			giant_HK_arr.append(float(line[30:39]))
		i += 1 

#creating data for CTTS Locus
for HK in CTTS_HK:
	CTTS_JH.append(0.5*HK + 0.52)

#creating data for reddening lines
i = 0
for Av in np.arange(0, 5, 1):
	r_linex_A7.append(r_linex_A7[i] + (((1.0/A_VperJ)  * A_HperJ)  - (1.0/A_VperJ)  * A_KperJ)*Av)
	r_liney_A7.append(r_liney_A7[i] + ((1.0/A_VperJ)               - (1.0/A_VperJ)  * A_HperJ)*Av)

	r_linex_B8.append(r_linex_B8[i] + (((1.0/A_VperJ)  * A_HperJ)  - (1.0/A_VperJ)  * A_KperJ)*Av)
	r_liney_B8.append(r_liney_B8[i] + ((1.0/A_VperJ)               - (1.0/A_VperJ)  * A_HperJ)*Av)
	i += 1

#plotting JHK data from Bessel and Brett colors and HAEBE stars 
ax1.plot(dwarf_HK_arr, dwarf_JH_arr, linewidth = 2)
ax1.plot(giant_HK_arr, giant_JH_arr, linewidth = 2)

#plotting reddening lines for A7 and B8 stars
ax1.plot(r_linex_A7, r_liney_A7, color = 'r', linestyle = '--', linewidth = 2, label = 'Reddening Lines')
ax1.plot(r_linex_B8, r_liney_B8, color = 'r', linestyle = '--', linewidth = 2)

#plotting CTTS Locus line
ax1.plot(CTTS_HK, CTTS_JH, color = 'black', label = 'CTTS Locus', linewidth = 2)

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
#plotting approximate box surrounding likely HAEBE stars
ax1.plot(x_box, y_box, color = 'brown', linestyle = ':', linewidth = 2, label = 'Hernandez Herbig Ae/Be Region')

#vertices for HAEBE box
verts = [
	(0.263555, 0.337268), # P0
	(0.396534, 0.218908), # P1
	(0.164894, -0.156756),  # P2
    (-0.0024022, -0.012666),  # P3
    (0.263555, 0.337268)  # IGNORE
    ]

path = Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='none', lw=2)      
x_box, y_box = zip(*verts) #creating x- and y-values for box that goes along with path and patch to form box
#plotting approximate box surrounding likely HAEBE stars
ax1.plot(x_box, y_box, color = 'black', linestyle = ':', linewidth = 2, label = 'Herbig Ae/Be Expected TDs')

#2MASS graph formatting
ax1.set_ylabel('J - H', fontsize = 15, fontweight = 'bold')         #y-axis title, color made from 2MASS J-H
ax1.set_xlabel('H - K', fontsize = 15, fontweight = 'bold')         #x-axis title, color made from 2MASS H-K
ax1.set_title('Dereddened JHK Diagram for Target HAEBE Stars', fontsize = 16, fontweight = 'bold')    #title of plot
ax1.set_xlim(-0.43, 2.3)       		#setting x-axis limits, zoom out
ax1.set_ylim(-0.5, 2.5) 	    	#setting y-axis limits, zoom out
# ax1.set_xlim(-0.2, 1.1)       	#setting x-axis limits, zoom in
# ax1.set_ylim(-0.2, 1.15) 	    	#setting y-axis limits, zoom in
ax1.legend(loc = 2, prop={'size':13}) 	    #legend of the plot, based on labels

#WISE graph formatting
#adding in some points that are irrelevant, quick way to get in labeling
ax2.scatter(-1, -1, color = 'orange', marker = "o", linewidths = 1.3, s = 70, label = 'Hernandez Herbig Ae/Be')
ax2.scatter(-1, -1, color = 'purple', marker = "o", linewidths = 1.3, s = 60, label = 'TD Herbig Ae/Be')
ax2.scatter(-1, -1, edgecolor = 'red', marker = "o", linewidths = 13, s = 1.4, facecolor = 'none', label = 'Group I Herbig Ae/Be Stars')

#formatting graphing
ax2.set_ylabel('J - [3.4]', fontsize = 15, fontweight = 'bold')         #y-axis title, color made from 2MASS J - WISE 3.4 microns
ax2.set_xlabel('J - [22]', fontsize = 15, fontweight = 'bold')         #x-axis title, color made from 2MASS J - WISE 22 microns
ax2.set_title('Color-Color Diagram for Transition Disk Identification', fontsize = 16, fontweight = 'bold')    #title of plot
ax2.set_xlim(2, 10)     #setting x-axis limits
ax2.set_ylim(-0.1, 3.2) 	    	#setting y-axis limits
ax2.legend(loc = 2) 	    #legend of the plot, based on labels


plt.minorticks_on()	 	    #display plot with minor ticks

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
plt.tick_params(direction='in', width=1.2, which='minor', labelsize=15)
plt.tick_params(direction='in', width=1.2, which='major', labelsize=15)



print total
plt.show()

sys.exit()