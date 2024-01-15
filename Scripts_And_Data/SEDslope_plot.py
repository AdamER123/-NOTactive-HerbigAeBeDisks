#code for comparing HAEBE stars in Meeus et al 2001

#imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy as sp


#array of text files to loop through
stars     = ['ab_aur.txt', 'HD100546.txt', 'HD142527.txt', 'HD179218.txt', 'HD100453.txt', 'HD135344.txt', \
	         'HD139614.txt', 'HD169142.txt', 'HD104237.txt', 'HD142666.txt', 'HD144432.txt', 'HD150193.txt', 'HD163296.txt', '51_oph.txt']   


#looping through and plotting data on stars
for i in range(len(stars)):

	#opening text file for reading in data
	f = open('Meeus Stars/' + stars[i], 'r')   

	lines     = f.readlines()         #getting all the lines of the file
	line_data = lines[58:]            #taking line with data
	data      = line_data[0]          #taking the string out of the list
	w1        = float(data[47:53])    #slice of data string, w1 (wavelength = 3.4 microns)
	w2        = float(data[66:71])    #slice of data string, w2 (wavelength = 4.6 microns)
	w3        = float(data[83:89])    #slice of data string, w3 (wavelength = 12 microns)
	w4        = float(data[101:107])  #slice of data string, w4 (wavelength = 22 microns)

	f.close()                 #closing text file

	#plotting sed slopes, colors represent 
	
	if i < 4:
		plt.scatter(w3 - w4, w1 - w2, color = 'red')    #plotting colors from data
	if i >= 4 and i < 8:
		plt.scatter(w3 - w4, w1 - w2, color = 'green')  #plotting colors from data
	if i >= 8:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'blue')   #plotting colors from data

plt.ylabel('[3.4] - [4.6]')        #y-axis title, color made from w1-w2
plt.xlabel('[12]  - [22]')         #x-axis title, color made from w3-w4
plt.title('Meeus HAEBE Sample SED Slope Comparison')    #title of plot

groups = ['Group Ia', 'Group Ib', 'Group IIa']    #list of strings for each of the HAEBE groups, used in legend
class_colours = ['r','g','b']                     #colors for the groups
recs = []                                         #empty list for rectangles
for i in range(0,len(class_colours)):             #loops through colors to create rectangles corresponding to the colors representing each group
    recs.append(mpatches.Rectangle((0,0),1,1,fc=class_colours[i]))
plt.legend(recs,groups)                           #legend for points

#display plot
plt.show()



''' for plotting every point (more efficient methods exist, but for now a fast test...may look up later)
	if i == 0:
		plt.scatter(w3 - w4, w1 - w2, color = 'red')    #plotting colors from data
	if i == 1:
		plt.scatter(w3 - w4, w1 - w2, color = 'green')  #plotting colors from data
	if i == 2:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'orange')   #plotting colors from data
	if i == 3:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'yellow')   #plotting colors from data
	if i == 4:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'aqua')   #plotting colors from data
	if i == 5:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'purple')   #plotting colors from data
	if i == 6:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'black')   #plotting colors from data
	if i == 7:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'grey')   #plotting colors from data
	if i == 8:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'pink')   #plotting colors from data
	if i == 9:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'brown')   #plotting colors from data
	if i == 10:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'gold')   #plotting colors from data
	if i == 11:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'blue')   #plotting colors from data
	if i == 12:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'aquamarine')   #plotting colors from data
	if i == 13:
	 	plt.scatter(w3 - w4, w1 - w2, color = 'magenta')   #plotting colors from data

'''