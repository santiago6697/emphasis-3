import sys
import time
import requests

reqs = int(sys.argv[1])
sec_per_req = 60/float(reqs)

output = open('act4_'+str(reqs)+'.txt','w')

def requestHTTP():
	start = time.time()
	contents = requests.get("http://10.0.0.4")
	# print(contents)
	trip_time = (time.time() - start)
	print('in ' + str(trip_time) + ' s')
	output.writelines(str(trip_time)+'\n')
	#print(str(trip_time))
	if sec_per_req > trip_time:
		time.sleep(sec_per_req - trip_time)
	return

for i in range(reqs):
	requestHTTP()

output.close()
