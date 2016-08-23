import os
import ConfigParser
import re
from geoip import geolite2

config = ConfigParser.ConfigParser()
config.read("config.txt")


def getIpInfo(inputFile):
	""" Reads in a flat input file

	Returns 3 dictionaries:

	1) ipAddressCount
	   Key: IP Address
	   Finds the number of times an IP address appears

	2) ip2Country
       Key: IP Address
	   Find the country of origin for the IP addresses

	3) ip2Activity
       Key: IP Address
	   Associates all activity in the logfile to the IP address
	"""

    ipAddressCount = {}
    ip2Country = {}
    ip2Activity = {}

    with open(infile) as f:
	    for line in f:
	        try:

	            # using regex to extract out current ip address in the line
	            curIpAdd = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

	            # regex returns 2 ips, interested in the second IP
	            targetIp = curIpAdd[1]

	            # 1) only adding in unique ip addreses, set initial count to 1
	            # 2) if ip is already in the list, increment the count by 1
	            # 3) look up the country for the ip
	            # 4) initializing a dynamic dictionary for each ip activity
	            if (targetIp not in ipAddressCount):
	                ipAddressCount[targetIp] = 1

	                match = geolite2.lookup(targetIp)
	                if match is not None and match.country is not None:
	                    ip2Country[targetIp] = match.country
	                else:
	                    ip2Country[targetIp] = "not found"
	                ip2Activity.setdefault(targetIp, [])
	            else:
	                ipAddressCount[targetIp] += 1

	            # adding each line of activity to the respective IP
	            ip2Activity[targetIp].append(line)
	        except Exception, e:
	            continue

    return ipAddressCount, ip2Country, ip2Activity


def writeToFile(filename, content):
	""" Appends the given content to a file"""
    with open(filename, "a+") as f:
        f.write(content)


inputPath = config.get('paths', 'inputPath')
outputPath = config.get('paths', 'outputPath')
activityOutputPath = config.get('paths', 'activityOutputPath')
filename = config.get('parameters', 'filename')

dirs = [inputPath, outputPath, activityOutputPath]

for directory in dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)

unqiueIpName = "unqiueIp.txt"
ipCountryHitsName = "ipCountryHits.txt"
inputFile = inputPath + filename

ipAddressCount, ip2Country, ip2Activity] = getIpInfo(inputFile)


print "writing unique addresses"
for ip in ipAddressCount:
    writeToFile(outputPath + unqiueIpName, ip + "\n")

print "writing unique addresses, country and hits"
for ip in ipAddressCount:
    line = ip + "|" + str ipAddressCount[ip]) + "|" + ip2Country[ip] + "\n"
    writeToFile(outputPath + ipCountryHitsName, line)

print "writing activity"
for ip in ip2Activity:
    for item in ip2Activity[ip]:
        writeToFile(activityOutputPath + ip, item)
