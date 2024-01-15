#program that creates color-color diagrams to make checks on stars; uses theoretically modeled JHK data
#This comes from interpolating between the model data and the filter transmissions to find what observed flux would be through some passband
#This version is also V2 (more efficient than first)

#imports
import glob
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np
from scipy.interpolate import interp1d
import sys


f1 = plt.figure()
f2 = plt.figure()
f3 = plt.figure()
ax1 = f1.add_subplot(111)
ax2 = f2.add_subplot(111)
ax3 = f3.add_subplot(111)

#for controlling which SED name is used
objNum = 3


#file names; JHK and WISE data using passbands for HAEBE stars
filterNames = ['2MASSFilterJ.txt', '2MASSFilterH.txt', '2MASSFilterKs.txt', 'WISE1.txt', 'WISE2.txt', 'WISE3.txt', 'WISE4.txt']
lamFilter 	= [1.235, 1.662, 2.159, 3.368, 4.618, 12.082, 22.194]
zeroPts 	= [3.129*pow(10,-13), 1.133*pow(10,-13), 4.283*pow(10,-14), 8.1787*pow(10,-15), 2.4150*pow(10,-15), 6.5151*pow(10,-17), 5.0901*pow(10,-18)]
zeroptDict	= dict(zip(filterNames, zeroPts))
markSym 	= ['o', '+', '^', 's'] 				#For spectral type/age ("star type")
markSize 	= [5, 20, 40, 80] 					#For epsilons
markColor 	= ['r', 'g', 'b', 'purple'] 		#For Mdots


####################################################THEORETICAL COLOR CALCULATIONS##########################################################3


folderNames = []
for file in glob.glob('A2 HAEBE Model/A2_t3_modA/*'):
	name = file
	folderNames.append(name[26:])

modelData = []
for folder in folderNames:
	for file in glob.glob('A2 HAEBE Model/A2_t3_modA/' + folder + '/*.dat'):
		modelData.append(file)

filteredModelNames = filter(lambda x: 'prop' not in x and 'alb0' in x, modelData)

count = 0
for i in filteredModelNames:
	name = filteredModelNames[count] 
	ind = name.index("modA", 25)
	filteredModelNames[count] = name[ind:]
	count += 1
print 'Number of models used is ', count


#Function for reading in model SED flux data
def fluxSEDModel(i, name, count):
	#Declaring variables for model SED
	lambdaModel 			= np.array([])
	lambda_F_lambda_Model 	= np.array([])
	star 					= []
	wall 					= []
	thermal 				= []
	scattered 				= []
				
	#Reading in data; Cutting out extraneous lines from file
	f = 'A2 HAEBE Model/A2_t3_modA/A2_t3_' + i + '/' + name
	dataArr = np.genfromtxt(f, skip_header = 2, usecols = (0,4,5,6,7,8))

	for j in dataArr: 
		lambdaModel = np.append(lambdaModel, j[0])
		lambda_F_lambda_Model = np.append(lambda_F_lambda_Model, (j[4] + j[3]) * np.exp(-j[5])  + j[1] + j[2] ) #This is nuFnu = (star + wall) * e^-tau + (therm + scatt) = lambda_F_lambda_Model

		if count == objNum:
			wall.append(j[3])
			star.append(j[4])
			thermal.append(j[1])
			scattered.append(j[2])

	print count, name

	if count == objNum:
		ax3.plot(np.log10(lambdaModel), np.log10(star) , label = 'Star')
		ax3.plot(np.log10(lambdaModel), np.log10(wall), label =  'Wall', linestyle = '--')
		ax3.plot(np.log10(lambdaModel), np.log10(thermal) , label = 'Thermal', linestyle = ':')
		ax3.plot(np.log10(lambdaModel), np.log10(scattered) , label = 'Scattered', linestyle = '-.')
		ax3.plot(np.log10(lambdaModel), np.log10(lambda_F_lambda_Model), label = 'Sum')

	return lambdaModel, lambda_F_lambda_Model

#Function for producing magnitudes from theoretically observed fluxes (based on filter integration from interpolated SED)
def interpSEDTransmission(lambdaModel, lambda_F_lambda_Model, count):
	magFilter = []
	fluxList = []

	#For a given model looping through different filters to get theoretically observed data
	for j in filterNames:
		dataArr = np.genfromtxt('FilterIntegration/' + j, usecols = (0, 1))
		lambdaFilter = []
		transmissionFilter = []

		for k in dataArr:
			if j[0:4] == 'WISE': 	#getting transmission and wavelength from WISE data file
				lambdaFilter.append(k[0])
				transmissionFilter.append(k[1])
			else: 					#getting transmission and wavelength from 2MASS data file
				lambdaFilter.append(k[0])
				transmissionFilter.append(k[1])

		#Using a built-in interpolation function to find where a given model flux would be for a given filter wavelength
		f1 = interp1d(lambdaModel,lambda_F_lambda_Model)
		f2 = f1(lambdaFilter)/lambdaFilter				#Creating interpolated array of F_lambda across all filter wavelengths, in case wavelengths don't match btwn model, filter
		TF = transmissionFilter*f2 						#With theoretical data, multiplying transmission in to find flux a transmission would observe from model
		
		trapsumTF = 0.0
		trapsumT = 0.0

		#performing trapezoidal sum on interpolated SED data and transmission filter
		for k in range(0,len(lambdaFilter)-1):
			trapsumTF = trapsumTF + 0.5*(TF[k]+TF[k+1])*(lambdaFilter[k+1] - lambdaFilter[k])
			trapsumT  = trapsumT  + 0.5*(transmissionFilter[k]+transmissionFilter[k+1])*(lambdaFilter[k+1] - lambdaFilter[k])
		
		#defining flux from ratio of numerical integrations (to normalize)
		fluxList.append(trapsumTF/trapsumT)
		flux = trapsumTF/trapsumT * 1e-7 #converting from erg/s -> W

		#for a given filter, converting the flux appropriately into a magnitude so they can be plotted as colors
		magFilter.append(-2.5 * np.log10(flux / zeroptDict[j] ))

	if count == objNum:
		ax3.scatter(np.log10(lamFilter), np.log10(np.array(fluxList) * lamFilter))
	return magFilter #array of magnitudes from theoretical fluxes

#Function for plotting colors for a given star
def fluxPlot(magFilter, name, starSym, starSize, starColor):
	if starSize > 20:
		opac = 0.3
	elif starSize == 20: 
		opac = 0.6
	else:
		opac = 1.0

	#Plotting JHK vals
	ax1.scatter(magFilter[1] - magFilter[2], magFilter[0] - magFilter[1], color = starColor, marker = starSym, s = starSize, alpha = opac) # (H-K, J-H) -> (x, y)
	# print name
	
	#Plotting 2MASS - WISE vals
	if magFilter[5] - magFilter[6] >= 1.8:
		ax2.scatter(magFilter[0] - magFilter[6], magFilter[0] - magFilter[3], color = starColor, marker = starSym, linewidths = 1.3, s = starSize, alpha = opac) #J - W4, J - W1
		ax2.scatter(magFilter[0] - magFilter[6], magFilter[0] - magFilter[3], edgecolor = 'red', marker = "o", linewidths = 13, s = 1.4, facecolor = 'none', alpha = opac)
	else:
		ax2.scatter(magFilter[0] - magFilter[6], magFilter[0] - magFilter[3], color = starColor, marker = starSym, linewidths = 1.3, s = starSize, alpha = opac)



count = 0
starSym = markSym[0]
'''
e0p001: 0 to 5 -> 6
e0p01: 6 to 17 -> 9
e0p1: 18 to 29 -> 11
e1: 30 to 41 -> 11
'''
#Looping through HAEBE models based on parameters
for name in filteredModelNames:
	#For different file names in given folder of epsilons
	if name.find('e0p1') != -1:
		i = 'e0p1'
		starSize = markSize[1]
	elif name.find('e1') != -1:
		i = 'e1'
		starSize = markSize[0]
	elif name.find('e0p01') != -1:
		i = 'e0p01'
		starSize = markSize[2]
	else:
		i = 'e0p001'
		starSize = markSize[3]

	if name.find('mp1em6') != -1:
		starColor = markColor[0]
	elif name.find('mp1em7') != -1:
		starColor = markColor[1]
	elif name.find('mp1em8') != -1:
		starColor = markColor[2]
	else:
		starColor = markColor[3]


	#Calling function that returns lambda and lambda_F_lambda_Model of a given model HAEBE SED
	lambdaModel, lambda_F_lambda_Model = fluxSEDModel(i, name, count)
	magFilter = interpSEDTransmission(lambdaModel, lambda_F_lambda_Model, count)
	fluxPlot(magFilter, name, starSym, starSize, starColor)
	count += 1

print count

ax3.set_ylim(-20, -5)
ax3.legend()

######################################################ADDING APPRPORIATE REFERENCE LINES OF COLOR-COLOR DIAGRAMS##################################################################

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

######################################################FORMATTING GRAPHS##################################################################

#2MASS graph formatting
ax1.set_ylabel('J - H', fontsize = 15, fontweight = 'bold')         #y-axis title, color made from 2MASS J-H
ax1.set_xlabel('H - K', fontsize = 15, fontweight = 'bold')         #x-axis title, color made from 2MASS H-K
ax1.set_title('Theoretical JHK Diagram for HAEBE Stars', fontsize = 16, fontweight = 'bold')    #title of plot
ax1.set_xlim(-0.2, 1.1)       				#setting x-axis limits, zoom out
ax1.set_ylim(-0.2, 1.3) 	    			#setting y-axis limits, zoom out
ax1.legend(loc = 2, prop={'size':10}) 	    #legend of the plot, based on labels


#formatting graphing
ax2.set_ylabel('J - [3.4]', fontsize = 15, fontweight = 'bold')         #y-axis title, color made from 2MASS J - WISE 3.4 microns
ax2.set_xlabel('J - [22]', fontsize = 15, fontweight = 'bold')         #x-axis title, color made from 2MASS J - WISE 22 microns
ax2.set_title('Theoretical Color-Color Diagram for Transition Disk Identification', fontsize = 16, fontweight = 'bold')    #title of plot
ax2.set_xlim(6.2, 9)     		#setting x-axis limits
ax2.set_ylim(1.2, 3) 	    	#setting y-axis limits


plt.minorticks_on()	 	    #display plot with minor ticks

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)
plt.tick_params(direction='in', width=1.2, which='minor', labelsize=15)
plt.tick_params(direction='in', width=1.2, which='major', labelsize=15)


plt.show()

sys.exit()