import subprocess
import os

pathToActivity = "/home/jinhao/Desktop/Horangi/outputs/activity/"
pathToSQLiOutput = "/home/jinhao/Desktop/Horangi/attackDetection/SQLi.txt"
pathToRemoteFileInclusionOutput = "/home/jinhao/Desktop/Horangi/attackDetection/RemoteFileInclusion.txt"
pathToWebShellsOutput = "/home/jinhao/Desktop/Horangi/attackDetection/WebShells.txt"

shells = ["r57","loaderz","c0derz","c99","kadot","h4ntu"]

for file in os.listdir(pathToActivity):
	print "processing file "+file
	with open(pathToActivity+file) as f:
		f = f.readlines()

	for line in f:
		if "union" in line:
			with open(pathToSQLiOutput,"a+") as f:
				f.write(file +":"+line)
		if "/etc/passwd" in line:
			with open(pathToRemoteFileInclusionOutput,"a+") as f:
				f.write(file +":"+line)
		for item in shells:
			if item in line:
				with open(pathToWebShellsOutput,"a+") as f:
					f.write(file +":"+line)


print "done"

