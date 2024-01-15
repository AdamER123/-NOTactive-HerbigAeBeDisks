#Program to check SED Output

#imports
import matplotlib.pyplot as plt
from numpy import log10
import numpy as np
from scipy.interpolate import interp1d
import sys

#arrays for filters, wavelengths, colors for plot
filterNames 	= ['2MASSFilterJ.txt', '2MASSFilterH.txt', '2MASSFilterKs.txt', 'WISE1.txt', 'WISE2.txt', 'WISE3.txt', 'WISE4.txt', 'IRACFilter3p6.txt', 'IRACFilter4p5.txt', 'IRACFilter5p8.txt', 'IRACFilter8p0.txt', \
						'MIPSFilter24p0.txt']
lamFilter 		= [1.235, 1.662, 2.159, 3.368, 4.618, 12.082, 22.194, 3.6, 4.5, 5.8, 8.0, 24.0]
colors 			= ['blue', 'blue', 'blue', 'green', 'green', 'green', 'green', 'orange', 'orange', 'orange', 'orange', 'red']

modelNames 		= ['modA.sed.A2.t3.mu0p25.mp1em6.e0p01.alb0.dat']#, modA.sed.A2.t3.mu0p75.mp1em7.e0p1.alb0.dat, 'modA.sed.A2.t3.mu0p25.mp1em6.e0p1.alb0.dat','modA.sed.A2.t3.mu0p25.mp1em7.e0p1.alb0.dat'] #Model names to plot with

#Function for reading in model SED flux data
def fluxSEDModel(i, name):
	with open('A2 HAEBE Model/A2_t3_modA/A2_t3_' + i + '/' + name) as f:
		#Declaring variables for model SED
		lambdaModel 				= np.array([])
		lambda_F_lambda_Model 		= np.array([])
				
		#Cutting out extraneous lines from file
		lines = f.readlines()
		line_data = lines[2:] 

		#Reading in data
		for line in line_data:
			lambdaLine = float(line[4:18])
			lambdaModel = np.append(lambdaModel, lambdaLine) 	#This is appending to a list of wavelengths associated with each flux energy
			lambda_F_lambda_Model = np.append(lambda_F_lambda_Model,  ( (float(line[100:113]) + float(line[116:130])) * np.exp(-float(line[132:145]) ) + \
				(float(line[84:98]) + float(line[68:82])) ) )  #This is nuFnu = (star + wall) * e^-tau + (therm + scatt) = lambda_F_lambda_Model

	return lambdaModel, lambda_F_lambda_Model

#Function for producing theoretically observed fluxes (based on filter integration from interpolated SED)
def interpSEDTransmission(lambdaModel, lambda_F_lambda_Model):
	F_lambda_theoretObs = np.array([])

	#For a given model looping through different filters to get theoretically observed data
	for j in filterNames:
		with open('FilterIntegration/' + j) as f:
			lambdaFilter = []
			transmissionFilter = []
			lines = f.readlines()

			#Reading in wavelength and transmission data for given passband
			for line in lines:
				if j[0:4] == 'WISE': 		#WISE
					lambdaFilter.append(float(line[0:6]))
					transmissionFilter.append(float(line[6:16]))
				elif j[0:5] == '2MASS': 	#2MASS
					lambdaFilter.append(float(line[0:7]))
					transmissionFilter.append(float(line[8:20]))
				elif j[0:4] == 'IRAC': 		#IRAC
					lambdaFilter.append(float(line[0:9]))
					transmissionFilter.append(float(line[10:22]))
				else: 						#MIPS
					lambdaFilter.append(float(line[0:7]))
					transmissionFilter.append(float(line[7:22]))


		#Using a built-in interpolation function to find where a given model flux would be for a given filter wavelength
		f1 = interp1d(lambdaModel,lambda_F_lambda_Model)
		f2 = f1(lambdaFilter)/(lambdaFilter)					#Creating interpolated array of F_lambda across all filter wavelengths, in case wavelengths don't match btwn model, filter
		TF = transmissionFilter*f2 						#With theoretical data, multiplying transmission in to find flux a transmission would observe from model

		trapsumTF = 0.0
		trapsumT = 0.0

		#performing trapezoidal sum on interpolated SED data and transmission filter
		for k in range(0,len(lambdaFilter)-1):
			trapsumTF = trapsumTF + 0.5*(TF[k]+TF[k+1])*(lambdaFilter[k+1] - lambdaFilter[k])
			trapsumT  = trapsumT  + 0.5*(transmissionFilter[k]+transmissionFilter[k+1])*(lambdaFilter[k+1] - lambdaFilter[k])

		#storing value for ratio of the two, which is really F_lambda (flux) for a given filter
		F_lambda_theoretObs = np.append(F_lambda_theoretObs, trapsumTF/trapsumT)	#Creating array of model values for integrated fluxes
		plt.scatter(log10(lambdaFilter), log10(f2 * lambdaFilter), s = 2)			#Plotting SED vals observed under some filter transmission (should lie along SED)

	plt.scatter(log10(lamFilter), log10(F_lambda_theoretObs * lamFilter), color = colors)


print modelNames
#looping through some models to output SEDs and integrated lambda_F_lambdas through different passbands
for name in modelNames:
	lambdaModel, lambda_F_lambda_Model = fluxSEDModel('e0p01', name) 								#gathering fluxes at some wavelength for a given model by summing contributions
	interpSEDTransmission(lambdaModel, lambda_F_lambda_Model) 										#interpolating model SED data, numerically integrating, and normalizing -> theoretically observed fluxes
	plt.plot(log10(lambdaModel),log10(lambda_F_lambda_Model ), label = 'My Calculated SED') 		#plotting model SED										

	plt.title('Filter Integration and SED Comparison', fontsize = 12, fontweight = 'bold')
	plt.ylabel(r'Log $\bf{\lambda F_\lambda }$', fontsize = 12, fontweight = 'bold')	#y-axis title, flux of light
	plt.xlabel(r'Log Wavelength $\bf{(\mu m)}$', fontsize = 12, fontweight = 'bold')         				#x-axis title, lambda or wavelength in microns
	plt.legend()

plt.show()

