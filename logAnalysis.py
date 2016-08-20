import re

infile = r"/home/jinhao/Desktop/Horangi/CTF1.log"

ipAddresses = []


count = 0

with open(infile) as f:
    f = f.readlines()

for line in f:

	# using regex to extract out current ip address in the line
	curIpAdd = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
	
	# regex returns 2 ips, interested in the second
	targetIp = curIpAdd[1]

	# only adding in unique ip addreses
	if (targetIp not in ipAddresses):
		ipAddresses.append(targetIp)

	count += 1
	if count == 10000:
		break

print ipAddresses


