import sys
import socket
import threading
import time

server_ip_address = sys.argv[1]
server_port = int(sys.argv[2])
users = int(sys.argv[3])
type_of_test = sys.argv[4]

tests = 32
output_array = []

output = open(type_of_test+"_"+str(tests)+"_"+str(users)+".txt", 'w')

def writer(output_array):
	for line in range(len(output_array)):
		output.writelines(output_array[line]+"\n")

def worker(test, user, server_ip_address, server_port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	global output_array
	try:
		start = time.perf_counter()
		s.connect((server_ip_address, server_port))
		# Increments ms
		s.close()
		RTT = (time.perf_counter() - start) * 1000
		output_array.append(str(RTT))
	except:
		output_array.append("failed")	

	if len(output_array)==tests*users:
		writer(output_array)
	return

for test in range(tests):
	threads = []

	for user in range(users):
		threads.append(threading.Thread(target = worker, args=(test, user, server_ip_address, server_port,)))
	
	for thrd in range(len(threads)):
		threads[thrd].start()

	for thrd in range(len(threads)):
		threads[thrd].join()
