# import shlex

# api_key = vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1

# exampe = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1&location=Denver+CO"

# curl -H "Content-Type:application/json" -d '{"ndbno":["01009","45202763","35193"],"type":"b"}' vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1@api.nal.usda.gov/ndb/V2/reports

# curl -H "Content-Type:application/json" -d '{"ndbno":["01009","45202763","35193"],"type":"b"}' vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1@api.nal.usda.gov/ndb/V2/reports

# import urllib2
# data = '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP", "actions": "ALLOW", "priority": "10"}'
# url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1&location=Denver+CO'
# req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
# f = urllib2.urlopen(req)
# for x in f:
#     print(x)
# f.close() 


import shlex
import subprocess
cmd = '''curl -H "Content-Type:application/json" -d '{"ndbno":["01009","45202763","35193"],"type":"b"}' vy9T2DDU77D0ZBLadzrI0bJswyF2A6PXfrtG59D1@api.nal.usda.gov/ndb/V2/reports'''
args = shlex.split(cmd)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout)