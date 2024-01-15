#program for getting HAEBE star data from IRSA (WISE and 2MASS specifically)

import urllib, urllib2

i = 0
j = 0

#resetting file of WISE data
with open('HAEBEdata_WISE.txt', 'w') as f:
	f.write('')

#resetting file of 2MASS data
with open('HAEBEdata_2MASS.txt', 'w') as f:
	f.write('')

table = open('HAEBEinput.txt', 'r') #for names from catalogs of HAEBE stars, edited to include as many as possible
lines = table.readlines()

#beginning loop that reads through name inputs from HAEBEinput.txt
for obj in lines:

	url = "http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query" #URL that is queried to get data

	#search terms for search to the WISE catalog, done for each object in a cone of a radius of 10''
	p = {}
	p['spatial'] = "Cone"
	p['objstr'] = obj
	p['outfmt'] = 1    # IPAC table format
	p['catalog'] = 'wise_allwise_p3as_psd'
	p['radius'] = 10

	#search terms for search to the 2MASS catalog, done for each object in a cone of a radius of 10''
	p2 = {}
	p2['spatial'] = "Cone"
	p2['objstr'] = obj
	p2['outfmt'] = 1    # IPAC table format
	p2['catalog'] = 'fp_psc'
	p2['radius'] = 10

	#encoding search to get data from WISE, put into variable raw
	query = urllib.urlencode(p)
	get_url = url + "?" + query
	handler = urllib2.urlopen(get_url)
	raw = handler.readlines()

	#encoding search to get data from 2MASS, put into variable raw2
	query2 = urllib.urlencode(p2)
	get_url2 = url + "?" + query2
	handler2 = urllib2.urlopen(get_url2)
	raw2 = handler2.readlines()

	#appending WISE data for each HAEBE star
	with open('HAEBEdata_WISE.txt', 'a') as f:
		#try:
		if i != 0:
			f.write(raw[-1]) #appends line with data, second to last line, from the WISE data table of each star
		else:
			for line in raw: #appends whole data table to have general reference on formatting of columns, along with the first star input for WISE
				f.write(line) 
		#except IndexError:
			#print obj

	i +=1
	print i

	with open('HAEBEdata_2MASS.txt', 'a') as f:
		#try:
		if j != 0:
			f.write(raw2[-1]) #writes line with data, second to last line, from the 2MASS data table of each star
		else:
			for line in raw2: #appends whole data table to have general reference on formatting of columns, along with the first star input for 2MASS
				f.write(line)
		#except IndexError:
			#print obj

	j +=1
	print j

table.close()