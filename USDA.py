import shlex
import subprocess

class USDA:
	# Tony's data.gov registered API key
	API_key = "vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1"


	def reportCurl(nbdno, reportType):
		# Ugly command to minimize escapes
		cmd = '''curl -H "Content-Type:application/json" -d '{'''
		cmd += '''"ndbno":["''' + "\",\"".join([str(x) for x in nbdno]) + '''"]'''
		cmd += ''',"type":"''' + reportType + '''"}' '''
		cmd += API_key + '''@api.nal.usda.gov/ndb/V2/reports'''
		args = shlex.split(cmd)
		process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		print(stdout)

	def searchCurl(nbdno, reportType):
		# # Ugly command to minimize escapes
		# cmd = '''curl -H "Content-Type:application/json" -d '{'''
		# cmd += '''"ndbno":["''' + "\",\"".join([str(x) for x in nbdno]) + '''"]'''
		# cmd += ''',"type":"''' + reportType + '''"}' '''
		# cmd += API_key + '''@api.nal.usda.gov/ndb/V2/reports'''
		# args = shlex.split(cmd)
		# process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# stdout, stderr = process.communicate()
		# print(stdout)

	def parseCurl(stdout):
		return stdout


	# A list of up to 25 NDB numbers
	nbdno = ["01009"]
	# Report type: [b]asic or [f]ull or [s]tats
	reportType = "b"
	reportCurl(nbdno, reportType)
