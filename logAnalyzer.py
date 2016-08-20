import os
import ConfigParser
import re
from geoip import geolite2

config = ConfigParser.ConfigParser()

config.read("config.txt")

def getIpInfo(inputFile):

	infile = inputFile
	
	ipAddressHits = {}
	ip2Country = {}
	ip2Activity = {}

	count = 0

	with open(infile) as f:
    		f = f.readlines()
	
	for line in f:

		# using regex to extract out current ip address in the line
		curIpAdd = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
	
		# regex returns 2 ips, interested in the second
		targetIp = curIpAdd[1]

		# 1) only adding in unique ip addreses, set initial hit to 1
		# 2) if ip is already in the list, increment the hits by 1
		# 3) look up the country for the ip
		# 4) initializing a dynamic dictionary for activity
		if (targetIp not in ipAddressHits):
			ipAddressHits[targetIp] = 1
			
			match = geolite2.lookup(targetIp)
			if match is not None:
				ip2Country[targetIp] = match.country
			
			ip2Activity.setdefault(targetIp,[])
							
		else:
			ipAddressHits[targetIp] += 1
		
		ip2Activity[targetIp].append(line)

		count += 1
		if count == 10000:
			break

	return ipAddressHits, ip2Country, ip2Activity

	

def writeToFile(filename,content):
	with open(filename,"a+") as f:
		f.write(content)



	
inputPath = config.get('paths','inputPath')
outputPath = config.get('paths','outputPath')
activityOutputPath = config.get('paths','activityOutputPath')
filename = config.get('parameters','filename')

dirs = [inputPath,outputPath,activityOutputPath]

for directory in dirs:
	if not os.path.exists(directory):
    		os.makedirs(directory)

unqiueIpName = "unqiueIp.txt"
ipCountryHitsName = "ipCountryHits.txt"

inputFile = inputPath + filename

[ipAddressHits,ip2Country,ip2Activity] = getIpInfo(inputFile)


print "writing unique addresses"
for ip in ipAddressHits:
	writeToFile(outputPath+unqiueIpName,ip+"\n")

print "writing unique addresses, country and hits"
for ip in ipAddressHits:
	line = ip+"|"+str(ipAddressHits[ip])+"|"+ip2Country[ip]+"\n"
	writeToFile(outputPath+ipCountryHitsName,line)

print "writing activity"
for ip in ip2Activity:
	for item in ip2Activity[ip]:
		writeToFile(activityOutputPath+ip,item)

