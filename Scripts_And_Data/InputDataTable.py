#gets data for HAEBE star Group I vs. Group II project

'''
PLAN
-plug it all into a data table
-query gator tool with every single name 
-inspect for exceptions ('null')
-take data for respective object and if matches another then don't print/that can go to graphing part
'''

import urllib 

#intialize sites and data to use for strings
site  = 'https://wesfiles.wesleyan.edu/home/wherbst/web/TTauriDataBase/HAEBE/'
site2 = 'http://www.eso.org/~mvandena/haebetab1.html' 
response  = urllib.urlopen(site)
response2 = urllib.urlopen(site2)
url  = response.readlines()
url2 = response2.readlines()

i = 1

f = open('HAEBEinput.txt', 'w')   

#parsing through for names of HAEBE stars from url, trying to eliminate names that would be repeats or would throw errors
first = 'BE/'
last = '.dat>'
for line in url:
    ind  = line.find(first)
    ind2 = line.find(last)
    if ind2 != -1:
        line = line[ind+3:ind2]
        line = line.replace('_', '')
        if i == 16:
            f.write(' ' + line[0:5] + ' ' + line[5:ind2-ind] + '\n')
        elif (i >= 27 and i <= 58) or (i >= 77 and i <= 85):
            f.write(' ' + line[0:4] + ' ' + line[4:ind2-ind] + '\n')
        elif i >= 59 and i <= 63:
            f.write(' ' + line[0:3] + ' ' + line[3:] + '\n')
        elif (i >= 66 and i <= 69) or (i >= 72 and i <= 74) or (i == 96):
            f.write(' ' + line[0] + ' ' + line[1:ind2-ind] + '\n')
        elif (i >= 86 and i <= 89):
            f.write(' ' + line[0:5] + ' ' + line[5:] + '\n')
        #f.write(' ' + line[ind:ind+2] + ' ' + line[ind+3:ind2] + '\n')
        else:
            f.write(' ' + line[0:2] + ' ' + line[2:] + '\n')

        i += 1


#parsing through for names of HAEBE stars from url2, trying to eliminate names that would be repeats or would throw errors
for line in url2[13:142]:
    try:
        if line[0] != ' ' and line[0:10] != 'LkH<img WI' and (line[12] + line[13]) != 'HD' and line[0:11] != '<img WIDTH=':
            myString = line[0:11]
            #myString = myString.replace(' ', '_', 1)
            f.write(' ' + myString + '\n')
        elif (line[12] + line[13]) == 'HD':
            myString = line[12:21]
            #myString = myString.replace(' ', '_', 1)
            f.write(' ' + myString + '\n')
    except IndexError:
        pass

f.close()