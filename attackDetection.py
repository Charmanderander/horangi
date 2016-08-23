import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.txt")

activityOutputPath = config.get('paths', 'activityOutputPath')
pathToSQLiOutput = config.get('parameters', 'SQLiOutput')
pathToRemoteOutput = config.get('parameters', 'RFIOutput')
pathToWebShellsOutput = config.get('parameters', 'WebShellsOutput')

shells = ["r57", "loaderz", "c0derz", "c99", "kadot", "h4ntu"]


def attackDetection():
	""" Attempts to detect web based attack through the log files
	SQLi attacks are found through matching of the word "UNION"
	Remote file inclusions are found through matching "/etc/passwd"
	Web shells are found through matching the predefine list of common shells
	"""
    for file in os.listdir(activityOutputPath):
        print "processing file " + file
        with open(activityOutputPath + file) as f:
            f = f.readlines()

        for line in f:
            if "union" in line:
                with open(pathToSQLiOutput, "a+") as f:
                    f.write(file + ":" + line)
            if "/etc/passwd" in line:
                with open(pathToRemoteFileInclusionOutput, "a+") as f:
                    f.write(file + ":" + line)
            for item in shells:
                if item in line:
                    with open(pathToWebShellsOutput, "a+") as f:
                        f.write(file + ":" + line)

attackDetection()